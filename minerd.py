import serial
import time
from functools import wraps
import requests
from flask import Flask, render_template, request, Response

ser=serial.Serial("/dev/ttyUSB0")

app=Flask(__name__)
def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    return username == 'admin' and password == 'secret'

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'FUCK OFF', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated
@app.route("/", methods=["GET","POST"])
@requires_auth
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
		try:
			return workerData["result"]["workers"][0][2]
		except IndexError:
			return "0"
	def getHashrate():
		try:
			return workerData["result"]["workers"][0][1]["a"]
		except IndexError:
			return "0"
	def getDiff():
		try:
			return workerData["result"]["workers"][0][4]
		except IndexError:
			return "0"
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
	miner1 = "Ylo"
	if request.method=="POST":
		password=request.form['password']
		if password=="salakala":
			print("RESTARTING")
			ser.write(b"a")
			time.sleep(10)
			ser.write(b"A")
	
	
	return render_template("template.html", status=status, uptime=uptime, hashrate=hashrate, diff=diff, balance=balance, eurprice=eurprice, usdprice=usdprice, zecprice=zecprice, miner1=miner1)
@app.route("/lul", methods=["GET","POST"])
def lol():
	return render_template("template.html")





if __name__=="__main__":
	app.run(host="0.0.0.0",port=80)
	 
