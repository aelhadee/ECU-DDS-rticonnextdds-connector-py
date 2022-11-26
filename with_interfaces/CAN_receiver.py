###############################################################################
# (c) 2005-2015 Copyright, Real-Time Innovations.  All rights reserved.       #
# No duplications, whole or partial, manual or electronic, may be made        #
# without express written permission.  Any such copies, or revisions thereof, #
# must display this notice unaltered.                                         #
# This code contains trade secrets of Real-Time Innovations, Inc.             #
###############################################################################

from __future__ import print_function

# Updating the system path is not required if you have pip-installed
# rticonnextdds-connector
from sys import path as sys_path
from os import path as os_path

file_path = os_path.dirname(os_path.realpath(__file__))
sys_path.append(file_path + "/../../../")

import rticonnextdds_connector as rti
import time
start_time = time.time()
start_time_data_received = time.time()
dt_data_received = []
MB = []

import pandas as pd
import matplotlib.pyplot as plt
with rti.open_connector(
        config_name="MyParticipantLibrary::MySubParticipant",
        url=file_path + "/../ShapeExample.xml") as connector:
    input = connector.get_input("MySubscriber::CANReader")

    print("Waiting for publications...")
    input.wait_for_publications()  # wait for at least one matching publication

    print("Waiting for data...")
    # for i in range(1, 5000000):
    while True:
        input.wait()  # wait for data on this input
        input.take()
        for sample in input.samples.valid_data_iter:
            # You can get all the fields in a get_dictionary()
            data = sample.get_dictionary()
            # Or you can access the field individually
            can = sample.get_string("can")
            print(len(can))
            dt_data_received.append((time.time() - start_time_data_received) * 1000)
            start_time_data_received = time.time()
            if (time.time() - start_time) >= (1 * 60):
                print(dt_data_received)
                logfilename_tcp_rx = "can_rx_dt_" + str(time.time_ns()) + ".log"
                with open(logfilename_tcp_rx, "a") as log1:
                    log1.write("can_RX_Delta_time" + "\n")
                    for ii in range(1, int(len(dt_data_received))):
                        log1.write(str(dt_data_received[ii]) + "\n")
                    log1.close()
                frames_plt = list(range(0, len(dt_data_received[5:])))
                frames_plt = [x / 1000 for x in frames_plt]
                plt.figure(figsize=(10, 8))
                plt.subplot(1, 2, 1)
                plt.scatter(frames_plt, dt_data_received[5:])
                plt.xlabel('NDN Data Packet Number (in thousands)')
                plt.ylabel('Delta time (in ms): Received CAN bytes over NDN Data Packets')

                plt.subplot(1, 2, 2)
                plt.boxplot(dt_data_received[5:])
                plt.savefig("can_dt_data_tx_box_" + str(time.time_ns()) + ".png")
                print("Data RX Ended...going to sleep")
                dt_data_received_pd = pd.DataFrame(dt_data_received[1:])
                logfilename_lidar_rx_summ = "summ_can_rx_dt_" + str(time.time_ns()) + ".log"
                with open(logfilename_lidar_rx_summ, "a") as log2:
                    log2.write("can_RX_dt_summary" + "\n")
                    log2.write(str(dt_data_received_pd.describe()) + "\n")
                    log2.close()
                print(dt_data_received_pd.describe())
                print(MB, 'bytes')
                #print(MB / 1000000, 'MB')
                #print(((MB / 1000000) * 8) / (40 * 60), 'Mbps')

                time.sleep(60 * 60)



