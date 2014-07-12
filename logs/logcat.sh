#!/bin/bash
adb logcat -c -b events
adb logcat -b events | grep com.packag
