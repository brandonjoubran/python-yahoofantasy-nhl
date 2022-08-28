from types import resolve_bases
import requests
from yahoo_oauth import OAuth2
import unicodedata
from datetime import datetime, date, timedelta

class Vertex(object):
    def __init__(self, 
    name = "", 
    gp = 0, 
    fp = 0, 
    perGameFp = 0, 
    fpLastFiveGP = 0, 
    perGameFpLastFiveGP = 0, 
    fpLastTenGP = 0, 
    perGameFpLastTenGP = 0,
    avgToi = "00:00", 
    avgToiLastFiveGP = "00:00", 
    avgToiLastTenGP = "00:00",
    avgPpTime = "00:00", 
    avgPpTimeLastFiveGP = "00:00", 
    avgPpTimeLastTenGP = "00:00"):

        self.name = name
        self.gp = gp
        self.fp = fp
        self.perGameFp = perGameFp
        self.fpLastFiveGP = fpLastFiveGP
        self.perGameFpLastFiveGP = perGameFpLastFiveGP
        self.fpLastTenGP = fpLastTenGP
        self.perGameFpLastTenGP = perGameFpLastTenGP
        self.avgToi = avgToi
        self.avgToiLastFiveGP = avgToiLastFiveGP
        self.avgToiLastTenGP = avgToiLastTenGP
        self.avgPpTime = avgPpTime
        self.avgPpTimeLastFiveGP = avgPpTimeLastFiveGP
        self.avgPpTimeLastTenGP = avgPpTimeLastTenGP
        self.left = None
        self.right = None

    
    def __str__(self):
        return 'Player name: %s\n'\
        '   Games Played: %d\n'\
        '   Total Fantasy Points: %d\n'\
        '   Total Fantasy Points/game: %s\n'\
        '   Fantasy Points in Last 5 GP: %s\n'\
        '   Fantasy Points/game in Last 5 GP: %s\n'\
        '   Fantasy Points in Last 10 GP: %s\n'\
        '   Fantasy Points/game in Last 10 GP: %s\n'\
        '   Average TOI: %s\n'\
        '   Average TOI in Last 5 GP: %s\n'\
        '   Average TOI in Last 10 GP: %s\n'\
        '   Average Powerplay Time: %s\n'\
        '   Average Powerplay Time in Last 5 GP: %s\n'\
        '   Average Powerplay Time in Last 10 GP: %s\n'\
        % (self.name,  
        self.gp, 
        self.fp, 
        format(self.perGameFp), 
        format(self.fpLastFiveGP),  
        format(self.perGameFpLastFiveGP), 
        format(self.fpLastTenGP), 
        format(self.perGameFpLastTenGP),
        self.avgToi,
        self.avgToiLastFiveGP,
        self.avgToiLastTenGP,
        self.avgPpTime, 
        self.avgPpTimeLastFiveGP, 
        self.avgPpTimeLastTenGP)

def insert(root, v):
    pass

def findMax(root):
    pass

def format(num):
    """Formatting floats to 2 decimals

    Keyword arguments:
    num -- number to format
    """
    return "{:.2f}".format(num)

def make_request(endpoint):
    response = requests.get(endpoint)
    resJson = response.json()
    return resJson

def get_seconds(time):
    """Convert a timestamp into seconds

    Keyword arguments:
    time -- timestamp to convert to seconds
    """

    mm, ss = time.split(':')
    return int(mm) * 60 + int(ss)

def get_time_hh_mm_ss(s):
    """Convert seconds into a mm:ss timestamp (hours not needed)

    Keyword arguments:
    s -- seconds to convert to timestamp
    """

    to_hhmmss = str(timedelta(seconds=s))
    to_mmss = to_hhmmss.split(':')
    return to_mmss[1] + ':' + to_mmss[2]

def normalize_text(text):
    """Removing accents from player and team names

    Keyword arguments:
    text -- string to remove accent from
    """
    text = unicodedata.normalize('NFKD', text)
    return "".join([c for c in text if not unicodedata.combining(c)])

def get_next_sunday():
    """Getting the date of the end of the current fantasy week i.e. next Sunday
    """
    d = date.today()
    if(d.weekday() == 6):
        d += timedelta(1)
    
    while(d.weekday() != 6):
        d += timedelta(1)
    return d

def is_goalie(playerInfo):
    isG = False
    for info in range(len(playerInfo)):
        #print(info)
        if(isinstance(playerInfo[info], list) == False):
            #print(list(playerInfo[info].keys()))
            if(list(playerInfo[info].keys())[0] == 'position_type'):
                if(playerInfo[info]['position_type'] != 'P'):
                    isG = True
    return isG

