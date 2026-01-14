from pymongo import MongoClient
from config import MONGO_URI

db = MongoClient(MONGO_URI).guardian

settings = db.settings
warnings = db.warnings
stats = db.stats
whitelist = db.whitelist

def get_lang(chat_id):
    d = settings.find_one({"chat_id": chat_id})
    return d.get("lang", "en") if d else "en"

def set_lang(chat_id, lang):
    settings.update_one({"chat_id": chat_id}, {"$set": {"lang": lang}}, upsert=True)

def add_warning(chat_id, user_id):
    d = warnings.find_one({"chat_id": chat_id, "user_id": user_id})
    c = d["count"] + 1 if d else 1
    warnings.update_one(
        {"chat_id": chat_id, "user_id": user_id},
        {"$set": {"count": c}},
        upsert=True
    )
    return c

def get_warnings(chat_id, user_id):
    d = warnings.find_one({"chat_id": chat_id, "user_id": user_id})
    return d["count"] if d else 0

def reset_warnings(chat_id, user_id):
    warnings.delete_one({"chat_id": chat_id, "user_id": user_id})

def add_stat(chat_id, key):
    stats.update_one({"chat_id": chat_id}, {"$inc": {key: 1}}, upsert=True)

def get_stats(chat_id):
    return stats.find_one({"chat_id": chat_id}) or {}

def add_whitelist(chat_id, link):
    whitelist.update_one(
        {"chat_id": chat_id},
        {"$addToSet": {"links": link}},
        upsert=True
    )

def get_whitelist(chat_id):
    d = whitelist.find_one({"chat_id": chat_id})
    return d.get("links", []) if d else []