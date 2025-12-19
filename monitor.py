import os
import requests
import json
import time
import random

API_URL = os.environ["API_URL"]
TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

GIST_ID = os.environ["GIST_ID"]
GIT_HUB_TOKEN = os.environ["GIST_PAT"]

GIST_URL = f"https://api.github.com/gists/{GIST_ID}"

HEADERS = {
    "Authorization": f"Bearer {GIT_HUB_TOKEN}",
    "Accept": "application/vnd.github+json",
    "User-Agent": "PythonMonitor"
}


def get_plafond():
    r = requests.get(API_URL, timeout=10)
    r.raise_for_status()
    return int(r.json()["residuoPlafond"])  # verifica il campo





def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, json={
        "chat_id": CHAT_ID,
        "text": msg
    })

def main():
    current = get_plafond()
    if current > 11000:
        send_telegram(
            f"🚨 PLAFOND Voucher T\n"
            f"Money: {current}"
        )
   
if __name__ == "__main__":
    try:
        while True:
            main()
            time.sleep(random.randint(9, 23))
    except KeyboardInterrupt:
        print("Monitor interrotto")
