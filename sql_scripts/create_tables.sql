-- Schema
-- STUDENT(sid, name, program, enrol_date, grad_date)
-- COMPANY(cid, name)
-- JOB(cid, jid, mmr, title)
-- PLACEMENT(cid, jid, pid, sid, term_num, salary, start_date, end_date)
-- REVIEW(cid, jid, rid, headline, review_desc, RATING)
-- TAG(tid, label)
-- JOB_TAG(cid, tid)

-- make sure we start from a fresh database
DROP TABLE IF EXISTS JOB_TAG;
DROP TABLE IF EXISTS TAG;
DROP TABLE IF EXISTS REVIEW;
DROP TABLE IF EXISTS PLACEMENT;
DROP TABLE IF EXISTS JOB;
DROP TABLE IF EXISTS COMPANY;
DROP TABLE IF EXISTS STUDENT;


CREATE TABLE STUDENT
  (
    sid         DECIMAL(9, 0) NOT NULL PRIMARY KEY,
    name        VARCHAR(30),
    program     TEXT NOT NULL,
    enrol_date  DATE NOT NULL,
    grad_date   DATE
  );

CREATE TABLE COMPANY
  (
    cid         DECIMAL(9, 0) NOT NULL,
    name        VARCHAR(30) NOT NULL,
    mmr         INT NOT NULL,
    PRIMARY KEY (cid)
  );

CREATE TABLE JOB
  (
    cid         DECIMAL(9, 0) NOT NULL,
    jid         DECIMAL(9, 0) NOT NULL,
    title       TEXT NOT NULL,
    PRIMARY KEY (jid),
    FOREIGN KEY (cid) REFERENCES COMPANY(cid)
  );

CREATE TABLE PLACEMENT
  (
     cid        DECIMAL(9, 0) NOT NULL,
     jid        DECIMAL(9, 0) NOT NULL,
     pid        DECIMAL(9, 0) NOT NULL,
     sid        DECIMAL(9, 0) NOT NULL,
     term_num   INT NOT NULL,
     salary     DECIMAL(9, 2),
     start_date DATE NOT NULL,
     end_date   DATE,
     PRIMARY KEY(pid),
     FOREIGN KEY(sid) REFERENCES STUDENT(sid),
     FOREIGN KEY(cid) REFERENCES COMPANY(cid),
     FOREIGN KEY(jid) REFERENCES JOB(jid)
  );

CREATE TABLE REVIEW
  (
    cid         DECIMAL(9, 0) NOT NULL,
    jid         DECIMAL(9, 0) NOT NULL,
    rid         DECIMAL(9, 0) NOT NULL,
    headline    TEXT NOT NULL,
    review_body TEXT NOT NULL,
    rating      INT,
    PRIMARY KEY(rid),
    FOREIGN KEY(cid) REFERENCES COMPANY(cid),
    FOREIGN KEY(jid) REFERENCES JOB(jid)
  );

CREATE TABLE TAG
  (
    tid         DECIMAL(9, 0) NOT NULL,
    label       VARCHAR(100) UNIQUE NOT NULL,
    PRIMARY KEY (tid)
  );

CREATE TABLE JOB_TAG
  (
    jid         DECIMAL(9, 0) NOT NULL,
    tid         DECIMAL(9, 0) NOT NULL,
    PRIMARY KEY(jid, tid),
    FOREIGN KEY(jid) REFERENCES JOB(jid)
  );
