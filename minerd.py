import _thread
import serial
import time
from functools import wraps
import requests
from flask import Flask, render_template, request, Response

no_of_times_serial_left_commented=6


def upString(minutes):
        minutes = int(minutes)
        r = ""
        dys = int(minutes/1440)
        hrs = int((minutes-dys*1440)/60)
        mns = minutes-dys*1440-hrs*60
        if dys == 1:
            days = " day "
        else:
            days = " days "
        if hrs == 1:
            hours = " hour "
        else:
            hours = " hours "
        if mns == 1:
            mins = " minute"
        else:
            mins = " minutes"
        if dys:
            r += str(dys)+days
        if hrs:
            r += str(hrs)+hours
        if mns:
            r += str(mns)+mins
        return r


def formatValue(raw):
    val1 = str(int(raw))+"."
    dec=int((raw-int(raw))*100)
    if(dec<10):
        val2="0"+str(dec)
    else:
        val2=str(dec)
    return val1+val2
class Apis:
    uptime = "Loading"
    hashrate = "Loading"
    balance = "Loading"
    eurprice = "Loading"
    usdprice = "Loading"
    zecprice = "Loading"
    profit = "Loading"
    miner1 = "Ylo"
    balEur = ""
    profEur = ""
    status = ""


    def apiGet(self):
        
        try:
            priceApi = requests.get("http://api.coindesk.com/v1/bpi/currentprice.json")
            minerApi = requests.get("https://api.nicehash.com/api?method=stats.provider&addr=36VitWXAXFyvdKaui9sPuKDnQwdtBWGieV")
            workerApi = requests.get("https://api.nicehash.com/api?method=stats.provider.workers&addr=36VitWXAXFyvdKaui9sPuKDnQwdtBWGieV&algo=24")
            zecApi = requests.get("https://api.coinmarketcap.com/v1/ticker/zcash/")
            profApi = requests.get("https://api.nicehash.com/api?method=stats.provider.ex&addr=36VitWXAXFyvdKaui9sPuKDnQwdtBWGieV")
            priceData = priceApi.json()
            minerData = minerApi.json()
            workerData = workerApi.json()
            zecData = zecApi.json()
            profData = profApi.json()
        except:
            print("API error")
            return

        try:
            self.uptime = upString(workerData["result"]["workers"][0][2])
            self.hashrate = workerData["result"]["workers"][0][1]["a"]
        except:
            self.uptime = "0 minutes"
            self.hashrate = "0"

        if self.hashrate == "0":
            self.status = "Fucked"
        else:
            self.status = "Up"

        balMbtc = 1000*float(minerData["result"]["stats"][1]["balance"])
        eurRate = priceData["bpi"]["EUR"]["rate_float"]
        eur = eurRate*balMbtc/1000
        self.balance=formatValue(balMbtc)+" mBTC"
        self.balEur = formatValue(eur)+" €"
        self.usdprice = str(priceData["bpi"]["USD"]["rate_float"])[:7]
        self.eurprice = str(eurRate)[:7]
        self.zecprice = zecData[0]["price_btc"]

        try:
            profMbtc = float(profData["result"]["current"][1]["profitability"])*1000*float(self.hashrate)
            self.profit = formatValue(profMbtc)+" mBTC"
            prfEur = profMbtc*eurRate/1000
            self.profEur = formatValue(prfEur)+" €"
        except KeyError:
            pass

        print("APIs updated")


ser = serial.Serial("/dev/ttyUSB0")

file = open("conf", "r")
confU = file.readline()[:-1]
confP = file.readline()[:-1]
confR = file.readline()[:-1]

app = Flask(__name__)

apis = Apis()


def refreshApis():
    while True:
        apis.apiGet()
        time.sleep(30)


def check_auth(username, password):
        return username == confU and password == confP


def authenticate():
    return Response('FUCK OFF', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated


@app.route("/", methods=["GET", "POST"])
@requires_auth
def hello():
    pwstat = ""
    if request.method == "POST":
        password = request.form['password']
        if password == confR:
            print("RESTARTING")
            pwstat = "Restart Successful"
            ser.write(b"a")
            time.sleep(10)
            ser.write(b"A")
        else:
            pwstat = "Incorrect Password"

    return render_template("template.html", profEur=apis.profEur, status=apis.status, profit=apis.profit, uptime=apis.uptime, hashrate=apis.hashrate, balEur=apis.balEur, balance=apis.balance, eurprice=apis.eurprice, usdprice=apis.usdprice, zecprice=apis.zecprice, miner1=apis.miner1, pwstat=pwstat)

if __name__ == "__main__":
    _thread.start_new_thread(app.run, ("0.0.0.0", 80))
    _thread.start_new_thread(refreshApis())
