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

# 🛡️ 終極殺招：拿掉 p4a 內建的 opencv 配方，改用純 Python 或預編譯版本的套件
# 我們使用 `opencv-python-headless`，並強制它只下載預編譯版本，不觸發 C++ 編譯
requirements = python3,kivy,plyer,numpy,opencv-python-headless

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

p4a.branch = develop

[buildozer]
log_level = 2
warn_on_root = 1