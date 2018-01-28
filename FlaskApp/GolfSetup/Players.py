#!/usr/local/bin/python2

import json
import random
import pymongo
import os
import uuid
from pymongo import MongoClient
import traceback

MONGO_URL = os.environ.get('MONGODB_URI')
client = MongoClient(MONGO_URL)
db = client.heroku_d00134zn
collection = db.Players

def getPlayers():
    try:
        return list(collection.find())
    except Exception, err:
        traceback.print_exc()


def getPlayerByIndex(uuid):
    try:
        return collection.find_one({'uuid':uuid})
    except Exception,err:
        traceback.print_exc()

def deletePlayer(uuid):
    try:
        collection.delete_one({'uuid':uuid})
    except Exception,err:
        traceback.print_exc()

def addPlayer(name,hc):
    print 'WTF?'
    try:
        collection.insert_one({'uuid':uuid.uuid4().hex, 'Name': name, 'hc':hc})
    except Exception,err:
        traceback.print_exc()

def updatePlayer(uuid,name,hc):
    print 'WTF? WTF?'
    try:
        collection.update_one({'uuid':uuid},{
            "$set": {
                "Name":name,
                "hc":hc,
            }})
    except Exception,err:
        traceback.print_exc()
