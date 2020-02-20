import bs4 as bs
import urllib.request
import re

def game_setup():
    """begins the clicks-to-hitler game
    """
    article_setup = ''
    current_article = ''
    counter_setup = -1
    current_counter = 0
    foundHitler = False
    #list that keeps track of the article path
    pathTaken = []
    print ('Welcome to Clicks-to-Hitler')

    #setting up which article to start on
    while (article_setup != 'y' and article_setup != 'n'):
        article_setup = input('\nWould you like to start on a random article? (y/n)\n')
        if (article_setup == 'y'):
            current_article = 'https://en.wikipedia.org/wiki/Special:Random'
            current_article = get_random_article(current_article)
        else:
            current_article = 'https://en.wikipedia.org/wiki/' + input('\nEnter a wiki page name to start on. Ex: Atom, Sudoku\n')

    pathTaken.append(current_article[29:])

    #setting up max number of paths
    while (counter_setup < 1):
        try:
            counter_setup = int(input("\nWhat's the max number of paths you would like to have to reach Hitler?\n"))
        except:
            pass
    
    while (current_counter < counter_setup):
        print('\nThese articles are listed on this page...\n')
        url_list = get_article_URLs(current_article)
        #remove duplicates and sort article pages
        url_list = list(dict.fromkeys(url_list))
        url_list.sort()
        for url in url_list:
            print(url[5:])
        current_article = '/wiki/' + input('\nYour current click counter is at ' + str(current_counter) + ". Type in the next wiki page name you'd like to go to. Ex: Atom, Sudoku\n")

        #check if you've reached Hitler article
        if current_article == '/wiki/Adolf_Hitler' and current_article in url_list:
            current_counter+=1
            foundHitler = True
            pathTaken.append(current_article[5:])
            break
        else:
            #input another article that's from the list
            while (current_article not in url_list):
                current_article = '/wiki/' + input("\nYou entered an article name not on the page! (Are you trying to cheat?) \nType in the next wiki page name you'd like to go to.\n")
            current_counter+=1
            pathTaken.append(current_article[5:])
            current_article = 'https://en.wikipedia.org' + current_article
    
    if foundHitler:
        print("\nCongratulations! You were able to reach Hitler's wiki page in " + str(current_counter) + " steps!\n")
    else:
        print("\nUnfortunately, you weren't able to reach Hitler's wiki page.\n")
    
    print("The path that you took was:\n")
    for path in pathTaken:
        print(path)


def get_article_URLs(sourceURL):
    """returns a list of wiki article urls from a single wiki url

    Parameters
    ----------
    sourceURL : str
        the wiki url that you are extracting article links from
    """
    sourceURL = sourceURL.encode().decode()
    articleList = []
    soup = bs.BeautifulSoup(urllib.request.urlopen(sourceURL),'lxml')
    #remove any tables
    for table in soup.find_all("table"):
        table.extract()
    #remove any special wiki pages
    for citation in soup.find_all(href=re.compile("^/wiki/Wikipedia:|^/wiki/User:|^/wiki/File:|^/wiki/MediaWiki:|^/wiki/Template:|^/wiki/Help:|^/wiki/Category:|^/wiki/Portal:|^/wiki/Draft:|^/wiki/TimedText:|^/wiki/Module:|^/wiki/Special:")):
        citation.extract()
    a = soup.find('div', {'class':'mw-parser-output'}).find_all('a', href=re.compile("^/wiki/"))
    for link in a:
        articleList.append(link['href'])
    return (articleList)


def get_random_article(sourceURL):
    """returns a string url that was generated randomly

    Parameters
    ----------
    sourceURL : str
        the wiki url that is generated from random
    """
    sourceURL = sourceURL.encode().decode()
    soup = bs.BeautifulSoup(urllib.request.urlopen(sourceURL),'lxml')
    return (('https://en.wikipedia.org/wiki/' + (str(soup.title.string))[0:-12]).replace(' ', '_'))


if __name__ == "__main__":
    game_setup()
