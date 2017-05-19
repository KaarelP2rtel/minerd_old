import requests

workerApi=requests.get("https://api.nicehash.com/api?method=stats.provider.workers&addr=36VitWXAXFyvdKaui9sPuKDnQwdtBWGieV&algo=24")
workerData=workerApi.json()
print(workerData["result"]["workers"][0][2])