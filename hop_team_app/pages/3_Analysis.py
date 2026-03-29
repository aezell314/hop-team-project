import plotly.express as px
import streamlit as st
import pandas as pd
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

st.image('figures/specialization_hospital_referral_heatmap1.png')

pcp_patient_count = hop.groupby("classification")["patient_count"].sum().reset_index()

fig = px.bar(
    pcp_patient_count,                         
    x="classification",          
    y="patient_count",               
    title="Top Referring Providers"
)

fig.update_layout(
    xaxis_title="Provider Classification",
    yaxis_title="Total Referrals"
)

st.plotly_chart(fig, use_container_width=True)  