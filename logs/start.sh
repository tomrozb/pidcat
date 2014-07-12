#!/bin/bash
adb install -r pidcat.apk && adb shell am start -n com.packag/.MyActivity
