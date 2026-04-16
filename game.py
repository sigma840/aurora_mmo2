import random
import json
import os

FILE = "players.json"

# -------------------------
# STATE (GLOBAL SAFE)
# -------------------------

PARTIES = {}
TERRITORIES = {
    "centro": None,
    "bairros": None,
    "industrial": None,
    "armazens": None
}

# -------------------------
# DATA HANDLING
# -------------------------

def load():
    try:
        if not os.path.exists(FILE):
            return {}
        with open(FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save(data):
    try:
        with open(FILE, "w") as f:
            json.dump(data, f, indent=2)
    except:
        pass


def init(uid, data):
    uid = str(uid)
    if uid not in data:
        data[uid] = {
            "money": 300,
            "actions": 3,
            "day": 1,
            "luck": 0,
            "scooter": False
        }

# -------------------------
# MAPA
# -------------------------

def mapa():
    txt = "🗺️ TERRITÓRIOS:\n\n"
    for t, owner in TERRITORIES.items():
        txt += f"{t} → {owner or 'neutro'}\n"
    return txt

# -------------------------
# RANKINGS
# -------------------------

def rankings(data):
    players = [(uid, p["money"]) for uid, p in data.items()]
    top = sorted(players, key=lambda x: x[1], reverse=True)[:5]

    txt = "🏆 RANKINGS\n"
    for i, p in enumerate(top):
        txt += f"{i+1}. {p[0]} - {p[1]}€\n"
    return txt

# -------------------------
# EXPLORAR
# -------------------------

def explore(p):
    p["actions"] -= 1

    events = [
        ("Encontraste dinheiro", random.randint(10, 50)),
        ("Dia calmo", 0),
        ("Roubo falhado", -20),
        ("Ajuda de desconhecido", 25)
    ]

    t, m = random.choice(events)
    p["money"] += m
    return f"🧍 {t} ({m}€)"

# -------------------------
# GAMBLING
# -------------------------

def gamble(p, n):
    p["actions"] -= 1
    roll = random.randint(1, 10)

    if roll == n:
        win = 100 + p["luck"] * 10
        p["money"] += win
        return f"🎰 GANHASTE +{win}€"
    else:
        p["money"] -= 20
        return f"💸 Perdeste ({roll})"

# -------------------------
# WORK
# -------------------------

def work(p, t):
    p["actions"] -= 1

    if t == "entregas":
        gain = random.randint(60, 120)
        if p.get("scooter"):
            gain += 30
    else:
        gain = random.randint(70, 130)

    p["money"] += gain
    return f"💼 Trabalho ({t}): +{gain}€"

# -------------------------
# SHOP
# -------------------------

def shop(p, item):
    if item == "scooter":
        if p["money"] >= 250:
            p["money"] -= 250
            p["scooter"] = True
            return "🛵 Scooter comprada"
        return "❌ sem dinheiro"

    if item == "sorte":
        if p["money"] >= 300:
            p["money"] -= 300
            p["luck"] += 1
            return "🍀 Sorte aumentada"
        return "❌ sem dinheiro"

    return "❌ item inválido"

# -------------------------
# GANGS
# -------------------------

def create_party(uid, name):
    if uid in [m for g in PARTIES.values() for m in g["members"]]:
        return "❌ já estás numa gang"

    PARTIES[name] = {
        "leader": uid,
        "members": [uid]
    }
    return f"🧑‍🤝‍🧑 Gang {name} criada"

def join_party(uid, name):
    if name not in PARTIES:
        return "❌ gang não existe"

    PARTIES[name]["members"].append(uid)
    return "🚪 Entraste na gang"

# -------------------------
# TERRITORY WAR (FIXED SAFE)
# -------------------------

def attack_territory(uid, territory):
    player_gang = None

    for g, data in PARTIES.items():
        if uid in data["members"]:
            player_gang = g

    if not player_gang:
        return "❌ não estás numa gang"

    if territory not in TERRITORIES:
        return "❌ território inválido"

    power = len(PARTIES[player_gang]["members"]) * random.randint(5, 15)

    if TERRITORIES[territory] is None:
        TERRITORIES[territory] = player_gang
        return f"🏴 conquistaste {territory}"

    enemy = TERRITORIES[territory]

    if enemy not in PARTIES:
        enemy_power = random.randint(20, 60)
    else:
        enemy_power = len(PARTIES[enemy]["members"]) * random.randint(5, 15)

    if power > enemy_power:
        TERRITORIES[territory] = player_gang
        return f"⚔️ conquistaste {territory} aos {enemy}"
    else:
        return "💥 falhaste a invasão"

# -------------------------
# CMD
# -------------------------

def cmd():
    return """
📌 COMANDOS:

💰 saldo
🗺️ mapa
🏆 rankings

💼 trabalhar entregas / construcao
🎰 apostar X
🧍 explorar

🏪 shop scooter / sorte

🧑‍🤝‍🧑 gang create NOME
🧑‍🤝‍🧑 gang join NOME

⚔️ atacar TERRITORIO

🛏️ dormir
"""

# -------------------------
# MAIN PROCESS
# -------------------------

def process(uid, text):
    data = load()
    uid = str(uid)

    init(uid, data)
    p = data[uid]

    t = text.lower()

    if "cmd" in t:
        return cmd()

    if "mapa" in t:
        return mapa()

    if "rankings" in t:
        return rankings(data)

    if "saldo" in t:
        return f"💰 {p['money']}€"

    if "explorar" in t:
        return explore(p)

    if "apostar" in t:
        try:
            n = int(t.split()[-1])
        except:
            return "uso: apostar X"
        return gamble(p, n)

    if "trabalhar" in t:
        if "entregas" in t:
            return work(p, "entregas")
        return work(p, "construcao")

    if "shop" in t:
        return shop(p, t.replace("shop", "").strip())

    if "gang create" in t:
        name = t.replace("gang create", "").strip()
        return create_party(uid, name)

    if "gang join" in t:
        name = t.replace("gang join", "").strip()
        return join_party(uid, name)

    if "atacar" in t:
        territory = t.replace("atacar", "").strip()
        return attack_territory(uid, territory)

    if "dormir" in t:
        p["day"] += 1
        p["actions"] = 3
        return f"🌙 novo dia"

    save(data)
    return "❌ comando inválido (/cmd)"
