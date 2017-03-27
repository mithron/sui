from fbprophet import Prophet
import pandas as pd
import datetime as dt

def read_convert(path='data_before_2015.csv'):
    '''
    read and make pandas DataFrame from suicide rosstat data
    '''
    df = pd.read_csv(path)
    minus = pd.Series(['-' for i in range(len(df['year']))])
    mon = pd.Series([str(month) for month in df['month_num']])
    yea = pd.Series([str(year) for year in df['year']])
    dat = pd.Series([str((dt.date(year, month+1, 1) - dt.timedelta(days=1)).day) 
                    if month != 12
                    else str((dt.date(year+1, 1, 1) - dt.timedelta(days=1)).day)
                    for month, year in zip(df['month_num'], df['year'])])
    fulldate = yea + minus + mon + minus + dat    
    return pd.DataFrame({'ds':fulldate, 'y':df['num']})
    
def predict_2016():
    '''
    make and return fbprophet monthly predictions for 2016 year based
    on prev years data
    '''
    df = read_convert()
    m = Prophet().fit(df)
    future = m.make_future_dataframe(periods=12, freq='M')
    fcst = m.predict(future)
    return fcst[-12:]

def compare():
    pass