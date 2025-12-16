import os
import json
import requests

API_URL = os.environ["API_URL"]
TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]
OLD_FILE = "old_value.json"

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": CHAT_ID, "text": msg})

def get_plafond():
    r = requests.get(API_URL, timeout=10)
    r.raise_for_status()
    data = r.json()
    return data["residuoPlafond"]  # adatta se il campo JSON è diverso

def load_old():
    if os.path.exists(OLD_FILE):
        with open(OLD_FILE) as f:
            return json.load(f).get("value")
    # Primo run: usa valore iniziale di riferimento
    return 0  # <-- metti qui il valore iniziale del plafond

def save(val):
    with open(OLD_FILE, "w") as f:
        json.dump({"value": val}, f)

def main():
    current = get_plafond()
    old = load_old()

    if old is None:
        # Primo avvio
        send_telegram(f"📊 Monitor avviato. Valore iniziale: {current}")
    elif current != old:
        send_telegram(f"🚨 PLAFOND MODIFICATO\nPrima: {old}\nOra: {current}")

    # Salva sempre l’ultimo valore per l’artifact
    save(current)

if __name__ == "__main__":
    main()
