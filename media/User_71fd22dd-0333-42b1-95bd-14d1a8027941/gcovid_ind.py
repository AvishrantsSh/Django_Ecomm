import calendar
import pandas as pd
from scipy.optimize import curve_fit
import numpy as np
from math import exp
import requests, json
from datetime import datetime
from fbprophet import Prophet
from fbprophet.plot import plot_plotly
import plotly.offline as py

def func_logistic(t, a, b, c):
    return c / (1 + a * np.exp(-b*t))

json_url = "https://api.covid19india.org/data.json"
response = requests.get(url = json_url)
todos = json.loads(response.text)
x = len(todos['cases_time_series'])
for i in range(x):
    cdate = todos['cases_time_series'][i]['date'].split()
    cdate[1] = str(list(calendar.month_name).index(cdate[1]))
    cdate.append("2020")
    cdate.reverse()
    todos['cases_time_series'][i]['date']=datetime.strptime("-".join(cdate) ,'%Y-%m-%d')

df = pd.DataFrame(todos['cases_time_series'])
df = df[:][['dailyconfirmed', 'date']]
df = df.rename(columns = {'dailyconfirmed': 'new_cases', 'dailydeceased':'fatalities'})
df['new_cases'] = df['new_cases'].astype(int)
df['date'] = pd.to_datetime(df.date)
df = df.reset_index(drop=False)


# Randomly initialize the coefficients
p0 = np.random.exponential(size=3)
bounds = (0, [100000., 1000., 1000000000.])
x = np.array(df['date']) + 1
y = np.array(df['new_cases'])
(a,b,c),cov = curve_fit(func_logistic, x, y, bounds=bounds, p0=p0, maxfev=1000000)
 
df['cap']=100000
df.columns = ['index', 'y', 'ds','cap']
# The time step at which the growth is fastest
t_fastest = np.log(a) / b
i_fastest = func_logistic(t_fastest, a, b, c)
m = Prophet(growth="logistic")
m.fit(df)
future = m.make_future_dataframe(periods=20)
future['cap'] = df['cap'].iloc[0]

forecast = m.predict(future)
forecast['trend'] = forecast['trend'].apply(np.ceil)
forecast['trend'] = forecast['trend'].astype(int)

# py.init_notebook_mode()
fig = plot_plotly(m, forecast)  # This returns a plotly Figure
py.plot(fig,output_type='div',
                auto_open=False,
                show_link=False,
                config=dict(
                    displayModeBar=False
                ))
# m.plot_components(forecast).savefig('test.png')
# py.iplot(fig)
# fig.write_html("/home/avishrant/Desktop/plottlyprediction.html")
