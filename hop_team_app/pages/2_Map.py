import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import utils


st.set_page_config(layout="wide")

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
        final_data = referral_data[(referral_data['hospital_community'].isin(filtered_data['hospital_community'].unique())) & (referral_data['provider_community'].isin(filtered_data['hospital_community'].unique()))]
    else:
        final_data = referral_data[(referral_data['hospital_community'] == selected_community) & (referral_data['provider_community'] == selected_community)]

    # defining ranks
    if selected_org == 'All Hospitals' or selected_community == 'All Communities':
        num_spec_rank = num_pcp_rank = num_ref_rank = '-'
    else:
        pcp_rank = referral_data.groupby('provider_community')['provider_npi'].nunique().sort_values(ascending=False).reset_index()
        pcp_rank['Rank'] = pcp_rank['provider_npi'].rank(method='dense',ascending=False).astype(int)
        num_pcp_rank = pcp_rank.loc[pcp_rank['provider_community'] == selected_community]['Rank'].item()

        spec_rank = referral_data.groupby('provider_community')['specialization_cleaned'].nunique().sort_values(ascending=False).reset_index()
        spec_rank['Rank'] = spec_rank['specialization_cleaned'].rank(method='dense',ascending=False).astype(int)
        num_spec_rank = spec_rank.loc[spec_rank['provider_community'] == selected_community]['Rank'].item()

        ref_rank = referral_data.groupby('provider_community')['transaction_count'].sum().sort_values(ascending=False).reset_index()
        ref_rank['Rank'] = ref_rank['transaction_count'].rank(method='dense',ascending=False).astype(int)
        num_ref_rank = ref_rank.loc[ref_rank['provider_community'] == selected_community]['Rank'].item()
    
    total_hospitals = final_data['org_address'].nunique()
    
    st.write(f"Total hospitals: {total_hospitals}")

    total_transactions = final_data['transaction_count'].sum()

    st.metric(
    label=f"Total Referrals Rank", 
    value=num_ref_rank,
    delta=f"{"{:,}".format(total_transactions)} Total Referrals",
    delta_arrow="off"
    )

    total_providers = final_data['provider_npi'].nunique()

    st.metric(
    label=f"Total Providers Rank", 
    value=num_pcp_rank,
    delta=f"{"{:,}".format(total_providers)} Total Providers",
    delta_arrow="off"
    )

    total_specializations = final_data['specialization_cleaned'].nunique()

    st.metric(
    label=f"Total Specializations Rank", 
    value=num_spec_rank,
    delta=f"{total_specializations} Total Specializations",
    delta_arrow="off"
    )

# group the selected community by hospital and calculate total transaction count
map_df = final_data.groupby(['organization_name','owning_entity','latitude','longitude','color']).agg({'transaction_count':'sum'}).reset_index()
# add commas to transaction count numbers
map_df['transaction_count'] = map_df['transaction_count'].apply(lambda x: "{:,}".format(x))

m = folium.Map(location=[map_df['latitude'].mean(), map_df['longitude'].mean()], zoom_start=8)
for _, row in map_df.iterrows():
    iframe = folium.IFrame('<b>Hospital: </b>' + row['organization_name'] + '<br>' + '<b>Part of: </b>' + row['owning_entity'] + '<br>' + '<b>Total Referrals: </b>' + str(row['transaction_count']))
    popup = folium.Popup(iframe, min_width=300, max_width=400, min_height=100, max_height=100)
    folium.Marker(location=[row['latitude'], row['longitude']], icon=folium.Icon(color=row['color'], icon='map-marker'), popup=popup).add_to(m)

st_folium(m, width=900, height=500)

if selected_org != 'All Hospitals' and selected_community != 'All Communities':
    st.write("Hospitals:")
    hosp = final_data[['organization_name','org_address']].drop_duplicates(subset=['organization_name','org_address']).rename(columns={'organization_name':'Hospital Name', 'org_address':'Address'})
    st.dataframe(hosp, use_container_width=True, hide_index=True)

vandy_top_3 = referral_data[(referral_data['hospital_community']==1359) & (referral_data['provider_community']==1359)].groupby('specialization_cleaned')['transaction_count'].sum().sort_values(ascending=False)[0:3].index.to_list()

# Checks if a specialization is in Vandy's top 3 specializations and highlights it in yellow if so
def highlight_growth_areas(value):
    if value in vandy_top_3:
        return 'background-color: yellow' 
    else:
        return '' 

st.write("Top specializations:")

top_spec = final_data.groupby('specialization_cleaned')['transaction_count'].sum().sort_values(ascending=False).head(5).reset_index().rename(columns={'specialization_cleaned':'Specialization','transaction_count':'Total Referrals'})
top_spec['Total Referrals'] = top_spec['Total Referrals'].apply(lambda x: "{:,}".format(x))

st.dataframe(top_spec.style.map(highlight_growth_areas, subset=(top_spec.index[-2:], 'Specialization')), use_container_width=True, hide_index=True)

st.caption("A specialization is highlighted in yellow if it is one of Vanderbilt's strongest specializations (in terms of referral count) and is ranked #4 or #5 in the selected community. These could represent possible areas of growth for Vanderbilt's referral network.")