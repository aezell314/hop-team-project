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

louvain_col1, louvain_col2, louvain_col3 = st.columns([1, 6, 1], vertical_alignment='center')

with louvain_col2:
    try:
        st.image('images/community_detection.jpg')
    except st.runtime.media_file_storage.MediaFileStorageError:
        st.image('../images/community_detection.jpg')

st.divider()

#-------------------------------------------------

st.header('Neo4j')

st.markdown(
    '''
    Neo4j is a native graph database. A Neo4j graph database stores data as nodes, relationships, and properties instead of in tables or documents.
    The data is stored in Neo4j in the same way you may whiteboard your ideas.<sup>2</sup>
    ''',
    unsafe_allow_html=True
)

neo4j_col1, neo4j_col2, neo4j_col3 = st.columns([2, 4, 2], vertical_alignment='center')

with neo4j_col2:
    try:
        st.image('images/node_structure.png', caption='**PCP -> Referral -> Hospital**')
    except st.runtime.media_file_storage.MediaFileStorageError:
        st.image('../images/node_structure.png', caption='**PCP -> Referral -> Hospital**')

    st.space('small')

    st.dataframe(
        data= (
            utils.hop_team_nashville_df[['providername', 'transaction_count', 'owning_entity']]
                .sort_values(by='transaction_count', ascending=False)
                .rename(columns={
                    'providername': 'Referring PCP',
                    'transaction_count': 'Number of Referrals',
                    'owning_entity': 'Receiving Hospital'
                })
        ),
        width='content',
        hide_index=True
    )

st.space('small')

#-------------------------------------------------

# Functions used
st.markdown(
    '''
    The Neo4j Graph Data Science (GDS) library provides efficiently implemented, parallel versions of common graph algorithms.<sup>2</sup>
    * Graph algorithms are used to compute metrics for graphs, nodes, or relationships.
    * They can provide insights on inherent structures like communities.
    ''',
    unsafe_allow_html=True
)

code1_col1, code1_col2, code1_col3 = st.columns([1, 6, 1], vertical_alignment='center')

with code1_col2:
    st.code(
        '''
        CALL
        gds.graph.project(
            'hopteam',
            'Provider',
            {
                Transaction: {
                    orientation: 'UNDIRECTED',
                    aggregation: 'SUM'
                }
            },
            {
                relationshipProperties: 'transaction_count'
            }
        )
    ''',
    language='sql'
    )

code2_col1, code2_col2, code2_col3 = st.columns([1, 6, 1], vertical_alignment='center')

with code2_col2:
    st.code(
        '''
        CALL
        gds.louvain.stream(
            'hopteam',
            {
                relationshipWeightProperty: 'transaction_count'
            }
        )
        YIELD nodeId, communityId
        RETURN gds.util.asNode(nodeId).npi AS npi, communityId
        ORDER BY npi ASC
    ''',
    language='sql'
    )

st.space('large')

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