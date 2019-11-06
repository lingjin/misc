#!/bin/bash

for (( c=1; c<=100; c++ ))
do
   adb wait-for-device
   sleep 20
   adb reboot
   echo "rebooted $c times"
   sleep 40
done
