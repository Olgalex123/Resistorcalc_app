[app]
title = Подбор Резисторов
package.name = resistorcalc
package.domain = org.olgalex

source.dir = .
source.include_exts = py,png,jpg,kv,atlas
source.exclude_exts = spec

version = 1.0.0

requirements = python3,kivy==2.3.0,kivymd==1.2.0

orientation = portrait
fullscreen = 0

android.api = 33
android.minapi = 21
android.arch = arm64-v8a
android.accept_sdk_license = True
android.permissions = INTERNET

[buildozer]
log_level = 2
warn_on_root = 1
