-- STUDENT(SID, NAME, ENROLMENT_DATE, GRAD_DATE, PROGRAM)
-- COMPANY(CID, NAME)
-- JOB(CID, JID, MMR, TITLE, TID)
-- PLACEMENT(CID, JID, PID, SID, TERM_NUM, SALARY, START_DATE, END_DATE)
-- REVIEW(CID, JID, RID, HEADLINE, review_desc, RATING)
-- TAG(TID, LABEL)
-- JOB_TAG(CID, TID)

CREATE TABLE TAG
  (
    tid         DECIMAL(9, 0) NOT NULL PRIMARY KEY, 
    label       VARCHAR(100) NOT NULL
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
    cid         DECIMAL(9, 0) NOT NULL PRIMARY KEY, 
    name        VARCHAR(30) NOT NULL, 
  ); 

CREATE TABLE JOB 
  ( 
    cid         DECIMAL(9, 0) NOT NULL, 
    jid         DECIMAL(9, 0) NOT NULL, 
    mmr         INT NOT NULL, 
    title       TEXT NOT NULL,
    tid         DECIMAL(9, 0) NOT NULL, 
    PRIMARY KEY(cid, jid),
    FOREIGN KEY(cid) REFERENCES COMPANY, 
    FOREIGN KEY(tid) REFERENCES TAG 
  ); 

CREATE TABLE PLACEMENT 
  ( 
     cid        DECIMAL(9, 0) NOT NULL, 
     jid        DECIMAL(9, 0) NOT NULL, 
     sid        DECIMAL(9, 0) NOT NULL, 
     term_num   INT NOT NULL,
     salary     DECIMAL(9, 2),
     start_date DATE NOT NULL,
     end_date   DATE,
     PRIMARY KEY(cid, jid, term_num, sid), 
     FOREIGN KEY(sid) REFERENCES STUDENT, 
     FOREIGN KEY(cid) REFERENCES COMPANY, 
     FOREIGN KEY(jid) REFERENCES JOB 
  ); 

CREATE TABLE REVIEW
  (
    cid         DECIMAL(9, 0) NOT NULL, 
    jid         DECIMAL(9, 0) NOT NULL, 
    rid         DECIMAL(9, 0) NOT NULL, 
    headline    TEXT NOT NULL,
    review_body TEXT NOT NULL,
    rating       INT
  );

CREATE TABLE JOB_TAG
  (
    cid         DECIMAL(9, 0) NOT NULL,
    tid         DECIMAL(9, 0) NOT NULL,
    PRIMARY KEY(cid, tid)
  );