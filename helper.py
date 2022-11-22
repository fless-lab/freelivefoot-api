from urllib.parse import urlparse
from bs4 import BeautifulSoup
import cfscrape


def fetchData():
    cf = cfscrape.create_scraper()
    req = cf.get("http://www.rojadirecta.me/en")

    bs = BeautifulSoup(req.content, 'lxml')
    list_ = bs.select("div#masterdiv  span.list > span")

    matchs = [ getMatchs(elt) for elt in list_]
    return matchs


def getMatchs(node):
    match_node = node.select("div.menutitle")
    match_link_node = node.select("span.submenu tr")
    match_infos_list = [text for text in match_node[0].stripped_strings]

    match = {
        "time": match_infos_list[0],
        "type": match_infos_list[2],
        "competition": match_infos_list[3],
        "vs": match_infos_list[4],
        "links":  extractLinks(match_link_node)
    }
    return match


def extractLinks(links_node=[]):
    links = []
    for i, el in enumerate(links_node):
        if i != 0:
            links.append( extractLink(el))
    return links


def extractLink(link_node):
    tds = link_node.select('td')
    link = {
        'P2P': tds[0].get_text(),
        'Name': tds[1].get_text(),
        'Lang': tds[2].get_text(),
        'Type': tds[3].get_text(),
        'Kbps': tds[4].get_text(),
        'Play': tds[5].select('a')[0].attrs["href"]
        #getIframeLink()
    }
    return link

def isValidUrl(string):
    try:
        result = urlparse(string)
        return all([result.scheme, result.netloc])
    except:
        return False

def getIframeLink(link):
    cf = cfscrape.create_scraper()
    iframe_src = ''
    try:
        req = cf.get(link)
        if req.status_code < 400:
            bs = BeautifulSoup(req.content, 'lxml')
            iframe = bs.select('iframe')
            if len(iframe) > 0:
                iframe_src = iframe[0].attrs["src"]
    except Exception as e:
        print("error")
        pass
    print(iframe_src)
    return iframe_src

def getOnlyFoot(matches):
   return [elt for elt in matches if elt["type"]=="Football"]

def getOnlyWorldCupMatches(matches):
    return [match for match in matches if "World Cup" in match["competition"]]

def filterByLanguage(matches,lang):
    for match in matches:
        match["links"]=[link for link in match["links"] if link["Lang"]==lang]
    return matches