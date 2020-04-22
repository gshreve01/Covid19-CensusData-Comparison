# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 18:12:02 2020

Methods dealing with census library

@author: gshre
"""

from census import Census
from config import (census_key, gkey)
from unc_zipcode_lib import get_state_zips
import pandas as pd



def divide_chunks(l, n): 
    '''
    Divides list of strings into list of lists 

    Parameters
    ----------
    l : TYPE: list
        DESCRIPTION. string series
    n : TYPE: int
        DESCRIPTION. number of items in each chunk

    Yields
    ------
    TYPE: List
        DESCRIPTION. a list of lists of strings

    '''
     
    # looping till length l 
    for i in range(0, len(l), n):  
        yield l[i:i + n] 

# Census API Key
c = Census(census_key)
#print(census_key)

def Load_Census_Data():
    # Load the zip codes
    state_zip_codes = get_state_zips("NC")
   
    # There is a limit to the number of zip codes that can be passed at
    # one time
    list_of_state_code_lists = list(divide_chunks(state_zip_codes["Zip Codes"]
                                                  , 40))
    
    print(list_of_state_code_lists) 
    
    
    #TODO: This should be moved to the config file
    census_tables = {"Population" : "B01003_001E",
                     "Per Capita Income": "B06011_001E",
                     "Median Household Income": "B19013_001E",
                     "Household Owner": "B07013_002E"}
    
    
    # convert to list of list of zip codes
    data_tables=list(census_tables.values())
    #print(data_tables)
    
    # create an empty census_data
    census_data = []
    
    # for each zip code list
    for state_zips in list_of_state_code_lists:
        # convert state zips to string
        zip_code_list = [str(i) for i in state_zips]
        # print(zip_code_list)
        zip_codes = ','.join(zip_code_list)
        print(f"Pulling data for zip codes: {zip_codes}")
        if len(census_data) > 0:
            new_census_data = pd.DataFrame(c.acs5.get((data_tables),
                                  {'for': f'zip code tabulation area:{zip_codes}'}))
            census_data = pd.concat([census_data, new_census_data], sort = False)
        else:
            census_data = pd.DataFrame(c.acs5.get((data_tables),
                                  {'for': f'zip code tabulation area:{zip_codes}'}))
        #print(len(census_data))
        
    # rename the census tables to desired column names
    for key in census_tables:
        census_data.rename(columns = {census_tables[key]: key}, inplace=True)
    census_data.rename(columns = {"zip code tabulation area": "Zip Codes"})
    
    # save to file
    census_data.to_csv("Resources/census_data.csv", index=False)
    print(census_data.head())
    
Load_Census_Data()
    
    
