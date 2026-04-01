import streamlit as st
import pandas as pd


# Load data
@st.cache_data
def load_data(path:str):
    return pd.read_csv(path)

hop_team_nashville_df = load_data('data/hop_team_nashville.csv')

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

#-------------------------------------------------

# CREATE DATAFRAME FOR HEATMAP: HOSPITAL REFERRALS VS PCP SPECIALIZATION

# Get top 10 hospitals by referral count
top_10_referred_hospitals = (
    hop_team_nashville_df
        .groupby('organization_name')
        .agg(
            referrals=('transaction_count', 'sum')
        )
        .sort_values('referrals', ascending=False)
        .head(10)
        .index
        .to_list()
)

# Get top 10 pcp specialties by referral count
top_10_referring_specializations = (
    hop_team_nashville_df
        .groupby('specialization')
        .agg(
            referrals=('transaction_count', 'sum')
        )
        .sort_values('referrals', ascending=False)
        .head(10)
        .index
        .to_list()
)

# Pivot the specialties wider
top_10_referral_df = pd.pivot_table(
    data=(
        hop_team_nashville_df.loc[
            (hop_team_nashville_df['organization_name'].isin(top_10_referred_hospitals)) &
            (hop_team_nashville_df['specialization'].isin(top_10_referring_specializations)),
            ['organization_name', 'specialization', 'transaction_count']
        ]
    ),
    values='transaction_count',
    index='organization_name', 
    columns='specialization', 
    aggfunc='sum'
).fillna(0)

#-------------------------------------------------