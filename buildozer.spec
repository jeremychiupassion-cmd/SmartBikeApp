[app]

# (str) Title of your application
title = SmartBikeApp

# (str) Package name
package.name = smartbikeapp

# (str) Package domain
package.domain = org.example

# (str) Application version
version = 0.2

# (str) Source code location
source.dir = .

# (list) Source files to include
source.include_exts = py,png,jpg,kv,atlas,ttf,wav,mp3

# (list) Application requirements
# 關鍵調整：使用預編譯輪子包，避開 C++ 原始碼重頭編譯
requirements = python3,kivy==2.3.0,plyer,opencv-python-headless,numpy

# (str) Supported orientations
orientation = landscape
fullscreen = 1

#
# Android specific
#
android.permissions = INTERNET,RECORD_AUDIO,CAMERA,ACCESS_FINE_LOCATION,ACCESS_COARSE_LOCATION,MODIFY_AUDIO_SETTINGS
android.wakelock = True
android.accept_sdk_license = True
android.api = 33
android.minapi = 24
android.ndk = 25b
android.skip_update = False
android.enable_androidx = True
android.archs = arm64-v8a

# 採用最穩定的 release 分支
p4a.branch = master

[buildozer]
log_level = 2
warn_on_root = 1