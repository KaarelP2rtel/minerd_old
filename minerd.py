import requests
from flask import Flask, render_template, request
app=Flask(__name__)
@app.route("/", methods=["GET","POST"])
def hello():
	
	priceApi=requests.get("https://api.coinmarketcap.com/v1/ticker/bitcoin/?convert=EUR")
	priceData=priceApi.json()
	minerApi=requests.get("https://api.nicehash.com/api?method=stats.provider&addr=36VitWXAXFyvdKaui9sPuKDnQwdtBWGieV")
	minerData=minerApi.json()
	workerApi=requests.get("https://api.nicehash.com/api?method=stats.provider.workers&addr=36VitWXAXFyvdKaui9sPuKDnQwdtBWGieV&algo=24")
	workerData=workerApi.json()
	zecApi=requests.get("https://api.coinmarketcap.com/v1/ticker/zcash/")
	zecData=zecApi.json()
	def getStatus():
		if hashrate=="000":
			
			return "Fucked"
		else:
			return "Up"
	def getUptime():
		return workerData["result"]["workers"][0][2]
	def getHashrate():
		return minerData["result"]["stats"][2]["accepted_speed"][8:]+"0"
	def getDiff():
		return workerData["result"]["workers"][0][4]
	def getBalance():
		return minerData["result"]["stats"][2]["balance"]+ " BTC"
	def getEur():
		return priceData[0]["price_eur"][:7]
	def getUsd():
		return priceData[0]["price_usd"]
	def getZec():
		return zecData[0]["price_btc"]

	
	
		  
	uptime = getUptime()
	hashrate = getHashrate()
	status =  getStatus()
	diff = getDiff()
	balance = getBalance()
	eurprice = getEur()
	usdprice = getUsd()
	zecprice = getZec()
	miner1 = "Ülo"
	if request.method=="POST":
		password=request.form['password']
		if password=="salakala":
			print("RESTARTING")
	
	
	return render_template("template.html", status=status, uptime=uptime, hashrate=hashrate, diff=diff, balance=balance, eurprice=eurprice, usdprice=usdprice, zecprice=zecprice, miner1=miner1)
	
if __name__=="__main__":
	app.run(host="0.0.0.0",port=80)
	 