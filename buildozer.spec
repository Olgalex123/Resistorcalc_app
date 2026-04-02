[app]
title = ResistorCalc
package.name = resistorcalc
package.domain = org.olgalex

version = 0.1

# === Исправлено: полная версия Python ===
requirements = python3==3.11.7,kivy==2.3.0,kivymd==1.2.0,cython==0.29.37,pyjnius==1.6.1,android

android.api = 33
android.minapi = 21
android.archs = arm64-v8a,armeabi-v7a
android.ndk = 25b
android.accept_sdk_license = True

p4a.branch = master

source.dir = .
source.include_exts = py,png,jpg,kv,atlas

orientation = portrait

android.permissions = 
