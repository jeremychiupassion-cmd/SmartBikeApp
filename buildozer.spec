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
# 回歸官方配方，環境變數已在 build.yml 鎖定
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

p4a.branch = master

[buildozer]
# 🛡️ 保持為 1 (Info)，避免幾萬行 C++ 編譯日誌塞爆 GitHub 被強制截斷
log_level = 1
warn_on_root = 1