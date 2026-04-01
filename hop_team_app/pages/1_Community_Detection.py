import streamlit as st
import utils

st.set_page_config(layout="wide")

st.title('Community Detection', text_alignment='center')

st.markdown(
    '''
    Community detection is a mechanism that clusters nodes in the network into groups such that nodes in each group are more 
    densely connected internally than externally.<sup>1</sup> Community detection algorithms are used to evaluate how groups of 
    nodes are clustered or partitioned, as well as their tendency to strengthen or break apart.<sup>2</sup> Because networks are 
    an integral part of many real-world problems, community detection algorithms have found their way into various fields, 
    ranging from social network analysis to public health initiatives.<sup>3</sup>
    ''',
    unsafe_allow_html=True
)

#-------------------------------------------------

st.header('Louvain')

st.markdown(
    '''
    The **Louvain method** is an algorithm to detect communities in large networks. It maximizes a modularity score for each community, 
    where the modularity quantifies the quality of an assignment of nodes to communities. This means evaluating how much more 
    densely connected the nodes within a community are, compared to how connected they would be in a random network.<br>
    The **Louvain algorithm** is a hierarchical clustering algorithm, that recursively merges communities into a single node and executes the 
    modularity clustering on the condensed graphs.<sup>2</sup>
    ''',
    unsafe_allow_html=True
)

try:
    st.image('images/community_detection.jpg')
except st.runtime.media_file_storage.MediaFileStorageError:
    st.image('../images/grant.png')

st.divider()

#-------------------------------------------------

st.header('PCP -> Referral -> Hospital')

try:
    st.image('images/node_structure.png')
except st.runtime.media_file_storage.MediaFileStorageError:
    st.image('../images/node_structure.png')

st.dataframe(
    data=utils.community_detection_df,
    width='content',
    hide_index=True
)

st.divider()

#-------------------------------------------------

# Functions used
'''Graph algorithms are used to compute metrics for graphs, nodes, or relationships.'''
st.code(
    '''
    CALL
    gds.graph.project(
        'hopteam',
        'Provider',
        {Transaction: {orientation: 'UNDIRECTED', aggregation: 'SUM'}},
        {relationshipProperties: 'transaction_count'}
    )
  '''
)

st.code(
    '''
    CALL
    gds.louvain.stream('hopteam', { relationshipWeightProperty: 'transaction_count' })
    YIELD nodeId, communityId
    RETURN gds.util.asNode(nodeId).npi AS npi, communityId
    ORDER BY npi ASC
  '''
)

#-------------------------------------------------

# Sources
st.markdown(
    '''
    <sup>1</sup> https://www.sciencedirect.com/topics/computer-science/community-detection<br>
    <sup>2</sup> https://neo4j.com/docs/graph-data-science/current/algorithms/community/<br>
    <sup>3</sup> https://memgraph.com/blog/community-detection-algorithms-with-python-networkx
    ''',
    unsafe_allow_html=True
)