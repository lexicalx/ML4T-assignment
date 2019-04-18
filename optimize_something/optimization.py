"""MC1-P2: Optimize a portfolio.  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
Copyright 2018, Georgia Institute of Technology (Georgia Tech)  		   	  			    		  		  		    	 		 		   		 		  
Atlanta, Georgia 30332  		   	  			    		  		  		    	 		 		   		 		  
All Rights Reserved  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
Template code for CS 4646/7646  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
Georgia Tech asserts copyright ownership of this template and all derivative  		   	  			    		  		  		    	 		 		   		 		  
works, including solutions to the projects assigned in this course. Students  		   	  			    		  		  		    	 		 		   		 		  
and other users of this template code are advised not to share it with others  		   	  			    		  		  		    	 		 		   		 		  
or to make it available on publicly viewable websites including repositories  		   	  			    		  		  		    	 		 		   		 		  
such as github and gitlab.  This copyright statement should not be removed  		   	  			    		  		  		    	 		 		   		 		  
or edited.  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
We do grant permission to share solutions privately with non-students such  		   	  			    		  		  		    	 		 		   		 		  
as potential employers. However, sharing with other current or future  		   	  			    		  		  		    	 		 		   		 		  
students of CS 7646 is prohibited and subject to being investigated as a  		   	  			    		  		  		    	 		 		   		 		  
GT honor code violation.  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
-----do not edit anything above this line---  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
Student Name: Tucker Balch (replace with your name)  		   	  			    		  		  		    	 		 		   		 		  
GT User ID: tb34 (replace with your User ID)  		   	  			    		  		  		    	 		 		   		 		  
GT ID: 900897987 (replace with your GT ID)  		   	  			    		  		  		    	 		 		   		 		  
"""

import datetime as dt

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.optimize as spo

from util import get_data, plot_data


# This is the function that will be tested by the autograder
# The student must update this code to properly implement the functionality
def optimize_portfolio(sd=dt.datetime(2008, 1, 1),
                       ed=dt.datetime(2009, 1, 1),
                       syms=['GOOG', 'AAPL', 'GLD', 'XOM'],
                       gen_plot=False):

    # Read in adjusted closing prices for given symbols, date range
    dates = pd.date_range(sd, ed)
    prices_all = get_data(syms, dates)  # automatically adds SPY
    prices = prices_all[syms]  # only portfolio symbols
    prices_SPY = prices_all['SPY']  # only SPY, for comparison later

    # find the allocations for the optimal portfolio
    # note that the values here ARE NOT meant to be correct for a test case
    prices_norm = prices / prices.iloc[0]

    def neg_sharpe(al):
        port_val = (np.array(al) * prices_norm).sum(axis=1)
        daily_return = (port_val / port_val.shift(1) - 1).dropna()
        avg_daily_reture = daily_return.mean()
        std_daily_return = daily_return.std()
        return -avg_daily_reture / std_daily_return

    allocs = spo.minimize(neg_sharpe, [1.0 / len(syms)] * len(syms),
                          method='SLSQP',
                          bounds=[(0, 1) for _ in range(len(syms))],
                          constraints=[{
                              'type': 'eq',
                              'fun': lambda inputs: 1 - np.sum(inputs)
                          }]).x

    # Get daily portfolio value
    port_val = (1 * np.array(allocs) / prices.iloc[0] * prices).sum(axis=1)
    # Get portfolio statistics (note: std_daily_ret = volatility)
    cr, adr, sddr, sr = [0.25, 0.001, 0.0005,
                         2.1]  # add code here to compute stats
    cr = np.sum(prices.iloc[-1].values / prices.iloc[0].values * allocs) - 1
    dr = (port_val / port_val.shift(1) - 1).dropna()
    adr = dr.mean()
    sddr = dr.std()
    sr = adr / sddr * np.sqrt(252)

    # Compare daily portfolio value with SPY using a normalized plot
    if gen_plot:
        # add code to plot here
        df_temp = pd.concat([port_val, prices_SPY],
                            keys=['Portfolio', 'SPY'],
                            axis=1)
        df_temp /= df_temp.iloc[0]
        df_temp.plot()
        plt.show()

    return allocs, cr, adr, sddr, sr


def test_code():
    # This function WILL NOT be called by the auto grader
    # Do not assume that any variables defined here are available to your function/code
    # It is only here to help you set up and test your code

    # Define input parameters
    # Note that ALL of these values will be set to different values by
    # the autograder!

    start_date = dt.datetime(2010, 1, 1)
    end_date = dt.datetime(2010, 12, 31)
    symbols = ['GOOG', 'AAPL', 'GLD', 'XOM']

    # Assess the portfolio
    allocations, cr, adr, sddr, sr = optimize_portfolio(sd = start_date, ed = end_date,\
        syms = symbols, \
        gen_plot = True)

    # Print statistics
    print "Start Date:", start_date
    print "End Date:", end_date
    print "Symbols:", symbols
    print "Allocations:", allocations
    print "Sharpe Ratio:", sr
    print "Volatility (stdev of daily returns):", sddr
    print "Average Daily Return:", adr
    print "Cumulative Return:", cr


if __name__ == "__main__":
    # This code WILL NOT be called by the auto grader
    # Do not assume that it will be called
    test_code()
