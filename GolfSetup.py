#!/usr/local/bin/python2

import itertools as i
import random as ran
import numpy as np
import functools as func



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

def _doFormatCheck1(list):
    # for entries 1,3,5 and 8, ( Round 2, Round4, Round6 and Round9) there must be a new team with the "paused" participant
    # and neither of the teams can be the same as the round before.

    check_entries = [1,3,5,8]
    for c in check_entries:
        print('.')
        teams_prev = []
        teams_post = []
        players_prev = []
        players_post = []
        for teams in random_tournament[c-1]:
            teams_prev.append(teams)
            for player in teams:
                players_prev.append(player)

        for teams in random_tournament[c]:
            teams_post.append(teams)
            for player in teams:
                players_post.append(player)

        players_prev.sort()
        players_post.sort()

        found = (set(players_prev) != set(players_post))
        if not found:
            return False

        # Checking that none of the teams are the same
        for x in teams_post:
            for y in teams_prev:
                if np.array_equal(x,y):
                    return False

    return True

def _addSinglePlayer2Tournament(list):
    newTournament = []
    for round in list:
        players = []
        for team in round:
            for player in team:
                players.append(player)

        for player in player_names:
            if player not in players:
                new_round = {}
                new_round['Team1'] = round[0]
                new_round['Team2'] = round[1]
                new_round['Single'] = player
                newTournament.append(new_round)
                break


    return newTournament


def _doDistroCheck(tournament):

    firstDay = tournament[0:3+1]
    secondDay = tournament[4:6+1]
    thirdDay = tournament[7:9+1]
    firstHalf = tournament[0:4+1]

    if _doPairDistroCheck(firstDay) and _doPairDistroCheck(secondDay) and _doPairDistroCheck(thirdDay):
        return _isSingleSliceUnique(firstHalf) and _isSingleSliceUnique(secondDay) and _isSingleSliceUnique(thirdDay)
    else:
        return False

def _doPairDistroCheck(slice):
    nrofteams = 2*len(slice)
    team_list = []
    res = map(lambda x : [x['Team1'][0] + x['Team1'][1]] +  [x['Team2'][0] + x['Team2'][1]] ,slice)
    for round in res:
        for team in round:
            team_list.append(team)
    return len(set(team_list)) == nrofteams

def _isSingleSliceUnique(slice):
    nrofentries = len(slice)
    res = map(lambda x  : x['Single'],slice)
    return len(set(res)) == nrofentries

def _addTeamHandicap(tournament):
    for round in tournament:
        round['Team1HC'] = _getHandicapForPlayers(round['Team1'])
        round['Team2HC'] = _getHandicapForPlayers(round['Team2'])
        round['SingleHC'] = _getHandicapForPlayers([round['Single']])

def _getHandicapForPlayers(players):
    hc = []
    for p in players:
        hc += map(lambda x : x['hc'], filter(lambda x: x['Name'] == p, player_list))
    return _calcTeamHc(hc)

def _calcTeamHc(hclist):
    newlist = sorted(hclist)
    if len(newlist) == 1:
        return hclist[0]
    elif len(newlist) == 2:
        return round(func.reduce(lambda x,y : x+ y[0]*y[1], zip(newlist,[0.35,0.15]),0 ),1)
    elif len(newlist) == 3:
        return round(func.reduce(lambda x, y: x + y[0] * y[1], zip(newlist, [0.25, 0.15, 0.10]), 0), 1)
    else:
        None


def _doFlightSetup(tournament,tournament_flights):

    special_indexes = [0,2,4,7]
    random_indexes = [6,9]


    name_first_flight = None

    for i in special_indexes:
        single = tournament[i]['Single']
        if tournament[i]['Single'] in tournament[i+1]['Team1']:
            name_first_flight = filter(lambda x : x != single, tournament[i+1]['Team1'] )
            pass
        elif tournament[i]['Single'] in tournament[i+1]['Team2']:
            name_first_flight = filter(lambda x: x != single, tournament[i+1]['Team2'])
            pass

        if name_first_flight[0] in tournament[i]['Team1']:
            tournament_flights.append({'Round' : i+1,  'Flight': 1, 'Team': tournament[i]['Team1'], 'Single': single})
            tournament_flights.append({'Round' : i+1,  'Flight': 2, 'Team': tournament[i]['Team2'] } )
        else:
            tournament_flights.append({'Round' : i+1,  'Flight': 1, 'Team': tournament[i]['Team2'], 'Single': single})
            tournament_flights.append({'Round' : i+1,  'Flight': 2, 'Team': tournament[i]['Team1'] } )

        if single in tournament[i+1]['Team1']:
            tournament_flights.append({'Round' : i+2,  'Flight': 1, 'Team': tournament[i+1]['Team1'] })
            tournament_flights.append({'Round' : i+2,  'Flight': 2, 'Team': tournament[i+1]['Team2'],'Single': tournament[i+1]['Single'] } )
        else:
            tournament_flights.append({'Round' : i+2,  'Flight': 1, 'Team': tournament[i+1]['Team2'] } )
            tournament_flights.append({'Round' : i+2,  'Flight': 2, 'Team': tournament[i+1]['Team1'],'Single': tournament[i+1]['Single']}  )

    for i in random_indexes:
        tournament_flights.append({'Round': i+1, 'Flight': 1, 'Team': tournament[i]['Team1']})
        tournament_flights.append({'Round': i+1, 'Flight': 2, 'Team': tournament[i]['Team2'],'Single': tournament[i]['Single']})

    players_flat_none = map(lambda x:  [ x['Team'][0], x['Team'][1], x['Single'] if 'Single' in x.keys() else None ],tournament_flights)

    count_matrix = [[0 for x in range(len(player_names))] for y in range(len(player_names))]

    for rank,name in enumerate(player_names):
        for rank2,rname in enumerate(reversed(player_names)):
            for entry in players_flat_none:
                if name in entry and rname in entry:
                    count_matrix[rank][rank2] += 1


    nr_of_3s = 0
    for x in count_matrix:
        for y in x:
            if y < 3 or ( y > 6 and y != 10 ):
                return False
            if y == 3:
                nr_of_3s += 1

    if nr_of_3s > 6:
        return False

    for x in count_matrix:
        if x.count(3) > 2:
            return False

    return True

