import requests
from flask import Flask, render_template, request
app=Flask(__name__)
@app.route("/", methods=["POST","GET"])

def hello():
	
	priceApi=requests.get("https://api.coinmarketcap.com/v1/ticker/bitcoin/?convert=EUR")
	priceData=priceApi.json()
	minerApi=requests.get("https://api.nicehash.com/api?method=stats.provider&addr=36VitWXAXFyvdKaui9sPuKDnQwdtBWGieV")
	minerData=minerApi.json()
	zecApi=requests.get("https://api.coinmarketcap.com/v1/ticker/zcash/")
	zecData=zecApi.json()
	def getStatus():
		if hashrate=="000":
			return "Fucked"
		else:
			return "Up"
	def getUptime():
		return "lol"
	def getHashrate():
		return minerData["result"]["stats"][2]["accepted_speed"][8:]+"0"
	def getMoneyrate():
		return "lol"
	def getBalance():
		return minerData["result"]["stats"][2]["balance"]
	def getEur():
		return priceData[0]["price_eur"][:7]
	def getUsd():
		return priceData[0]["price_usd"]
	def getZec():
		return zecData[0]["price_btc"]
	def getProf():
		return "lol"
	
	
		
	uptime = getUptime()
	hashrate = getHashrate()
	status =  getStatus()
	moneyrate = getMoneyrate()
	balance = getBalance()
	eurprice = getEur()
	usdprice = getUsd()
	zecprice = getZec()
	zecprof = getProf()
	miner1 = "Ülo"
	
	
	return render_template("template.html", status=status, uptime=uptime, hashrate=hashrate, moneyrate=moneyrate, balance=balance, eurprice=eurprice, usdprice=usdprice, zecprice=zecprice,zecprof=zecprof, miner1=miner1)
	

if __name__=="__main__":
	app.run(host="0.0.0.0",port=80)
	