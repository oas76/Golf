#!/usr/local/bin/python2

import json
from GolfSetup import Players

print json.dumps(Players.getPlayers('../../data/TestData.json'))
print json.dumps(Players.deletePlayer('../../data/TestData.json',1))
print json.dumps(Players.editPlayer('../../data/TestData.json',2,"Stig",15.0))
print json.dumps(Players.addPlayer('../../data/TestData.json',"Stig",16.0))


