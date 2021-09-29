# Starting off with libraries
import pandas as pd
import numpy as np
import os
import warnings
from datetime import date
import reporting
import functions
import queues
import easygui
# import dropout


pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('max_colwidth', None)

warnings.filterwarnings('ignore')

# Delete output map first, to create a clean slate
os.makedirs('output', exist_ok=True)

today = date.today()

date = today.strftime('%B+%d,+%Y')
other_date = today.strftime('%Y%m%d')

programme_db = pd.read_csv('Overview of programme courses.csv')
programme_courses = programme_db['CourseID'].unique()


# Start defining the type of report we want to have
def normal_edx_pre(course_id, course_run):
    os.makedirs('output', exist_ok=True)

    filename = '2019T1_General_Pre-course+survey_' + date + '.csv'
    db = pd.read_csv(filename)
    course_code = course_id + ' ' + course_run

    db['course_code'] = db['course_code'].replace(np.nan, 'Unknown')
    db = db[db['course_code'].str.contains(course_code)]
    size = len(db)

    if db.empty is False:
        print(course_code + ' is being created \n')

        # Split up verified and audit
        db = db[db['Q2.3.2'].notnull()]
        audit = db[db['Q2.3.2'].str.contains('Audit')]
        verified = db[db['Q2.3.2'].str.contains('Verified')]

        # Q2.1 - How did you discover this course?
        functions.bar_chart(db, 'Q2.1')
        functions.standard_table(db, audit, verified, 'Q2.1')
        functions.other_list(audit, verified, 'Q2.1_8_TEXT')

        # Q2.2 - Were you actively looking for a course before enrolling in this course?
        functions.bar_chart(db, 'Q2.2')
        functions.standard_table(db, audit, verified, 'Q2.2')

        # Q2.2.1 - What type of course were you initially looking for?
        functions.bar_chart(db, 'Q2.2.1')
        functions.standard_table(db, audit, verified, 'Q2.2.1')

        # Q2.3 - What best describes your motivation for enrolling in this course? My motivation is
        functions.bar_chart(db, 'Q2.3')
        functions.standard_table(db, audit, verified, 'Q2.3')
        functions.other_list(audit, verified, 'Q2.3_5_TEXT')

        # Q2.3.1 - Could you elaborate on your reasons for taking this course?
        functions.other_list(audit, verified, 'Q2.3.1')

        # Q2.3.2 - What is your current type of enrollment in the course?
        functions.bar_chart(db, 'Q2.3.2')
        functions.count(db, 'Q2.3.2')

        # Q178 - Why did you enroll in the verified track?
        functions.normal_list(db, 'Q178')

        # Q2.4 - How important were the following factors in your decision to enrol in this course?
        functions.stacked_bar_pre(db, 'Q2.4', 'Q2.4_1', 'Q2.4_7')
        functions.categories(db, audit, verified, 'Q2.4', 'Q2.4_1', 'Q2.4_7',
                             ['Uniqueness of this course', 'Potential usefulness of this course',
                              'Interesting topic of this course', 'Lecturer(s) involved with this course',
                              'University(ies) involved with this course', 'That the course is offered online',
                              'The possibility to receive a certificate or credentials'])

        # Q3.1 - What do you think might be the biggest challenge in completing this course for you?
        functions.bar_chart(db, 'Q3.1')
        functions.standard_table(db, audit, verified, 'Q3.1')
        functions.other_list(audit, verified, 'Q3.1_5_TEXT')

        # Q3.2 - How important are the following elements for you in this course?
        functions.stacked_bar_pre(db, 'Q3.2', 'Q108_1', 'Q108_4')
        functions.categories(db, audit, verified, 'Q3.2', 'Q108_1', 'Q108_4', ['Uniqueness of this course',
                                                                               'Potential usefulness of this course',
                                                                               'Interesting topic of this course',
                                                                               'Lecturer(s) involved with this course'])

        # Q3.3 - On average, how many hours per week can you dedicate to this course?
        functions.standard_statistics_mooc(db, audit, verified, 'Q3.3_1')

        # Q4.1 - Which best describes your familiarity with TU Delft (Delft University of Technology)?
        functions.bar_chart(db, 'Q4.1')
        functions.standard_table(db, audit, verified, 'Q4.1')

        # Q4.2 - Which of the following best describes your current situation?
        functions.bar_chart(db, 'Q4.2')
        functions.standard_table(db, audit, verified, 'Q4.2')
        functions.other_list(audit, verified, 'Q4.2_7_TEXT')

        # Q4.2.1 - Which of the following most closely matches your job title?
        functions.bar_chart(db, 'Q4.2.1')
        functions.standard_table(db, audit, verified, 'Q4.2.1')
        functions.other_list(audit, verified, 'Q4.2.1_15_TEXT')

        # Q4.2.4 - In which industry do you currently work?
        functions.standard_table(db, audit, verified, 'Q4.2.4_1')
        functions.other_list(audit, verified, 'Q4.2.1_15_TEXT')

        # Q4.3 - What is your age?
        functions.standard_statistics_mooc(db, audit, verified, 'Q4.3_1')

        # Q4.4 - What is your gender?
        functions.bar_chart(db, 'Q4.4')
        functions.standard_table(db, audit, verified, 'Q4.4')

        # Q4.5 - What is your (first) nationality? Please select the corresponding country.
        functions.standard_table(db, audit, verified, 'Q4.5_1')
        functions.standard_table(db, audit, verified, 'Q4.5_2')

        # Q4.6 - What is the highest degree or level of education you have completed?
        functions.bar_chart(db, 'Q4.6')
        functions.standard_table(db, audit, verified, 'Q4.6')
        functions.other_list(audit, verified, 'Q4.6_9_TEXT')

        resource_queue, name_queue = queues.find_edx_pre_queue(course_id, course_run)

        if course_id in programme_courses:
            functions.programme_expectations(db, resource_queue, name_queue)

        name_dict = dict(zip(resource_queue, name_queue))

        reporting.HTMLDocument(other_date + ' Pre-survey results ' + course_code, resource_queue, name_dict)

        print('\n Progress check: We would lose ', db['Progress'][db['Progress'] < 50].count(), 'values out of ',
              len(db))
        print('Duration check: We would lose ', db['Duration (in seconds)'][db['Duration (in seconds)'] < 60].count(),
              'values out of ', len(db))
        print('Enrollment check: We would lose ', (size - len(audit) - len(verified)), 'values out of', len(db), '\n')

    else:
        print('\n', course_code, 'has no responses (yet)!')

    print('-------------------------------------')


