IS423-SIS436 Business Process Mining: Assignment (Chapters 5 and 6)
Student ID: 20236113        Process domain: Hospital Patient Intake
=====================================================================

You have two data files, both about the SAME process (Hospital Patient Intake):
  Q1_raw_event_log.csv    raw export from the information system (messy)  -> Question 1
  Q2_clean_event_log.csv  validated, clean log of the same process        -> Question 2
Both files are personal to you. Your numbers will differ from your classmates'.

HOW TO ANSWER
  Open the Google Form (link on the course page), enter your Student ID, and type the NUMBERS
  your own analysis produces. For the footprint matrix, tick one relation per cell pair.
  You may use any AI tool or software, but every number must be one you verified against
  your own files (see the AI policy at the end).

---------------------------------------------------------------------
QUESTION 1: Event representation and data quality (Chapter 5)
---------------------------------------------------------------------
Columns of Q1_raw_event_log.csv: case_id, activity, timestamp, resource (one row = one event).

The 8 official activity names of this process are:
  - Register Patient
  - Triage
  - Take Vitals
  - Order Lab Tests
  - Doctor Consultation
  - Prescribe Treatment
  - Billing
  - Discharge Patient

Your MANDATORY activity (every case should contain it): Triage
Label normalization rule (for Q1.10 only): trim spaces, lowercase, replace underscores by spaces.

Quality-issue codes (Chapter 5 classification): CASE-MIS, TS-MIS, TS-IMP, RES-MIS, ACT-IMP,
POS-INC (attribute level: missing / incorrect / imprecise) and EV-MIL, EV-CIL (event level:
missing in log / concealed in log), with recurrence CONT, INT, CHNG.

Questions (enter numbers in the form):
  Q1.1  Number of data rows in Q1_raw_event_log.csv (header excluded)
  Q1.2  Number of distinct, non-empty case IDs
  Q1.3  Rows whose case ID is empty [CASE-MIS]
  Q1.4  Rows whose timestamp is empty [TS-MIS]
  Q1.5  Rows whose timestamp has a date but NO time of day (format YYYY-MM-DD) [TS-IMP]
  Q1.6  Rows whose resource is empty [RES-MIS]
  Q1.7  Rows identical in ALL four columns to an EARLIER row; each extra copy counts 1 [EV-CIL]
  Q1.8  Number of distinct activity strings exactly as written in the file (no cleaning)
  Q1.9  Rows whose activity string is NOT exactly one of the 8 official activity names [ACT-IMP]
  Q1.10  Cases (non-empty IDs) with NO event of your mandatory activity, after normalizing labels (trim spaces, lowercase, underscores to spaces) [EV-MIL]
        (The mandatory activity is named in your README.)
  Q1.11  Cases whose rows, in FILE order, are not in non-decreasing timestamp order [POS-INC]
        (Use only rows that have a full date-time timestamp; ignore rows with empty case ID.)
  Q1.12  Recurrence pattern of the empty-resource problem: 1 = CONT, 2 = INT, 3 = CHNG
        (CONT = continuous, INT = intermittent, CHNG = changing (see Chapter 5 slides on recurrence).)
  Q1.13  Which issue affects the MOST rows/cases? 1=TS-MIS (Q1.4)  2=TS-IMP (Q1.5)  3=RES-MIS (Q1.6)  4=EV-CIL (Q1.7)  5=ACT-IMP (Q1.9)  6=CASE-MIS (Q1.3)  7=EV-MIL (Q1.10)  8=POS-INC (Q1.11)
        (Compare the counts you computed above.)

---------------------------------------------------------------------
QUESTION 2: Footprint matrix and the alpha-algorithm (Chapter 6)
---------------------------------------------------------------------
Use Q2_clean_event_log.csv (columns case_id, activity, timestamp, resource). Work with the
traces (the order of activities within each case). To keep the matrix readable, the activities
are labelled by letters, assigned in ALPHABETICAL order of the activity names:
  a = Billing
  b = Discharge Patient
  c = Doctor Consultation
  d = Order Lab Tests
  e = Prescribe Treatment
  f = Register Patient
  g = Take Vitals
  h = Triage

Ordering relations (as in the slides): x >L y (directly follows), x → y (causality: x>y and
not y>x), x || y (parallel: both x>y and y>x), x # y (neither x>y nor y>x; also x # x when x
never directly follows itself). The matrix is symmetric in the sense that x→y means y←x, so you
only fill the pairs (x, y) with x before y in the alphabet: 28 pairs.

Alpha-algorithm steps: TL (activities), TI (start activities), TO (end activities), XL (all pairs
(A,B) with every a in A causally followed by every b in B and the members of A, and of B,
pairwise #), YL (maximal pairs of XL), places = one per pair in YL plus source and sink,
arcs = all arcs of FL (pair places to their A and B transitions, plus source to TI and TO to sink).

Questions (enter numbers in the form):
  Q2.1  Number of distinct traces (variants) in Q2_clean_event_log.csv
  Q2.2  Number of ordered pairs (x, y) with x >L y (x is directly followed by y somewhere in the log)
  Q2.3  Number of unordered activity pairs {x, y} in causality (x → y or y → x)
  Q2.4  Number of unordered pairs {x, y}, x ≠ y, in parallel (x || y)
  Q2.5  Number of unordered pairs {x, y}, x ≠ y, with x # y
  Q2.6  |TI|: number of start activities
  Q2.7  TI: list the start activities (comma separated, no spaces)
  Q2.8  |TO|: number of end activities
  Q2.9  TO: list the end activities (comma separated, no spaces)
  Q2.10  |XL|: number of pairs (A, B) found in step 4 of the α-algorithm
  Q2.11  |YL|: number of maximal pairs kept in step 5
  Q2.12  Number of places in α(L), including the source place iL and sink place oL
  Q2.13  Number of arcs in FL (step 7)
Q2.14 Footprint matrix: for each pair (x vs y) choose one of → ← || #.
        The form lists the 28 pairs above the diagonal; the lower half follows by symmetry
        (if a → b then b ← a; || and # are symmetric) and the diagonal is x # x here.

Scratch worksheet (not submitted; rows = first letter, columns = second letter):
       a   b   c   d   e   f   g   h
    a  .   .   .   .   .   .   .   .
    b  .   .   .   .   .   .   .   .
    c  .   .   .   .   .   .   .   .
    d  .   .   .   .   .   .   .   .
    e  .   .   .   .   .   .   .   .
    f  .   .   .   .   .   .   .   .
    g  .   .   .   .   .   .   .   .
    h  .   .   .   .   .   .   .   .

---------------------------------------------------------------------
AI-USE POLICY (short version)
---------------------------------------------------------------------
Allowed: brainstorming, explaining concepts, writing analysis code (pandas, PM4Py, etc.).
You must: run the code yourself on your own files, check the output, and correct AI mistakes.
Declare in the form which AI tools you used and which answers you had to correct.
Not allowed: submitting numbers that you did not obtain from your own files, or sharing your files.
A short oral check may be asked: you may need to explain one of your numbers.
