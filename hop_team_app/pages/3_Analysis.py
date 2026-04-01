import plotly.express as px
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import utils


st.set_page_config(layout="wide")

pcp_specialization_selectbox = st.sidebar.selectbox(
    label='PCP Specialization',
    options=utils.pcp_specialization_list
)

hospital_selectbox = st.sidebar.selectbox(
    label='Hospital',
    options=utils.hospital_list
)

hop = utils.hop_team_nashville_df

st.title('Analysis', text_alignment='center')

#-------------------------------------------------

st.header('Hospital Patient Share')

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

#-------------------------------------------------

st.header('Heatmap')

st.markdown(
    '''
    The following heatmap is a graphical representation of referrals by color intensity demonstrating the top 10 hospitals with the most referrals across the top 10 referring PCP specializations.
    '''
)

heatmap_col1, heatmap_col2, heatmap_col3 = st.columns([1, 6, 1], vertical_alignment='center')

with heatmap_col2:
    # Create heatmap
    heatmap_fig = plt.figure(figsize=(15, 10))

    heatmap_ax = sns.heatmap(
        data=utils.top_10_referral_df,
        cmap='Greens',
        linewidths=0.5,
        annot=True, # Show values
        fmt='.0f' # Display as int
    )

    # Format labels
    heatmap_ax.set_title('Referrals From PCP Specialties to Hospitals', fontsize=18)
    heatmap_ax.set_ylabel('Top 10 Hospitals')
    heatmap_ax.set_xlabel('Top 10 PCP Specializations')
    heatmap_ax.set_xticklabels(
        heatmap_ax.get_xticklabels(),
        rotation=45,
        ha='right'
    )
    for label in heatmap_ax.get_yticklabels():
        if 'VANDERBILT' in label.get_text():
            label.set_weight('bold')
            label.set_size(14)

    heatmap_fig.tight_layout()

    st.pyplot(
        fig=heatmap_fig
    )

st.markdown(
    '''
    * Vanderbilt UMC is the top hospital for referrals by PCP specialization. The next largest number of referrals for Cardiovascular Disease is Saint Thomas, then HCA.
    * Vanderbilt's larget areas of opportunity are within Interventional Cardiology and Pulmonary Disease.
    '''
)

#-------------------------------------------------

pcp_specialization_selectbox
hospital_selectbox

#-------------------------------------------------

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

#-------------------------------------------------

