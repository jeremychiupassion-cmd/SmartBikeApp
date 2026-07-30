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
# 關鍵修正：還原為原生配方名稱 (不加 == 避免 git pathspec 錯誤)
requirements = python3,kivy,plyer,opencv,numpy

# (str) Supported orientations (橫屏顯示)
orientation = landscape

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 1


#
# Android specific
#

# (list) Permissions
android.permissions = INTERNET,RECORD_AUDIO,CAMERA,ACCESS_FINE_LOCATION,ACCESS_COARSE_LOCATION,MODIFY_AUDIO_SETTINGS

# (bool) 啟用螢幕常亮
android.wakelock = True

# (bool) Indicate if you want to accept SDK license automatically
android.accept_sdk_license = True

# (int) Target Android API
# 關鍵修正：切換至 API 31，這是目前 p4a + opencv + numpy 相容性最佳的 API 版本
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