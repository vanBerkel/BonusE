import os
import requests
import json

print("DEBUG: env keys =", list(os.environ.keys()))

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

def get_old_value():
    r = requests.get(GIST_URL, headers=HEADERS)
    r.raise_for_status()
    print("DEBUG: response text (first 500 chars) =", r.text[:500])

    content = r.json()["files"]["plafond.json"]["content"]
    return int(json.loads(content)["value"])

def save_value(value):
    value = int(value)
    payload = {
        "files": {
            "plafond.json": {
                "content": json.dumps({"value": value})
            }
        }
    }
    
    r = requests.patch(GIST_URL, headers=HEADERS, json=payload)
    print("PATCH STATUS:", r.status_code)
    print("PATCH RESPONSE:", r.text)
    r.raise_for_status()

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, json={
        "chat_id": CHAT_ID,
        "text": msg
    })

def main():
    current = get_plafond()
    print("DEBUG: type(current) =", type(current), "value =", current)
    if current > 11000:
        send_telegram(
            f"🚨 PLAFOND Voucher\n"
            f"Money: {current}"
        )
    old = get_old_value()

    if current != old:
        send_telegram(
            f"🚨 PLAFOND MODIFICATO\n"
            f"Prima: {old}\n"
            f"Ora: {current}"
        )
        save_value(current)

if __name__ == "__main__":
    main()
