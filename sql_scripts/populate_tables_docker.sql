LOAD DATA INFILE '/docker-entrypoint-initdb.d/data/student.tsv' IGNORE INTO TABLE STUDENT COLUMNS TERMINATED BY '\t';
LOAD DATA INFILE '/docker-entrypoint-initdb.d/data/company.tsv' IGNORE INTO TABLE COMPANY COLUMNS TERMINATED BY '\t';
LOAD DATA INFILE '/docker-entrypoint-initdb.d/data/job.tsv' IGNORE INTO TABLE JOB COLUMNS TERMINATED BY '\t';
LOAD DATA INFILE '/docker-entrypoint-initdb.d/data/placement.tsv' IGNORE INTO TABLE PLACEMENT COLUMNS TERMINATED BY '\t';