# Stat modifiers for the fantasy league
stat_mod_key = {
    "goals": 3,
    "assists": 1.5,
    "plusMinus": 0.5,
    "powerPlayPoints": 1, 
    "shots": 0.3, 
    "hits": 0.5, 
    "blocked": 0.5 
    #"wins": 2, 
    #"goalsAgainst": -1, 
    #"saves": 0.25, 
    #"shutouts": 2
}

playerList = []

def get_num_games_left(teamId):
    """Calculating how many games a team plays in the fantasy week. Deducts
    postponed games.

    Keyword arguments:
    teamId -- the team ID of the team that the player is on, used to see the team's roster where the link is 
    stored.
    """
    scheduleEndPoint = 'https://statsapi.web.nhl.com/api/v1/schedule'
    teamScheduleUrl = scheduleEndPoint + '?teamId=' + teamId + '&startDate=' + str(date.today()) + '&endDate=' + str(get_next_sunday())
    resJson = make_request(teamScheduleUrl)
    #print(resJson)
    dates = resJson["dates"]
    numGames = len(dates)

    for gameday in dates:
        #print(gameday['games'])
        print(gameday['games'][0]['status']['detailedState'])
        print()
        isPlayed = gameday['games'][0]['status']['detailedState']
        if(isPlayed == 'Postponed'):
            numGames -= 1
    print(numGames)
    return numGames

def get_team_id(teamName):
    """Retrieving the team ID of the team that the requested player is on.

    Keyword arguments:
    teamName -- the name of the team that the player is on
    """

    teamsEndPoint = 'https://statsapi.web.nhl.com/api/v1/teams'
    print(teamName)
    #response = requests.get(teamsEndPoint)
    #resJson = response.json()
    resJson = make_request(teamsEndPoint)
    id = None
    for team in resJson['teams']:
        if normalize_text(team['name']) == teamName:
            id = team['id']
    return id

def get_player_link(teamId, playerName):
    """Retrieving the link of a player that stores his stats (including the playerId).

    Keyword arguments:
    teamId -- the team ID of the team that the player is on, used to see the team's roster where the link is 
    stored.
    playerName -- the name of the player that is being searched for 
    """

    rosterEndPoint = 'https://statsapi.web.nhl.com/api/v1/teams/' + str(teamId) + '/roster/fullRoster'
    #response = requests.get(rosterEndPoint)
    #resJson = response.json()
    resJson = make_request(rosterEndPoint)

    for player in resJson['roster']:
        if(normalize_text(player['person']['fullName']) == playerName):
            return player['person']['link']

def get_player_stats(playerLink, playerName):
    """Retrieving various stats not provided by Yahoo Fantasy from NHL APIs of a given player.

    Keyword arguments:
    playerLink -- a portion of a url that includes the players ID that stores a JSON representation of his 
    stats
    playerName -- the name of the player that is being searched for 
    """

    gameLogEndPoint = "https://statsapi.web.nhl.com/" + playerLink + "/stats?stats=gameLog&season=20212022"
    
    #response = requests.get(gameLogEndPoint)
    #resJson = response.json()
    resJson = make_request(gameLogEndPoint)
    perGameStats = resJson['stats'][0]['splits']
    gamesPlayed = len(perGameStats)

    goals = 0
    assists = 0
    plusMinus = 0
    blocked = 0
    shots = 0
    hits = 0
    powerPlayPoints = 0
    powerPlaySeconds = 0
    toiSeconds = 0

    fp = 0
    v = Vertex()
    v.name = playerName
    v.gp = gamesPlayed

    if(gamesPlayed == 0):
        return v

    for i in range(gamesPlayed):
        #print(perGameStats[i]['stat'])
        #print()
        for key in list(stat_mod_key.keys()):
            fp += perGameStats[i]['stat'][key] * stat_mod_key[key]

        powerPlaySeconds += get_seconds(perGameStats[i]['stat']['powerPlayTimeOnIce'])
        toiSeconds += get_seconds(perGameStats[i]['stat']['timeOnIce'])

        if i == 4: # Last 5 games
            v.fpLastFiveGP = fp
            v.perGameFpLastFiveGP = fp/5
            v.avgPpTimeLastFiveGP = get_time_hh_mm_ss(int(powerPlaySeconds/5))
            v.avgToiLastFiveGP = get_time_hh_mm_ss(int(toiSeconds/5))

        if i == 9: # Last 10 games
            v.fpLastTenGP = fp
            v.perGameFpLastTenGP = fp/10
            v.avgPpTimeLastTenGP = get_time_hh_mm_ss(int(powerPlaySeconds/10))
            v.avgToiLastTenGP = get_time_hh_mm_ss(int(toiSeconds/10))

    v.fp = fp
    v.perGameFp = fp / gamesPlayed
    v.avgPpTime = get_time_hh_mm_ss(int(powerPlaySeconds/gamesPlayed))
    v.avgToi = get_time_hh_mm_ss(int(toiSeconds/gamesPlayed))
    return v
    



