[app]
title = 智慧單車中控台
package.name = smartbike
package.domain = org.bike
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
source.main = main.py
version = 0.1

requirements = python3, kivy, pyjnius, android, plyer

orientation = portrait

android.permissions = RECORD_AUDIO, CAMERA, ACCESS_FINE_LOCATION, ACCESS_COARSE_LOCATION, INTERNET, FLASHLIGHT, QUERY_ALL_PACKAGES
android.api = 34
android.minapi = 21
android.ndk = 25b

android.add_compile_pyo = 1
android.remove_src = 1

[buildozer]
log_level = 2
warn_on_root = 1