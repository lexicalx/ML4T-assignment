"""Assess a betting strategy. 			  		 			     			  	   		   	  			  	
                                                                                                 
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

from __future__ import print_function
import numpy as np
import matplotlib.pyplot as plt


def author():
    return 'lostleaf'  # replace tb34 with your Georgia Tech username.


def gtid():
    return 12345  # replace with your GT ID number


def get_spin_result(win_prob):
    result = False
    if np.random.random() <= win_prob:
        result = True
    return result


def simulate(win_prob, win_limit, bet_times, lose_limit=10**100):
    # add your code here to implement the experiments
    winnings = []
    episode_winnings = 0
    bet_amount = 1
    for i in range(bet_times):
        if episode_winnings <= -lose_limit:
            winnings.append(-lose_limit)
            continue

        if episode_winnings >= win_limit:
            winnings.append(win_limit)
            continue

        won = get_spin_result(win_prob)
        if won:
            episode_winnings += bet_amount
            bet_amount = 1
        else:
            episode_winnings -= bet_amount
            bet_amount *= 2
            if episode_winnings < 0:
                bet_amount = min(bet_amount, lose_limit + episode_winnings)
        winnings.append(episode_winnings)
    return np.array(winnings)

def test_code():
    win_prob = 0.50  # set appropriately to the probability of a win
    np.random.seed(gtid())  # do this only once
    win_limit = 80

    def p1():
        for i in range(10):
            winnings = simulate(win_prob, win_limit, 1000)
            plt.plot(winnings)
        plt.xlim([0, 300])
        plt.ylim([-256, 100])
        plt.show()

    def p2():
        means = []
        stds = []
        for i in range(1000):
            winnings = simulate(win_prob, win_limit, 1000)
            means.append(np.mean(winnings))
            stds.append(np.std(winnings))
        means = np.array(means)
        stds = np.array(stds)

        # plt.xlim([0, 300])
        plt.ylim([-250, 250])
        plt.plot(means)
        plt.plot(means + stds)
        plt.plot(means - stds)
        plt.show()

    def p3():
        means = []
        stds = []
        for i in range(1000):
            winnings = simulate(win_prob, win_limit, 1000)
            means.append(np.median(winnings))
            stds.append(np.std(winnings))
        means = np.array(means)
        stds = np.array(stds)

        # plt.xlim([0, 300])
        plt.ylim([-250, 250])
        plt.plot(means)
        plt.plot(means + stds)
        plt.plot(means - stds)
        plt.show()

    def p4():
        means = []
        stds = []
        for i in range(1000):
            winnings = simulate(win_prob, win_limit, 1000, 256)
            means.append(np.mean(winnings))
            stds.append(np.std(winnings))
        means = np.array(means)
        stds = np.array(stds)

        # plt.xlim([0, 300])
        plt.ylim([-250, 250])
        plt.plot(means)
        # plt.plot(means + stds)
        # plt.plot(means - stds)
        plt.show()
    
    def p5():
        means = []
        stds = []
        for i in range(1000):
            winnings = simulate(win_prob, win_limit, 1000, 256)
            means.append(np.median(winnings))
            stds.append(np.std(winnings))
        means = np.array(means)
        stds = np.array(stds)

        # plt.xlim([0, 300])
        plt.ylim([-250, 250])
        plt.plot(means)
        # plt.plot(means + stds)
        # plt.plot(means - stds)
        plt.show()
    # p1()
    # p3()
    p5()

if __name__ == "__main__":
    test_code()
