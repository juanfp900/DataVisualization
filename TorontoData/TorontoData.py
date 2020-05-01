#-------- MAY NEED TO DO THE FOLLOWING:
#-------- pip install descartes 
#-------- OR
#-------- conda install -c conda-forge descartes

import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

class TorontoData:

    def organizeNeighbourhoodData(self):
        dataFile = pd.read_csv('neighbourhood-profiles-2016.csv')
        dataFile.drop(dataFile.columns[[0, 1, 3]],inplace=True, axis=1)
        dataFile.set_index('Topic',inplace=True) #set index before transponse.
        df = dataFile.T  #Transpose   
        df.reset_index(inplace=True) #reset index of dataframe
        for col in df.columns:
            try:
                col.strip()
            except:
                print(col)
        
        df.rename(columns={'index': 'Neighbourhood'},inplace = True) #rename column header
        df.drop(df.columns.difference(['Income of households in 2015', 'Neighbourhood']), 1, inplace=True)
        df.columns = df.iloc[0] #these next 3 lines remove top row
        df = df.reindex(df.index.drop(0)).reset_index(drop=True)
        df.columns.name = None 
        df.rename(columns={'Characteristic' : 'Neighbourhood'}, inplace=True)
    
        neighbourhoodCol = df[['Neighbourhood']].copy()
        updated_df = df.loc[:,'Total - Household after-tax income groups in 2015 for private households - 100% data':]
        
        
        return (updated_df, neighbourhoodCol)
       
        
    
    def readShapeData(self):
        shapeFile = 'Neighbourhoods.shp'
        shape_df = gpd.read_file(shapeFile)
        
        shape_df['Neighbourhood'] = shape_df['FIELD_7'].str.replace(r"\(.*\)","") 
        shape_df['Neighbourhood'] = shape_df['Neighbourhood'].str.strip()
       
    
        return(shape_df)
        
    

    def calculateMedianIncome(self, updated_df, neighbourhoodCol):
        
        string_df = updated_df.replace(',','', regex=True) #remove commas from strings
        float_df = string_df.astype(float) #convert strings to floats for computation
         #float_df.columns = [col.strip() for col in float_df.columns]
        float_df = pd.concat([neighbourhoodCol,  float_df], axis=1)
        float_df.columns = [col.strip() for col in float_df.columns]
        
        rowIndex = 0
        columnIndex = 2
        constantCol = 1
        totalPercentage = 0
        incomeList = []
       
        while True: # loops through 1st until 20th column
            if rowIndex == 141: #loop until 140th row
                break
            floatTotal = np.float64(float_df.iloc[rowIndex,constantCol])
            currfloat = np.float64(float_df.iloc[rowIndex,columnIndex])
            currPercentage = (np.divide(currfloat,floatTotal))
            currPercentage = currPercentage*100
            totalPercentage = totalPercentage + currPercentage
            
            if totalPercentage > 50: #reset row index and column index (Loop to next neighbourhood)
                neighbourhood = float_df.iloc[rowIndex,0] #print neighbourhood analyzed
                medianIncomeForNeighbourhood = float_df.columns[columnIndex]
                incomeList.append(medianIncomeForNeighbourhood)
                rowIndex = rowIndex + 1
                columnIndex = 2 #go back to second column in index position 1 (second column)
                totalPercentage = 0
            
            columnIndex = columnIndex + 1
        
        float_df['Median Income'] = incomeList
        
        calculated_df = float_df[['Neighbourhood','Median Income']] 
      
        calculated_df.columns = [col.strip() for col in calculated_df.columns]

        return(calculated_df)
        


    def merge(self,shape_df, calculated_df):
        merged_left = pd.merge(left=shape_df, right=calculated_df, how='left', 
                               left_on='Neighbourhood', right_on='Neighbourhood')
        return(merged_left)
    
    

    def plotData(self, merged_left, shape_df):
        
        fig, ax = plt.subplots(1, figsize=(60, 40)) #need a fig to create a title. Can hide
        ax.axis('off') #Hide uneecessary axis we only care about title right now
        ax.set_title('Household After-Tax Income by Neighbourhood - 2015', fontdict={'fontsize': '40'})
        
        color = 'Greens'

        shape_df.plot('Neighbourhood', cmap=color, linewidth=2, ax=ax, edgecolor='0.8', figsize=(160,80))
        
        for index, row in merged_left.iterrows():
            ann = '         {}\n'.format(row) #add a space to prevent overlaps
            plt.annotate(row['Neighbourhood'], xy=(row['FIELD_11'], row['FIELD_12']),
            horizontalalignment='center', fontsize='small', color='black')

        plt.show()
 
       
def main():
    sns.set(style="darkgrid") 
    obj = TorontoData() #instantiate class
    updated_df, neighbourhoodCol = obj.organizeNeighbourhoodData()
    
    calculated_df =  obj.calculateMedianIncome(updated_df, neighbourhoodCol)
    shape_df = obj.readShapeData()

    merged_left  = obj.merge(calculated_df,shape_df)
    
    obj.plotData(merged_left, shape_df)

 
main()









