* Encoding: UTF-8.
* An Assessment of Medical Students' Adherence to Infection Prevention
* Practices during Clinical Training at Omdurman Islamic University, 2025
* Sample: N = 156
*
* NOTE: Update the FILE path below before running.

GET DATA
  /TYPE = XLSX
  /FILE = 'C:\path\to\1_data\cleaned\cleaned_data.xlsx'
  /SHEET = NAME 'Sheet1'
  /CELLRANGE = FULL
  /READNAMES = ON
  /DATATYPEMIN PERCENTAGE = 95.0.
EXECUTE.

SET DECIMAL = DOT.


VARIABLE LABELS
  gender                      'Gender'
  age                         'Age (years)'
  year_of_study               'Year of Study'
  ipc_training                'Previous IPC Training'
  heard_5moments              'Heard of WHO 5 Moments of Hand Hygiene'
  know_wash_tech              'Knows Proper Hand-Washing Technique'
  aware_risks                 'Aware of IPC Risk to Patients and HCWs'
  wash_before                 'Hand Washing Before Patient Contact'
  wash_after                  'Hand Washing After Patient Contact'
  alcohol_rub                 'Alcohol Rub Use When Soap Unavailable'
  gloves                      'Gloves Use for Invasive or Aseptic Procedures'
  mask                        'Face Mask Use in Indicated Situations'
  sharp_disposal              'Proper Sharps Disposal Without Recapping'
  needle_stick                'Needle-Stick Injury Experience'
  time_pressure               'Time Pressure Affects IPC Adherence'
  staff_support               'Supported by Hospital Staff in Following IPC'
  seniors_follow              'Senior Staff Follow IPC Guidelines'
  observation_influence       'Observing Staff Behavior Influences Compliance'
  training_type_lecture       'Training Type: Lecture'
  training_type_workshop      'Training Type: Workshop'
  training_type_online_course 'Training Type: Online Course'
  training_type_bedside_teaching 'Training Type: Bedside Teaching'
  training_type_others        'Training Type: Other'
  barrier_personal_lack_of_knowledge  'Personal Barrier: Lack of Knowledge'
  barrier_personal_forgetfulness      'Personal Barrier: Forgetfulness'
  barrier_personal_poor_attitude      'Personal Barrier: Poor Attitude'
  barrier_personal_lack_of_experience 'Personal Barrier: Lack of Experience'
  barrier_hospital_overcrowding             'Hospital Barrier: Overcrowding'
  barrier_hospital_lack_of_gloves_masks     'Hospital Barrier: Lack of Gloves/Masks'
  barrier_hospital_no_alcohol_sanitizer     'Hospital Barrier: No Alcohol Sanitizer'
  barrier_hospital_poor_facility_hygiene    'Hospital Barrier: Poor Facility Hygiene'
  barrier_hospital_inadequate_supervision   'Hospital Barrier: Inadequate Supervision'
  influence_training            'Influence: Training'
  influence_role_models         'Influence: Role Models'
  influence_hospital_environment 'Influence: Hospital Environment'
  influence_personal_motivation  'Influence: Personal Motivation'
  influence_supervision          'Influence: Supervision'
  knowledge_score             'Knowledge Score (0-5: WHO 5 Moments)'
  total_adherence_score       'Total Adherence Score (6-30)'
  mean_adherence_score        'Mean Adherence Score (1-5)'
  knowledge_level             'Knowledge Level (1=Poor, 2=Moderate, 3=Good)'
  adherence_level             'Adherence Level (1=Poor, 2=Moderate, 3=Good)'
  adherence_binary            'Good Adherence Binary (0=Poor/Moderate, 1=Good)'
  barriers_personal_sum       'Total Personal Barriers (0-4)'
  barriers_hospital_sum       'Total Hospital Barriers (0-5)'
  barriers_total              'Total Barriers (0-9)'
  influences_sum              'Total Adherence Influences (0-5)'.
EXECUTE.


VALUE LABELS gender
  1 'Male'
  2 'Female'.

VALUE LABELS year_of_study
  4 '4th Year'
  5 '5th Year'.

VALUE LABELS
  ipc_training heard_5moments know_wash_tech aware_risks
  adherence_binary
  training_type_lecture training_type_workshop training_type_online_course
  training_type_bedside_teaching training_type_others
  barrier_personal_lack_of_knowledge barrier_personal_forgetfulness
  barrier_personal_poor_attitude barrier_personal_lack_of_experience
  barrier_hospital_overcrowding barrier_hospital_lack_of_gloves_masks
  barrier_hospital_no_alcohol_sanitizer barrier_hospital_poor_facility_hygiene
  barrier_hospital_inadequate_supervision
  influence_training influence_role_models influence_hospital_environment
  influence_personal_motivation influence_supervision
  0 'No'
  1 'Yes'.

