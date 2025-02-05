import streamlit as st
import requests
from requests.structures import CaseInsensitiveDict
import numpy as np
import pandas as pd
import pyvista as pv
from stpyvista import stpyvista
import math
from func_costing import *
from func_design_config import *
from func_design_output import *

st.set_page_config(page_title="CRC#53 Demo App", page_icon=":earth_americas:", layout="wide")
Geoapify_API_KEY = '76a57c51582c4fa08e0d406924508349'

def Geoapify_geocoding(place):
    # Prompt user for the address
    address = str(place)

    # Replace spaces with '%20' for URL encoding (or use urllib.parse.quote)
    encoded_address = address.replace(" ", "%20")

    # Construct the API URL with the user-provided address
    url = f"https://api.geoapify.com/v1/geocode/search?text={encoded_address}&apiKey={Geoapify_API_KEY}"

    # Prepare headers
    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"

    # Optional: Add the address in a custom header if needed
    headers["User-Address"] = address  # Custom header example

    # Send GET request
    resp = requests.get(url, headers=headers)

    # Check the response status and handle accordingly
    if resp.status_code == 200:
        # print("Request was successful!")
        # # Print or process the response JSON
        # print(resp.json())
        return resp.json()
    else:
        return None
        # print(f"Request failed with status code: {resp.status_code}")
        # print(resp.text)

def get_location(place):
    response = Geoapify_geocoding(place)
    if response:
        return response['features'][0]['geometry']['coordinates'][0], response['features'][0]['geometry']['coordinates'][1]
    else:
        return None


def create_building(num_floors, width, length, color):
    plotter = pv.Plotter()
    floor_height = 3  # height of each floor in meters
    
    for i in range(num_floors):
        z = i * floor_height  # Set the height of each floor
        box = pv.Box(bounds=(0, width, 0, length, z, z + floor_height))
        plotter.add_mesh(box, color=color, opacity=0.8, show_edges=True)
    
    plotter.view_isometric()
    plotter.zoom_camera(0.5)
    return plotter


def costing(**kwargs):
    pass


def building_design(**kwargs):
    pass

def APS_API(**kwargs):
    pass

def Dynamo_connector(**kwargs):
    pass




# """
# ========================================================================
# MAIN PROGRAM
# ========================================================================
# """


# """
# ------------------------------------------------------------------------
# SIDE BAR SECTION
# ------------------------------------------------------------------------
# """

st.sidebar.title("User parameters")




address = st.sidebar.text_input("Enter the address", value ="Melbourne")

# Input fields
num_floors = st.sidebar.slider("Number of Floors", min_value=1, max_value=50, value=10)
width = st.sidebar.slider("Width (meters)", min_value=5.0, max_value=100.0, value=20.0)
length = st.sidebar.slider("Length (meters)", min_value=5.0, max_value=100.0, value=20.0)


# """
# ------------------------------------------------------------------------
# MAIN APP SECTION
# ------------------------------------------------------------------------
# """
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs(["Dashboard","Site location", "Building parameters", "Functional typology", "Interior typology", "Exterior typology", "Fire/acoustic", "MEP"])

with tab2:

    long, lat = get_location(address)
    # Custom Latitude & Longitude data
    map_data = {
        "lat": [lat],   # Example: Melbourne latitude
        "lon": [long]    # Example: Melbourne longitude
    }

    col1, col2 = st.columns(2)
    with col1:
        mapON = st.checkbox('Display Map')
        if mapON:
            # Display Map
            st.map(map_data)

maxcost = math.floor(500000*(num_floors/5 + width/10))
avgcost = math.floor(250000*(num_floors/5 + length/10))
mincost = math.floor(100000*(num_floors/5+ width*length/100))

    
with tab1:
    col1, col2 = st.columns([1,2])

    with col1:
        scol1, scol2, scol3 = st.columns(3)
        variant = st.selectbox('Select the variant from below', ['Variant 1', 'Variant 2', 'Variant 3'])
        with scol1:    
            if variant == 'Variant 1':
                st.metric(label = 'Production Cost', value = math.floor(maxcost/3), delta = math.floor((maxcost - avgcost)/3))
            elif variant == 'Variant 2':
                st.metric(label = 'Production Cost', value = math.floor(avgcost/3), delta = math.floor((avgcost - mincost)/3))
            elif variant == 'Variant 3':
                st.metric(label = 'Production Cost', value = math.floor(mincost/3), delta = math.floor((mincost - 200000)/3))

        with scol2:
            if variant == 'Variant 1':
                st.metric(label = 'Design Cost', value = math.floor(maxcost/3), delta = math.floor((maxcost - avgcost)/3))
            elif variant == 'Variant 2':
                st.metric(label = 'Design Cost', value = math.floor(avgcost/3), delta = math.floor((avgcost - mincost)/3))
            elif variant == 'Variant 3':
                st.metric(label = 'Design Cost', value = math.floor(mincost/3), delta = math.floor((mincost - 200000)/3))


        with scol3:
            if variant == 'Variant 1':
                st.metric(label = 'On site Cost', value = math.floor(maxcost/3), delta = math.floor((maxcost - avgcost)/3))
            elif variant == 'Variant 2':
                st.metric(label = 'On site  Cost', value = math.floor(avgcost/3), delta =  math.floor((avgcost - mincost)/3))
            elif variant == 'Variant 3':
                st.metric(label = 'On site  Cost', value = math.floor(mincost/3), delta =  math.floor((mincost - 200000)/3))

    with col2:
        if variant == 'Variant 1':
            # Generate 3D model
            plotter = create_building(num_floors*2, width/2, length, 'lightblue')
            stpyvista(plotter)
        elif variant == 'Variant 2':
            # Generate 3D model
            plotter = create_building(num_floors, width, length, 'lightgreen')
            stpyvista(plotter)
        elif variant == 'Variant 3':
            # Generate 3D model
            plotter = create_building(num_floors+1, width*2, length/2, 'lightgray')
            stpyvista(plotter)



        

        

    

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button('Save'):
            st.write("Save button clicked")
        if st.button('Load'):
            st.write("Load button clicked")
        if st.button('Close'):
            st.write("Close button clicked")

    with col2:
        st.button('Export to PDF')
        st.button('Export to Revit')
   

