import datetime
import os
from typing import Any
from dateutil.relativedelta import relativedelta

import bson
import pymongo.collection
from pymongo import MongoClient as MongoClient
from pymongo.command_cursor import CommandCursor

import credentials
import processing


class DatabaseControl:
    CONNECT_WITH_CREDENTIALS: dict = {
        "host": credentials.DATABASE_HOST_URI,
        "port": credentials.DATABASE_PORT,
        "username": credentials.DATABASE_USER,
        "password": credentials.DATABASE_USER_PASSWORD,
        "authSource": credentials.DATABASE_AUTH_DB_NAME,
        "authMechanism": "SCRAM-SHA-256",
    }

    def restore_from_dump(self,
                          database_name: str,
                          path_to_dump: str,
                          db_flag: bool = True,
                          _credentials: dict = None) -> None:
        if not db_flag:
            return

        _credentials: dict = _credentials or self.CONNECT_WITH_CREDENTIALS
        client = MongoClient(**_credentials)

        db = client[database_name]
        for coll in os.listdir(path_to_dump):
            if coll.endswith('.bson'):
                with open(os.path.join(path_to_dump, coll), 'rb+') as f:
                    db[coll.split('.')[0]].insert_many(bson.decode_all(f.read()))

    def get_collection(self,
                       database_name: str,
                       collection_name: str,
                       db_flag: bool = True,
                       _credentials: dict = None) -> pymongo.collection.Collection | None:
        if not db_flag:
            return

        _credentials: dict = _credentials or self.CONNECT_WITH_CREDENTIALS
        client = MongoClient(**_credentials)

        db = client[database_name]
        data_collection = db[collection_name]

        return data_collection

    def get_statistics_collection(self) -> pymongo.collection.Collection | None:
        return self.get_collection(database_name=credentials.DATABASE_NAME,
                                   collection_name=credentials.DATABASE_STATISTICS_COLLECTION_NAME)

    def get_result(self, dt_from: datetime.datetime,
                   dt_upto: datetime.datetime,
                   group_type: str) -> dict:
        sample_collection: pymongo.collection.Collection = self.get_statistics_collection()
        key_value: dict = {
            "dt": {
                "$gte": dt_from,
                "$lte": dt_upto
            }
        }
        grouping_mapping: dict = {
            "_id": {
                "date": {
                    "$dateTrunc": {
                        "date": "$dt",
                        "unit": group_type
                    }
                }
            },
            "dataset": {
                "$sum":
                    "$value"
            }
        }
        _arguments: dict = {f"{group_type}s": +1}
        extra_step_to_include_upper_bound: relativedelta = relativedelta(**_arguments)
        dt_upto_including_upper_bound = dt_upto + extra_step_to_include_upper_bound
        density: dict = {
            "field": "_id.date",
            "range": {
                "bounds": [dt_from, dt_upto_including_upper_bound if dt_upto.minute == 0 else dt_upto],
                "step": 1,
                "unit": group_type
            },
        }
        filling: dict = {"output": {"dataset": {"value": 0}}}

        result: CommandCursor[Any] = sample_collection.aggregate([
            # retrieve matching dates
            {"$match": key_value},

            # group by 'group_type'
            {"$group": grouping_mapping},

            # densify (create missing dates)
            # 'densify' only available since MongoDB 5.1
            {"$densify": density},

            # fill missing data with zeroes
            {"$fill": filling},

            # sort by ascending data
            {"$sort": {"_id": 1}}
        ])
        # print(list(result))
        _out: tuple[str, str] = ("dataset", "labels")
        _out_values: list[tuple[Any, str]] = [(record["dataset"],
                                               processing.DateTimeConverter.dt_to_str(
                                                   record["_id"]["date"], group_type)
                                               )
                                              for record in result]
        to_return: dict = dict(zip(_out,
                                   list(zip(*_out_values))
                                   )
                               )

        return to_return