VALUE LABELS
  wash_before wash_after alcohol_rub gloves mask sharp_disposal
  needle_stick seniors_follow
  1 'Never'
  2 'Rarely'
  3 'Sometimes'
  4 'Often'
  5 'Always'.

VALUE LABELS time_pressure staff_support observation_influence
  0 'No'
  1 'Yes'
  2 'Maybe/Sometimes'.

VALUE LABELS knowledge_level adherence_level
  1 'Poor'
  2 'Moderate'
  3 'Good'.

EXECUTE.


VARIABLE LEVEL
  gender year_of_study ipc_training heard_5moments know_wash_tech aware_risks
  adherence_binary
  training_type_lecture training_type_workshop training_type_online_course
  training_type_bedside_teaching training_type_others
  barrier_personal_lack_of_knowledge barrier_personal_forgetfulness
  barrier_personal_poor_attitude barrier_personal_lack_of_experience
  barrier_hospital_overcrowding barrier_hospital_lack_of_gloves_masks
  barrier_hospital_no_alcohol_sanitizer barrier_hospital_poor_facility_hygiene
  barrier_hospital_inadequate_supervision
  influence_training influence_role_models influence_hospital_environment
  influence_personal_motivation influence_supervision
  (NOMINAL).

VARIABLE LEVEL
  wash_before wash_after alcohol_rub gloves mask sharp_disposal
  needle_stick seniors_follow time_pressure staff_support observation_influence
  knowledge_level adherence_level
  (ORDINAL).

VARIABLE LEVEL
  age knowledge_score total_adherence_score mean_adherence_score
  barriers_personal_sum barriers_hospital_sum barriers_total influences_sum
  (SCALE).

EXECUTE.


RELIABILITY
  /VARIABLES = wash_before wash_after alcohol_rub gloves mask sharp_disposal
  /SCALE ('IPC Adherence Scale') ALL
  /MODEL = ALPHA
  /STATISTICS = DESCRIPTIVE SCALE
  /SUMMARY = TOTAL.

* Knowledge items are binary (0/1); MODEL=ALPHA yields the KR-20 equivalent.
RELIABILITY
  /VARIABLES =
    moment_before_patient_contact
    moment_after_patient_contact
    moment_after_exposure_to_body_fluids
    moment_before_cleaning_aseptic_procedures
    moment_after_touching_patient_surroundings
  /SCALE ('Knowledge Scale KR-20') ALL
  /MODEL = ALPHA
  /STATISTICS = DESCRIPTIVE SCALE
  /SUMMARY = TOTAL.


FREQUENCIES VARIABLES = gender year_of_study age
  /STATISTICS = MEAN STDDEV MIN MAX
  /ORDER = ANALYSIS.

DESCRIPTIVES VARIABLES = age
  /STATISTICS = MEAN STDDEV MIN MAX.

FREQUENCIES VARIABLES =
  ipc_training heard_5moments know_wash_tech aware_risks
  training_type_lecture training_type_workshop training_type_online_course
  training_type_bedside_teaching training_type_others
  /ORDER = ANALYSIS.

DESCRIPTIVES VARIABLES =
  knowledge_score total_adherence_score mean_adherence_score
  barriers_personal_sum barriers_hospital_sum barriers_total influences_sum
  /STATISTICS = MEAN STDDEV MIN MAX.

FREQUENCIES VARIABLES = knowledge_level adherence_level
  /BARCHART PERCENT
  /ORDER = ANALYSIS.

FREQUENCIES VARIABLES =
  wash_before wash_after alcohol_rub gloves mask sharp_disposal
  needle_stick seniors_follow time_pressure staff_support observation_influence
  /ORDER = ANALYSIS.

FREQUENCIES VARIABLES =
  barrier_personal_lack_of_knowledge barrier_personal_forgetfulness
  barrier_personal_poor_attitude barrier_personal_lack_of_experience
  barrier_hospital_overcrowding barrier_hospital_lack_of_gloves_masks
  barrier_hospital_no_alcohol_sanitizer barrier_hospital_poor_facility_hygiene
  barrier_hospital_inadequate_supervision
  influence_training influence_role_models influence_hospital_environment
  influence_personal_motivation influence_supervision
  /ORDER = ANALYSIS.


T-TEST GROUPS = gender(1 2)
  /MISSING = ANALYSIS
  /VARIABLES = knowledge_score total_adherence_score barriers_total
  /CRITERIA = CI(0.95).

T-TEST GROUPS = ipc_training(0 1)
  /MISSING = ANALYSIS
  /VARIABLES = knowledge_score total_adherence_score
  /CRITERIA = CI(0.95).

