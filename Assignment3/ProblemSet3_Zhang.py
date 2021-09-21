# -*- coding: utf-8 -*-
"""
Created on Sat Sep 11 20:43:37 2021

@author: Siwen Z
"""

# lets import some pcks first
import os # set up the working dir
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from pandas.plotting import register_matplotlib_converters
from matplotlib.dates import DateFormatter
register_matplotlib_converters()


#%% adding more info inside to fill the blank? use different colors to distinguish groups? sort on the ipodate?

# 1. A timeline stacked bar charts for all 180 SPAC deals
# read in the source excel file

spac_date_timeline = pd.read_excel('C:\\Users\\f1060\\OneDrive - University of South Carolina\\First_year_paper\\data_code\\temp\\All_firms_180_identifers_new.xls',
                         sheet_name = "Sheet1", header = 0, index_col = 0)
spac_date_timeline.sort_values(by=["ipodate"], inplace=True)


time_diff = spac_date_timeline.deal_closed_date - spac_date_timeline.ipodate
# time_diff = sorted(time_diff) # doing this makes the deals messed up!

# =============================================================================
# # I was thinking to use the dataframe to sort and apply the df later - but more complex! 
# # change it into dataframe for sorting easier
# time_diff = pd.DataFrame(time_diff)
# # so if the column name is a number, do not use ''!!
# time_diff.sort_values(by=[0], inplace=True) # so the sorted df replaces the previous one
# =============================================================================

# using to_datetime did not work well
# spac_date_timeline['ipodate'] = pd.to_datetime(spac_date_timeline['ipodate'])
# spac_date_timeline['closed_date'] = pd.to_datetime(spac_date_timeline['closed_date'])


fig, spac_tl = plt.subplots(figsize=(8,10)) # set the size of the figure


# these codes are used for a vertical stacked bar chart!
# spac_tl.bar(spac_date_timeline.newco_BB, spac_date_timeline.ipodate, align='center', color = 'w')
# spac_tl.bar(spac_date_timeline.newco_BB, time_diff, align='center', bottom = spac_date_timeline.ipodate)


spac_tl.barh(spac_date_timeline.newco_BB, 
             spac_date_timeline.ipodate, 
             align='center', 
             color = 'w')
spac_tl.barh(spac_date_timeline.newco_BB, 
             time_diff, 
             align = 'center', 
             left = spac_date_timeline.ipodate, 
             linewidth = 1.5, 
             color = 'r')

# add a vertical year noting the spac boom year!
spac_tl.axvline('2020-01-01', 
                color = "blue",  
                linestyle = "dashdot")

# date the x axis!
date_form = DateFormatter("%y-%m-%d")
spac_tl.xaxis.set_major_formatter(date_form)


# set up the graph info!
spac_tl.set(xlim=["2015-01-01", "2021-06-30"])
spac_tl.set(title='SPACs Timeline')
# make y axis looks better
spac_tl.set_yticklabels([])
spac_tl.set(ylabel=None) # remove the y-axis label!!
spac_tl.tick_params(left=False)  # remove the ticks!!

fig.savefig("SPACs_tl.png")

plt.show()

#%% 

# 2. average twitter sentiment/count to the trading volumn

spac_date_timeline['log_trading_vloumn'] = np.log10(spac_date_timeline['traVol_daily_avg_perfirm'])
avg_trading_vloumn = spac_date_timeline["log_trading_vloumn"].mean()
avg_news_pub = spac_date_timeline["news_count_daily_avg_perfirm"].mean()
avg_twi_pub = spac_date_timeline["twi_count_daily_avg_perfirm"].mean()

fig, twi_news_perfirm = plt.subplots()

twi_news_perfirm.plot()

twi_news_perfirm.scatter(spac_date_timeline.log_trading_vloumn,
                         spac_date_timeline.twi_count_daily_avg_perfirm,
                         color='blue')
twi_news_perfirm.set(xlabel='Log of Average Daily Trading Volume', 
                     ylabel='Daily Average Twitter Publication Count',
                     title='Daily Average Media Attention and Trading Volume')

twi_news_perfirm.axhline(avg_twi_pub, 
                color = "blue",  
                linestyle = "dashdot")

# get a second y-axis
twi_news_perfirm = twi_news_perfirm.twinx()
twi_news_perfirm.scatter(spac_date_timeline.log_trading_vloumn,
                         spac_date_timeline.news_count_daily_avg_perfirm,
                         color='red')
twi_news_perfirm.set(ylabel='Daily Average News Count')

twi_news_perfirm.axhline(avg_news_pub, 
                color = "red",  
                linestyle = "dashdot")


# twi_news_perfirm.grid() # do you wanna grid?

# twi_news_perfirm.set(xlim=[0, 50]) # 

plt.show()

fig.savefig("daily_avg_media.png")


#%%

# 3. deals' characteristics - subsample analysis/circle analysis (size differs!)

# create a subsample based on the series issuers
spac_series_issuers = spac_date_timeline[spac_date_timeline["series"] == 1]
spac_not_series_issuers = spac_date_timeline[spac_date_timeline["series"] != 1]
spac_series_issuers['ID'] = np.arange(len(spac_series_issuers))+1 #this is the y var I want
spac_not_series_issuers['ID'] = np.arange(len(spac_not_series_issuers))+1 #this is the y var I want

# it turns out that making a stacking figure, we cannot use individual figure names! Just use [,] is fine

fig, series_issuers = plt.subplots(2,2) # create two rows and two columns for a subsample figure


series_issuers[0,0].scatter(spac_series_issuers.ID, 
                         spac_series_issuers.redeemed)

series_issuers[0,1].scatter(spac_not_series_issuers.ID, 
                         spac_not_series_issuers.redeemed,
                         color = "red")
series_issuers[0,1].sharey(series_issuers[0,0]) # share the same y!

# series_issuers[0,].set(title = 'Series Issuers and Daily Average Twitter Publication Count')
# not sure how to set the title for the first row and then another one for the second row
# for four titles four graphs: use axs[0, 0].set_title("main") one by one!

series_issuers[1,0].plot(spac_series_issuers.ID, 
                      spac_series_issuers.twi_count_daily_avg_perfirm)
series_issuers[1,0].sharex(series_issuers[0,0]) # share the same x!

series_issuers[1,1].plot(spac_not_series_issuers.ID, 
                      spac_not_series_issuers.twi_count_daily_avg_perfirm)
series_issuers[1,1].sharey(series_issuers[1,0]) # share the same y!
series_issuers[1,1].sharex(series_issuers[0,1]) # share the same x!


fig.tight_layout()
fig.savefig("subsample.png")
