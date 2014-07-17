#!/usr/bin/env python

import urllib2, json, urllib, hashlib, time, hmac

user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_0) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31"
api_key = "" 	##  Replace with your api key!    ##
api_secret = ""	##  Replace with your api secret! ##
base_url = "https://coinbase.com/api/v1/"


class Coinbase(object):
	def parse_request(self, request_type, arg = None, body = None):
		req = None
		if request_type == "accounts":
			url = base_url + "accounts?page=" + str(arg)
		elif request_type == "addresses": ## arg is current page index
			url = base_url + "addresses?page=" + str(arg)
		elif request_type == "create_account":
			url = base_url + "accounts";
#		elif request_type == "exchange_rates":
#		elif request_type == "buy_price":
#		elif request_type == "sell_price":
#		elif request_type == "buy":
#		elif request_type == "sell":

		nonce = int(time.time() * 1e6)
		message = str(nonce) + url + ('' if body is None else body)
		signature = hmac.new(api_secret, message, hashlib.sha256).hexdigest()
		header = {
			"ACCESS_KEY" : api_key,
			"ACCESS_SIGNATURE" : signature,
			"ACCESS_NONCE" : nonce,
			"Accept" : "application/json",
		}

		if body:
			header.update({"Content-Type": "application/json"})
			req = urllib2.Request(url, data = body, headers = header);
		else:
			req = urllib2.Request(url, headers = header);

		if req:
			content = urllib2.urlopen(req)
			return json.loads(content.read())
		else:
			print "Invalid request!"
			return None

	def getAddresses(self):
		addr = self.parse_request("addresses", arg = 1)
		if addr:
			pages = addr["num_pages"]
			print "=============== Bitcoin addresses I have associated with my primary account: ================"
			for page in range(pages):
				addr = self.parse_request("addresses", arg = page+1)
				for _addr in addr["addresses"]:
					print _addr["address"]["address"] + "\t Created at: " + _addr["address"]["created_at"]

	def getAccounts(self):
		acc = self.parse_request("accounts", arg = 1)
		if acc:
			pages = acc["num_pages"]
			print "===== Bitcoin accounts: ====="
			for page in range(pages):
				acc = self.parse_request("accounts", arg = page+1)
				for _acc in acc["accounts"]:
					print "id:%s\tname:%s\t\tbalance:%s %s" % (_acc["id"], _acc["name"], _acc["balance"]["amount"], _acc["balance"]["currency"])

	def createAccount(self, name):
		account = {
			"account" : {
				"name": name
			}
		}
		result = self.parse_request("create_account", body = json.dumps(account));
#		print json.dumps(result, indent = 4, separators = (",", ":"))

if __name__ == "__main__":
	coinbase = Coinbase()
#	coinbase.getAddresses()
	coinbase.getAccounts()
#	coinbase.createAccount("test")
