import quandl
import pandas as pd
import numpy as np
import datetime
from matplotlib import pyplot
import mpld3
from flask import Flask, request
from bs4 import BeautifulSoup as BS
import requests
import re


quandl.ApiConfig.api_key = "oSysYNKB7dqj4asAuDQy"
indicator_to_code = pd.read_csv("indicators_table.csv")

app = Flask(__name__)

def get_indicator(input_data_type):
    return indicator_to_code['Indicator'][list(np.where((indicator_to_code['Code']==input_data_type)==True))[0][0]]

def get_quandl_data(input_zipcode, code, from_date, to_date):
    return quandl.get('ZILLOW/Z{}_{}'.format(input_zipcode, code), start_date=from_date, end_date=to_date)


def plot_time_series(series, input_data_type, input_zipcode):
    print(series)
    fig = pyplot.figure()
    pyplot.scatter(series.index, series, c="blue")
    pyplot.plot(series)
    pyplot.xlabel("Time", fontsize="x-large", weight="bold")
    pyplot.ylabel(input_data_type, fontsize="x-large", weight="bold")
    pyplot.title("{} for area {}".format(input_data_type, input_zipcode))

    html = mpld3.fig_to_html(fig, template_type="simple")
    print (html)
    return html

def get_school_link(zipcode):
    zipcode = "07871"
    state = 'NJ'
    text = requests.get('https://nces.ed.gov/ccd/districtsearch/district_list.asp?Search=1&details=1&InstName=&DistrictID=&Address=&City=&State=&Zip=' +  zipcode + '&Miles=&County=&PhoneAreaCode=&Phone=&DistrictType=1&DistrictType=2&DistrictType=3&DistrictType=4&DistrictType=5&DistrictType=6&DistrictType=7&DistrictType=8&NumOfStudents=&NumOfStudentsRange=more&NumOfSchools=&NumOfSchoolsRange=more')
    soup = BS(text.content, 'html5lib') 

    links = []
    for link in soup.findAll('a', attrs={'href': re.compile("district_detail")}):
        links.append('https://nces.ed.gov/ccd/districtsearch/' + link.get('href'))

    finallink = links[0]
    text2 = requests.get(finallink)

    soup2 = BS(text2.content, 'html5lib') 

    links2 = []
    for link in soup2.findAll('a', attrs={'href': re.compile("/Programs/Edge")}):
        links2.append('https://nces.ed.gov' + link.get('href'))
        
    return links2[0]

@app.route('/')
def home():
    indicators = {
        'MLPAH': 'Median Listing Price - All Homes',
        'MRPAH': 'Median Rental Price - All Homes',
        'MSPAH': 'Median Sold Price - All Homes',
        'ZHVIAH': 'Zillow Home Value Index - All Homes',
        'ZRIAH': 'Zillow Rental Index - All Homes'
    }
    html = '''
    <form action="/data">
    Zip Code: <input type="text" name="zip_code"><br>
    From date: <input type="date" name="start_date"><br>
    To date: <input type="date" name = "end_date"><br>
    Indicators:<br>
    '''

    html += '\n'.join(['<input type="radio" name="indicator" value=' + i + '>' + indicators[i] + '<br>' for i in indicators])

    html += '''
    <input type="submit" value="Submit">
    </form>
    '''
    return html

@app.route('/data')
def data():
    zip_code = request.args.get('zip_code')
    indicator = request.args.get('indicator')
    from_date = request.args.get('start_date')
    to_date = request.args.get('end_date')

    link = get_school_link(zip_code)

    return plot_time_series(get_quandl_data(zip_code, indicator, from_date, to_date), get_indicator(indicator), zip_code) + "<p>School: {}</p>".format(link)


if __name__ == '__main__':
    app.run()
