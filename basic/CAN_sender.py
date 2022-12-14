###############################################################################
# (c) 2005-2015 Copyright, Real-Time Innovations.  All rights reserved.       #
# No duplications, whole or partial, manual or electronic, may be made        #
# without express written permission.  Any such copies, or revisions thereof, #
# must display this notice unaltered.                                         #
# This code contains trade secrets of Real-Time Innovations, Inc.             #
###############################################################################
import random
import string
from time import sleep
import os
# Updating the system path is not required if you have pip-installed
# rticonnextdds-connector
from sys import path as sys_path
from os import path as os_path
file_path = os_path.dirname(os_path.realpath(__file__))
sys_path.append(file_path + "/../../../")

import rticonnextdds_connector as rti

with rti.open_connector(
        config_name="MyParticipantLibrary::MyPubParticipant",
        url=file_path + "/../ShapeExample.xml") as connector:

    output = connector.get_output("MyPublisher::CANWriter")

    print("Waiting for subscriptions...")
    output.wait_for_subscriptions()

    print("Writing...")
   
       
    while True:
        string_data = ''.join(random.choice(string.ascii_lowercase) for i in range(160))
        output.instance.set_string('can',string_data)
        output.write()

        sleep(8 / 1000) # Write at a rate of one sample every 0.5 seconds, for ex.

    print("Exiting...")
    output.wait() # Wait for all subscriptions to receive the data before exiting