T-TEST GROUPS = heard_5moments(0 1)
  /MISSING = ANALYSIS
  /VARIABLES = knowledge_score total_adherence_score
  /CRITERIA = CI(0.95).

T-TEST GROUPS = know_wash_tech(0 1)
  /MISSING = ANALYSIS
  /VARIABLES = total_adherence_score
  /CRITERIA = CI(0.95).

T-TEST GROUPS = year_of_study(4 5)
  /MISSING = ANALYSIS
  /VARIABLES = knowledge_score total_adherence_score
  /CRITERIA = CI(0.95).


ONEWAY total_adherence_score BY knowledge_level
  /STATISTICS DESCRIPTIVES HOMOGENEITY
  /MISSING ANALYSIS
  /POSTHOC = TUKEY ALPHA(0.05).

ONEWAY total_adherence_score BY seniors_follow
  /STATISTICS DESCRIPTIVES HOMOGENEITY
  /MISSING ANALYSIS
  /POSTHOC = TUKEY ALPHA(0.05).

ONEWAY knowledge_score total_adherence_score BY year_of_study
  /STATISTICS DESCRIPTIVES HOMOGENEITY
  /MISSING ANALYSIS.


CROSSTABS
  /TABLES = gender BY knowledge_level
  /CELLS = COUNT ROW EXPECTED
  /STATISTICS = CHISQ PHI.

CROSSTABS
  /TABLES = gender BY adherence_level
  /CELLS = COUNT ROW EXPECTED
  /STATISTICS = CHISQ PHI.

CROSSTABS
  /TABLES = year_of_study BY knowledge_level
  /CELLS = COUNT ROW EXPECTED
  /STATISTICS = CHISQ PHI.

CROSSTABS
  /TABLES = year_of_study BY adherence_level
  /CELLS = COUNT ROW EXPECTED
  /STATISTICS = CHISQ PHI.

CROSSTABS
  /TABLES = ipc_training BY knowledge_level
  /CELLS = COUNT ROW EXPECTED
  /STATISTICS = CHISQ PHI.

CROSSTABS
  /TABLES = ipc_training BY adherence_level
  /CELLS = COUNT ROW EXPECTED
  /STATISTICS = CHISQ PHI.

CROSSTABS
  /TABLES = know_wash_tech BY adherence_level
  /CELLS = COUNT ROW EXPECTED
  /STATISTICS = CHISQ PHI.

CROSSTABS
  /TABLES = knowledge_level BY adherence_level
  /CELLS = COUNT ROW EXPECTED
  /STATISTICS = CHISQ PHI.


CORRELATIONS
  /VARIABLES = knowledge_score total_adherence_score barriers_total
               influences_sum age
  /PRINT = TWOTAIL NOSIG
  /MISSING = PAIRWISE.

NONPAR CORR
  /VARIABLES = seniors_follow total_adherence_score knowledge_score
  /PRINT = SPEARMAN TWOTAIL
  /MISSING = PAIRWISE.


* Full model: all predictors of total adherence score.
REGRESSION
  /MISSING LISTWISE
  /STATISTICS COEFF OUTS CI(95) R ANOVA CHANGE
  /DEPENDENT total_adherence_score
  /METHOD = ENTER gender year_of_study knowledge_score ipc_training
                  age barriers_total seniors_follow influences_sum
  /SCATTERPLOT = (*ZRESID, *ZPRED)
  /RESIDUALS HISTOGRAM(ZRESID) NORMPROB(ZRESID).

* Hierarchical regression to test incremental contribution of knowledge
* and environmental factors.
REGRESSION
  /MISSING LISTWISE
  /STATISTICS COEFF OUTS R ANOVA CHANGE
  /DEPENDENT total_adherence_score
  /METHOD = ENTER gender year_of_study age
  /METHOD = ENTER knowledge_score
  /METHOD = ENTER ipc_training barriers_total seniors_follow influences_sum.


LOGISTIC REGRESSION VARIABLES adherence_binary
  /METHOD = ENTER gender year_of_study knowledge_level ipc_training
                  age barriers_total seniors_follow
  /CONTRAST (gender) = Indicator(1)
  /CONTRAST (year_of_study) = Indicator(4)
  /CONTRAST (knowledge_level) = Indicator(1)
  /CONTRAST (ipc_training) = Indicator(0)
  /PRINT = GOODFIT CI(95) SUMMARY
  /CRITERIA = PIN(0.05) POUT(0.10) ITERATE(20) CUT(0.5).


* NOTE: Update the OUTFILE path below before running.
SAVE OUTFILE = 'C:\path\to\1_data\cleaned\IPC_Adherence_OIU_Final.sav'
  /COMPRESSED.
