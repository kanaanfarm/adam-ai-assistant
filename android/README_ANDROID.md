# Adam AI Android Application

This Android Studio project is a secure WebView wrapper for the Personal AI Assistant server.

1. Keep the desktop assistant running.
2. Find the `Same Wi-Fi mobile URL` printed by the desktop server.
3. Open this `android` folder in Android Studio.
4. Allow Gradle Sync, then select **Build > Build APK(s)**.
5. Install the generated debug APK on the Android phone.
6. In the app, enter the desktop URL, for example `http://192.168.1.20:8770`, and press Connect.

The server URL is saved on the phone. Telephone links open the Android dialer. Real secrets remain on the desktop/server and are not embedded in the APK.