def nhlApi(teamName, playerName, playerList):
    """Everything to do with NHL undocumented APIs. A Vertex object is retrieved and stored in the playerList
    data structure.

    Keyword arguments:
    teamName -- number of free agents to look for (Yahoo stipulates it must be a multiple of 25) 
    playerName -- the name of the player that is being searched for 
    playerList -- list (data structure) to store player objects that hold info of their stats
    """

    teamId = get_team_id(teamName)
    playerLink = get_player_link(teamId, playerName)
    v = get_player_stats(playerLink, playerName)
    playerList += [v]
    
def yahooSettingsApi():
    '''
        In progress (scratch): This function can get any league's stat mods, removes the need for a 
        stat_mod_key.
    '''
    oauth = OAuth2(None, None, from_file='/Users/brandonjoubran/Downloads/yahoofantasy/yahoo_api_creds.json') 
    url = 'https://fantasysports.yahooapis.com/fantasy/v2/league/nhl.l.76805/settings'
    response = oauth.session.get(url, params={'format': 'json'})
    raw_response = response.json()
    settingsInfo = raw_response['fantasy_content']['league'][1]['settings'][0]

    print(settingsInfo['stat_modifiers'])
    print()

    statsDict = settingsInfo['stat_categories']['stats']
    print(statsDict)
    print()
    for t in statsDict:
        print(t)
        print()

def yahooSearchPlayer():
    '''
        In progress (scratch): This function searches Yahoo for player stats (not preferable to NHL stats)
    '''
    oauth = OAuth2(None, None, from_file='/Users/brandonjoubran/Downloads/yahoofantasy/yahoo_api_creds.json') 
    url = 'https://fantasysports.yahooapis.com/fantasy/v2/league/nhl.l.76805/players;player_keys=nhl.p.7493/stats'
    response = oauth.session.get(url, params={'format': 'json'})
    raw_response = response.json()

def yahooApi(numFA, playerList):
    """Looping through the fantasy league's free agents, and getting stats from the NHL on each player using
    the players full name and team name.

    Keyword arguments:
    numFa -- number of free agents to look for (Yahoo stipulates it must be a multiple of 25) 
    playerList -- list (data structure) to store player objects that hold info of their stats
    """

    #AppID: CICcgvz2
    #Share code: xpyktx3
    oauth = OAuth2(None, None, from_file='/Users/brandonjoubran/Downloads/yahoofantasy/yahoo_api_creds.json') 
    isG = False
    for i in range(numFA):
        url = 'https://fantasysports.yahooapis.com/fantasy/v2/league/nhl.l.76805/players?status=A&pos=P&cut_type=33&stat1=S_S_2021&myteam=0&sort=AR&sdir=1&start=' + str(25 * i) + '&count=25'
        response = oauth.session.get(url, params={'format': 'json'})
        raw_response = response.json()
        players = raw_response['fantasy_content']['league'][1]['players']
        
        for player in range(24):
            playerInfo = players[str(player)]['player'][0]
            print("player " + str(player + 1 + (25 * i)) + ": " + str(playerInfo[2]['name']['full']))
            print(playerInfo)
            
            if(is_goalie(playerInfo)):
                continue
            
            print('here')
            
            playerName = normalize_text(playerInfo[2]['name']['full']) #removing accents from names
            for j in range(len(playerInfo)):
                #print(playerInfo[j])
                if list(playerInfo[j].keys())[0] == 'editorial_team_full_name':
                    #print("found it")
                    #print(playerInfo[j]['editorial_team_full_name'])
                    teamName = normalize_text(playerInfo[j]['editorial_team_full_name'])
                    break
            
            nhlApi(teamName, playerName, playerList)
            print()
            

if __name__ == '__main__':
    playerList = []
    #get_num_games_left("53")
    yahooApi(1, playerList)
    #yahooSearchPlayer()
    '''nhlApi('Pittsburgh Penguins', 'Bryan Rust', playerList)
    nhlApi('New Jersey Devils', 'Jack Hughes', playerList)
    nhlApi('Tampa Bay Lightning', 'Brayden Point', playerList)
    nhlApi('Toronto Maple Leafs', 'Nick Ritchie', playerList)
    nhlApi('Toronto Maple Leafs', 'Auston Matthews', playerList)
    nhlApi('Toronto Maple Leafs', 'Mitchell Marner', playerList)
    nhlApi('Edmonton Oilers', 'Connor McDavid', playerList)'''

    '''nhlApi('NJD', 'Jack Hughes', playerList)
    nhlApi('NYR', 'Barclay Goodrow', playerList)
    nhlApi('NSH', 'Eeli Tolvanen', playerList)
    nhlApi('WSH', 'Alex Ovechkin', playerList)
    nhlApi('EDM', 'Connor McDavid', playerList)'''
    print()
    for p in playerList:
        print(p)
        print()