from flask import Flask, render_template, request
app=Flask(__name__)
app.config["DEBUG"]=True
@app.route("/", methods=["POST","GET"])


def hello():
		
		return render_template("template.html", status="fucked", uptime="0", hashrate="0", moneyrate="0", balance="13.74", eurprice="1500", usdprice="1800", zecprice="0.054",zecprof="5.4", miner1="Ülo")
if __name__=="__main__":
	app.run(port=80)
	