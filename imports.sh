#!/bin/bashRun; 
 mysql -uroot -proot openmrs_nazombe < db/sql/openmrs_metadata_1_7.sql -v -f
 mysql -uroot -proot openmrs_nazombe < db/sql/alternative_drug_names.sql -v -f
 mysql -uroot -proot openmrs_nazombe < db/sql/moh_regimens_v2020.sql -v -f
 mysql -uroot -proot openmrs_nazombe < db/sql/bart2_views_schema_additions.sql -v -f