def normal_profed_pre(course_id, course_run):
    os.makedirs('output', exist_ok=True)

    filename = '2019T1_General_Pre-course+survey_' + date + '.csv'
    db = pd.read_csv(filename)
    course_code = course_id + ' ' + course_run

    db['course_code'] = db['course_code'].replace(np.nan, 'Unknown')
    db = db[db['course_code'].str.contains(course_code)]

    if db.empty is False:
        print(course_code + ' is being created \n')

        # Q2.1 - How did you discover this course?
        functions.bar_chart(db, 'Q2.1')
        functions.standard_table_profed(db, 'Q2.1')
        functions.other_total(db, 'Q2.1_8_TEXT')

        # Q2.2 - Were you actively looking for a course before enrolling in this course?
        functions.bar_chart(db, 'Q2.2')
        functions.standard_table_profed(db, 'Q2.2')

        # Q2.2.1 - What type of course were you initially looking for?
        functions.bar_chart(db, 'Q2.2.1')
        functions.standard_table_profed(db, 'Q2.2.1')

        # Q2.3 - What best describes your motivation for enrolling in this course? My motivation is
        functions.bar_chart(db, 'Q2.3')
        functions.standard_table_profed(db, 'Q2.3')
        functions.other_total(db, 'Q2.3_5_TEXT')

        # Q2.3.1 - Could you elaborate on your reasons for taking this course?
        functions.other_total(db, 'Q2.3.1')

        # Q2.4 - How important were the following factors in your decision to enrol in this course?
        functions.stacked_bar_pre(db, 'Q2.4', 'Q2.4_1', 'Q2.4_7')
        functions.categories_total(db, 'Q2.4', 'Q2.4_1', 'Q2.4_7', ['Uniqueness of this course',
                                                                    'Potential usefulness of this course',
                                                                    'Interesting topic of this course',
                                                                    'Lecturer(s) involved with this course',
                                                                    'University(ies) involved with this course',
                                                                    'That the course is offered online',
                                                                    'The possibility to receive a certificate or '
                                                                    'credentials'])

        # Q3.1 - What do you think might be the biggest challenge in completing this course for you?
        functions.bar_chart(db, 'Q3.1')
        functions.standard_table_profed(db, 'Q3.1')
        functions.other_total(db, 'Q3.1_5_TEXT')

        # Q3.2 - How important are the following elements for you in this course?
        functions.stacked_bar_pre(db, 'Q3.2', 'Q108_1', 'Q108_4')
        functions.categories_total(db, 'Q3.2', 'Q108_1', 'Q108_4', ['Uniqueness of this course',
                                                                    'Potential usefulness of this course',
                                                                    'Interesting topic of this course',
                                                                    'Lecturer(s) involved with this course'])

        # Q3.3 - On average, how many hours per week can you dedicate to this course?
        functions.standard_statistics_profed(db, 'Q3.3_1')

        # Q4.1 - Which best describes your familiarity with TU Delft (Delft University of Technology)?
        functions.bar_chart(db, 'Q4.1')
        functions.standard_table_profed(db, 'Q4.1')

        # Q4.2 - Which of the following best describes your current situation?
        functions.bar_chart(db, 'Q4.2')
        functions.standard_table_profed(db, 'Q4.2')
        functions.other_total(db, 'Q4.2_7_TEXT')

        # Q4.2.2 - What is your current job title?
        functions.other_total(db, 'Q4.2.2')

        # Q4.2.3 - What is your educational background?
        # (e.g. I have a Bachelor's degree in ... / MSc in ... / training on ...)
        functions.other_total(db, 'Q4.2.3')

        # Q4.2.4 - In which industry do you currently work?
        functions.standard_table_profed(db, 'Q4.2.4_1')
        functions.other_total(db, 'Q4.2.1_15_TEXT')

        # Q4.3 - What is your age?
        functions.standard_statistics_profed(db, 'Q4.3_1')

        # Q4.4 - What is your gender?
        functions.bar_chart(db, 'Q4.4')
        functions.standard_table_profed(db, 'Q4.4')

        # Q4.5 - What is your (first) nationality? Please select the corresponding country.
        functions.standard_table_profed(db, 'Q4.5_1')
        functions.standard_table_profed(db, 'Q4.5_2')

        # Q4.6 - What is the highest degree or level of education you have completed?
        functions.bar_chart(db, 'Q4.6')
        functions.standard_table_profed(db, 'Q4.6')
        functions.other_total(db, 'Q4.6_9_TEXT')

        resource_queue, name_queue = queues.find_profed_pre_queue(course_id, course_run)

        if course_id in programme_courses:
            functions.programme_expectations(db, resource_queue, name_queue)

        name_dict = dict(zip(resource_queue, name_queue))

        reporting.HTMLDocument(other_date + ' Pre-survey results ' + course_code, resource_queue, name_dict)

        print('\n Progress check: We would lose ', db['Progress'][db['Progress'] < 50].count(), 'values out of ',
              len(db))
        print('Duration check: We would lose ', db['Duration (in seconds)'][db['Duration (in seconds)'] < 60].count(),
              'values out of ', len(db), '\n')

    else:
        print(course_code, 'has no responses (yet)!')

    print('-------------------------------------')


