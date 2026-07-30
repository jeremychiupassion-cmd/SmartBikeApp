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
# 🛡️ 關鍵修正：加入 hostpython3 與 libffi 以啟用穩定的 C-Extension 配方
requirements = hostpython3,python3,kivy,plyer,opencv,numpy,libffi

# (str) Supported orientations (鎖定橫屏顯示)
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

# 🛡️ 關鍵設定：強制 p4a 使用主線分支配方，避開 Ninja 本地編譯崩潰
p4a.branch = master


#
# Buildozer section
#

[buildozer]

# (int) Log level
log_level = 2

# (int) Display warning if buildozer is run as root
warn_on_root = 1