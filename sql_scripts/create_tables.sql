-- Schema
-- STUDENT(sid, name, program, enrol_date, grad_date)
-- COMPANY(cid, name)
-- JOB(cid, jid, mmr, title)
-- PLACEMENT(cid, jid, pid, sid, term_num, salary, start_date, end_date)
-- REVIEW(cid, jid, rid, headline, review_desc, RATING)
-- TAG(tid, label)
-- JOB_TAG(cid, tid)

-- make sure we start from a fresh database
DROP VIEW IF EXISTS JOB_DETAILS;
DROP VIEW IF EXISTS COMPANY_DETAILS;
DROP TABLE IF EXISTS JOB_TAG;
DROP TABLE IF EXISTS TAG;
DROP TABLE IF EXISTS REVIEW;
DROP TABLE IF EXISTS PLACEMENT;
DROP TABLE IF EXISTS JOB;
DROP TABLE IF EXISTS COMPANY;
DROP TABLE IF EXISTS STUDENT;


-- INDEXES

CREATE TABLE STUDENT
  (
    sid         INT UNSIGNED NOT NULL AUTO_INCREMENT,
    name        VARCHAR(30),
    program     TEXT NOT NULL,
    enrol_date  DATE NOT NULL,
    grad_date   DATE,
    PRIMARY KEY (sid)
  );

CREATE TABLE COMPANY
  (
    cid         INT UNSIGNED NOT NULL AUTO_INCREMENT,
    name        VARCHAR(30) NOT NULL,
    mmr         INT UNSIGNED NOT NULL,
    PRIMARY KEY (cid)
  );

CREATE TABLE JOB
  (
    cid         INT UNSIGNED NOT NULL,
    jid         INT UNSIGNED NOT NULL AUTO_INCREMENT,
    title       TEXT NOT NULL,
    PRIMARY KEY (jid),
    FOREIGN KEY (cid) REFERENCES COMPANY(cid) ON DELETE CASCADE
  );

CREATE TABLE PLACEMENT
  (
     cid        INT UNSIGNED NOT NULL,
     jid        INT UNSIGNED NOT NULL,
     pid        INT UNSIGNED NOT NULL AUTO_INCREMENT,
     sid        INT UNSIGNED NOT NULL,
     term_num   INT UNSIGNED NOT NULL,
     salary     DECIMAL(9, 2),
     start_date DATE NOT NULL,
     end_date   DATE,
     PRIMARY KEY(pid),
     FOREIGN KEY(sid) REFERENCES STUDENT(sid) ON DELETE CASCADE,
     FOREIGN KEY(cid) REFERENCES COMPANY(cid),
     FOREIGN KEY(jid) REFERENCES JOB(jid) ON DELETE CASCADE
  );

CREATE TABLE REVIEW
  (
    cid         INT UNSIGNED NOT NULL,
    jid         INT UNSIGNED NOT NULL,
    rid         INT UNSIGNED NOT NULL AUTO_INCREMENT,
    headline    TEXT NOT NULL,
    review_body TEXT NOT NULL,
    rating      INT UNSIGNED,
    PRIMARY KEY(rid),
    FOREIGN KEY(cid) REFERENCES COMPANY(cid),
    FOREIGN KEY(jid) REFERENCES JOB(jid) ON DELETE CASCADE
  );

CREATE TABLE TAG
  (
    tid         INT UNSIGNED NOT NULL AUTO_INCREMENT,
    label       VARCHAR(100) UNIQUE NOT NULL,
    PRIMARY KEY (tid)
  );

CREATE TABLE JOB_TAG
  (
    jid         INT UNSIGNED NOT NULL,
    tid         INT UNSIGNED NOT NULL,
    PRIMARY KEY(jid, tid),
    FOREIGN KEY(jid) REFERENCES JOB(jid)
  );


-- ASSERTIONS
-- MySQL doesn't support assertions so we have to use triggers instead to make
-- sure that the cid FKs refers to the same company as the jid FK.

CREATE TRIGGER INSERT_PLACEMENT_CID_CONSISTENT
BEFORE INSERT ON PLACEMENT
FOR EACH ROW
SET NEW.cid = (SELECT cid FROM JOB WHERE jid = NEW.jid);

CREATE TRIGGER UPDATE_PLACEMENT_CID_CONSISTENT
BEFORE UPDATE ON PLACEMENT
FOR EACH ROW
SET NEW.cid = (SELECT cid FROM JOB WHERE jid = NEW.jid);

CREATE TRIGGER INSERT_REVIEW_CID_CONSISTENT
BEFORE INSERT ON REVIEW
FOR EACH ROW
SET NEW.cid = (SELECT cid FROM JOB WHERE jid = NEW.jid);

CREATE TRIGGER UPDATE_REVIEW_CID_CONSISTENT
BEFORE UPDATE ON REVIEW
FOR EACH ROW
SET NEW.cid = (SELECT cid FROM JOB WHERE jid = NEW.jid);


-- VIEWS

CREATE VIEW COMPANY_DETAILS AS
SELECT
    COMPANY.cid,
    COMPANY.name AS company_name,
    COMPANY.mmr AS company_mmr,
    company_min_salary,
    company_avg_salary,
    company_max_salary,
    company_avg_rating
FROM COMPANY
LEFT OUTER JOIN (
    SELECT
        cid,
        MIN(salary) AS company_min_salary,
        AVG(salary) AS company_avg_salary,
        MAX(salary) AS company_max_salary
    FROM PLACEMENT
    WHERE salary IS NOT NULL
    GROUP BY cid
) AS COMPANY_SALARY
ON COMPANY.cid = COMPANY_SALARY.cid
LEFT OUTER JOIN(
    SELECT
        cid,
        AVG(rating) AS company_avg_rating
    FROM REVIEW
    WHERE rating IS NOT NULL
    GROUP BY cid
) AS COMPANY_REVIEW
ON COMPANY.cid = COMPANY_REVIEW.cid;

CREATE VIEW JOB_DETAILS AS
SELECT
    JOB.cid,
    COMPANY_DETAILS.company_name,
    COMPANY_DETAILS.company_mmr,
    JOB.jid,
    JOB.title AS job_title,
    COMPANY_DETAILS.company_min_salary,
    COMPANY_DETAILS.company_avg_salary,
    COMPANY_DETAILS.company_max_salary,
    COMPANY_DETAILS.company_avg_rating,
    job_min_salary,
    job_avg_salary,
    job_max_salary,
    job_avg_rating
FROM JOB
JOIN COMPANY_DETAILS
ON JOB.cid = COMPANY_DETAILS.cid
LEFT OUTER JOIN (
    SELECT
        jid,
        MIN(salary) AS job_min_salary,
        AVG(salary) AS job_avg_salary,
        MAX(salary) AS job_max_salary
    FROM PLACEMENT
    WHERE salary IS NOT NULL
    GROUP BY jid
) AS JOB_SALARY
ON JOB.jid = JOB_SALARY.jid
LEFT OUTER JOIN(
    SELECT
        jid,
        AVG(rating) AS job_avg_rating
    FROM REVIEW
    WHERE rating IS NOT NULL
    GROUP BY jid
) AS JOB_REVIEW
ON JOB.jid = JOB_REVIEW.jid;


-- INDEXES

CREATE UNIQUE INDEX TAG_LABEL ON TAG(label);
