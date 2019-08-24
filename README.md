# Seezeit menu scraper

### Introduction

Seezeit is a student union that runs five cafeterias in the Lake of
Constance Region. It offers various dishes at each cafeteria and publishes its
menus on its website in a format that covers 14 days, beginning with a Monday
and the menu is changed after 14 days. The purpose if this script is to scrape
the menus of the current day and to export it to a .csv file.

### How it works

Simply run the script `seezeit_scraper.py`. It will create two files
in a folder named `retrieved_data` that will be created, if it does
not already exists. There is one .csv file for each language the menus
are available in on the website. The files are appended, if the menu for
the current day is not already stored.

The script gets the data for the current date only. So a cron job
or a daily routine are advised to be used.

> **troubleshooting** Current date is defined by the active "today" tab
on the website. If it was not set up correctly, which could happen
during the lecture free period or more precisely at the changing dates
from lecture free period to lecture period, it will use whatever data is in the
active tab.

### Useful information

Mensa Friedrichshafen is supplied by ZF Friedrichshafen canteen. Beside the main
canteens some of the sites also have cafés run by Seezeit.

#### Filenames

Menu in English: `retrieved_data/menu_EN.csv`

Menu in German: `retrieved_data/menu_DE.csv`

#### Retrieved data file format

| Header | Description
| --- | ---
| cafeteria |  Uni_KN: Konstanz University<br>HTWG_KN: Konstanz University of Applied Sciences<br>Weingarten: PH Weingarten<br>Ravensburg: DHBW Ravensburg<br>Friedrichshafen: Mensa Friedrichshafen<br>
| date | Date in DD.MM.YYYY format.
| day_of_the_week | Day of the week.
| menu | Name of the menu category.
| menu_name | Name of the dish.
| category_1 to category_4 | Veg: Vegetarian<br>Vegan: Vegan<br>Sch: Pork<br>R: Beef/Veal<br>Po: Poultry<br>L: Lamb<br>W: Game<br>F: Fish<br>B: Better animal husbandry
| timestamp | YYYYMMDD-HHMMSS
