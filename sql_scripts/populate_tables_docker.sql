LOAD DATA INFILE '/docker-entrypoint-initdb.d/data/student.tsv' INTO TABLE STUDENT COLUMNS TERMINATED BY '\t';
LOAD DATA INFILE '/docker-entrypoint-initdb.d/data/company.tsv' INTO TABLE COMPANY COLUMNS TERMINATED BY '\t';
LOAD DATA INFILE '/docker-entrypoint-initdb.d/data/job.tsv' INTO TABLE JOB COLUMNS TERMINATED BY '\t';
LOAD DATA INFILE '/docker-entrypoint-initdb.d/data/placement.tsv' IGNORE INTO TABLE PLACEMENT COLUMNS TERMINATED BY '\t' (
    cid,
    jid,
    pid,
    sid,
    term_num,
    @salary,
    start_date,
    end_date
)
SET salary = nullif(@salary, -1);
