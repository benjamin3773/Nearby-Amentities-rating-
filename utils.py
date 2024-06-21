import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import plotly.io as pio
import requests
import googlemaps



# This function returns latitude and longitude for an input address
def gecodingapi(address):
    Google_key='' # Put your google api key here
    gmaps = googlemaps.Client(key=Google_key)
    # Geocoding an address
    geocode_result = gmaps.geocode(address)
    latitude = geocode_result[0]['geometry']['location']['lat']
    longitude = geocode_result[0]['geometry']['location']['lng']
    return latitude,longitude

# This function calls the Google API and returns dataframe based on your input fields
def google_api(url,search_type,search_type_name,maxcount,exclude_type,lat,lon,radius,field):
    # Define the API endpoint
    url = url
    # Define the payload
    Google_key='' # Put your google api key here
    if not exclude_type:
        payload = {
            "includedTypes": search_type, # List of types can be found at Table A, B
            "maxResultCount": maxcount, # Number of results returns(max: 20)
            "locationRestriction": {
                "circle": {
                    "center": {
                        "latitude": lat, # Latitude
                        "longitude": lon # Longitude
                    },
                    "radius": radius # Radius of circle in metre
                }
            }
        }
    else:
        payload = {
            "includedTypes": search_type, # List of types can be found at Table A, B
            "maxResultCount": maxcount, # Number of results returns(max: 20)
            "excludedTypes": exclude_type, # List of types that exluded in the result
            "locationRestriction": {
                "circle": {
                    "center": {
                        "latitude": lat, # Latitude
                        "longitude": lon # Longitude
                    },
                    "radius": radius # Radius of circle in metre
                }
            }
        }

    # Define the headers
    headers = {
        'Content-Type': 'application/json',
        'X-Goog-Api-Key': Google_key,
        'X-Goog-FieldMask': field # Address informations
    }

    # Make the POST request
    response = requests.post(url, json=payload, headers=headers)
    places = response.json()['places']
    # Create a DataFrame
    df_search= pd.DataFrame([{
        'Searched': search_type_name,
        'Name': place.get('displayName', {}).get('text', 'N/A'),
        'Address': place['formattedAddress'],
        'Website': place.get('websiteUri', 'N/A'),
        'Google Maps': place.get('googleMapsUri', 'N/A'),
        'Types': ', '.join(place['types']),
        'Latitude': place.get('location', {}).get('latitude', 'N/A'),
        'Longitude': place.get('location', {}).get('longitude', 'N/A'),
        'Primary Type': place.get('primaryTypeDisplayName', {}).get('text', 'N/A'),
        'Photos': 'https://places.googleapis.com/v1/'+place.get('photos')[0].get('name', 'N/A')+'/media?key='+Google_key+'&maxHeightPx=600'
    } if place.get('photos') is not None else {'Searched': search_type_name,
        'Name': place.get('displayName', {}).get('text', 'N/A'),
        'Address': place['formattedAddress'],
        'Website': place.get('websiteUri', 'N/A'),
        'Google Maps': place.get('googleMapsUri', 'N/A'),
        'Types': ', '.join(place['types']),
        'Latitude': place.get('location', {}).get('latitude', 'N/A'),
        'Longitude': place.get('location', {}).get('longitude', 'N/A'),
        'Primary Type': place.get('primaryTypeDisplayName', {}).get('text', 'N/A'),
        'Photos': None}
    for place in places])
    return df_search

def google_api_primary(url,search_type,search_type_name,maxcount,exclude_type,lat,lon,radius,field):
    # Define the API endpoint
    url = url
    # Define the payload
    Google_key='' # Put your google api key here
    if not exclude_type:
        payload = {
            "includedPrimaryTypes": search_type,
            "maxResultCount": maxcount,
            "locationRestriction": {
                "circle": {
                    "center": {
                        "latitude": lat,
                        "longitude": lon
                    },
                    "radius": radius
                }
            }
        }
    else:
        payload = {
            "includedPrimaryTypes": search_type,
            "maxResultCount": maxcount,
            "excludedTypes": exclude_type,
            "locationRestriction": {
                "circle": {
                    "center": {
                        "latitude": lat,
                        "longitude": lon
                    },
                    "radius": radius
                }
            }
        }

    # Define the headers
    headers = {
        'Content-Type': 'application/json',
        'X-Goog-Api-Key': Google_key, 
        'X-Goog-FieldMask': field
    }

    # Make the POST request
    response = requests.post(url, json=payload, headers=headers)
    # print(response.json())
    places = response.json()['places']
    
    # Create a DataFrame
    df_search= pd.DataFrame([{
        'Searched': search_type_name,
        'Name': place.get('displayName', {}).get('text', 'N/A'),
        'Address': place['formattedAddress'],
        'Website': place.get('websiteUri', 'N/A'),
        'Google Maps': place.get('googleMapsUri', 'N/A'),
        'Types': ', '.join(place['types']),
        'Latitude': place.get('location', {}).get('latitude', 'N/A'),
        'Longitude': place.get('location', {}).get('longitude', 'N/A'),
        'Primary Type': place.get('primaryTypeDisplayName', {}).get('text', 'N/A'),
        'Photos': 'https://places.googleapis.com/v1/'+place.get('photos')[0].get('name', 'N/A')+'/media?key='+Google_key+'&maxHeightPx=600'
    } if place.get('photos') is not None else {'Searched': search_type_name,
        'Name': place.get('displayName', {}).get('text', 'N/A'),
        'Address': place['formattedAddress'],
        'Website': place.get('websiteUri', 'N/A'),
        'Google Maps': place.get('googleMapsUri', 'N/A'),
        'Types': ', '.join(place['types']),
        'Latitude': place.get('location', {}).get('latitude', 'N/A'),
        'Longitude': place.get('location', {}).get('longitude', 'N/A'),
        'Primary Type': place.get('primaryTypeDisplayName', {}).get('text', 'N/A'),
        'Photos': None}
    for place in places])
    return df_search

def map_generate(combined_df):
    # Define colors for categories
    colors = {
        "LEISURE & RECREATION": "blue",
        "EDUCATION": "green",
        "CAFES & RESTAURANTS": "orange",
        "SHOPPING & RETAIL": "brown"
    }

    # Create a map with custom styling
    fig = px.scatter_mapbox(combined_df, lat="Latitude", lon="Longitude", hover_name="Name", 
                            color="Searched", size_max=15, zoom=13, height=600, width=800,
                            color_discrete_map=colors)

    fig.update_layout(mapbox_style="carto-positron", showlegend=False)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    annotations = []
    y_start = 0.02  # Starting y position for the bottom-left corner
    y_step = 0.3   # Step to place annotations closely

    for category, color in colors.items():
        names = combined_df[combined_df['Searched'] == category]['Name'].tolist()
        text = f"<b>{category}</b><br>" + "<br>".join([f"• {name}" for name in names])
        annotations.append(
            go.layout.Annotation(
                text=text,
                showarrow=False,
                align="left",
                xref="paper",
                yref="paper",
                x=0.01,  # Position on the left side of the map
                y=y_start,
                bordercolor=color,
                borderwidth=3,
                borderpad=4,
                bgcolor="white",
                font=dict(color="black")
            )
        )
        y_start += y_step  # Adjust this value to add spacing between legend items

    fig.update_layout(annotations=annotations)
    return pio.to_html(fig, full_html=False)





