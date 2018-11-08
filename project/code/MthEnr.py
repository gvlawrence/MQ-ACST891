""" Enrich monthly fuel price data with new columns    G.Lawrence  83186557 """
import pandas as pd
df2 = pd.DataFrame()

# get list of yymm values to process (1706 to 1808)
mths = list(range(1706,1713))   # 2017 mths 06-12
mths.extend(range(1801,1809))   # 2018 mths 01-08 

# read PostcodeRegions and PriceAdjustments
inReg=pd.read_csv('./PostcodeRegArea.csv')
inAdj=pd.read_csv('./vDiff.csv')

# setup season lookups
SeaCode = ['17B','17B','17B','17C','17C','17C','17D',   # 2017 mths 06-12
     '17D','17D','18A','18A','18A','18B','18B','18B']   # 2018 mths 01-08 
Mth2Code = dict(zip(mths,SeaCode))
Char2Name = {'A':'Autumn', 'B':'Winter', 'C':'Spring', 'D':'Summer'}

# loop thru all months
for yymm in mths[0:15]: 
  df1 = pd.read_excel('./FuelCheck/pricehist_20%s.xlsx' % yymm) 
  print("\nyymm=",yymm," #rows=",len(df1))      
  print("Column headings:"); print(df1.columns)  
        
  # append split PUdate & other new cols, incl static season cols
  df1['Pdate'] = df1.PriceUpdatedDate.dt.strftime("%Y-%m-%d")
  df1['Ptime'] = df1.PriceUpdatedDate.dt.strftime("%X")
  df1['MonthYear'] = df1.PriceUpdatedDate.dt.strftime("%b-%y")
  df1['YearMonth'] = df1.PriceUpdatedDate.dt.strftime("%Y-%m")
  df1['Weekday'] = df1.PriceUpdatedDate.dt.strftime("%A")
  df1['AMPM'] = df1.PriceUpdatedDate.dt.strftime("%p")
  df1['SeasonCode'] = Mth2Code[yymm]
  df1['SeasonName'] = Char2Name[Mth2Code[yymm][2]]  #Char is pos2 of SeaCode

  # merge to append Region and Area columns
  df1 = pd.merge(df1, inReg, on='Postcode', how='left')

  # merge to append vDiff col then create adjPrice (Price+vDiff) col  
  df1 = pd.merge(df1, inAdj, on='Pdate', how='left')
  df1['AdjPrice'] = round( df1['Price'] + df1['vDiff'], 1)
  
  # write out individual result and append to overall df
  df1.to_csv('./FuelCheck/PriceNew_20%s.csv' % yymm,
             sep=',',header=True,index=False)
  df2 = df2.append(df1) 

# remove unwanted cols & fuel-types; write out overall result
df2 = df2.drop(['PriceUpdatedDate','Address','Region','vDiff'], axis=1)  
remCodes = set(['CNG','LPG','E85','B20','EV'])
df2 = df2[~df2['FuelCode'].isin(remCodes)]
df2.to_csv('./FuelCheck/PriceNew_15.csv', sep=',',header=True,index=False)
