import os
import json
import requests

# ===== CONFIG DA ENV =====
API_URL = os.environ["API_URL"]
TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]
STATE_FILE = "stato_plafond.json"

# Funzione invio Telegram
def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": CHAT_ID, "text": msg})

# Legge il plafond dall'API
def get_plafond():
    r = requests.get(API_URL, timeout=10)
    r.raise_for_status()
    data = r.json()
    # ⚠️ Modifica se il campo JSON è diverso
    return data["residuoPlafond"]

# Carica ultimo valore salvato
def load_old():
    if not os.path.exists(STATE_FILE):
        return None
    with open(STATE_FILE) as f:
        return json.load(f)["value"]

# Salva valore corrente
def save(val):
    with open(STATE_FILE, "w") as f:
        json.dump({"value": val}, f)

# Logica principale
def main():
    current = get_plafond()
    old = load_old()

    if old is None:
        save(current)
        send_telegram(f"📊 Monitor avviato\nValore iniziale: {current}")
    elif current != old:
        send_telegram(f"🚨 PLAFOND MODIFICATO\nPrima: {old}\nOra: {current}")
        save(current)

if __name__ == "__main__":
    main()
