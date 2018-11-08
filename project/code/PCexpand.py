""" Expand Postcode ranges into Postcode lists - G.Lawrence  83186557 """
import pandas as pd

#############################################################################
## Read and expand input ranges (G=range, R=region, A=area)
#############################################################################
inGR=pd.read_csv('./PostcodeRanges.csv')
print("#ranges=",len(inGR))
pc2reg = dict()

for j in range(len(inGR)):    # 
  parts = inGR['Range'][j].split(' - ')
  part1 = int(parts[0])
  part2 = part1 if len(parts)==1 else int(parts[1])
  #print("j=",j," r=",inGR['Range'][j]," p1=",part1," p2=",part2)  
  for pc in range(part1,part2+1):
    #print("j=",j," pc=",pc,"reg=",inGR['Region'][j])
    pc2reg[pc] = inGR['Region'][j]

# create Postcode-Region dataframe
dfPR = pd.DataFrame(list(pc2reg.items()),columns=['Postcode','Region'])

# merge to add RegionA and Area cols
inRA=pd.read_csv('./RegionArea.csv')
dfPRA = pd.merge(dfPR, inRA, on='Region', how='left')

# write out PRA lookup file
dfPRA.to_csv('./PostcodeRegArea.csv',sep=',',header=True,index=False)
