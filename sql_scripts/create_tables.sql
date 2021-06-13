-- STUDENT(SID, NAME, ENROLMENT_DATE, GRAD_DATE, PROGRAM)
-- COMPANY(CID, NAME)
-- JOB(CID, JID, MMR, TITLE, TID)
-- PLACEMENT(CID, JID, PID, SID, TERM_NUM, SALARY, START_DATE, END_DATE)
-- REVIEW(CID, JID, RID, HEADLINE, review_desc, RATING)
-- TAG(TID, LABEL)
-- JOB_TAG(CID, TID)

DROP TABLE IF EXISTS REVIEW;
DROP TABLE IF EXISTS PLACEMENT;
DROP TABLE IF EXISTS JOB_TAG;
DROP TABLE IF EXISTS JOB;
DROP TABLE IF EXISTS COMPANY;
DROP TABLE IF EXISTS STUDENT;
DROP TABLE IF EXISTS TAG;


CREATE TABLE TAG
  (
    tid         DECIMAL(9, 0) NOT NULL, 
    label       VARCHAR(100) NOT NULL,
    PRIMARY KEY (tid)
  );

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
    PRIMARY KEY (cid)
  ); 

CREATE TABLE JOB 
  ( 
    cid         DECIMAL(9, 0) NOT NULL, 
    jid         DECIMAL(9, 0) NOT NULL, 
    mmr         INT NOT NULL, 
    title       TEXT NOT NULL,
    tid         DECIMAL(9, 0) NOT NULL, 
    PRIMARY KEY (jid),
    FOREIGN KEY (cid) REFERENCES COMPANY(cid),
    FOREIGN KEY (tid) REFERENCES TAG(tid)
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

CREATE TABLE JOB_TAG
  (
    cid         DECIMAL(9, 0) NOT NULL,
    tid         DECIMAL(9, 0) NOT NULL,
    PRIMARY KEY(cid, tid),
    FOREIGN KEY(cid) REFERENCES COMPANY(cid)
  );