def normal_edx_post(course_id, course_run):
    os.makedirs('output', exist_ok=True)

    filename = '2019T1_General_Post-course+survey_' + date + '.csv'
    db = pd.read_csv(filename)
    course_code = course_id + ' ' + course_run

    db['course_code'] = db['course_code'].replace(np.nan, 'Unknown')
    db = db[db['course_code'].str.contains(course_code)]
    size = len(db)

    if db.empty is False:
        print(course_code + ' is being created \n')

        # Split up verified and audit
        db = db[db['Q202'].notnull()]
        audit = db[db['Q202'].str.contains('Audit')]
        verified = db[db['Q202'].str.contains('Verified')]

        # Q2.1 - Since the start of the course, how would you describe your participation level?
        functions.bar_chart(db, 'Q2.1')
        functions.standard_table(db, audit, verified, 'Q2.1')

        # Q2.2.1 - Could you please describe the reason(s) why you did not start the course?'
        functions.normal_list(db, 'Q2.2.1')

        # Q2.2.2 - Could you please describe which specific parts of the course you were interested in and why?'
        functions.normal_list(db, 'Q2.2.2')

        # Q3.1 - On a scale from 1 to 10, what overall grade would you give this course? (1: very poor, 10: excellent)
        functions.standard_statistics_mooc(db, audit, verified, 'Q3.1_1')

        # Q3.3 - What was the most valuable in this course for you?
        functions.normal_list(db, 'Q3.3')

        # Q4.4 - Which aspects of this course would you like us to improve?
        functions.normal_list(db, 'Q4.4')

        # Q202 - What is your current type of enrollment in the course?
        functions.bar_chart(db, 'Q202')
        functions.count(db, 'Q202')

        # Q204 - What additional value did you get from the verified track?
        functions.normal_list(db, 'Q204')

        # Q4.5 - How would you rate the following aspects of the course? The course was ...
        functions.stacked_bar_post(db, 'Q4.5', 'Q4.5_1.1', 'Q4.5_3.1')
        functions.standard_table(db, audit, verified, 'Q4.5_1.1')
        functions.standard_table(db, audit, verified, 'Q4.5_2.1')
        functions.standard_table(db, audit, verified, 'Q4.5_3.1')

        # Q4.6 - How would you rate the difficulty level of the course?
        functions.describing_the_course(db, 'Q4.6')
        functions.standard_table(db, audit, verified, 'Q4.6')

        # Q4.7 - How would you describe the amount of work required for the course?
        functions.describing_the_course(db, 'Q4.7')
        functions.standard_table(db, audit, verified, 'Q4.7')

        # Q4.8 - How would you describe the breadth of topics covered in this course?
        functions.describing_the_course(db, 'Q4.8')
        functions.standard_table(db, audit, verified, 'Q4.8')

        # Q4.9 - How would you describe the length of the course (i.e. number of weeks)?
        functions.describing_the_course(db, 'Q4.9')
        functions.standard_table(db, audit, verified, 'Q4.9')

        # Q5.1 - On average, how many hours did you work on this course per week?
        functions.standard_statistics_mooc(db, audit, verified, 'Q5.1_1')

        # Q4.2 - Which elements of the course did you use or participate in?
        functions.split_choose_all_that_apply_mooc(db, audit, verified, 'Q4.2')

        # Q4.2.1 - How satisfied were you with the following elements of this course?
        functions.stacked_bar_post_split(audit, verified, 'Q5.2.1_x1')
        functions.standard_table(db, audit, verified, 'Q5.2.1_x1')
        functions.stacked_bar_post_split(audit, verified, 'Q5.2.1_x2')
        functions.standard_table(db, audit, verified, 'Q5.2.1_x2')
        functions.stacked_bar_post_split(audit, verified, 'Q5.2.1_x3')
        functions.standard_table(db, audit, verified, 'Q5.2.1_x3')
        functions.stacked_bar_post_split(audit, verified, 'Q5.2.1_x4')
        functions.standard_table(db, audit, verified, 'Q5.2.1_x4')

        # Q4.2.2 - How valuable do you feel were the following elements of this course?
        functions.stacked_bar_post_split(audit, verified, 'Q5.2.2_x1')
        functions.standard_table(db, audit, verified, 'Q5.2.2_x1')
        functions.stacked_bar_post_split(audit, verified, 'Q5.2.2_x2')
        functions.standard_table(db, audit, verified, 'Q5.2.2_x2')
        functions.stacked_bar_post_split(audit, verified, 'Q5.2.2_x3')
        functions.standard_table(db, audit, verified, 'Q5.2.2_x3')
        functions.stacked_bar_post_split(audit, verified, 'Q5.2.2_x4')
        functions.standard_table(db, audit, verified, 'Q5.2.2_x4')

        # Q4.2.3 - Why didn't you use or participate in [QID117-ChoiceGroup-UnselectedChoices]?
        functions.normal_list(db, 'Q4.2.3')

        # Q4.3 - What was the biggest challenge in completing this course?
        functions.bar_chart(db, 'Q4.3')
        functions.standard_table(db, audit, verified, 'Q4.3')
        functions.other_total(db, 'Q4.3_5_TEXT')

        # Q4.3.1 - At the beginning of the survey you said that you participated in the course, but stopped
        # participating along the way. Why did you not participate in the course until the end?
        # Choose the answer that applies the most.
        functions.bar_chart(db, 'Q4.3.1')
        functions.standard_table(db, audit, verified, 'Q4.3.1')
        functions.other_total(db, 'Q4.3.1_6_TEXT')

        resource_queue, name_queue = queues.find_edx_post_queue(course_run, course_id)

        if course_id in programme_courses:
            functions.programme_questions(db, resource_queue, name_queue)

        if course_id is 'IB01x':
            functions.ib_questions(db, resource_queue, name_queue)

        functions.nps_score(db, resource_queue, name_queue)

        name_dict = dict(zip(resource_queue, name_queue))

        reporting.HTMLDocument(other_date + ' Post-survey results ' + course_code, resource_queue, name_dict)

        cols = ['Progress', 'Duration (in seconds)']
        db[cols] = db[cols].applymap(np.int64)
        print('\n Progress check: We would lose ', db['Progress'][db['Progress'] < 50].count(), 'values out of ',
              len(db))
        print('Duration check: We would lose ', db['Duration (in seconds)'][db['Duration (in seconds)'] < 60].count(),
              'values out of ', len(db))
        print('Enrollment check: We would lose ', (size - len(audit) - len(verified)), 'values out of', len(db), '\n')

    else:
        print('\n', course_code, 'has no responses (yet)!')

    print('-------------------------------------')


