#!/usr/bin/python3

import urllib, re, time
import urllib.request as urllib2
from http.cookiejar import CookieJar

username = 'tgfuellner'
password = '*'

spieler_clickId = {
  'Josef Moser': 1033954,
  'Thomas Gfüllner': 1228839,
  'Hermann Zacherl': 1062619,
  'Thomas Alsters': 996036,
  'Herbert Kalb': 1025762,
  'Helmut Brandl': 999395,
  'Stefan Hofinger': 1022921,
  'Michael Schleinkofer': 1050265,
  'David Alsters': 996035,
  'Jakob Luberstetter': 1030734,
  'Stefan Brandlhuber': 999610,
  'Andreas Haas': 1352979,
  'Paul Rott': 1044464,
  'Guy Vince': 1061493,
  'Christina Schleinkofer': 1050263,
  'Stefan Frank': 1647366,
  'Thomas Döllel': 1002741,
  'Julian Rumpfinger': 1327215,
  'Matthias Gfüllner': 1351358,
  'Florian Gfüllner': 1327214,
  'Tanja Pointner': 1043409,
  'Peter Jeltsch': 1020762,
  'Alex Huppmann': 1585775,
  'Alexander Fritsch': 1010619,
  'Andreas Gfüllner': 1574650,
  'Marko': 1708207,
  'Eva Brandlhuber': 999607,
  'Kilian Lekse': 1691150,
  'Korbinian Beer': 1327213,
  'Johannes Gfüllner': 1588739,
  'Jakob Taubenthaler': 1691159,
}

cj = CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
login_data = urllib.parse.urlencode({'userNameB' : username, 'userPassWordB' : password})
opener.open('https://www.mytischtennis.de/community/login', login_data.encode(encoding='UTF-8'))
allUrl = 'https://www.mytischtennis.de/community/matches?timeInterval=all&matchType=all&statisticType=all&clickttid={}'


reAll = re.compile(b'Alle Spiele \((\d+)\)')
reSiege = re.compile(b'Siege \((\d+)\)')
reNiederlagen = re.compile(b'Niederlagen \((\d+)\)')

def extract(url):
  resp = opener.open(url)
  html = resp.read()
  matchAll = reAll.search(html)
  matchSiege = reSiege.search(html)
  matchNiederlagen = reNiederlagen.search(html)

  return (matchAll, matchSiege, matchNiederlagen)


def getNumberOfPlayedGames(clickId):
  url = allUrl.format(clickId)
  matchAll, siege, niederlagen = extract(url)

  if not matchAll:
    time.sleep(5)
    matchAll, siege, niederlagen = extract(url)
    
  return (int(matchAll.group(1)), int(siege.group(1)), int(niederlagen.group(1)))



print('Sieg Verhältnis, Gesamt, Siege, Niederlagen, Name')
for name, id in spieler_clickId.items():
  alle, siege, niederlagen = getNumberOfPlayedGames(id)
  print('{siegVerlust:.2f},{alle},{siege},{niederlagen},{name}'.format(
        name=name, alle=alle, siege=siege,
        siegVerlust=siege/niederlagen, niederlagen=niederlagen))
