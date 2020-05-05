
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


class TorontoData:
    years = ['2011', '2006', '2001'] #tabs that appear in excel file
    
    def OrgainzeOldData(self):
        
        dfList = []
        global years
        for year in years:
            oldData = pd.read_excel('neighbourhood-data-2001-2011.xlsx', sheet_name=year)
            oldData.drop(oldData.columns[[0]], inplace = True, axis = 1)
            oldData.set_index('Topic',inplace=True)
            oldData.columns = [col.strip() for col in oldData.columns]
            dfOld = oldData.T  #Transpose   
            dfOld.reset_index(inplace=True) #reset index of dataframe
            
            dfOld.rename(columns={'index': 'Neighbourhood'},inplace = True) #rename column header
            dfOld.drop(dfOld.columns.difference(['Income of households', 'Neighbourhood']), 1, inplace=True)
            
            #drops top row
            dfOld.columns = dfOld.iloc[0] 
            dfOld = dfOld.reindex(dfOld.index.drop(0)).reset_index(drop=True)
            
            #removes white spaces from column headers
            dfOld.rename(columns=lambda x: x.strip(), inplace=True)
           
            dfOld.rename(columns={'Attribute': 'Neighbourhood'},inplace = True) #rename column header
            neighbourhoodCol = dfOld[['Neighbourhood']].copy()
          
            if year == '2001':
                dfOld = dfOld.loc[:,'Census family income in 2000 of all families - 20% Sample Data':'$100,000 and over']
            
            if year == '2006':
                dfOld = dfOld.loc[:,'After-tax income in 2005 of private households - 20% sample data':'$100,000 and over']
                
            if year == '2011':
                dfOld = dfOld.loc[:,'After-tax income of households in 2010 of private households':'$125,000 and over']
                dfOld.drop(['$100,000 and over'], inplace = True, axis = 1)
              
            dfList.append(dfOld)
        return(dfList, neighbourhoodCol)
    
    
  
    def Organize2016Data(self):
        newData = pd.read_csv('neighbourhood-profiles-2016.csv')
        newData.drop(newData.columns[[0, 1, 3]],inplace=True, axis=1)
        newData.set_index('Topic',inplace=True) #set index before transponse.
        dfNew = newData.T  #Transpose   
        dfNew.reset_index(inplace=True) #reset index of dataframe
        for col in dfNew.columns:
            try:
                col.strip()
            except:
                print(col)
        dfNew.rename(columns={'index': 'Neighbourhood'},inplace = True) #rename column header
        dfNew.drop(dfNew.columns.difference(['Income of households in 2015', 'Neighbourhood']), 1, inplace=True)
        dfNew.columns = dfNew.iloc[0] #these next 3 lines remove top row
        dfNew = dfNew.reindex(dfNew.index.drop(0)).reset_index(drop=True)
        dfNew.columns.name = None 
        dfNew.rename(columns={'Characteristic' : 'Neighbourhood'}, inplace=True)
    
        neighbourhoodCol = dfNew[['Neighbourhood']].copy()
        dfNew = dfNew.loc[:,'Total - Household after-tax income groups in 2015 for private households - 100% data':]
        
        
        return (dfNew, neighbourhoodCol)
    
    
    def ListToDataFrame(self, dfList, neighbourhoodCol):
        
        incomeList = []
        
        for dataframe in dfList:
            oldIncome = self.CalculateMedianIncome(dataframe,neighbourhoodCol)
            incomeList.append(oldIncome)
      
        return(incomeList)
  

    def CalculateMedianIncome(self, dataFrame, neighbourhoodCol):
        
        string_df = dataFrame.replace(',','', regex=True) #remove commas from strings
        float_df = string_df.astype(float) #convert strings to floats for computation
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

       # colname = df.columns[pos]
        
        if dataFrame.columns[0] == 'Census family income in 2000 of all families - 20% Sample Data':
            float_df['Median Income 2000'] = incomeList
            calculated_df = float_df[['Neighbourhood','Median Income 2000']] 
        
        if dataFrame.columns[0] == 'After-tax income in 2005 of private households - 20% sample data':
            float_df['Median Income 2005'] = incomeList
            calculated_df = float_df[['Neighbourhood','Median Income 2005']] 
        
        if dataFrame.columns[0] == 'After-tax income of households in 2010 of private households':
            float_df['Median Income 2010'] = incomeList
            calculated_df = float_df[['Neighbourhood','Median Income 2010']] 
        
        if dataFrame.columns[0] == 'Total - Household after-tax income groups in 2015 for private households - 100% data':
            float_df['Median Income 2015'] = incomeList
            calculated_df = float_df[['Neighbourhood','Median Income 2015']] 
        
     
        calculated_df.columns = [col.strip() for col in calculated_df.columns]
  

        return(calculated_df)
        

        
    def ReadShapeData(self):
        shapeFile = '/Users/Juanp/Desktop/PythonProjects/DataVisualization/TorontoData/Neighbourhoods/Neighbourhoods.shp'
        shape_df = gpd.read_file(shapeFile)
        
        shape_df['Neighbourhood'] = shape_df['FIELD_7'].str.replace(r"\(.*\)","") 
        shape_df['Neighbourhood'] = shape_df['Neighbourhood'].str.strip()
       
    
        return(shape_df)
        
    
    def SendToShapeFile(self, shape_df, incomeList):
        i=0
        for income in incomeList:
           if i==0:
              temp1 = self.Merge(shape_df, income)
           if i==1:
              temp2 = self.Merge(temp1, income)
           if i==2:
              merged_shapeFile = self.Merge(temp2, income)
           i=i+1
          
        return(merged_shapeFile)
       
  

    def Merge(self,shape_df, income):
        merged_left = pd.merge(left=shape_df, right=income, how='left', 
                               left_on='Neighbourhood', right_on='Neighbourhood')
        merged_left.fillna(0)
        return(merged_left)
        
       
    
    def CreateShapeFile(self, mergedFinal):
        mergedFinal.columns = [col.strip() for col in mergedFinal.columns]
        
        
        gdf = gpd.GeoDataFrame(mergedFinal, geometry='geometry')
        gdf.to_file('TorontoIncomeData.shp', driver='ESRI Shapefile')
        
        
    def Printall(self, mergedPrint): 
        new = mergedPrint['Median Income 2000'].unique().toList()
        
        
        print("year 2000: " + str(mergedPrint['Median Income 2000'].unique()))
        print("year 2005: " + str(mergedPrint['Median Income 2005'].unique()))
        print("year 2010: " + str(mergedPrint['Median Income 2010'].unique()))
        print("year 2015: " + str(mergedPrint['Median Income 2015'].unique()))
        
        

       
def main():
    sns.set(style="darkgrid") 
    obj = TorontoData() #instantiate class
    
    
    dfList, neighbourhoodCol = obj.OrgainzeOldData()
    #This method calls the CalculateMedianIncome function inside it. Returns a list of dataframes
    incomeList = obj.ListToDataFrame(dfList, neighbourhoodCol)
    shape_df = obj.ReadShapeData()
    mergedShapeFile = obj.SendToShapeFile(shape_df, incomeList)

    dfNew, neighbourhoodCol = obj.Organize2016Data()
    incomeNew =  obj.CalculateMedianIncome(dfNew, neighbourhoodCol)
    
    
    mergedFinal = obj.Merge(mergedShapeFile, incomeNew)
    
    mergedPrint = obj.CreateShapeFile(mergedFinal)
    
    #obj.Printall(mergedFinal)
    #obj
    

main()