################################################################################

# Running the script


# Define player details, Name and handicap
player_list  = [{'Name':'Andy', 'hc': 20.2 },
                {'Name':'Jorgen', 'hc': 23.5},
                {'Name':'Poggen', 'hc': 10.4},
                {'Name':'Oddis', 'hc': 13.0},
                {'Name':'Smu', 'hc': 16.8 }]

# Get player names only
player_names = [ entry['Name'] for entry in player_list ]

# Randomiz order of playrs
random_player_list = np.random.permutation(player_names)

# Find possible teams, and represent it in a number
teams_list = i.combinations(random_player_list,2)

# Find all combinations of 2 teams
team_combinations = i.combinations(teams_list,2)

# Filter all combination to avoid duplicats of players in team combinations
clean_combinations = _cleanTeamCobinations(team_combinations)

# Find how many combinations to have 10 rounds with the teams
tournament_combinations = i.combinations(clean_combinations,10)

# check that each team is exactly present twice and return the set of valid tournaments
valid_tournaments = []

for c in tournament_combinations:
    team_count = {}
    for p in i.combinations(random_player_list,2):
        sum = 0
        for l in c:
            if p in l:
                sum += 1
        team_count[p] = sum

    if team_count.values().count(2) == 10:
        valid_tournaments.append(c)


# select a valid tournament set
rand = ran.randint(0,len(valid_tournaments)-1)
selected_tournament = valid_tournaments[1]

# do validation if setup is OK, given strckt Raymon Tour rules...

found = False
while not found:

    # fina  a random permutation of tournament...
    random_tournament = np.random.permutation(selected_tournament)

    found = _doFormatCheck1(random_tournament)

    if found:

        # when found a good candidate, add single player and check if distrubution is OK.

        tournament_with_single = _addSinglePlayer2Tournament(random_tournament)

        found = _doDistroCheck(tournament_with_single)

        if found:
            # Do flight setup, and make sure that everyone at least plays 4 flights togeter with each of the other persons in the group

            tournament_flights = []
            found = _doFlightSetup(tournament_with_single,tournament_flights)

print('[SUCSESS] Setup found and is printed to RoundSetup.txt. Enjoy')


with open('./RoundSetup.txt','wt') as list:
    list.write(' OFFICIAL TOURNAMENT SETUP PORTUGAL 2017 \n\n\n')

    for i in range(1,10+1):
        info_flight1 = filter(lambda x: x['Round'] == i and x['Flight'] == 1,tournament_flights)
        info_flight2 = filter(lambda x: x['Round'] == i and x['Flight'] == 2,tournament_flights)
        map_flight1 = map(lambda x: [ x['Team'], x['Single'] if 'Single' in x.keys() else None ],info_flight1)
        map_flight2 = map(lambda x: [ x['Team'], x['Single'] if 'Single' in x.keys() else None], info_flight2)


        list.write('ROUND %s \n\n' % i)

        list.write('Flight 1:  Team: %s and %s  hc: %s \n' % (map_flight1[0][0][0],map_flight1[0][0][1],_getHandicapForPlayers([map_flight1[0][0][0],map_flight1[0][0][1]])))
        if map_flight1[0][1] != None:
            list.write('Flight 1:  Single: %s  hc: %s \n\n' % (map_flight1[0][1],_getHandicapForPlayers([map_flight1[0][1]])) )
        else:
            list.write('\n')

        list.write('Flight 2:  Team: %s and %s  hc: %s \n' % (map_flight2[0][0][0],map_flight2[0][0][1],_getHandicapForPlayers([map_flight2[0][0][0],map_flight2[0][0][1]])))
        if map_flight2[0][1] != None:
            list.write('Flight 2:  Single: %s  hc: %s \n\n' % (map_flight2[0][1], _getHandicapForPlayers([map_flight2[0][1]])))
        else:
            list.write('\n')

        list.write('\n\n')



















