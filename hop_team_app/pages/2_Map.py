import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import utils

st.header("Referral Community Geolocator")

referral_data = utils.hop_team_nashville_df

with st.sidebar:
    # Create hospital dropdown
    hospital_list = ['All Hospitals'] + sorted(referral_data['owning_entity'].unique())
    selected_org = st.selectbox(
        'Select a Hospital',
        options=hospital_list
    )
    
    # Get the list of community IDs associated with that hospital
    if selected_org == 'All Hospitals':
        filtered_data = referral_data
    else:
        filtered_data = referral_data[referral_data['owning_entity'] == selected_org]
        
    #Create dependent dropdown for community selection 
    community_list = ['All Communities'] + sorted(filtered_data['hospital_community'].unique())
    selected_community = st.selectbox(
        f'Select a Referral Community for {selected_org}',
        options=community_list
    )
    
    if selected_community == 'All Communities':
        final_data = referral_data[referral_data['hospital_community'].isin(filtered_data['hospital_community'].unique())]
    else:
        final_data = referral_data[referral_data['hospital_community'] == selected_community]

    total_hospitals = final_data['org_address'].nunique()
    st.write(f"Total hospitals: {total_hospitals}")
    total_providers = final_data['provider_npi'].nunique()
    st.write(f"Total providers: {total_providers}")
    total_transactions = final_data['transaction_count'].sum()
    st.write(f"Total referrals: {"{:,}".format(total_transactions)}")


# group the selected community by hospital and calculate total transaction count
map_df = final_data.groupby(['organization_name','owning_entity','latitude','longitude','color']).agg({'transaction_count':'sum'}).reset_index()
# add commas to transaction count numbers
map_df['transaction_count'] = map_df['transaction_count'].apply(lambda x: "{:,}".format(x))

m = folium.Map(location=[map_df['latitude'].mean(), map_df['longitude'].mean()], zoom_start=8)
for _, row in map_df.iterrows():
    iframe = folium.IFrame('<b>Hospital: </b>' + row['organization_name'] + '<br>' + '<b>Part of: </b>' + row['owning_entity'] + '<br>' + '<b>Total Referrals: </b>' + str(row['transaction_count']))
    popup = folium.Popup(iframe, min_width=300, max_width=400, min_height=100, max_height=100)
    folium.Marker(location=[row['latitude'], row['longitude']], icon=folium.Icon(color=row['color'], icon='map-marker'), popup=popup).add_to(m)

st_folium(m, width=1000, height=600)

st.write("Top specializations:")
top_spec = final_data.groupby('specialization_cleaned')['transaction_count'].sum().sort_values(ascending=False).head(5).reset_index().rename(columns={'specialization_cleaned':'Specialization','transaction_count':'Total Referrals'})
top_spec['Total Referrals'] = top_spec['Total Referrals'].apply(lambda x: "{:,}".format(x))

st.dataframe(top_spec, use_container_width=True, hide_index=True)

