import requests
from bs4 import BeautifulSoup


page = requests.get("http://www.imdb.com/title/tt0903747/episodes?season=1")
soup = BeautifulSoup(page.content, 'html.parser')

def get_text(soup_entity):
    '''This function gets a clean version of the text from a soup entity.'''
    return ' '.join([line.strip() for line in soup_entity.get_text().strip().splitlines()]).lower()

list = soup.find('div', attrs={'class': 'list detail eplist'})

for element in list.children:
    # if img['alt'] != 'loading':
  

    img = element.find('img')
    print (img)
    # if img['alt'] != 'loading':
    #     for children in img.children:
    #          if children.name == 'div':
    #             season, episode = children.text.split(', ')
    #             print (season)
    #             print (episode)
        


    