def normal_profed_post(course_id, course_run):
    os.makedirs('output', exist_ok=True)

    filename = '2019T1_General_Post-course+survey_' + date + '.csv'
    db = pd.read_csv(filename)
    course_code = course_id + ' ' + course_run

    db['course_code'] = db['course_code'].replace(np.nan, 'Unknown')
    db = db[db['course_code'].str.contains(course_code)]

    if db.empty is False:
        print(course_code + ' is being created \n')

        # Q2.1 - Since the start of the course, how would you describe your participation level?
        functions.bar_chart(db, 'Q2.1')
        functions.standard_table_profed(db, 'Q2.1')

        # Q2.2.1 - Could you please describe the reason(s) why you did not start the course?'
        functions.normal_list(db, 'Q2.2.1')

        # Q2.2.2 - Could you please describe which specific parts of the course you were interested in and why?'
        functions.normal_list(db, 'Q2.2.2')

        # Q3.1 - On a scale from 1 to 10, what overall grade would you give this course? (1: very poor, 10: excellent)
        functions.standard_statistics_profed(db, 'Q3.1_1')

        # Q3.3 - What was the most valuable in this course for you?
        functions.normal_list(db, 'Q3.3')

        # Q4.4 - Which aspects of this course would you like us to improve?
        functions.normal_list(db, 'Q4.4')

        # Q4.5 - How would you rate the following aspects of the course? The course was ...
        functions.stacked_bar_post(db, 'Q4.5', 'Q4.5_1.1', 'Q4.5_3.1')
        functions.standard_table_profed(db, 'Q4.5_1.1')
        functions.standard_table_profed(db, 'Q4.5_2.1')
        functions.standard_table_profed(db, 'Q4.5_3.1')

        # Q4.6 - How would you rate the difficulty level of the course?
        functions.describing_the_course(db, 'Q4.6')
        functions.standard_table_profed(db, 'Q4.6')

        # Q4.7 - How would you describe the amount of work required for the course?
        functions.describing_the_course(db, 'Q4.7')
        functions.standard_table_profed(db, 'Q4.7')

        # Q4.8 - How would you describe the breadth of topics covered in this course?
        functions.describing_the_course(db, 'Q4.8')
        functions.standard_table_profed(db, 'Q4.8')

        # Q4.9 - How would you describe the length of the course (i.e. number of weeks)?
        functions.describing_the_course(db, 'Q4.9')
        functions.standard_table_profed(db, 'Q4.9')

        # Q5.1 - On average, how many hours did you work on this course per week?
        functions.standard_statistics_profed(db, 'Q5.1_1')

        # Q4.2 - Which elements of the course did you use or participate in?
        functions.split_choose_all_that_apply_profed(db, 'Q4.2')

        # Q4.2.1 - How satisfied were you with the following elements of this course?
        functions.stacked_bar_post_profed(db, 'Q4.2.1', 'Q5.2.1_x1', 'Q5.2.1_x4')
        functions.categories_total_profed(db, 'Q4.2.1', 'Q5.2.1_x1', 'Q5.2.1_x4', ['Videos', 'Reading materials',
                                                                                   'Forums',
                                                                                   'Exercises, quizzes, assignments'])

        # Q4.2.2 - How valuable do you feel were the following elements of this course?
        functions.stacked_bar_post_profed(db, 'Q4.2.2', 'Q5.2.2_x1', 'Q5.2.2_x4')
        functions.categories_total_profed(db, 'Q4.2.2', 'Q5.2.2_x1', 'Q5.2.2_x4', ['Videos', 'Reading materials',
                                                                                   'Forums',
                                                                                   'Exercises, quizzes, assignments'])

        # Q4.2.3 - Why didn't you use or participate in [QID117-ChoiceGroup-UnselectedChoices]?
        functions.normal_list(db, 'Q4.2.3')

        # Q4.3 - What was the biggest challenge in completing this course?
        functions.bar_chart(db, 'Q4.3')
        functions.standard_table_profed(db, 'Q4.3')
        functions.other_total(db, 'Q4.3_5_TEXT')

        # Q4.3.1 - At the beginning of the survey you said that you participated in the course, but stopped
        # participating along the way. Why did you not participate in the course until the end?
        # Choose the answer that applies the most.
        functions.bar_chart(db, 'Q4.3.1')
        functions.standard_table_profed(db, 'Q4.3.1')
        functions.other_total(db, 'Q4.3.1_6_TEXT')

        resource_queue, name_queue = queues.find_profed_post_queue(course_run, course_id)

        if len(db['Q4.3.1']) > 3:
            del resource_queue[-3]
            del name_queue[-2]

        if course_id in programme_courses:
            functions.programme_questions(db, resource_queue, name_queue)

        name_dict = dict(zip(resource_queue, name_queue))

        reporting.HTMLDocument(other_date + ' Post-survey results ' + course_code, resource_queue, name_dict)

        print('\n Progress check: We would lose ', db['Progress'][db['Progress'] < 50].count(), 'values out of ',
              len(db))
        print('Duration check: We would lose ', db['Duration (in seconds)'][db['Duration (in seconds)'] < 60].count(),
              'values out of ', len(db), '\n')

    else:
        print('\n', course_code, 'has no responses (yet)!')

    print('-------------------------------------')


