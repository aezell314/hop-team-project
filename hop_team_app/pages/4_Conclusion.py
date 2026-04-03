import streamlit as st


st.set_page_config(layout="wide")

st.title('Conclusion')

st.header('Summary', divider='rainbow', text_alignment='left')

st.markdown(
    '''
    * Vanderbilt's larget areas of opportunity are within Interventional Cardiology and Pulmonary Disease.
    * Vanderbilt's share of the Cardiovascular Disease referrals is 37.28% (74,723 / 200,426)
    * Vanderbilt is part of 3 communities (HCA has 7 and Saint Thomas have 4).
    * Some communities that are further out have higher wait times.
    '''
)

st.space('large')

st.header('Recommendations', divider='rainbow', text_alignment='left')

st.markdown(
    '''
    * Find ways to increase referrals from PCP's with specialties in Interventional Cardiology and Pulmonary Disease.
    * Find ways to increase the share of specialties that Vanderbilt is strong in.
    * Find a way to reach further out in Middle TN.
    * Find a way to reach out to patients with higher wait times who can drive a little further.
    '''
)