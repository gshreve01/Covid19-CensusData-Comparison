# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 18:12:59 2020

Functions dealing with zip code api

@author: gshre
"""

# Dependencies
import requests
import pandas as pd
import os.path
from config import zipcode_url


def get_state_zips_api(state_code):
    '''
    Returns zip codes data frame for a state using API

    Parameters
    ----------
    state_code : TYPE: string
        DESCRIPTION. State Code abbreviation; ex: NC

    Returns
    -------
    TYPE: DataFrame
        DESCRIPTION. Zip Codes data frame

    '''
    url=zipcode_url.replace("{state_code}", state_code)
    response = requests.get(url)
    zip_code_data = response.json()
    return pd.DataFrame(zip_code_data)


def get_state_zips(state_code):
    '''
    Returns zip coes data frame for a state using csv if available
    otherwise it calls API

    Parameters
    ----------
    state_code : TYPE: string
        DESCRIPTION. State Code abbreviation; ex: NC

    Returns
    -------
    df : TYPE: DataFrame
        DESCRIPTION. Zip Codes data frame

    '''
    csv_filename = f"Resources/{state_code}_ZipCodes.csv"
    # try to open file...if it does not exist, then create it
    df = ''
    try:
        df = pd.read_csv(csv_filename)
    except: 
        print("Loading zip codes with API")
        df = get_state_zips_api(state_code)
        df.rename(columns = {"zip_codes" : "Zip Codes"}, inplace=True)
        df.to_csv(csv_filename, index=False)
    return df

