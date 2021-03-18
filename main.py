#!/usr/bin/python3.6
#coding:utf-8
from gameManager import GameManager
import sys

if __name__ == '__main__':
	gm = GameManager()
	
	if len(sys.argv) > 1 :
		if sys.argv[1] == "False" :
			sys.argv[1] = False
		elif sys.argv[1] == "True" :
			sys.argv[1] = True
		else :
			sys.argv[1] = None
	
	if len(sys.argv) == 2 :
		gm.start(sys.argv[1])
	elif len(sys.argv) == 3 :
		gm.start(sys.argv[1], int(sys.argv[2]))
	else :
		gm.start()
