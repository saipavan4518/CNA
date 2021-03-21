import os
import datetime
from zipfile import ZipFile
import pymongo
import re
import json


def insertBasicInfo(jsonData):
    dbName = "CNA_Visualizer"
    dbClient = pymongo.MongoClient('localhost', 27017)
    db = dbClient[dbName]
    collection = db['upload_information']
    ins = collection.insert_one(jsonData)
    del jsonData["_id"]
    dbClient.close()


def gettime(format):
    if (format == "timestamp"):
        return (str(datetime.datetime.timestamp(datetime.datetime.now())).split(".")[0])
    elif (format == "date"):
        return (datetime.datetime.now())


def mainfunction(fname):
    startTime = gettime("date")
    print("Script Initiating at : ", str(datetime.datetime.now()).split(".")[0])
    infoJson = []
    with open(fname, "r") as f:
        infoJson = json.loads(f.read())

    filename = infoJson[""]
