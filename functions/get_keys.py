# Citation: Box of Hats (https://github.com/Box-Of-Hats)

import win32api as wapi 
import time

key_list = ["\b"]
for char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ 1234567890,.'APS$/\\":
	key_list.append(char)

def key_check():
	keys = []
	for key in key_list:
		if wapi.GetAsyncKeyState(ord(key)):
			keys.append(key)
	return keys