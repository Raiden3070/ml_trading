import datetime as dt
import random
import pandas as pd
from data_utils import fetch_stock_data
import random_tree_learner as rtl
import bagging_learner as bl
import indicator_calculator as ind
  		  	   		 	   			  		 			     			  	 
  		  	   		 	   			  		 			     			  	 
class MLTrading(object):  		  	   		 	   			  		 			     			  	 
		  	   		 	   			  		 			     			  	 	  	   		 	   			  		 			     			  	  		  	   		 	   			  		 			     			  	 
    # constructor  		  	   		 	   			  		 			     			  	 
    def __init__(self, impact=0.0, commission=0.0):  		  	   		 	   			  		 			     			  	 
    	  	   		 	   			  		 			     			  	 
        #Constructor 		  	   		 	   			  		 			     			  	 
      	   		 	   			  		 			     			  	 		  	   		 	   			  		 			     			  	 
        self.impact = impact  		  	   		 	   			  		 			     			  	 
        self.commission = commission
        self.learner = bl.BaggingLearner(learner=rtl.RandomTreeLearner, bags=50, kwargs={"leaf_size": 5}, boost=False)

     # Creates a ML model based on indicators                                                                   	  	   		 	   			  		 			     			  	 
    def append_training_data(   
        self,  		  	   		 	   			  		 			     			  	 
        symbol="IBM",  		  	   		 	   			  		 			     			  	 
        sd=dt.datetime(2008, 1, 1),  		  	   		 	   			  		 			     			  	 
        ed=dt.datetime(2009, 1, 1),  		  	   		 	   			  		 			     			  	 
        sv=100000,
        price_series=None,
    ):  		  	   		 	   			  		 			     			  	 	  	   		 	   			  		 			     			  	 
  		  	   		 	   			  		 			     			  	 
        # Prefer injected series to avoid filesystem reads (works on Streamlit Cloud)
        if price_series is not None:
            prices = pd.Series(price_series).loc[sd:ed].ffill().bfill()
        else:
            prices = fetch_stock_data([symbol], pd.date_range(sd, ed))[symbol]

        # Compute indicators (use provided series if any)
        sma = ind.compute_price_sma(sd, ed, symbol, price_series=price_series)
        bb = ind.compute_bb_percentage(sd, ed, symbol, price_series=price_series)
        macd = ind.compute_macd(sd, ed, symbol, price_series=price_series)
        momen = ind.compute_momentum(sd, ed, symbol, price_series=price_series)
        ppo = ind.compute_ppo(sd, ed, symbol, price_series=price_series)

        N = 19
        # Use forward N-day return for labeling; simulator handles impact/commission
        returns = (prices.shift(-N) / prices) - 1.0

        YBUY = 0.06
        YSELL = -0.18
        # Build target as integer Series from the start to avoid downcast warnings
        Y = pd.Series(0, index=returns.index, dtype=int, name='Y')
        Y.loc[returns > YBUY] = 1
        Y.loc[returns < YSELL] = -1

        dataset = pd.concat([sma, bb, macd, ppo, momen, Y], axis=1).fillna(0)

        X = dataset.iloc[:, :-1].values
        Y = dataset.iloc[:, -1].values
        self.learner.append_training_data(X, Y)
    #  Test the ML model and output trades  	
    	 	   			  		 			     			  	 
    def testPolicy(   
        self,  		  	   		 	   			  		 			     			  	 
        symbol="IBM",  		  	   		 	   			  		 			     			  	 
        sd=dt.datetime(2009, 1, 1),  		  	   		 	   			  		 			     			  	 
        ed=dt.datetime(2010, 1, 1),  		  	   		 	   			  		 			     			  	 
        sv=100000,
        price_series=None,
    ):  		  	   		 	   			  		 			     			  	 

        if price_series is not None:
            prices = pd.Series(price_series).loc[sd:ed].ffill().bfill()
        else:
            prices = fetch_stock_data([symbol], pd.date_range(sd, ed))[symbol]

        sma = ind.compute_price_sma(sd, ed, symbol, price_series=prices)
        bb = ind.compute_bb_percentage(sd, ed, symbol, price_series=prices)
        macd = ind.compute_macd(sd, ed, symbol, price_series=prices)
        momen = ind.compute_momentum(sd, ed, symbol, price_series=prices)
        ppo = ind.compute_ppo(sd, ed, symbol, price_series=prices)

        indicators = pd.concat([sma, bb, macd, ppo, momen], axis=1).fillna(0)

        dataX = indicators.values
        dataY = self.learner.query(dataX)


        trades = pd.DataFrame(index=prices.index, columns=[symbol])
        holding = 0
        for i in range(len(prices)):
            if dataY[i] == 1:  # LONG
                trades.iloc[i] = 1000 - holding
            elif dataY[i] == -1:  # SHORT
                trades.iloc[i] = -1000 - holding
            else:  # CASH
                trades.iloc[i] = -holding
            holding += trades.iloc[i]

# Debug output
            """
            print("This is trades type")
            print(type(trades))
            print("This is trades")
            print(trades)
            print("This is prices for testing policy period")
            print(prices)
            """
        return trades

