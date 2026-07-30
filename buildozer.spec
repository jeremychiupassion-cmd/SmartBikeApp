[app]

# (str) Title of your application
title = SmartBikeApp

# (str) Package name
package.name = smartbikeapp

# (str) Package domain (needed for android/ios packaging)
package.domain = org.example

# (str) Application version
version = 0.1

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,ttf

# (list) Application requirements
requirements = python3,kivy,plyer

# (str) 橫屏顯示設定
orientation = landscape

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 1


#
# Android specific
#

# (list) Permissions
android.permissions = INTERNET,RECORD_AUDIO,CAMERA,ACCESS_FINE_LOCATION,ACCESS_COARSE_LOCATION

# (bool) 啟用螢幕常亮 (防止騎車時黑屏)
android.wakelock = True

# (bool) Indicate if you want to accept SDK license automatically
android.accept_sdk_license = True

# (int) Target Android API
android.api = 33

# (int) Minimum API your APK will support.
android.minapi = 21

# (str) Android NDK version to use
android.ndk = 25b

# (bool) If True, then skip trying to update the Android sdk
android.skip_update = False

# (str) Android NDK directory
android.ndk_path =

# (str) Android SDK directory
android.sdk_path =

# (bool) Enable AndroidX support
android.enable_androidx = True

# (list) Architecture to build for
android.archs = arm64-v8a


#
# Buildozer section
#

[buildozer]

# (int) Log level
log_level = 2

# (int) Display warning if buildozer is run as root
warn_on_root = 1