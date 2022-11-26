#! /bin/bash
while true; do ps aux | grep simple/ | head -n 3; sleep 1; done > pc_tx_dds_sec.log # to get 3 tx scripts on the PC 
# while true; do ps aux | grep simple/ | head -n 1; sleep 1; done > rpi12_can_dds_sec.log
# while true; do ps aux | grep simple/ | head -n 1; sleep 1; done > rpi11_lidar_dds_sec.log
# while true; do ps aux | grep simple/ | head -n 1; sleep 1; done > rpi13_cam_dds_sec.log
