# -*- coding: utf-8 -*-
"""
Created on Sat Apr 18 15:54:41 2020

@author: gshre
"""

import requests
import numpy as np
import pandas as pd
from math import radians, sin, cos, acos, atan2, sqrt
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

from pprint import pprint

# Based on google search
#https://stackoverflow.com/questions/837872/calculate-distance-in-meters-when-you-know-longitude-and-latitude-in-java
def Lat_Lng_Distance_From(lat1, lng1, lat2, lng2):
    earthRadius = 6371000 # meters
    dLat = radians(lat2-lat1);
    dLng = radians(lng2-lng1);
    a = sin(dLat/2) * sin(dLat/2) + cos(radians(lat1)) * cos(radians(lat2)) * sin(dLng/2) * sin(dLng/2)
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    dist = (float) (earthRadius * c)

    return dist;
    

def Load_Charlotte_Boundaries():
    url = "https://nominatim.openstreetmap.org/search.php?q=Charlotte%20NC&polygon_geojson=1&format=json"
    response = requests.get(url).json()
    
    #pprint(response)
    return response

def Bounding_Poligon_Into_Box(points):
    xmin = min(points[1])
    xmax = max(points[1])
    ymin = min(points[0])
    ymax = max(points[0])
    
    return {
       'topleft' : { 'x': xmax, 'y' : ymax },
       'topright' : { 'x' : xmin, 'y' : ymax },
       'bottomleft' : { 'x' : xmax, 'y' : ymin },
       'bottomright' : { 'x' : xmin, 'y' : ymin }}

def Quad_Box(box):
    quad_boxes = []
    # take half of the distance between the length and width of box
    half_width = abs((box["topleft"]["x"] - box["topright"]["x"]) / 2)
    half_height = abs((box["topleft"]["y"] - box["bottomleft"]["y"]) / 2)
    
    print(half_width)
    print(half_height)
    
    # define top left box
    top_left_box = {"topleft": {"x": box["topleft"]["x"],
                                   "y": box["topleft"]["y"]},
                       "topright": {"x": box["topleft"]["x"] - half_width,
                                    "y": box["topright"]["y"]},
                       "bottomleft": {"x": box["topleft"]["x"],
                                      "y": box["topleft"]["y"] - half_height},
                       "bottomright":{"x": box["topleft"]["x"] - half_width,
                                      "y": box["topright"]["y"] - half_height}                              
        }
    
    # define top right box
    top_right_box = {"topleft": {"x":top_left_box["topright"]["x"] - 0.000001,
                                   "y": top_left_box["topleft"]["y"]},
                       "topright": {"x": box["topright"]["x"] ,
                                    "y": top_left_box["topright"]["y"]},
                       "bottomleft": {"x": top_left_box["bottomright"]["x"] - 0.000001,
                                      "y": top_left_box["bottomleft"]["y"]},
                       "bottomright":{"x": box["topright"]["x"],
                                      "y": top_left_box["bottomright"]["y"]}                              
        }

    
    # define bottom left box
    bottom_left_box = {"topleft": {"x": top_left_box["topleft"]["x"],
                                   "y": top_left_box["bottomleft"]["y"] - 0.000001},
                       "topright": {"x": top_left_box["topright"]["x"],
                                    "y": box["topright"]["y"]- half_height - 0.000001},
                       "bottomleft": {"x": top_left_box["bottomleft"]["x"],
                                      "y": box["bottomleft"]["y"]},
                       "bottomright":{"x": top_left_box["bottomright"]["x"],
                                      "y": box["bottomright"]["y"]}                              
        }
    
    # define bottom right box
    bottom_right_box = {"topleft": {"x": top_right_box["topleft"]["x"],
                                   "y": bottom_left_box["topleft"]["y"]},
                       "topright": {"x": top_right_box["topright"]["x"],
                                    "y": bottom_left_box["topright"]["y"]},
                       "bottomleft": {"x": top_right_box["bottomleft"]["x"],
                                      "y": box["bottomleft"]["y"]},
                       "bottomright":{"x": box["bottomright"]["x"],
                                      "y": box["bottomright"]["y"]}                              
        }
                        
    quad_boxes.append(top_left_box)
    quad_boxes.append(top_right_box)
    quad_boxes.append(bottom_left_box)
    quad_boxes.append(bottom_right_box)
    
    return quad_boxes
    
def Get_Radius_Of_Box(box):
    # determin radius based on center to topleft point
    half_width = abs((box["topleft"]["x"] - box["topright"]["x"]) / 2)
    half_height = abs((box["topleft"]["y"] - box["bottomleft"]["y"]) / 2)
    
    print(half_height)
    print(half_width)
    
    midpoint = {"x": box["topleft"]["x"] - half_width,
                "y": box["topleft"]["y"] - half_height}
    
    radius = Lat_Lng_Distance_From(box["topleft"]["y"], box["topleft"]["x"],
                                   midpoint["y"], midpoint["x"])
    
    return radius

    
    
def Is_Point_Within_Charlotte_Boundary(lat, lng):
    # define variable as global to prevent multiple loads of geo data
    global charlote_boundary_polygon
    if not 'charlote_boundary_polygon' in globals():
        print("Loading Geo Data boundaries for Charlotte")
        geo_data = Load_Charlotte_Boundaries()
        
        lng=[]
        lat=[]
        coordintates = geo_data[0]["geojson"]["coordinates"][0]
        for x in range(len(coordintates)):
            lng.append(coordintates[x][0])
            lat.append(coordintates[x][1])
        
        
        lons_lats_vect = np.column_stack((lat, lng)) # Reshape coordinates
        charlote_boundary_polygon = Polygon(lons_lats_vect) # create polyg        
    return charlote_boundary_polygon.contains(point)    


point = Point(35.227085,-80.843124) # Charlotte Center
print(Is_Point_Within_Charlotte_Boundary(35.227085, -80.043124)) # check if polygon contains point
print(Is_Point_Within_Charlotte_Boundary(35.227085, -80.043124)) # check if polygon contains point

print(type(charlote_boundary_polygon))


charlotte_box = Bounding_Poligon_Into_Box(charlote_boundary_polygon.exterior.coords.xy)
print(charlotte_box)
charlotte_box["radius"] = Get_Radius_Of_Box(charlotte_box)
print(f"charlotte radius: {charlotte_box['radius']}")

right_sized_boxes = []

box_stack = []

box_stack.append(charlotte_box)

while len(box_stack) > 0:
    box = box_stack.pop()
    
    boxes = Quad_Box(box)
    for box in boxes:
        box["radius"] = Get_Radius_Of_Box(box)
        print(box)
        if box["radius"] > 500:
            box_stack.append(box)
        else:
            right_sized_boxes.append(box)


    
charlotte_boxes_df = pd.DataFrame(right_sized_boxes)
charlotte_boxes_df.head()
charlotte_boxes_df.to_csv("Charlotte_Boxes_LngLat.csv")


 
 
	