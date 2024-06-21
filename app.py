from flask import Flask, render_template, request
from utils import gecodingapi,google_api,google_api_primary,map_generate
import pandas as pd

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    map_html = None
    data_list = None
    if request.method == 'POST':
        # Get user input
        address = request.form.get('address')
        radius = request.form.get('radius') 
        # Generate the map
        url='https://places.googleapis.com/v1/places:searchNearby'
        field= 'places.displayName,places.formattedAddress,places.types,places.primaryTypeDisplayName,places.websiteUri,places.location,places.googleMapsUri,places.primaryType,places.photos'
        if radius is not None and address is not None:
            latitudes,longitudes=gecodingapi(address)
            df_shop=google_api_primary(url=url,maxcount=5,search_type=["supermarket","shopping_mall","market","liquor_store","jewelry_store","home_improvement_store","home_goods_store","grocery_store","furniture_store","gift_shop","hardware_store","clothing_store","convenience_store"],search_type_name="SHOPPING & RETAIL",exclude_type=["child_care_agency"],lat=float(latitudes),lon=float(longitudes),radius=float(radius),field=field)
            df_res=google_api(url=url,maxcount=5,search_type="restaurant",search_type_name="CAFES & RESTAURANTS",exclude_type=[],lat=float(latitudes),lon=float(longitudes),radius=float(radius),field=field)
            df_edu=google_api(url=url,maxcount=5,search_type="school",search_type_name="EDUCATION",exclude_type=["fitness_center"],lat=float(latitudes),lon=float(longitudes),radius=float(radius),field=field)
            df_lr=google_api(url=url,maxcount=5,search_type=["amusement_center", "amusement_park", "aquarium", "banquet_hall", "bowling_alley", "casino", "community_center", "convention_center", "cultural_center", "dog_park", "hiking_area", "historical_landmark", "marina", "movie_rental", "movie_theater", "national_park", "park", "tourist_attraction", "visitor_center", "zoo"],search_type_name="LEISURE & RECREATION",exclude_type="",lat=float(latitudes),lon=float(longitudes),radius=float(radius),field=field)
            combined_df = pd.concat([df_shop, df_res,df_edu,df_lr], axis=0)
            combined_df.reset_index().drop("index", axis=1)
            map_html = map_generate(combined_df)
            data_list = combined_df.to_dict(orient='records')
    return render_template('index.html', map_html=map_html,data=data_list)

if __name__ == '__main__':
    app.run(debug=True)


