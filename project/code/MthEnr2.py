""" Enrich overall fuel data with Weeknum+Rank    G.Lawrence  83186557 """
import pandas as pd
df2 = pd.DataFrame()

# read overall file
F1 = pd.read_csv('./FuelCheck/PriceNew_15.csv')

# append Weeknum column
F1['Date4Week'] = pd.to_datetime(F1['Pdate'])
F1['Weeknum'] = F1.Date4Week.dt.strftime("%yW%W")  

# append WeekRank column (of AdjPrice within SSname/FuelCode/Weeknum)
F1 = F1.sort_values(by=['ServiceStationName','FuelCode','Weeknum','AdjPrice'])
GB1 = F1.groupby(['ServiceStationName','FuelCode','Weeknum'])
F1['WeekRank'] = GB1.rank(method='dense',axis=0,numeric_only=True)['AdjPrice']

# append MonthRank column (of AdjPrice within SSname/FuelCode/YearMonth)
F1 = F1.sort_values(by=['ServiceStationName','FuelCode','YearMonth','AdjPrice'])
GB2 = F1.groupby(['ServiceStationName','FuelCode','YearMonth'])
F1['MonthRank'] = GB2.rank(method='dense',axis=0,numeric_only=True)['AdjPrice']

# remove unwanted cols; write out overall result
F1 = F1.drop(['MonthYear','Date4Week'], axis=1)  
F1.to_csv('./FuelCheck/PriceRank15.csv', sep=',',header=True,index=False)
