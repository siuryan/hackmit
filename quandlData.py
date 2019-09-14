import quandl
import pandas as pd 
import numpy as np
from matplotlib import pyplot
quandl.ApiConfig.api_key = "EiNsSSrDs1Xr29Xz4RYe"

def indicators_reformat():
	ind_csv = pd.read_csv("indicators.csv")
	data = {"Indicator": [], "Code": []}
	for i in ind_csv["INDICATOR|CODE"]:
		indicator, code = i.split("|")[0], i.split("|")[1]
		data['Indicator'].append(indicator)
		data['Code'].append(code)
	pd_data = pd.DataFrame.from_dict(data)
	pd_data.to_csv("indicators_table.csv")
		
indicator_to_code = pd.read_csv("indicators_table.csv")

input_zipcode = "07871"
input_data_type = "Median Listing Price - All Homes"
code = indicator_to_code['Code'][list(np.where((indicator_to_code['Indicator']==input_data_type)==True))[0][0]]
start_date = "2009-01-31"
end_date = '2019-01-31'

series= quandl.get('ZILLOW/Z{}_{}'.format(input_zipcode, code), start_date=start_date, end_date=end_date)

pyplot.scatter(series.index, series, c="blue")
pyplot.plot(series)
pyplot.xlabel("Time", fontsize="x-large", weight="bold")
pyplot.ylabel(input_data_type, fontsize="x-large", weight="bold")
pyplot.title("{} for area {}".format(input_data_type, input_zipcode))
pyplot.show()
