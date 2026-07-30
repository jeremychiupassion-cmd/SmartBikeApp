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

# 🛡️ 乾淨配方：不鎖定任何版本號，全權交給 p4a develop 分支內部處理
requirements = python3,kivy,plyer,numpy,opencv

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

# 🛡️ 核心修復：使用最新的 develop 分支，裡面有最新修復的 OpenCV 與 NumPy 配方
p4a.branch = develop

[buildozer]
# 🛡️ 改回 1 (Info)，避免幾十萬行的 C++ 編譯細節癱瘓 GitHub Actions 輸出介面
log_level = 1
warn_on_root = 1