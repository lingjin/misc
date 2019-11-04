#!/bin/bash

for (( c=1; c<=100; c++ ))
do
   adb wait-for-device
   adb root
   sleep 20
   adb shell "echo c > /proc/sysrq-trigger"
   echo "rebooted $c times"
   sleep 60
done