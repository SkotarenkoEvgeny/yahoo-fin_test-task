## Scraper for yahoo-finance site
The program can download data from web page or csv file, 
save his to the SQLite database and return data in json format

A program created on Flask rest framework. 
```sh
$ pipenv install
```
For your comfort, you can use apidocs (172.17.0.2:5000/apidocs/) or set two arguments in html request:
 - data_source => set 'csv' or 'page'
 - company => set name of company for searching in site ['PD', 'AAPL', 'ZUO', 'PINS', 'ZM', 'DOCU', 'CLDR', 'RUN'] for example
