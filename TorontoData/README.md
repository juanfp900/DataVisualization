# Visualize Median Income by Toronto Neighbourhood with Tableau

[Link to Tableau Project!](https://public.tableau.com/profile/juanp5926#!/vizhome/TorontoIncomeByNeighbourhood/Sheet8?publish=yes)

# Project Description

This project was created by parsing through a csv file and an xlsx file that contains census data from 140 Toronto Neighbourhoods.
The csv file contains 2015 data while the xlsx file contains 2000, 2005, 2010 data. 

# How To Run?

Some of the libaries used within project include, Pandas, GeoPandas, Seaborn, NumPy. A full list of libraries will be included in the 
requirements.txt file. To install these packages simply type the following commad in your respective directory. 
  
   **pip install -r requirements.txt**

To run this project you will need to download the files within the TorontoData folder:
  - TorontoData.py
  - neighbourhood-profiles-2016.csv
  - neighbourhood-data-2001-2011.xlsx
  - Neighbourhoods.zip
  - You will also need access to Tableau Public as this project is best displayed in Tableau. (It is free)
    [link to Tabelau Public](https://public.tableau.com/en-us/s/)
    
When you run the file "TorontoData.py". It should create a shape file called "TorontoIncomeData.shp" that you can then use to create a view using Tableau. To do this.
   - Go to the blue menu on the left side of the start page. You should see "Connect" as the title to this menu.
   - Click "Spatial File" under the Connect section of the menu. 
   - Here you will be able to import the shape file that was just created
   - Now your data is in Tableau.
  
Note: It is also possible to display the map using the MatplotLib Python libray instead of Tableau but it will not show as well. 
I included the code for this if needed. It will be commented out in the python file. 
  

  
  
