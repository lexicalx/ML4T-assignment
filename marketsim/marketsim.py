from datetime import datetime
import pandas as pd
import numpy as np
import os
from util import get_data, plot_data


def author():
    return 'lostleaf'


def compute_portvals(orders_file="./orders/orders.csv", start_val=1000000, commission=9.95, impact=0.005):
    def trade_cost(x):
        if not x['Symbol']:
            return 0
        return -(x[x['Symbol']] * x['Order'] * x['Shares']) * 1 - impact * x[x['Symbol']] * x['Shares'] - commission

    orders = pd.read_csv(orders_file)

    orders.loc[orders['Order'] == 'BUY', 'Order'] = 1
    orders.loc[orders['Order'] == 'SELL', 'Order'] = -1
    orders['Order'] = pd.to_numeric(orders['Order'])
    orders['Date'] = pd.to_datetime(orders['Date'])
    orders.set_index('Date', inplace=True)

    start_date = orders.index.min()
    end_date = orders.index.max()
    symbols = orders['Symbol'].unique()

    market_data = get_data(symbols, pd.date_range(start_date, end_date))
    tmp = market_data.join(orders).fillna(0)
    cash_delta = tmp.apply(trade_cost, axis=1).groupby(level=0).sum()
    cash = start_val + cash_delta.cumsum()

    pos_delta = pd.DataFrame(index=market_data.index)
    for symbol, df in orders.groupby('Symbol'):
        pos_delta[symbol] = (df['Order'] * df['Shares']).groupby(level=0).sum()
    pos = pos_delta.fillna(0).cumsum()
    port_val = (pos * market_data[symbols]).sum(axis=1) + cash

    return port_val


def evaluate_portfolio(port_val):
    cr = port_val.iloc[-1] / port_val.iloc[0]
    dr = (port_val / port_val.shift(1) - 1).dropna()
    adr = dr.mean()
    sddr = dr.std()
    sr = (adr) / sddr * np.sqrt(252)
    return cr, adr, sddr, sr


def test_code():
    # this is a helper function you can use to test your code  		   	  			    		  		  		    	 		 		   		 		  
    # note that during autograding his function will not be called.  		   	  			    		  		  		    	 		 		   		 		  
    # Define input parameters  		   	  			    		  		  		    	 		 		   		 		  

    of = "./orders/orders-02.csv"
    sv = 1000000

    # Process orders  		   	  			    		  		  		    	 		 		   		 		  
    portvals = compute_portvals(orders_file=of, start_val=sv)
    if isinstance(portvals, pd.DataFrame):
        portvals = portvals[portvals.columns[0]]
    else:
        "warning, code did not return a DataFrame"

        # Get portfolio stats
    # Here we just fake the data. you should use your code from previous assignments.  		   	  			    		  		  		    	 		 		   		 		  
    start_date = datetime(2011, 1, 5)
    end_date = datetime(2011, 1, 20)
    data_SPY = get_data(['SPY'], pd.date_range(start_date, end_date))
    cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio = evaluate_portfolio(portvals)
    cum_ret_SPY, avg_daily_ret_SPY, std_daily_ret_SPY, sharpe_ratio_SPY = evaluate_portfolio(data_SPY)

    # Compare portfolio against $SPX
    print "Date Range: {} to {}".format(start_date, end_date)
    print
    print "Sharpe Ratio of Fund: {}".format(sharpe_ratio)
    # print "Sharpe Ratio of SPY : {}".format(sharpe_ratio_SPY)
    print
    print "Cumulative Return of Fund: {}".format(cum_ret)
    # print "Cumulative Return of SPY : {}".format(cum_ret_SPY)
    print
    print "Standard Deviation of Fund: {}".format(std_daily_ret)
    # print "Standard Deviation of SPY : {}".format(std_daily_ret_SPY)
    print
    print "Average Daily Return of Fund: {}".format(avg_daily_ret)
    # print "Average Daily Return of SPY : {}".format(avg_daily_ret_SPY)
    print
    print "Final Portfolio Value: {}".format(portvals[-1])


if __name__ == "__main__":
    test_code()
