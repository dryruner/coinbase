#!/usr/bin/env python

import urllib2, json

user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_0) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31"
api_key = #### Enter your own api key! ####
url = "https://coinbase.com/api/v1/"


class Coinbase(object):
	def parse_request(self, request_type, arg = None):
		req = None
		if request_type == "balance":
			req = urllib2.Request(url + "account/balance?api_key=" + api_key, headers = {"User-Agent" : user_agent})
		elif request_type == "receive_address":
			req = urllib2.Request(url + "account/receive_address?api_key=" + api_key, headers = {"User-Agent": user_agent})
		elif request_type == "addresses":
			req = urllib2.Request(url + "addresses?api_key=" + api_key, headers = {"User-Agent": user_agent})
		elif request_type == "exchange_rates":
			req = urllib2.Request(url + "currencies/exchange_rates?api_key=" + api_key, headers = {"User-Agent" : user_agent})
		elif request_type == "buy_price":
			req = urllib2.Request(url + ("prices/buy?qty=%g&api_key=%s" % (arg, api_key)), headers = {"User-Agent" : user_agent})
		elif request_type == "sell_price":
			req = urllib2.Request(url + ("prices/sell?qty=%g&api_key=%s" % (arg, api_key)), headers = {"User-Agent" : user_agent})

		if req:
			content = urllib2.urlopen(req)
			return json.loads(content.read())
		else:
			print "Invalid request!"
			return None


	def getBalance(self):
		balance = self.parse_request("balance")
		if balance:
			print "My bitcoin balance: " + balance["amount"] + " BTC"

	def getReceiveAddress(self):
		recv_addr = self.parse_request("receive_address")
		if recv_addr:
			print "My address for receiving bitcoin: " + recv_addr["address"]

	def getAddresses(self):
		addr = self.parse_request("addresses")
		if addr:
			print "=============== Bitcoin addresses I have associated with my account: ================"
			for _addr in addr["addresses"]:
				print _addr["address"]["address"]
			print "====================================================================================="
	
	def getCurrency(self):
		btc_to_rates = self.parse_request("exchange_rates")
		if btc_to_rates:
			print "1 BTC = " + btc_to_rates['btc_to_usd'] + ' USD'
			print "1 BTC = " + btc_to_rates['btc_to_cny'] + ' CNY'
	
	def getBuyPrice(self, qty = 1):
		buy_price = self.parse_request("buy_price", qty)
		if buy_price:
			print "Total buy price for %g BTCs that will be deducted from bank account is: %s USD" % (qty, buy_price['total']['amount'])

	def getSellPrice(self, qty = 1):
		sell_price = self.parse_request("sell_price", qty)
		if sell_price:
			print "Total sell price for %g BTCs that will be transferred to bank account is: %s USD" % (qty, sell_price['total']['amount'])

qty = 1
if __name__ == "__main__":
	coinbase = Coinbase()
	coinbase.getBalance()
#	coinbase.getReceiveAddress()
#	coinbase.getAddresses()
	coinbase.getCurrency()
	coinbase.getBuyPrice(qty)
	coinbase.getSellPrice(qty)