#!/usr/bin/env python

import Coinbase
import sys

coinbase = None
prompt = "BTC $ "

def print_usage():
	print """Usage: 
	'balance' - show account balance
	'p_b - show current buying price'
	'p_s - show current selling price'
	'b - buy bitcoin'
	's - sell bitcoin'
	'h or help - show help'
	'exit - Ctrl + D'
	"""

def parse_command(cmd):
	if cmd == "balance":
		coinbase.getBalance()
	elif cmd == "p_b":
		coinbase.getBuyPrice()
	elif cmd == "p_s":
		coinbase.getSellPrice()
	elif cmd == "b":
		qty = raw_input("How many bitcoin you wanna buy?  >> ")
		try:
			qty = float(qty)
		except ValueError, ex:
			print "Invalid input: " + str(ex)
		else:
			coinbase.BuyBTC(qty)
	elif cmd == "s":
		qty = raw_input("How many bitcoin you wanna sell?  >> ")
		try:
			qty = float(qty)
		except ValueError, ex:
			print "Invalid input: " + str(ex)
		else:
			coinbase.SellBTC(qty)
	elif cmd == "h" or cmd == "help":
		print_usage()
	elif cmd == "clc": # clear screen
		pass
	else:
		print "Invalid command, type 'h' or 'help' to query the supported commands."


if __name__ == "__main__":
	if coinbase == None:
		coinbase = Coinbase.Coinbase()

	while True:
		try:
			cmd = raw_input(prompt)
		except KeyboardInterrupt:
			print ""
			continue
		except EOFError:
			print ""
			break
		try:
			parse_command(cmd)
		except KeyboardInterrupt:
			print ""
			continue
