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

# 🛡️ 關鍵修正 1：直接在配方中強制將 numpy 鎖定在 1.26.4，徹底封殺 NumPy 2.0 帶來的 C++ 編譯崩潰
requirements = python3,kivy,plyer,numpy==1.26.4,opencv

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

# 🛡️ 關鍵修正 2：改用 develop 分支，這裡擁有最新的 OpenCV 下載修復與相容性補丁
p4a.branch = develop

[buildozer]
# 保持為 2，若有問題才看得到詳細死因
log_level = 2
warn_on_root = 1