# Hop Teaming Analysis (Nashville CBSA) 

## Executive Summary
We analyzed referral patterns from Primary Care Physicians (PCPs) to hospitals within the Nashville CBSA using the CareSet Labs DocGraph Hop Teaming Dataset (2018), which is the most comprehensive open map of the healthcare system in the United States and is also the largest graph dataset available as open data that uses real names. We combined SQL-based aggregation, graph/community detection (Neo4j + Louvain), and interactive visualizations (Streamlit) to identify where Vanderbilt University Medical Center is strong, where competitors dominate, and which provider communities represent the clearest growth opportunities.

## What We Built
- **Curated analytical dataset** (PCP → Hospital referrals) filtered to meaningful relationships (high volume / low wait time).
- **Market-share and specialty mix views** (treemap + heatmaps) to understand where patients are going by organization and by referring PCP specialty.
- **Neo4j graph + Louvain community detection** to identify clusters of providers that behave like referral “communities.”
- **Operational view** of **wait time vs. patient volume** by community to highlight access/efficiency differences across communities.

## Key Findings
### 1) Hospital patient share (market distribution)
- Patient referrals are concentrated among a small number of large hospital systems.
- After consolidating facilities under common umbrellas (e.g., Vanderbilt, Saint Thomas, HCA), Vanderbilt appears as a top destination overall in the Nashville CBSA referral network.

### 2) Specialty-level referral patterns (heatmaps)
- **Vanderbilt UMC is the top hospital destination across PCP specializations** in the top-referral cohort.
- For **Cardiovascular Disease**, Vanderbilt leads, with Saint Thomas and HCA as the next major recipients.
- **Largest growth opportunities for Vanderbilt are:**
  - **Interventional Cardiology**
  - **Pulmonary Disease**
- Quantified highlight from the analysis:
  - **Vanderbilt’s share of Cardiovascular Disease referrals is ~37.28%** 

### 3) Community structure (Neo4j + Louvain algorithm)
- Referral behavior clusters into distinct communities (dense internal referral patterns).
- **Vanderbilt appears in 3 referral communities**, compared with **HCA in 7** and **Saint Thomas in 4**, suggesting competitors participate across more distinct referral “ecosystems” in the network.

### 4) Access signals (wait time vs. patients)
- Some communities that are **further out geographically show higher average wait times**, indicating potential access friction (and potential opportunity) in the outer Middle TN region.

## Recommendations
1. **Target outreach to grow referrals** from PCPs whose patient flows align with:
   - **Interventional Cardiology**
   - **Pulmonary Disease**
2. **Defend and expand strongholds** by increasing share within specialties where Vanderbilt already performs well (e.g., Cardiovascular Disease).
3. **Extend influence farther into Middle TN** by identifying and prioritizing outer communities with high wait times and meaningful referral volume. Consider establishing satellite offices or acquiring existing hospitals that are farther from the metro Nashville area.
4. **Compete at the community level** (not just provider-by-provider):
   - Use community detection outputs to identify competitor-dominant clusters and design network-based engagement strategies.

## Artifacts in This Repo
- The **data** folder has csv files containing the raw data used in the project
   - _hop_team_nashville.csv_ contains the contents of a PostgreSQL materialized view that we created to capture meaningful Medicare referral relationships in the Nashville CBSA.
       - The SQL code that was used to generate this data can be found in the **sql** folder.
   - _neo4j_hop_team_algorithm.csv_ contains the results of applying the Louvain community detection algorithm to the above referral data.
- The **notebooks** folder contains a Jupyter notebook with some exploratory data analysis.
- The **hop_team_app** folder (as well as the **figures** and **images** folders) contain the component files of a Streamlit application that summarizes our data analysis and conclusions.
  - The application can be accessed on the web at https://nashville-healthcare-referrals-analysis.streamlit.app/ 

## Project Outcome
This project translated raw referral transactions into actionable network insights. By combining specialty mix, market share, and graph-based communities, we identified concrete referral-growth opportunities for Vanderbilt—especially in Interventional Cardiology and Pulmonary Disease—and highlighted where competitor systems appear to span more referral communities across the Nashville CBSA.

---
**Sources referenced in the app**
- Neo4j GDS community detection docs: https://neo4j.com/docs/graph-data-science/current/algorithms/community/
- Community detection background: https://www.sciencedirect.com/topics/computer-science/community-detection
- Additional overview: https://memgraph.com/blog/community-detection-algorithms-with-python-networkx
