import os
import sys
import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
from pathlib import Path


def find_date(day_string, language):
    list_day_string = list(day_string)
    if language == 'EN':
        day_month = list_day_string[6:]
    else:
        day_month = list_day_string[5:]
    day_month = ''.join(day_month)
    year = time.strftime('%Y')
    date = day_month + year
    return date


def find_day(day_string):
    week = {'Mon.': 'Monday', 'Tue.': 'Tuesday', 'Wed.' : 'Wednesday',
            'Thu.' : 'Thursday', 'Fri.' : 'Friday',
            'Mo. ' : 'Montag', 'Di. ' : 'Dienstag', 'Mi. ' : 'Mittwoch',
            'Do. ' : 'Donnerstag', 'Fr. ' : 'Freitag'}
    list_day_string = list(day_string)
    day_of_the_week = list_day_string[1:5]
    day_of_the_week = ''.join(day_of_the_week)
    if day_of_the_week in week:
        day_of_the_week = week[day_of_the_week]
    return day_of_the_week


def new_filepath():
    newpath = 'retrieved_data/'
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    return newpath


def check_df_dates(date, df_to_check):
    if any(df_to_check['date'].str.contains(date)):
        print(date + " already in retrieved data. Script stops.")
        sys.exit()


def write_to_file(date, language, data_to_write, filename):
    filepath = new_filepath()
    check_filename = Path('retrieved_data/' + filename)
    if check_filename.is_file():
        df_to_check = pd.read_csv(filepath + filename, sep=';', header=0)
        check_df_dates(date, df_to_check)
        with open(filepath + filename, 'a') as f:
            data_to_write.to_csv(f, sep=';', encoding='utf-8', header=None,
                                 index=False)
    else:
        data_to_write.to_csv(filepath + filename, sep=';', encoding='utf-8',
                             index=False)


def scraper(url_list, language):
    global counter
    global df_columns

    # Data frame for menu data. Will be appended for every url.
    df_menu_database = pd.DataFrame(columns = df_columns)

    for key, value in url_list.items():
        place = key
        url = value

        # progress indicator
        counter += 1
        print('Scraping {} ({}),'\
              ' which is url #{} out of {}'.format(place,
                                                  language,
                                                  str(counter),
                                                  str(len(url_list_EN) +
                                                  len(url_list_DE))))

        # Request url and get its text.
        html_source = requests.get(url)
        data = html_source.text

        # Setting up the soup.
        soup = BeautifulSoup(data, 'html.parser')

        # Data frame to store the menu.
        df_menu = pd.DataFrame(columns = df_columns)

        # Find the current date and day.
        # Transform it to format: DD.MM.YYYY
        # and day to full day of the week.
        if language == 'EN':
            try:
                date = find_date(soup.find("a", class_="today").span.text,
                                 language)
                day = find_day(soup.find("a", class_="today").span.text)
            except:
                print('')
                print('failed to scrape: ' + place + ' (' + language + ')')

        if language == 'DE':
            try:
                date = find_date(soup.find('a', class_='heute').span.text,
                                 language)
                day = find_day(soup.find('a', class_='heute').span.text)
            except:
                print('')
                print('failed to scrape: ' + place + ' (' + language + ')')

        # Parsing for today's menu
        divTag = soup.find_all('div', class_= 'contents_aktiv')
        for tag in divTag:
            divTags = tag.find_all('div', {'class' : 'category'})
            i = 0
            for tag in divTags:
                df_menu.loc[i, ['cafeteria']] = place
                df_menu.loc[i, ['date']] = date
                df_menu.loc[i, ['day_of_the_week']] = day
                df_menu.loc[i, ['menu']] = tag.text
                df_menu.loc[i, ['menu_name']] = tag.find_next('div', {'class' : 'title'}).text
                find_category = tag.find_next('div', {'class': 'title_preise_2'}).contents[1:]
                category = []
                for j in range(len(find_category)):
                    category_string = str(find_category[j])
                    category_string = list(category_string)
                    category_string = category_string[33:-8]
                    category_string = ''.join(category_string)
                    if category_string != '':
                        category.append(category_string)
                try:
                    df_menu.loc[i, ['category_1']] = str(category[0])
                    df_menu.loc[i, ['category_2']] = str(category[1])
                    df_menu.loc[i, ['category_3']] = str(category[2])
                    df_menu.loc[i, ['category_4']] = str(category[3])

                except:
                    None
                df_menu.loc[i, ['timestamp']] = timestr
                i += 1

        # Append data frame
        df_menu_database = df_menu_database.append(df_menu, ignore_index=True)

    # Write to .csv file
    filename = 'menu_' + language + '.csv'
    write_to_file(date, language, df_menu_database, filename)
    df_menu_database = df_menu_database.drop(df_menu_database.index,
                                             inplace=True)


url_list_EN = {'Uni_KN': 'https://www.seezeit.com/en/food/menus/giessberg-canteen/?no_cache=1',
                'HTWG_KN' : 'https://www.seezeit.com/en/food/menus/htwg-canteen/?no_cache=1',
                'Weingarten': 'https://www.seezeit.com/en/food/menus/weingarten-canteen/?no_cache=1',
                'Ravensburg' : 'https://www.seezeit.com/en/food/menus/ravensburg-canteen/?no_cache=1',
                'Friedrichshafen' : 'https://www.seezeit.com/en/food/menus/friedrichshafen-canteen/?no_cache=1'}

url_list_DE = {'Uni_KN': 'https://www.seezeit.com/essen/speiseplaene/mensa-giessberg/?no_cache=1',
               'HTWG_KN' : 'https://www.seezeit.com/essen/speiseplaene/mensa-htwg/?no_cache=1',
               'Weingarten': 'https://www.seezeit.com/essen/speiseplaene/mensa-weingarten/?no_cache=1',
               'Ravensburg' : 'https://www.seezeit.com/essen/speiseplaene/mensa-ravensburg/?no_cache=1',
               'Friedrichshafen' : 'https://www.seezeit.com/essen/speiseplaene/mensa-friedrichshafen/?no_cache=1'}

counter = 0

# Data frame columns
df_columns = ['cafeteria',
              'date',
              'day_of_the_week',
              'menu',
              'menu_name',
              'category_1',
              'category_2',
              'category_3',
              'category_4',
              'timestamp']

# Time stamp for .csv file.
timestr = time.strftime('%Y%m%d-%H%M%S')

# Scrape url lists
scraper(url_list_EN, 'EN')
scraper(url_list_DE, 'DE')

# Print done when done.
print('')
print('done')
