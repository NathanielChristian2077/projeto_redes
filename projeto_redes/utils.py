import json
import os

PATH = "chat_history.json"

def hist_save(mensagem):
    hist = load_hist()
    if mensagem not in hist:    
        hist.append(mensagem)
        with open(PATH, 'w', encoding='utf-8') as file:
            json.dump(hist, file, ensure_ascii=False, indent=4)

def load_hist():
    if not os.path.exists(PATH):
        return []
    try:
        with open(PATH, 'r', encoding='utf-8') as file:
            return json.load(file)
    except json.JSONDecodeError:
        return[]