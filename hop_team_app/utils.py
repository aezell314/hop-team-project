import streamlit as st
import pandas as pd


# Load data
@st.cache_data
def load_data(path:str):
    data = pd.read_csv(path)
    return data

hop_team_nashville_df = load_data('data/hop_team_nashville.csv')

#-------------------------------------------------

community_detection_df = (
    hop_team_nashville_df[['providername', 'transaction_count', 'owning_entity']]
        .sort_values(by='transaction_count', ascending=False)
        .rename(columns={
            'providername': 'Referring PCP',
            'transaction_count': 'Number of Referrals',
            'owning_entity': 'Receiving Hospital'
        })
)

#-------------------------------------------------

# Get list of Nashville PCP Specialties
pcp_specialization_list = (
    hop_team_nashville_df['specialization']
        .fillna('None')
        .unique()
        .tolist()
)
pcp_specialization_list.insert(0, 'Any')

# Get list of Nashville Hospitals
hospital_list = (
    hop_team_nashville_df['owning_entity']
    .unique()
    .tolist()
)
hospital_list.insert(0, 'All')
