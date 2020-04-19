# -*- coding: utf-8 -*-
"""
Created on Sat Apr 18 15:54:41 2020

@author: gshre
"""

import requests
import numpy as np
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
       'topleft' : { 'x': xmin, 'y' : ymax },
       'topright' : { 'x' : xmax, 'y' : ymax },
       'bottomleft' : { 'x' : xmin, 'y' : ymin },
       'bottomright' : { 'x' : xmax, 'y' : ymin }}

def Quad_Box(box):
    quad_boxes = []
    # take half of the distance between the length and width of box
    half_width = (box["topleft"]["x"] - box["topright"]["x"]) / 2
    half_height = (box["topleft"]["y"] - box["bottomleft"]["y"]) / 2
    
    # define top left box
    quad_boxes.append({"topleft": {"x": box["topleft"]["x"],
                                   "y": box["topleft"]["y"]},
                       "topright": {"x": box["topleft"]["x"] + half_width,
                                    "y": box["topright"]["y"]},
                       "bottomleft": {"x": box["topleft"]["x"],
                                      "y": box["topleft"]["y"] + half_height},
                       "bottomright":{"x": box["topleft"]["x"] + half_width,
                                      "y": box["topright"]["y"] + half_height}                              
        })  
    
    # define top right box
    quad_boxes.append({"topleft": {"x": box["topleft"]["x"] + half_width + 0.000001,
                                   "y": box["topleft"]["y"]},
                       "topright": {"x": box["topright"]["x"] ,
                                    "y": box["topright"]["y"]},
                       "bottomleft": {"x": box["topleft"]["x"] + half_width + 0.000001,
                                      "y": box["topleft"]["y"] + half_height + 0.000001},
                       "bottomright":{"x": box["topright"]["x"],
                                      "y": box["topright"]["y"] + half_height + 0.000001}                              
        })

    
    # define bottom left box
    quad_boxes.append({"topleft": {"x": box["topleft"]["x"],
                                   "y": box["topleft"]["y"] + half_height + 0.000001},
                       "topright": {"x": box["topright"]["x"] + half_width + 0.000001 ,
                                    "y": box["topright"]["y"]+ half_height + 0.000001},
                       "bottomleft": {"x": box["bottomleft"]["x"],
                                      "y": box["bottomleft"]["y"]},
                       "bottomright":{"x": box["topright"]["x"]  + half_width + 0.000001,
                                      "y": box["bottomright"]["y"]}                              
        })
    
    # define bottom right box
    quad_boxes.append({"topleft": {"x": box["topleft"]["x"] + half_width + 0.000001,
                                   "y": box["topleft"]["y"] + half_height + 0.000001},
                       "topright": {"x": box["bottomright"]["x"],
                                    "y": box["topright"]["y"]+ half_height + 0.000001},
                       "bottomleft": {"x": box["bottomleft"]["x"] + half_width + 0.000001,
                                      "y": box["bottomleft"]["y"]},
                       "bottomright":{"x": box["bottomright"]["x"],
                                      "y": box["bottomright"]["y"]}                              
        })
    
    return quad_boxes
    

    
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

dist = Lat_Lng_Distance_From(36.0001, -80.0001, 36.1001, -80.0001)
print(dist)

charlotte_box = Bounding_Poligon_Into_Box(charlote_boundary_polygon.exterior.coords.xy)
print(charlotte_box)

quad_boxes = Quad_Box(charlotte_box)
print(len(quad_boxes))
print(quad_boxes)


 
 
	