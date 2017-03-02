import urllib
from bs4 import BeautifulSoup as bs
import csv
import re
import numpy as np
from datetime import datetime
from textbox import encase, encase_fancy

## [0] Settings
siteurl = 'http://www.pokerwa.com/fortunepoker/index.php'
# print output? 
verbose = True
# write wait list information?
writewaitlist = False

# record access date/time
access_date = datetime.now().strftime('%Y-%m-%d')
access_time = datetime.now().strftime('%H:%M:%S')

# draw live Muckleshoot cash game information from url
# (default is pokeratlas: Muckleshoot casino)
page = urllib.urlopen(siteurl)
soup = bs(page, "html.parser")

if verbose: # if verbose, print access site + date + time.
    encase_fancy(["Drawing information from site:", siteurl,
                  "on " + access_date + " at " + access_time], sym="$")
    print "\n"*2

## [3] Gather live cash game activity

# information on current games
timestamp = soup.select('span[class="timestamp"]')[0].text
livegames = soup.select('img[class="PokerTable"]')

foo = {}
for tag in livegames:
    reg_lg = re.search('images\/icons\/FP\_(\w+\_\w+).+', tag['src'])
    if reg_lg:
        gamestr = reg_lg.group(1)
        if foo.get(gamestr):
            foo[gamestr] = {}
            foo[gamestr] += 1
        else:
            foo[gamestr] = 1
        # end else
    # end if reg_lg
# end for(livegames)

if verbose:
    for gamestr in foo.keys():
        print "game: "+gamestr+" has " + str(foo[gamestr]) + " tables"
    # end for(foo.keys())
# end if verbose


waitlists = soup.select('img[class="PokerList"]')
    



count = 0
for tag in livegames:
    for child in tag.descendants:
        count += 1
        encase_fancy(["TAG NUMBER:"+str(count), "has value:"])
        child.string
        


count = 0
for tag in going:
    count += 1 
    print count
    tag.attrs
    for child in tag.children:
        print child

# TODO: CHANGE FORMATTING!
#       READ https://docs.scipy.org/doc/numpy/reference/arrays.dtypes.html
game_info = np.empty([3,len(going)], dtype="object") # empty numpy array
for i in range(3): # 0 = game type, 1 = going, 2 = waiting
    game_info[i] = [tr.findAll('td')[i].text for tr in going]
    live_games = game_info.T

def get_live_game_info_fortune(soup):
    # information on current games
    going = soup.select('tr[class="live-cash-game aside-activity-item"]')
    # TODO: CHANGE FORMATTING!
    #       READ https://docs.scipy.org/doc/numpy/reference/arrays.dtypes.html
    game_info = np.empty([3,len(going)], dtype="object") # empty numpy array
    for i in range(3): # 0 = game type, 1 = going, 2 = waiting
        game_info[i] = [tr.findAll('td')[i].text for tr in going]
        live_games = game_info.T
    return live_games

live_games = get_live_game_info(soup)

if verbose:
    encase("Live game information:")
    print "\t".join(["Game type", "Tables", "Waiting"])
    print 30*"-"
    for tr in live_games:
        print "\t".join(tr)
    print "\n"*2

# [4] Process waitlist information
# get the waitlists
# returnplayers = True returns a dictionary 'player'
# player['name'] returns a tuple ('game-name', 'position on waitlist')
waitlists = soup.select('div[class="live-waitlist"]')
list_info = [wl.findAll('div', attrs={
            'class':["game-name","index","name"]}) for wl in waitlists]
# store waitlist in nested dictionary:
#   lobby['game-name']['index'] returns 'name'
lobby = {}
player = {}
for element in list_info:
    lobby[element[0].text] = {}
    for i in range(len(element))[1::2]:
        lobby[element[0].text][element[i].text] = element[i+1].text
        player[element[i+1].text] = (element[0].text, element[i].text)
        out = lobby
        if returnplayers:
            out = player


    # [4] process waitlist information
    lobby = get_waitlist_info(soup)

    # [5] get player information
    players = get_waitlist_info(soup, returnplayers=True)
    # TODO: add section to test if players are present!
    # ref: http://stackoverflow.com/questions/1602934/check-if-a-given-key-already-exists-in-a-dictionary
    # TODO: add feature to say last time seen on waitlist

    # traversing the waitlist
    if verbose:
        encase("Wait list information:")
        for k in lobby.keys():
            print "Game: " + k
            for x in range(1,len(lobby[k])):
                print str(x) + ". " + lobby[k][str(x)]
                print "\n"
if verbose:
    encase("Wait list information:")
    for k in lobby.keys():
        print "Game: " + k
        for x in range(1,len(lobby[k])):
            print str(x) + ". " + lobby[k][str(x)]
            print "\n"


import os, csv

if writewaitlist:
    with open("lobbying.csv", "w") as toWrite:
        writer = csv.writer(toWrite, delimiter=",")
        writer.writerow(["game", "order", "name"])
        for key in lobby.keys():
            for order in lobby[key].keys():
                writer.writerow([key.encode("utf-8"), order.encode("utf-8"), lobby[key][order]])
            # end for order
        # end for key
    # end with
# end if writewaitlist




          
              
