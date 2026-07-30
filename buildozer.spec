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

# (list) Source files to include
source.include_exts = py,png,jpg,kv,atlas,ttf,wav,mp3

# (list) Application requirements
# 🛡️ 回歸官方配方名稱，不加任何版本號，把版本控制交給 GitHub Actions
requirements = hostpython3,python3,kivy,plyer,numpy,opencv,libffi

# (str) Supported orientations
orientation = landscape
fullscreen = 1

#
# Android specific
#
android.permissions = INTERNET,RECORD_AUDIO,CAMERA,ACCESS_FINE_LOCATION,ACCESS_COARSE_LOCATION,MODIFY_AUDIO_SETTINGS
android.wakelock = True
android.accept_sdk_license = True
android.api = 31
android.minapi = 24
android.ndk = 25b
android.skip_update = False
android.enable_androidx = True
android.archs = arm64-v8a

# 採用官方穩定分支
p4a.branch = master

[buildozer]
log_level = 2
warn_on_root = 1