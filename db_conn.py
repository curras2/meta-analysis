from pymongo import MongoClient
import extras.extras as ext
from bson.codec_options import CodecOptions

class DbConnection:
    def __init__(self):
        self.client = MongoClient(ext.string_connection)
        self.conn = self.client[ext.db]
        self.banrate_collection = self.conn[ext.banrate_collection]
        self.champion_winrate_collection = self.conn[ext.champion_winrate_collection]
        self.pickrate_collection = self.conn[ext.pickrate_collection]
        self.objectives_winrate_collection = self.conn[ext.objectives_winrate_collection]
        self.side_winrate_collection = self.conn[ext.side_winrate_collection]
        self.dragon_soul_winrate_collection = self.conn[ext.dragon_soul_winrate_collection]
        self.game_length_mean_collection = self.conn[ext.game_length_mean_collection]

    def __upsert_record(self, collection, new_data):
        for i in new_data:
            query = {
                    "league": i["league"],
                    "split": i["split"],
                    "patch": i["patch"],
                }
            if "champion" in i:
                query["champion"] = i["champion"]
            elif "side" in i:
                query["side"] = i["side"]
            elif "soul" in i:
                query["soul"] = i["soul"]
            elif "objective" in i:
                query["objective"] = i["objective"]
            
            collection.update_one(query, {"$set": i}, upsert=True)

    def upsert_banrate_record(self, data):
        self.__upsert_record(self.banrate_collection, data)

    def upsert_champion_winrate_record(self, data):
        self.__upsert_record(self.champion_winrate_collection, data)

    def upsert_pickrate_record(self, data):
        self.__upsert_record(self.pickrate_collection, data)

    def upsert_objectives_winrate_record(self, data):
        self.__upsert_record(self.objectives_winrate_collection, data)

    def upsert_side_winrate_record(self, data):
        self.__upsert_record(self.side_winrate_collection, data)

    def upsert_dragon_soul_winrate_record(self, data):
        self.__upsert_record(self.dragon_soul_winrate_collection, data)

    def upsert_game_length_mean_record(self, data):
        self.__upsert_record(self.game_length_mean_collection, data)

    def __get_records(self, collection):
        codec_options = CodecOptions(unicode_decode_error_handler='replace')
        collection_with_options = collection.with_options(codec_options=codec_options)

        results = collection_with_options.find({}, {'_id': 0})

        return results

    def get_banrate(self):
        results = self.__get_records(self.banrate_collection)

        return results

    def get_pickrate(self):
        results = self.__get_records(self.pickrate_collection)

        return results

    def get_champion_winrate(self):
        results = self.__get_records(self.champion_winrate_collection)

        return results

    def get_objectives_winrate(self):
        results = self.__get_records(self.objectives_winrate_collection)

        return results

    def get_side_winrate(self):
        results = self.__get_records(self.side_winrate_collection)

        return results

    def get_dragon_soul_winrate(self):
        results = self.__get_records(self.dragon_soul_winrate_collection)

        return results

    def get_game_length_mean(self):
        results = self.__get_records(self.game_length_mean_collection)

        return results
