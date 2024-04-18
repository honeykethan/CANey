#!/usr/bin/python3

from base64 import b64encode as b64e
from requests import get
from time import sleep 
from struct import unpack
from os import system as e
from binascii import hexlify as hexd

CAN_SET_MODE = "http://192.168.4.1/hardware"	# Set Hardware Mode
CAN_READ_CMD = "http://192.168.4.1/write?len=21&data=AAAAAAAAAAAAAAAAAA=="

mode = get(CAN_SET_MODE)
print("Mode Set:  {}".format(mode.text))

ecu_list = {}

def encode_frame(frame):

	can_id = pack("I", frame[0:4])[0]
	can_dlc = frame[4]
	data = frame[5:13]

	if(can_id not in ecu_list):
		ecu_list.update({hex(can_id):{'data':hexd(data).decode()}})

	print("[+] Detected CAN-ID: {} ECU(s)\n".format(len(ecu_list)))
	for ecu in ecu_list:
		print("\tCAN-ID: {} -> DATA: {}".format(ecu, ecu_list[ecu]['data']))

while True:
	data = get(CAN_READ_CMD)
	try:
		frame = b64e(data.text)
		e('clear')
		encode_frame(frame)
		sleep(0.05)
	except 	Exception as ex:
		print(ex)
		print("[!] No CAN message sent")
