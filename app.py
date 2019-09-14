import quandl
import pandas as pd
import numpy as np
import datetime
from matplotlib import pyplot
import mpld3
from flask import Flask, request

quandl.ApiConfig.api_key = "oSysYNKB7dqj4asAuDQy"
indicator_to_code = pd.read_csv("indicators_table.csv")


app = Flask(__name__)


def get_indicator_code(input_data_type):
    return indicator_to_code['Code'][list(np.where((indicator_to_code['Indicator']==input_data_type)==True))[0][0]]

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
    return mpld3.fig_to_html(fig, template_type="simple")




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
    code = get_indicator_code(indicator)
    from_date = request.args.get('start_date')
    to_date = request.args.get('end_date')
    # from_date_string = from_date.strftime('%Y-%m-%d')
    # to_date_string = to_date.strftime('%Y-%m-%d')
    return plot_time_series(get_quandl_data(zip_code, code, from_date, to_date), indicator, zip_code)

    # return str(quandl.get('ZILLOW/Z{}_{}'.format(zip_code, indicator), start_date=now_string, end_date=now_string))

if __name__ == '__main__':
    app.run()
