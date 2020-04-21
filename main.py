#!/usr/bin/python3

# WARNING: This code is very ugly. Handle with care

# SECOND WARNING: It worked on my computer (with Linux). On Windows it might
# require God's intervention

# to download html page
import requests
# to parse html
from bs4 import BeautifulSoup
# to save date to csv easily
import numpy as np

url = "https://onemocneni-aktualne.mzcr.cz/covid-19"
# deaths by day filename
dbd_filename = "dbd.csv"
# deaths by age filename
dba_filename = "dba.csv"

# open url as html
html_content = requests.get(url, allow_redirects=True).text

# parse html content with BeutifulSoup
soup = BeautifulSoup(html_content, features="lxml")

# DEATHS BY DAY
# this table probably sucks data from some remote source. But for reasons, they are
# all hidden in an invisible <div></div> nearby:
# <div id="js-total-died-table-data" ... data-table="HERE"></div>
# We find this element by its ID and exploit the fact that the actual data are
# in a somewhat JSON-y format and convert it directly to a Python dictionary
# see eval(...) few lines later

# if this stops working, it should be easy to fix by some semi-random fiddling

div_id = "js-total-died-table-data"
data_attr_name = "data-table"

# find div with the correct id
results = soup.findAll("div", { "id" : div_id })
# extract data from attribute 'data_attr_name;
data_table = results[0][data_attr_name]
# it is a dictionary, so we evaluate it as one (i.e. convert from string to dict)
data_dict = eval(data_table)

# there is some surrounding mess but the raw data is under the key "body"
data = np.array(data_dict["body"])
np.savetxt(dbd_filename, data, delimiter=', ', fmt="%s")


# DEATHS BY AGE
# this is rather unfortunate. In contrast to other tables, this one does not
# posses a unique ID. Currently is is the 6th table on the webpage (althought
# most of them are not directly visible), but it might (and probably will) change.
# If it does change, the program will crash horribly. You may try changing
# the deaths_by_age_table_index below until it starts working again. The index
# denotes the position of the table on the webpage minus one.
deaths_by_age_table_index = 5

# if the structure of the table changes, the following lines might stop working.
table = soup.findAll('table')[deaths_by_age_table_index]
rows = []
for row in table.findAll('tr'):
    cols = [] 
    for col in row.findAll('td'):
        cols.append(col.text.strip())
    rows.append(cols)

rows = rows[1:-1]
for row in rows:
    row[1] = row[1].splitlines()[0]

np.savetxt(dba_filename, rows, delimiter=', ', fmt="%s")
