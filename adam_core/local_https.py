from pathlib import Path
from datetime import datetime, timedelta, timezone
import ipaddress


def ensure_local_https_certificate(base_dir, lan_ip):
    """Create a private local CA and a LAN server certificate.

    The CA certificate must be installed/trusted on guest devices once.  The
    private CA key never needs to leave the Adam computer.
    """
    try:
        from cryptography import x509
        from cryptography.x509.oid import NameOID, ExtendedKeyUsageOID
        from cryptography.hazmat.primitives import hashes, serialization
        from cryptography.hazmat.primitives.asymmetric import rsa
    except Exception as exc:
        raise RuntimeError("local_https_dependency_missing: run INSTALL_REQUIREMENTS.bat") from exc

    cert_dir = Path(base_dir) / "data" / "local_https"
    cert_dir.mkdir(parents=True, exist_ok=True)
    ca_key_p = cert_dir / "adam-local-ca.key"
    ca_cert_p = cert_dir / "adam-local-ca.crt"
    server_key_p = cert_dir / "adam-lan.key"
    server_cert_p = cert_dir / "adam-lan.crt"
    ip = ipaddress.ip_address(lan_ip)
    now = datetime.now(timezone.utc)

    if not ca_key_p.exists() or not ca_cert_p.exists():
        ca_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        ca_name = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, "Adam Acquisition Local CA")])
        ca_cert = (x509.CertificateBuilder().subject_name(ca_name).issuer_name(ca_name)
                   .public_key(ca_key.public_key()).serial_number(x509.random_serial_number())
                   .not_valid_before(now-timedelta(days=1)).not_valid_after(now+timedelta(days=3650))
                   .add_extension(x509.BasicConstraints(ca=True, path_length=0), critical=True)
                   .sign(ca_key, hashes.SHA256()))
        ca_key_p.write_bytes(ca_key.private_bytes(serialization.Encoding.PEM, serialization.PrivateFormat.PKCS8, serialization.NoEncryption()))
        ca_cert_p.write_bytes(ca_cert.public_bytes(serialization.Encoding.PEM))
    else:
        ca_key = serialization.load_pem_private_key(ca_key_p.read_bytes(), password=None)
        ca_cert = x509.load_pem_x509_certificate(ca_cert_p.read_bytes())

    regenerate = True
    if server_cert_p.exists() and server_key_p.exists():
        try:
            old = x509.load_pem_x509_certificate(server_cert_p.read_bytes())
            san = old.extensions.get_extension_for_class(x509.SubjectAlternativeName).value
            regenerate = ip not in san.get_values_for_type(x509.IPAddress) or old.not_valid_after_utc < now + timedelta(days=7)
        except Exception:
            regenerate = True
    if regenerate:
        server_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        subject = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, str(ip))])
        server_cert = (x509.CertificateBuilder().subject_name(subject).issuer_name(ca_cert.subject)
                       .public_key(server_key.public_key()).serial_number(x509.random_serial_number())
                       .not_valid_before(now-timedelta(days=1)).not_valid_after(now+timedelta(days=825))
                       .add_extension(x509.SubjectAlternativeName([x509.IPAddress(ip), x509.DNSName("localhost")]), critical=False)
                       .add_extension(x509.ExtendedKeyUsage([ExtendedKeyUsageOID.SERVER_AUTH]), critical=False)
                       .sign(ca_key, hashes.SHA256()))
        server_key_p.write_bytes(server_key.private_bytes(serialization.Encoding.PEM, serialization.PrivateFormat.PKCS8, serialization.NoEncryption()))
        server_cert_p.write_bytes(server_cert.public_bytes(serialization.Encoding.PEM))
    return str(server_cert_p), str(server_key_p), str(ca_cert_p)
