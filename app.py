import quandl

import datetime

quandl.ApiConfig.api_key = "oSysYNKB7dqj4asAuDQy"

from flask import Flask, request
app = Flask(__name__)

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

    now = datetime.datetime.now()
    now_string = now.strftime('%Y-%m-%d')
    five_y_ago = now - datetime.timedelta(days=365*5)
    five_y_ago_string = five_y_ago.strftime('%Y-%m-%d')

    try:
        ret_data = str(quandl.get('ZILLOW/Z{}_{}'.format(zip_code, indicator), start_date=five_y_ago_string, end_date=now_string))
    except:
        ret_data = "Could not get data for input parameters"

    return ret_data

if __name__ == '__main__':
    app.run()
