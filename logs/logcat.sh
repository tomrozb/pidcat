#!/bin/bash
echo "Cleaning logs..."
adb logcat -c -b events >/dev/null
echo "Run the start.sh script now"
echo "================== LOGS  =================="
adb logcat -b events | grep com.packag
