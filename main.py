from fbprophet import Prophet
import pandas as pd
import numpy as np
import datetime as dt

def read_convert(path='all_data.csv'):
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
    data_prev = read_convert()[:-13]
    m = Prophet().fit(data_prev)
    future = m.make_future_dataframe(periods=13, freq='M')
    print(future.tail())
    predictions = m.predict(future)
    print(predictions)
    return predictions[-13:]

def compare(path='all_data.csv'):
    '''
    compare predictions and true results
    '''
    data2016 = read_convert(path)[-13:]
    predictions = predict_2016()
    cmp['error'] = data2016['y'] - predictions['yhat']
    cmp['prob'] = 100*cmp['error']/data2016[y]
    print('MAPE: ' + str(np.mean(abs(cmp[-13:]['prob']))))
    print('MAE :'+ str(np.mean(abs(cmp[-13:]['error']))))

    