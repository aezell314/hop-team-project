import plotly.express as px
import streamlit as st
import pandas as pd
import numpy as np
import utils

pcp_specialization_selectbox = st.sidebar.selectbox(
    label='PCP Specialization',
    options=utils.pcp_specialization_list
)

hospital_selectbox = st.sidebar.selectbox(
    label='Hospital',
    options=utils.hospital_list
)

hop = utils.hop_team_nashville_df

st.title('Analysis')

try:
    st.image('figures/specialization_hospital_referral_heatmap1.png')
except st.runtime.media_file_storage.MediaFileStorageError:
    st.image('../figures/specialization_hospital_referral_heatmap1.png')

pcp_patient_count = hop.groupby("classification")["patient_count"].sum().reset_index()

fig = px.bar(
    pcp_patient_count,                         
    x="classification",          
    y="patient_count"
)

fig.update_layout(
    xaxis_title="Provider Classification",
    yaxis_title="Total Referrals"
)

fig.update_traces(marker_color='#2d7a48')

st.plotly_chart(fig, use_container_width=True)  

st.title('Hospital Patient Share')

hop['organization_name'] = hop['organization_name'].str.replace(r'SAINT THOMAS.*', 'SAINT THOMAS', regex=True)
hop['organization_name'] = hop['organization_name'].str.replace(r'MAURY REGIONAL.*', 'MAURY REGIONAL', regex=True)
hop['organization_name'] = hop['organization_name'].str.replace(r'RIVERVIEW.*', 'RIVERVIEW', regex=True)
hop['organization_name'] = hop['organization_name'].str.replace(r'VANDERBILT.*', 'VANDERBILT', regex=True)
hop['organization_name'] = hop['organization_name'].str.replace(r'MACON.*', 'MACON COUNTY, INC.', regex=True)
hop['organization_name'] = hop['organization_name'].str.replace(r'SUMNER.*', 'SUMNER REGIONAL', regex=True)

hop_referal_pct = hop.groupby("organization_name")["patient_count"].sum()
hop_referal_pct = hop_referal_pct / hop_referal_pct.sum() * 100

hop_referal_pct_df = hop_referal_pct.reset_index(name='Percentage of Patients')

fig = px.treemap(
    hop_referal_pct_df, 
    path=['organization_name'], 
    values='Percentage of Patients',
    color='Percentage of Patients',           
    color_continuous_scale='Greens'
)

fig.update_traces(texttemplate='%{label}<br>%{value:.1f}%',
                   textfont=dict(size=16)
                   )

st.plotly_chart(fig, use_container_width=True)  