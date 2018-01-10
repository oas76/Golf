#!/usr/local/bin/python2

import random as ran
import numpy as np
import functools as func
import itertools as itertools
import Config as C

def _cleanTeamCobinations(list):
    res = []
    for tc in list:
        if _isUniqueTupple(tc):
            res.append(tc)
    return res

def _isUniqueTupple(tupple):
    a = tupple[0][0]
    b = tupple[0][1]
    return a not in tupple[1] and b not in tupple[1]

def _randomTeamCombination(iterable,nrPlayers,size):
    final = ()

    while len(final) < int(nrPlayers/2)*2:
        try:
            pool = tuple(iterable)
            n = len(pool)
            indices = sorted(ran.sample(xrange(n), nrPlayers/size))
            final = func.reduce(lambda x, y: set(x) | set(y), tuple(pool[i] for i in indices))
        except ValueError:
            print 'e'
            pass

    return tuple(pool[i] for i in indices)

def _setOfPossibleTeams(listOfTeams,size):
    i = 0
    round_setup = []
    print listOfTeams

    while i < 1000:
        res = _randomTeamCombination(listOfTeams,len(C.players),size)
        round_setup.append(res)
        i = i+1

    return set(round_setup)

def _getRandomRounds(setOfRounds, nrOfRounds):
    return ran.sample(setOfRounds,nrOfRounds)

def _getHandicapForPlayers(players):
    hc = []
    for p in players:
        hc += map(lambda x : x['hc'], filter(lambda x: x['Name'] == p, C.players))
    return _calcTeamHc(hc)

def _calcTeamHc(hclist):
    newlist = sorted(hclist)
    if len(newlist) == 1:
        return hclist[0]
    elif len(newlist) == 2:
        return round(func.reduce(lambda x,y : x+ y[0]*y[1], zip(newlist,[0.35,0.15]),0 ),1)
    elif len(newlist) == 3:
        return round(func.reduce(lambda x, y: x + y[0] * y[1], zip(newlist, [0.25, 0.15, 0.10]), 0), 1)
    elif len(newlist) > 3:
        return round(func.reduce(lambda x, y: x + y[0] * y[1], zip(newlist, [0.15, 0.10, 0.07, 0.05]), 0), 1)
    else:
        None

################################################################################


def createPairing(size=C.teamsize):

    # Define player details, Name and handicap
    player_list  = C.players

    # Get player names only
    player_names = [ entry['Name'] for entry in player_list ]

    # Randomiz order of playrs
    random_player_list = np.random.permutation(player_names)

    # Find possible teams, and represent it in a number
    teams_list = itertools.combinations(random_player_list,size)
    t_list = list(teams_list)

    # Find set of random team combination
    possible_pairings = _setOfPossibleTeams(t_list,size)

    tournament = _getRandomRounds(possible_pairings,1)
    res = []

    for t_round in tournament:
        i = 1

        for players in t_round:
            entry = {}
            #print 'Handicap Team %d : %.1f' % (i,_getHandicapForPlayers(players))
            entry['players'] = players
            entry['hc'] =  round(_getHandicapForPlayers(players),1)
            i = i+1
            res.append(entry)

    return res

if __name__ == "__main__":
    createPairing()
