from pymongo import MongoClient
import extras.extras as ext

client = MongoClient(ext.string_connection)

conn = client[ext.db]

banrate_collection = conn[ext.banrate_collection]
champion_winrate_collection = conn[ext.champion_winrate_collection]
pickrate_collection = conn[ext.pickrate_collection]
objectives_winrate_collection = conn[ext.objectives_winrate_collection]
side_winrate_collection = conn[ext.side_winrate_collection]
dragon_soul_winrate_collection = conn[ext.dragon_soul_winrate_collection]
game_length_mean_collection = conn[ext.game_length_mean_collection]

def upsert_record(collection, new_data):
    query = {
        "league": new_data["league"],
        "split": new_data["split"],
        "patch": new_data["patch"],
    }
    collection.update_one(query, {"$set": new_data}, upsert=True)

def upsert_banrate_record(data):
    upsert_record(banrate_collection, data)

def upsert_champion_winrate_record(data):
    upsert_record(champion_winrate_collection, data)

def upsert_pickrate_record(data):
    upsert_record(pickrate_collection, data)

def upsert_objectives_winrate_record(data):
    upsert_record(objectives_winrate_collection, data)

def upsert_side_winrate_record(data):
    upsert_record(side_winrate_collection, data)

def upsert_dragon_soul_winrate_record(data):
    upsert_record(dragon_soul_winrate_collection, data)

def upsert_game_length_mean_record(data):
    upsert_record(game_length_mean_collection, data)