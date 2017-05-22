import serial
import time
from functools import wraps
import requests
from flask import Flask, render_template, request, Response

#ser=serial.Serial("/dev/ttyUSB0")

file = open("conf","r")
confU=file.readline()[:-1]
confP=file.readline()[:-1]
confR=file.readline()[:-1]

app=Flask(__name__)

def upString(minutes):
        minutes=int(minutes)
        r=""
        dys=int(minutes/1440)
        hrs=int((minutes-dys*1440)/60)
        mns=minutes-dys*1440-hrs*60
        if dys==1:
            days=" day "
        else:
            days=" days "
        if hrs==1:
            hours=" hour "
        else:
            hours=" hours "
        if mns==1:
            mins=" minute"
        else:
            mins=" minutes"
        if dys:
            r+=str(dys)+days
        if hrs:
            r+=str(hrs)+hours
        if mns:
            r+=str(mns)+mins
        return r

def check_auth(username, password):
        return username == confU and password == confP

def authenticate():
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
    pwstat=""
    if request.method=="POST":
        password=request.form['password']
        if password==confR:
            print("RESTARTING")
            pwstat="Restart Successful"
            #ser.write(b"a")
            time.sleep(10)
            #ser.write(b"A")
        else:
            pwstat="Incorrect Password"
            
    priceApi=requests.get("http://api.coindesk.com/v1/bpi/currentprice.json")
    minerApi=requests.get("https://api.nicehash.com/api?method=stats.provider&addr=36VitWXAXFyvdKaui9sPuKDnQwdtBWGieV")
    workerApi=requests.get("https://api.nicehash.com/api?method=stats.provider.workers&addr=36VitWXAXFyvdKaui9sPuKDnQwdtBWGieV&algo=24")
    zecApi=requests.get("https://api.coinmarketcap.com/v1/ticker/zcash/")
    priceData=priceApi.json()
    minerData=minerApi.json()
    workerData=workerApi.json()
    zecData=zecApi.json()
		  
    try:
        uptime = upString(workerData["result"]["workers"][0][2])
        hashrate = workerData["result"]["workers"][0][1]["a"]
    except IndexError:
        uptime = "0 minutes"
        hashrate = "0"
    if hashrate == "0":
        status = "Fucked"
    else:
        status = "Up"
	            
    balance = minerData["result"]["stats"][2]["balance"]
    eurprice = str(priceData["bpi"]["EUR"]["rate_float"])[:-2]
    balEur = str(float(balance)*float(eurprice))
    usdprice = str(priceData["bpi"]["USD"]["rate_float"])[:-2]
    zecprice = zecData[0]["price_btc"]
    miner1 = "Ylo"
    
    return render_template("template.html", status=status, uptime=uptime, hashrate=hashrate, balEur=balEur, balance=balance, eurprice=eurprice, usdprice=usdprice, zecprice=zecprice, miner1=miner1, pwstat=pwstat)

if __name__=="__main__":
    app.run(host="0.0.0.0",port=80)
	 
