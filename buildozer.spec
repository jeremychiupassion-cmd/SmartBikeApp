[app]

# (str) Title of your application
title = SmartBikeApp

# (str) Package name
package.name = smartbikeapp

# (str) Package domain (needed for android/ios packaging)
package.domain = org.example

# (str) Application version (關鍵修正：Buildozer 強制要求此欄位)
version = 0.1

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,ttf

# (list) Application requirements
# 注意：已加入專案所需的 plyer 與 pyjnius 套件
requirements = python3,kivy,plyer,pyjnius

# (str) Custom source folders for requirements
# requirements.source.kivy =

# (str) Presplash of the application
#presplash.filename = %(source.dir)s/data/presplash.png

# (str) Icon of the application
#icon.filename = %(source.dir)s/data/icon.png

# (str) Supported orientations (one of landscape, sensorLandscape, portrait or all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0


#
# Android specific
#

# (list) Permissions
# 宣告語音所需的 INTERNET，以及麥克風、相機（閃光燈）與 GPS 定位權限
android.permissions = INTERNET,RECORD_AUDIO,CAMERA,ACCESS_FINE_LOCATION,ACCESS_COARSE_LOCATION

# (bool) 啟用螢幕常亮 (防止騎車時黑屏)
android.wakelock = True

# (bool) Indicate if you want to accept SDK license automatically
android.accept_sdk_license = True

# (int) Target Android API, should be one of the known API levels (33 為穩定支援版本)
android.api = 33

# (int) Minimum API your APK will support.
android.minapi = 21

# (str) Android NDK version to use (25b 穩定度極高)
android.ndk = 25b

# (bool) If True, then skip trying to update the Android sdk
android.skip_update = False

# (str) Android NDK directory (leave empty to automatically download)
android.ndk_path =

# (str) Android SDK directory (leave empty to automatically download)
android.sdk_path =

# (bool) Enable AndroidX support. Required for modern Android build
android.enable_androidx = True

# (list) Architecture to build for (ARM64-v8a 為現代手機標準)
android.archs = arm64-v8a


#
# Buildozer section
#

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = ignore, 1 = warn, 2 = error)
warn_on_root = 1