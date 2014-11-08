#!/bin/sh

./sketch.elf /dev/pts/0 &
sleep 5
killall sketch.elf
