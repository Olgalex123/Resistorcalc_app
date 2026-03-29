
[app]
title = ResistorCalc
package.name = resistorcalc
package.domain = org.olgalex

# === КРИТИЧНО: версии ===
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
requirements = python3==3.10.12,kivy==2.3.0,kivymd==1.2.0,cython==0.29.37,pyjnius==1.6.1,android

# === Android ===
android.api = 33
android.minapi = 21
android.arch = arm64-v8a
android.ndk = 25b
android.accept_sdk_license = True

# === Оптимизация сборки ===
android.add_aars = 
android.gradle_dependencies = 
p4a.local_recipes = 
