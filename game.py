import random
import json

FILE = "players.json"

PARTIES = {}        # gangs
TERRITORIES = {     # mapa de controlo
    "centro": None,
    "bairros": None,
    "industrial": None,
    "armazens": None
}


# -------------------------
# DATA
# -------------------------

def load():
    try:
        with open(FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=2)


def init(uid, data):
    uid = str(uid)
    if uid not in data:
        data[uid] = {
            "money": 300,
            "actions": 3,
            "day": 1,
            "luck": 0,
            "rep": 0,
            "crime": 0,
            "scooter": False,
            "location": "centro",
            "party": None
        }


# -------------------------
# MAPA
# -------------------------

MAPA = {
    "centro": ["bairros"],
    "bairros": ["centro", "industrial"],
    "industrial": ["bairros", "armazens"],
    "armazens": ["industrial"]
}


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
        ("Ajuda de gang local", 30)
    ]
    t, m = random.choice(events)
    p["money"] += m
    return f"🧍 {t} ({m}€)"


# -------------------------
# GAMBLING
# -------------------------

def gamble(p, n):
    roll = random.randint(1, 10)
    p["actions"] -= 1

    if roll == n:
        win = 120 + p["luck"] * 10
        p["money"] += win
        return f"🎰 GANHASTE +{win}€"
    else:
        p["money"] -= 25
        return f"💸 Perdeu ({roll})"


# -------------------------
# TRABALHO
# -------------------------

def work(p, t):
    bonus = 1.5 if p["scooter"] and t == "entregas" else 1

    if t == "entregas":
        gain = int(random.randint(60, 110) * bonus)
    else:
        gain = random.randint(70, 130)

    p["money"] += gain
    p["actions"] -= 1
    return f"💼 {t}: +{gain}€"


# -------------------------
# SHOP
# -------------------------

def shop(p, item):
    if item == "scooter":
        if p["money"] >= 250:
            p["money"] -= 250
            p["scooter"] = True
            return "🛵 Scooter comprada"
    if item == "sorte":
        if p["money"] >= 300:
            p["money"] -= 300
            p["luck"] += 1
            return "🍀 Sorte +1"
    return "❌ item inválido"


# -------------------------
# GANGS (PARTIES)
# -------------------------

def create_party(uid, name):
    if uid in PARTIES:
        return "❌ já tens gang"

    PARTIES[name] = {
        "leader": uid,
        "members": [uid],
        "power": 0
    }
    return f"🧑‍🤝‍🧑 gang {name} criada"


def join_party(uid, name):
    if name not in PARTIES:
        return "❌ não existe"

    PARTIES[name]["members"].append(uid)
    return "🚪 entraste na gang"


# -------------------------
# GUERRA DE TERRITÓRIOS
# -------------------------

def attack_territory(uid, territory):
    player_gang = None

    for g, data in PARTIES.items():
        if uid in data["members"]:
            player_gang = g

    if not player_gang:
        return "❌ não estás numa gang"

    power = len(PARTIES[player_gang]["members"]) * random.randint(5, 15)

    if TERRITORIES[territory] is None:
        TERRITORIES[territory] = player_gang
        return f"🏴 conquistaste {territory}"

    enemy = TERRITORIES[territory]

    enemy_power = len(PARTIES.get(enemy, {"members": []})["members"]) * random.randint(5, 15)

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
# PROCESSOR
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
        save(data)
        return f"🌙 dia {p['day']}"

    save(data)
    return "❌ comando inválido (/cmd)"
