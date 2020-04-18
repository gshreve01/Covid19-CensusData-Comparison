# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 20:00:09 2020

@author: gshre
"""


import zillow
import pprint

if __name__=="__main__":
    key = ""
    with open("./zillow_key.conf", 'r') as f:
        key = f.readline().replace("\n", "")
    print(key)

    address = "3400 Pacific Ave., Marina Del Rey, CA"
    postal_code = "90292"

    api = zillow.ValuationApi()
    data = api.GetSearchResults(key, address, postal_code)

    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(data.get_dict())

    detail_data = api.GetZEstimate(key, data.zpid)

    comp_data = api.GetComps(key, data.zpid)

    pp.pprint(comp_data['comps'][1].get_dict())

    deep_results = api.GetDeepSearchResults(key, "1920 1st Street South Apt 407, Minneapolis, MN", "55454")
    pp.pprint(deep_results.get_dict())
    
    http://www.zillow.com/webservice/GetSearchResults.htm?zws-id=X1-ZWz179yot8r9jf_282ek&address=2114+Bigelow+Ave&citystatezip=Seattle%2C+WA
    