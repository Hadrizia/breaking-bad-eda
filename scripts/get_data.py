import requests
import pandas
import os
from bs4 import BeautifulSoup

DATA_HEADER = ['name', 'season', 'episode', 'rating', 'votes']
URL = 'https://www.imdb.com/title/tt0903747/episodes/?season='
page = requests.get("https://www.imdb.com/title/tt0903747/episodes/?season=1")
PATH = '../data/data.csv'
soup = BeautifulSoup(page.content, 'html.parser')


def get_text(soup_entity):
    '''This function gets a clean version of the text from a soup entity.'''
    return ' '.join([line.strip() for line in soup_entity.get_text().strip().splitlines()]).lower()

def exists(soup_entity):
    return soup_entity != -1 and soup_entity != None

def load_csv(path, columns):
  try:
    dataframe = pandas.read_csv(path)
  except:
    dataframe = pandas.DataFrame(columns=columns)
  return dataframe

def save_csv(dataframe, path):
    # create directory if doesn't exists
    directory = os.path.dirname(path)
    if not os.path.exists(directory):
        os.makedirs(directory)
    # save dataframe
    dataframe.to_csv(path, encoding='utf-8', index=False)

def get_dataframe(path, columns):
    return load_csv(path, columns)

def get_rows(soup, dataframe):
    list = soup.find('div', attrs={'class': 'list detail eplist'})

    for element in list.children:
        name, season, episode, rating, votes = '','','','',''
        img = element.find('img')
        if exists(img):
            name = element.find('img')['alt']
            div = img.find('div')
            if exists(div):
                season, episode = get_text(div).split(', ')
                season = season.replace('s', '')
                episode = episode.replace('ep','')

        info = element.find('svg')
        if exists(info):
            parent = info.parent
            if exists(parent):
                for v in parent.next_siblings:
                    if exists(v) and v.name == 'span':
                        if v['class'] == ['ipl-rating-star__rating']:
                            rating = get_text(v)
                        elif v['class'] == ['ipl-rating-star__total-votes']:
                            votes = int(get_text(v).replace('(','').replace(')', '').replace(',', ''))
        row = [name, season, episode, rating, votes]
        if row != ['','','','','']:
            dataframe.loc[len(dataframe)] = row

def get_season_rows(season, dataframe):
    page = requests.get(URL + str(season))
    soup = BeautifulSoup(page.content, 'html.parser')
    get_rows(soup, dataframe)

def generate_dataframe():
    dataframe = get_dataframe(PATH, DATA_HEADER)
    for i in range(1,6):
        print ("Getting data from season", i)
        get_season_rows(i, dataframe)
    return dataframe

def download_data(path):
    dataframe = generate_dataframe()
    save_csv(dataframe, path)

def main():
    download_data(PATH)

if __name__ == '__main__':
  main()
