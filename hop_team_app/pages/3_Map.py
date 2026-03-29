import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import utils

st.header("Referral Community Geolocator")

referral_data = utils.hop_team_nashville_df

with st.sidebar:
    # Create hospital dropdown
    selected_org = st.selectbox("Select a Hospital", sorted(referral_data['owning_entity'].unique()) )
    
    # Get the list of community IDs associated with that hospital 
    communities = referral_data[referral_data['owning_entity'] == selected_org]['hospital_community'].unique()
    
    #Create dependent dropdown for community selection 
    selected_community = st.selectbox(
        f'Select a Referral Community for {selected_org}',
        communities
    )
    
    st.write(f"You selected commmunity #{selected_community} for {selected_org}.")

filtered_df = referral_data[referral_data['hospital_community'] == selected_community].groupby(['organization_name','owning_entity','latitude','longitude','color']).agg({'transaction_count':'sum'}).reset_index()
filtered_df['transaction_count'] = filtered_df['transaction_count'].apply(lambda x: "{:,}".format(x))

m = folium.Map(location=[filtered_df['latitude'].mean(), filtered_df['longitude'].mean()], zoom_start=8)
for _, row in filtered_df.iterrows():
    iframe = folium.IFrame('<b>Hospital: </b>' + row['organization_name'] + '<br>' + '<b>Part of: </b>' + row['owning_entity'] + '<br>' + '<b>Total Referrals: </b>' + str(row['transaction_count']))
    popup = folium.Popup(iframe, min_width=300, max_width=400, min_height=100, max_height=100)
    folium.Marker(location=[row['latitude'], row['longitude']], icon=folium.Icon(color=row['color'], icon='map-marker'), popup=popup).add_to(m)

st_folium(m, width=1000, height=600)

