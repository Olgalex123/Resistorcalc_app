[app]
title = ResistorCalc
package.name = resistorcalc
package.domain = org.olgalex

# === Версии (стабильная комбинация) ===
requirements = python3==3.10.12,kivy==2.3.0,kivymd==1.2.0,cython==0.29.37,pyjnius==1.6.1,android

# === Android настройки ===
android.api = 33
android.minapi = 21
android.arch = arm64-v8a
android.ndk = 25b
android.accept_sdk_license = True

# === p4a настройки (критично!) ===
p4a.branch = master
p4a.source_dir = 

# === Пути ===
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
