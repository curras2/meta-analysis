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