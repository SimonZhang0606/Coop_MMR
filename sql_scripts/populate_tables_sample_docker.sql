LOAD DATA INFILE '/docker-entrypoint-initdb.d/sample_data/student.tsv' INTO TABLE STUDENT COLUMNS TERMINATED BY '\t';
LOAD DATA INFILE '/docker-entrypoint-initdb.d/sample_data/company.tsv' INTO TABLE COMPANY COLUMNS TERMINATED BY '\t';
LOAD DATA INFILE '/docker-entrypoint-initdb.d/sample_data/job.tsv' INTO TABLE JOB COLUMNS TERMINATED BY '\t';
LOAD DATA INFILE '/docker-entrypoint-initdb.d/sample_data/placement.tsv' INTO TABLE PLACEMENT COLUMNS TERMINATED BY '\t';
LOAD DATA INFILE '/docker-entrypoint-initdb.d/sample_data/review.tsv' INTO TABLE REVIEW COLUMNS TERMINATED BY '\t';
LOAD DATA INFILE '/docker-entrypoint-initdb.d/sample_data/tag.tsv' INTO TABLE TAG COLUMNS TERMINATED BY '\t';
LOAD DATA INFILE '/docker-entrypoint-initdb.d/sample_data/job_tag.tsv' INTO TABLE JOB_TAG COLUMNS TERMINATED BY '\t';
