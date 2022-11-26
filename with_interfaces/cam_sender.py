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
import cv2
import imutils

# Updating the system path is not required if you have pip-installed
# rticonnextdds-connector
from sys import path as sys_path
from os import path as os_path
file_path = os_path.dirname(os_path.realpath(__file__))
sys_path.append(file_path + "/../../../")

import rticonnextdds_connector as rti
vid_obj = cv2.VideoCapture(4)
# 0 - colored webcam
# 2 - grayscale 
# 4 & 5 - USB webcam 

with rti.open_connector(
        config_name="MyParticipantLibrary::MyPubParticipant3",
        url=file_path + "/../ShapeExample.xml") as connector:

    output = connector.get_output("MyPublisher3::CamWriter")

    print("Waiting for subscriptions...")
    output.wait_for_subscriptions()

    print("Writing...")
    while True:
        ret, frame = vid_obj.read()

        # frame = imutils.resize(frame, width=449)
        cv2.imshow("Transmitting...", frame)
        e, tx_img = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY,70])  # encoding each frame into an image
        img_bytes = tx_img.tobytes()  # you can also try pickle

        
        string_data = ''.join(random.choice(string.ascii_lowercase) for i in range(8000))
        output.instance.set_string('cam','Start'+ string_data)
 
        output.write()

        sleep(20 / 1000) # Write at a rate of one sample every 0.5 seconds, for ex.

    print("Exiting...")
    output.wait() # Wait for all subscriptions to receive the data before exiting
