import quandl

import datetime

quandl.ApiConfig.api_key = "oSysYNKB7dqj4asAuDQy"

from flask import Flask, request
app = Flask(__name__)

@app.route('/')
def home():
    return '''
    <form action="/data">
    Zip Code: <input type="text" name="zip_code"><br>
    Indicator Code: <input type="text" name="indicator"><br>
    <input type="submit" value="Submit">
    </form>
    '''

@app.route('/data')
def data():
    zip_code = request.args.get('zip_code')
    indicator = request.args.get('indicator')

    now = datetime.datetime.now()
    now_string = now.strftime('%Y-%m-%d')
    five_y_ago = now - datetime.timedelta(days=365*5)
    five_y_ago_string = five_y_ago.strftime('%Y-%m-%d')

    return str(quandl.get('ZILLOW/Z{}_{}'.format(zip_code, indicator), start_date=five_y_ago_string, end_date=now_string))

if __name__ == '__main__':
    app.run()
