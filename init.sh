#!/bin/bash

for i in $*
do
    ip addr flush dev $i
    ethtool -K $i tx off rx off ufo off gso off gro off tso off
done

/usr/bin/vpp -c /etc/hicn/super_startup.config &>log.txt &
sleep 20
sysrepod -d -l 0 &
sleep 5
sysrepo-plugind -d -l 0 &
sleep 5
netopeer2-server -d -v 0 &
sleep 5
echo 'root:1' | chpasswd
trap "kill -9 $$" SIGHUP SIGINT SIGTERM SIGCHLD
wait
