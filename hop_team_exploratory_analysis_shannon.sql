/*
HOP TEAM EXPLORATORY ANALYSIS

NOTES:
- RECEIVING PROVIDERS: NUCC.GROUPING=<hospitals> AND NPPES.TYPE=1 (orgs)
- CBSA: 34980
- NPPES POSTAL CODE DOES NOT DIRECTLY MATCH THE ZIP_CBSA ZIP
- NPPES TAXONOMY SWITCH VALUES CAN BE ('Y' or 'N') OR ('X' or NULL)
*/

-- nppes (TN): 138156 rows
SELECT *
FROM nppes
WHERE address_state_name ILIKE ANY(ARRAY['tennessee', 'tn'])
ORDER BY address_postal_code;

-- hop_team: 217911308 rows
-- SELECT COUNT(*)
-- FROM hop_team;

select *
from hop_team
limit 5;

-- nucc: 883 rows
SELECT *
FROM nucc;

-- cbsa (34980): 157 rows
SELECT *
FROM zip_cbsa
WHERE cbsa = 34980
ORDER BY zip;

-- SELECT column_name
-- FROM information_schema.columns
-- WHERE table_name = 'nppes'
-- 	AND column_name LIKE 'healthcare_primary_taxonomy_switch%'

-- Create a materialized view for NPPES in TN with primary taxonomy column
-- CREATE MATERIALIZED VIEW nppes_tn_primary_taxonomy_mv AS
SELECT
	*,
	CASE
		WHEN healthcare_primary_taxonomy_switch_1 IN ('Y', 'X') THEN healthcare_taxonomy_code_1
		WHEN healthcare_primary_taxonomy_switch_2 IN ('Y', 'X') THEN healthcare_taxonomy_code_2
		WHEN healthcare_primary_taxonomy_switch_3 IN ('Y', 'X') THEN healthcare_taxonomy_code_3
		WHEN healthcare_primary_taxonomy_switch_4 IN ('Y', 'X') THEN healthcare_taxonomy_code_4
		WHEN healthcare_primary_taxonomy_switch_5 IN ('Y', 'X') THEN healthcare_taxonomy_code_5
		WHEN healthcare_primary_taxonomy_switch_6 IN ('Y', 'X') THEN healthcare_taxonomy_code_6
		WHEN healthcare_primary_taxonomy_switch_7 IN ('Y', 'X') THEN healthcare_taxonomy_code_7
		WHEN healthcare_primary_taxonomy_switch_8 IN ('Y', 'X') THEN healthcare_taxonomy_code_8
		WHEN healthcare_primary_taxonomy_switch_9 IN ('Y', 'X') THEN healthcare_taxonomy_code_9
		WHEN healthcare_primary_taxonomy_switch_10 IN ('Y', 'X') THEN healthcare_taxonomy_code_10
		WHEN healthcare_primary_taxonomy_switch_11 IN ('Y', 'X') THEN healthcare_taxonomy_code_11
		WHEN healthcare_primary_taxonomy_switch_12 IN ('Y', 'X') THEN healthcare_taxonomy_code_12
		WHEN healthcare_primary_taxonomy_switch_13 IN ('Y', 'X') THEN healthcare_taxonomy_code_13
		WHEN healthcare_primary_taxonomy_switch_14 IN ('Y', 'X') THEN healthcare_taxonomy_code_14
		WHEN healthcare_primary_taxonomy_switch_15 IN ('Y', 'X') THEN healthcare_taxonomy_code_15
		ELSE NULL
	END AS primary_taxonomy_code
FROM nppes
WHERE address_state_name IN ('TENNESSEE', 'TN')
ORDER BY npi;
-- 138156 rows

--------------------------------------------------
-- REFERRING PROVIDERS
--------------------------------------------------
-- PCP only: Family Medicine, Internal Medicine, Pediatrics, General Practice
-- nucc.classification=<pcp>
-- nppes.type=1 (people)

-- Create a materialized view for NUCC PCPs
-- CREATE MATERIALIZED VIEW nucc_pcp_mv AS
SELECT *
FROM nucc
WHERE classification ILIKE ANY(
	ARRAY[
		'family medicine',
		'internal medicine',
		'pediatrics',
		'general practice'
	]
)
ORDER BY code;
-- 68 ROWS

-- Create a materialized view for NPPES PCPs in TN with primary taxonomy column
-- (UPDATE TO USE CBSA WHEN READY)
-- CREATE MATERIALIZED VIEW nppes_tn_pcp_mv AS
SELECT *
FROM nppes_tn_primary_taxonomy_mv n
	INNER JOIN nucc_pcp_mv p ON n.primary_taxonomy_code = p.code
WHERE entity_type_code = 1;	
-- 13157 rows


--------------------------------------------------
-- RECEIVING PROVIDERS
--------------------------------------------------
-- Hospitals only
-- nucc.grouping=hospital
-- nppes.entity_type=2 (orgs)

-- Create a materialized view for NUCC Hospitals
-- CREATE MATERIALIZED VIEW nucc_hospitals_mv AS
SELECT *
FROM nucc
WHERE grouping ILIKE '%hospital%'
ORDER BY code;
-- 23 ROWS

-- Create a materialized view for NPPES hospitals in TN with primary taxonomy column
-- (UPDATE TO USE CBSA WHEN READY)
-- CREATE MATERIALIZED VIEW nppes_tn_hospitals_mv AS
SELECT *
FROM nppes_tn_primary_taxonomy_mv n
	INNER JOIN nucc_hospitals_mv h ON n.primary_taxonomy_code = h.code
WHERE entity_type_code = 2;
-- 635 rows