# --------------------------------------------
# To-do
normal_edx_post('MIND101x', '1T2020')
normal_edx_post('RI101x', '2T2020')
normal_edx_post('DDA691NLx', '2T2020')
normal_edx_post('UnixTx', '3T2020')
normal_profed_pre('RAIL_02P', '2020_Q4')
normal_profed_post('RAIL_02p', '2020_Q4')
normal_profed_pre('RAIL_04P', '2020_Q4')
normal_profed_post('RAIL_04p', '2020_Q4')
normal_edx_post('TP201x', '3T2020')
normal_edx_post('TP101x', '3T2020')


def graphical_method():
    profed = easygui.ynbox('Is it ProfEd or edX?', 'Version', ['ProfEd', 'MOOC'])
    pre = easygui.ynbox('Is it pre or post?', 'Version', ['Pre', 'Post'])
    input_id = easygui.enterbox('Please enter the course ID', 'Course_ID')
    input_run = easygui.enterbox('Please enter the course run', 'Course_run')

    if profed is True:
        if pre is True:
            normal_profed_pre(input_id, input_run)
        else:
            normal_profed_post(input_id, input_run)
    else:
        if pre is True:
            normal_edx_pre(input_id, input_run)
        else:
            normal_edx_post(input_id, input_run)


def to_do_list_method():
    to_do_list = pd.read_csv('To-do.csv', delimiter='+').reset_index()

    # This is all specific for the list
    for i in range(len(to_do_list)):
        normal_edx_pre(to_do_list.iloc[i, 0], to_do_list.iloc[i, 1])
        normal_edx_post(to_do_list.iloc[i, 0], to_do_list.iloc[i, 1])

        # if i <= 9:
        #     normal_edx_post(to_do_list.iloc[i, 0], to_do_list.iloc[i, 1])
        # if 18 >= i >= 10:
        #     normal_edx_pre(to_do_list.iloc[i, 0], to_do_list.iloc[i, 1])
        #     normal_edx_post(to_do_list.iloc[i, 0], to_do_list.iloc[i, 1])
        # if i >= 18:
        #     normal_edx_pre(to_do_list.iloc[i, 0], to_do_list.iloc[i, 1])


# to_do_list_method()
# graphical_method()

# dropout.counts(date)


if __name__ == '__main__':
    print('All reports are in the folder!')
