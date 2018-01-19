#!/usr/local/bin/python2

import json
import random

def getPlayers(file):
    with open(file,'r') as jsonFile:
        return json.load(jsonFile)

def getPlayerByIndex(file,pid):
    with open(file,'r') as jsonFile:
        old_data = json.load(jsonFile)
        for p in old_data['Players']:
            if p['pid'] == pid:
                return p
    return None


def deletePlayer(file,pid):
    with open(file,'r') as jsonFile:
        old_data = json.load(jsonFile)
        new_data = {'Players':[]}
        for p in old_data['Players']:
            if p['pid'] != pid:
                new_data['Players'].append(p)

    with open(file,'w') as newfile:
        json.dump(new_data, newfile, indent=4, sort_keys=True, separators=(',', ':'))
    return new_data

def editPlayer(file,pid,name,hc):
    with open(file,'r') as jsonFile:
        old_data = json.load(jsonFile)
        new_data = {'Players':[]}
        for p in old_data['Players']:
            if p['pid'] == pid:
                new_data['Players'].append({'pid':pid,'Name':name,'hc':hc})
            else:
                new_data['Players'].append(p)

    with open(file,'w') as newfile:
        json.dump(new_data, newfile, indent=4, sort_keys=True, separators=(',', ':'))
    return new_data

def addPlayer(file,name,hc):
    with open(file, 'r') as jsonFile:
        old_data = json.load(jsonFile)
        while True:
            pid = random.sample(xrange(1,100),1)[0]
            if pid not in filter(lambda x : x['pid'], old_data['Players']):
                break
    new_data = old_data
    new_data['Players'].append({'pid':pid,'Name':name,'hc':hc})

    with open(file,'w') as newfile:
        json.dump(new_data, newfile, indent=4, sort_keys=True, separators=(',', ':'))
    return new_data
