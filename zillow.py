import quandl

import datetime

quandl.ApiConfig.api_key = "oSysYNKB7dqj4asAuDQy"

zip_code = 11228

now = datetime.datetime.now()
now_string = now.strftime('%Y-%m-%d')
five_y_ago = now - datetime.timedelta(days=365*5)
five_y_ago_string = five_y_ago.strftime('%Y-%m-%d')

print (quandl.get('ZILLOW/Z{}_{}'.format(zip_code, 'MLPAH'), start_date=five_y_ago_string, end_date=now_string))
print (quandl.get('ZILLOW/Z{}_{}'.format(zip_code, 'ZHVIAH'), start_date=five_y_ago_string, end_date=now_string))
