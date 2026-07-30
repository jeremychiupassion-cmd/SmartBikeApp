[app]

# (str) Title of your application
title = SmartBikeApp

# (str) Package name
package.name = smartbikeapp

# (str) Package domain (needed for android/ios packaging)
package.domain = org.example

# (str) Application version
version = 0.2

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,ttf,wav,mp3

# (list) Application requirements
# 包含 OpenCV, NumPy, Plyer 及 Kivy 官方標準配方名稱
requirements = python3,kivy,plyer,opencv,numpy

# (str) Custom source folders for requirements
# requirements.source.kivy =

# (str) Presplash of the application
#presplash.filename = %(source.dir)s/data/presplash.png

# (str) Icon of the application
#icon.filename = %(source.dir)s/data/icon.png

# (str) Supported orientations (鎖定橫屏顯示)
orientation = landscape

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 1


#
# Android specific
#

# (list) Permissions (宣告麥克風、相機、GPS 定位、音量調整與網路權限)
android.permissions = INTERNET,RECORD_AUDIO,CAMERA,ACCESS_FINE_LOCATION,ACCESS_COARSE_LOCATION,MODIFY_AUDIO_SETTINGS

# (bool) 啟用螢幕常亮 (防止騎車時自動黑屏)
android.wakelock = True

# (bool) Indicate if you want to accept SDK license automatically
android.accept_sdk_license = True

# (int) Target Android API (API 31 相容性與穩定度最佳)
android.api = 31

# (int) Minimum API your APK will support
android.minapi = 24

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

# (list) Architecture to build for (現代 64 位元架構)
android.archs = arm64-v8a


#
# Buildozer section
#

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug)
log_level = 2

# (int) Display warning if buildozer is run as root
warn_on_root = 1