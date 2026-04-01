import streamlit as st

st.set_page_config(layout="wide")

st.title('Hop Teaming Analysis: Nashville Referral Network', text_alignment='center')

st.space('small')

#-------------------------------------------------

st.header('Goals', divider='rainbow', text_alignment='left')

goals_col1, goals_col2 = st.columns([2, 1], vertical_alignment='center')

with goals_col1:
    '''
    Explore how primary care physicians (PCPs) refer patients to hospitals and analyze referral communities to make recommendations.

    * Identify which PCP specialties represent the largest potential growth opportunities for Vanderbilt
    * Gather key insights from the referral network and community structure
    * Recommendations for visualizations or dashboards that could support hospital decision-making
    '''

with goals_col2:
    try:
        st.image('images/goals.png', width=200)
    except st.runtime.media_file_storage.MediaFileStorageError:
        st.image('../images/goals.png', width=200)

st.space('small')

#-------------------------------------------------

st.header('Dataset', divider='rainbow', text_alignment='left')

data_col1, data_col2 = st.columns([1, 2], vertical_alignment='center')

with data_col1:
    try:
        st.image('images/dataset.png', width=200)
    except st.runtime.media_file_storage.MediaFileStorageError:
        st.image('../images/dataset.png', width=200)

with data_col2:
    '''
    #### CareSet Labs DocGraph Hop Teaming Dataset (2018)

    This dataset is the most comprehensive open map of the healthcare system in the United States and is also the largest graph dataset available as open data that uses real names.
    It offers the most detailed and up-to-date picture of the patient-sharing relationships found between all Medicare providers in the US healthcare system.
    The updated HOP Teaming dataset continues to provide some of the most timely and necessary insights into how healthcare ecosystems work across the US.
    '''

st.space('small')

#-------------------------------------------------

st.header('Approach', divider='rainbow', text_alignment='left')

postgres_col1, postgres_col2 = st.columns([2, 1], vertical_alignment='center')

with postgres_col1:
    '''
    * **PostgreSQL:** The World's Most Advanced Open Source Relational Database
    '''

with postgres_col2:
    try:
        st.image('images/postgresql.png', width=75)
    except st.runtime.media_file_storage.MediaFileStorageError:
        st.image('../images/postgresql.png', width=75)
    
neo_col1, neo_col2 = st.columns([2, 1], vertical_alignment='center')

with neo_col1:
    "* **Neo4j:** The World's Leading Graph Intelligence Platform"

with neo_col2:
    try:
        st.image('images/neo4j.png', width=75)
    except st.runtime.media_file_storage.MediaFileStorageError:
        st.image('../images/neo4j.png', width=75)
    
streamlit_col1, streamlit_col2 = st.columns([2, 1], vertical_alignment='center')

with streamlit_col1:
    '* **Streamlit:** an open-source app framework'

with streamlit_col2:
    try:
        st.image('images/streamlit.png', width=75)
    except st.runtime.media_file_storage.MediaFileStorageError:
        st.image('../images/streamlit.png', width=75)

st.space('large')

#-------------------------------------------------

st.header('Nashville Software School', text_alignment='center')

nss_col1, nss_col2, nss_col3, nss_col4, nss_col5, nss_col6 = st.columns([2, 1, 1, 1, 1, 2], vertical_alignment='top')


with nss_col2:
    try:
        st.image('images/grant.png', caption='Grant Alan')
    except st.runtime.media_file_storage.MediaFileStorageError:
        st.image('../images/grant.png', caption='Grant Alan')

with nss_col3:
    try:
        st.image('images/abigail.png', caption='Abigail Ezell')
    except st.runtime.media_file_storage.MediaFileStorageError:
        st.image('../images/abigail.png', caption='Abigail Ezell')

with nss_col4:
    try:
        st.image('images/shannon.png', caption='Shannon Lee')
    except st.runtime.media_file_storage.MediaFileStorageError:
        st.image('../images/shannon.png', caption='Shannon Lee')

with nss_col5:
    try:
        st.image('images/micheal.png', caption='Micheal Major')
    except st.runtime.media_file_storage.MediaFileStorageError:
        st.image('../images/micheal.png', caption='Micheal Major')
