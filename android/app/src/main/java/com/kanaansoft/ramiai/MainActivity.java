package com.kanaansoft.ramiai;

import android.Manifest;
import android.app.Activity;
import android.app.AlertDialog;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.net.Uri;
import android.os.Bundle;
import android.webkit.PermissionRequest;
import android.webkit.WebChromeClient;
import android.webkit.WebResourceRequest;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.EditText;

public class MainActivity extends Activity {
    private WebView web;
    private static final String PREFS="rami_ai", KEY="server_url";
    @Override public void onCreate(Bundle state){super.onCreate(state);web=new WebView(this);setContentView(web);configure();String url=getPreferences(MODE_PRIVATE).getString(KEY,"");if(url.isEmpty())chooseServer();else web.loadUrl(url);}
    private void configure(){web.getSettings().setJavaScriptEnabled(true);web.getSettings().setDomStorageEnabled(true);web.getSettings().setMediaPlaybackRequiresUserGesture(false);web.setWebViewClient(new WebViewClient(){@Override public boolean shouldOverrideUrlLoading(WebView v, WebResourceRequest r){String u=r.getUrl().toString();if(u.startsWith("tel:")){startActivity(new Intent(Intent.ACTION_DIAL,Uri.parse(u)));return true;}return false;}});web.setWebChromeClient(new WebChromeClient(){@Override public void onPermissionRequest(PermissionRequest r){runOnUiThread(()->{if(checkSelfPermission(Manifest.permission.RECORD_AUDIO)!=PackageManager.PERMISSION_GRANTED)requestPermissions(new String[]{Manifest.permission.RECORD_AUDIO},7);else r.grant(r.getResources());});}});web.setOnLongClickListener(v->{chooseServer();return true;});}
    private void chooseServer(){EditText input=new EditText(this);input.setHint("http://192.168.1.20:8770");input.setText(getPreferences(MODE_PRIVATE).getString(KEY,""));new AlertDialog.Builder(this).setTitle("Adam AI server address").setMessage("Enter the Same Wi-Fi mobile URL shown by the desktop assistant. Long-press the app later to change it.").setView(input).setCancelable(false).setPositiveButton("Connect",(d,w)->{String u=input.getText().toString().trim();if(!u.startsWith("http://")&&!u.startsWith("https://"))u="http://"+u;getPreferences(MODE_PRIVATE).edit().putString(KEY,u).apply();web.loadUrl(u);}).show();}
    @Override public void onBackPressed(){if(web.canGoBack())web.goBack();else super.onBackPressed();}
}
