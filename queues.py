def find_edx_pre_queue(course_id, run):
    resource_queue = ['Q2.1.jpg', 'Q2.1_table.png', 'Q2.1_8_TEXT_other_audit.txt', 'Q2.1_8_TEXT_other_verified.txt',
                      'Q2.2.jpg', 'Q2.2_table.png', 'Q2.2.1.jpg', 'Q2.2.1_table.png', 'Q2.3.jpg', 'Q2.3_table.png',
                      'Q2.3_5_TEXT_other_audit.txt', 'Q2.3_5_TEXT_other_verified.txt', 'Q2.3.1_other_audit.txt',
                      'Q2.3.1_other_verified.txt', 'Q2.3.2.jpg', 'Q2.3.2_table.png', 'Q178_list.txt', 'Q2.4.jpg',
                      'Q2.4_audit_table.png', 'Q2.4_verified_table.png', 'Q2.4_total_table.png', 'Q3.1.jpg',
                      'Q3.1_table.png', 'Q3.1_5_TEXT_other_audit.txt', 'Q3.1_5_TEXT_other_verified.txt',
                      'Q3.2.jpg', 'Q3.2_audit_table.png', 'Q3.2_verified_table.png', 'Q3.2_total_table.png',
                      'Q3.3_1_statistics_table.png', 'Q4.1.jpg', 'Q4.1_table.png', 'Q4.2.jpg', 'Q4.2_table.png',
                      'Q4.2_7_TEXT_other_audit.txt', 'Q4.2_7_TEXT_other_verified.txt', 'Q4.2.1.jpg',
                      'Q4.2.1_table.png', 'Q4.2.1_15_TEXT_other_audit.txt', 'Q4.2.1_15_TEXT_other_verified.txt',
                      'Q4.2.4_1_table.png', 'Q4.3_1_statistics_table.png', 'Q4.4.jpg', 'Q4.4_table.png',
                      'Q4.5_1_table.png', 'Q4.5_2_table.png', 'Q4.6.jpg', 'Q4.6_table.png',
                      'Q4.6_9_TEXT_other_audit.txt', 'Q4.6_9_TEXT_other_verified.txt']

    name_queue = ['Q2.1 - How did you discover this course?', 'Q2.1 Table', 'Other - Audit', 'Other - Verified',
                  'Q2.2 - Were you actively looking for a course before enrolling in this course?', 'Q2.2 Table',
                  'Q2.2.1 - What type of course were you initially looking for?', 'Q2.2.1 Table',
                  'Q2.3 - What best describes your motivation for enrolling in this course? My motivation is ...',
                  'Q2.3 Table', 'Q2.3_5 Other - Audit', 'Q2.3_5 Other - Verified',
                  'Q2.3.1 - Could you elaborate on your reasons for taking this course? - Audit',
                  'Q2.3.1 - Could you elaborate on your reasons for taking this course? - Verified',
                  'Q2.3.2 - What is your current type of enrollment in the course?', 'Q2.3.2 Table',
                  'Q178 - Why did you enroll in the verified track?',
                  'Q2.4 - How important were the following factors in your decision to enrol in this course?',
                  'Audit', 'Verified', 'Total',
                  'Q3.1 - What do you think might be the biggest challenge in completing this course for you?',
                  'Q3.1 Table', 'Other - Audit', 'Other - Verified',
                  'Q3.2 - How important are the following elements for you in this course?', 'Audit', 'Verified',
                  'Total', 'Q3.3 - On average, how many hours per week can you dedicate to this course?',
                  'Q4.1 - Which best describes your familiarity with TU Delft (Delft University of Technology)?',
                  'Q4.1 Table', 'Q4.2 - Which of the following best describes your current situation?',
                  'Q4.2 Table', 'Other - Audit', 'Other - Verified',
                  'Q4.2.1 - Which of the following most closely matches your job title?', 'Q4.2.1 Table',
                  'Other - Audit', 'Other - Verified', 'Q4.2.4 - In which industry do you currently work?',
                  'Q4.3 - What is your age?', 'Q4.4 - What is your gender?', 'Q4.4 Table',
                  'Q4.5 - What is your (first) nationality? Please select the corresponding country.', 'Others',
                  'Q4.6 - What is the highest degree or level of education you have completed?', 'Q4.6 Table',
                  'Other - Audit', 'Other - Verified']

    course_code = course_id + ' ' + run

    if 'CircularX 3T2020' in course_code:
        resource_queue.append('Q185.jpg')
        name_queue.append('Q185 - What kind of sustainability ideas, methods, '
                          'or tools are you looking for in this MOOC?')

    if 'RAIL_01P' in course_id:
        resource_queue.extend(['Q145.jpg', 'Q145_table.png', 'Q146.jpg', 'Q146_table.png', 'Q146_5_other.txt'])

    return resource_queue, name_queue


def find_profed_pre_queue(course_id, run):
    resource_queue = ['Q2.1.jpg', 'Q2.1_table.png', 'Q2.1_8_TEXT_other.txt', 'Q2.2.jpg', 'Q2.2_table.png',
                      'Q2.2.1.jpg', 'Q2.2.1_table.png', 'Q2.3.jpg', 'Q2.3_table.png', 'Q2.3_5_TEXT_other.txt',
                      'Q2.3.1_other.txt', 'Q2.4.jpg', 'Q2.4_total_table.png', 'Q3.1.jpg', 'Q3.1_table.png',
                      'Q3.1_5_TEXT_other.txt', 'Q3.2.jpg', 'Q3.2_total_table.png', 'Q3.3_1_statistics_table.png',
                      'Q4.1.jpg', 'Q4.1_table.png', 'Q4.2.jpg', 'Q4.2_table.png', 'Q4.2_7_TEXT_other.txt',
                      'Q4.2.2_other.txt', 'Q4.2.3_other.txt', 'Q4.2.4_1_table.png', 'Q4.3_1_statistics_table.png',
                      'Q4.4.jpg', 'Q4.4_table.png', 'Q4.5_1_table.png', 'Q4.5_2_table.png', 'Q4.6.jpg',
                      'Q4.6_table.png', 'Q4.6_9_TEXT_other.txt']

    name_queue = ['Q2.1 - How did you discover this course?', 'Q2.1 Table', 'Other',
                  'Q2.2 - Were you actively looking for a course before enrolling in this course?', 'Q2.2 Table',
                  'Q2.2.1 - What type of course were you initially looking for?', 'Q2.2.1 Table',
                  'Q2.3 - What best describes your motivation for enrolling in this course? My motivation is ...',
                  'Q2.3 Table', 'Q2.3_5 Other',
                  'Q2.3.1 - Could you elaborate on your reasons for taking this course?',
                  'Q2.4 - How important were the following factors in your decision to enrol in this course?', 'Total',
                  'Q3.1 - What do you think might be the biggest challenge in completing this course for you?',
                  'Q3.1 Table', 'Other',
                  'Q3.2 - How important are the following elements for you in this course?', 'Total',
                  'Q3.3 - On average, how many hours per week can you dedicate to this course?',
                  'Q4.1 - Which best describes your familiarity with TU Delft (Delft University of Technology)?',
                  'Q4.1 Table', 'Q4.2 - Which of the following best describes your current situation?', 'Q4.2 Table',
                  'Other', 'Q4.2.2 - What is your current job title?', 'Q4.2.3 - What is your educational background? '
                  '(e.g. I have a Bachelors degree in ... / MSc in ... / training on ...)',
                  'Q4.2.4 - In which industry do you currently work?', 'Q4.3 - What is your age?',
                  'Q4.4 - What is your gender?', 'Q4.4 Table',
                  'Q4.5 - What is your (first) nationality? Please select the corresponding country.', 'Others',
                  'Q4.6 - What is the highest degree or level of education you have completed?', 'Q4.6 Table', 'Other']

    return resource_queue, name_queue


def find_edx_post_queue(course_id, run):
    resource_queue = ['Q2.1.jpg', 'Q2.1_table.png', 'Q2.2.1_list.txt', 'Q2.2.2_list.txt', 'Q3.1_1_statistics_table.png',
                      'Q3.3_list.txt', 'Q4.4_list.txt', 'Q202.jpg', 'Q202_table.png', 'Q204_list.txt', 'Q4.5.jpg',
                      'Q4.5_1.1_table.png', 'Q4.5_2.1_table.png', 'Q4.5_3.1_table.png', 'Q4.6.jpg', 'Q4.6_table.png',
                      'Q4.7.jpg', 'Q4.7_table.png', 'Q4.8.jpg', 'Q4.8_table.png', 'Q4.9.jpg', 'Q4.9_table.png',
                      'Q5.1_1_statistics_table.png', 'Q4.2.jpg', 'Q4.2_table.png', 'Q5.2.1_x1.jpg',
                      'Q5.2.1_x1_table.png', 'Q5.2.1_x2.jpg', 'Q5.2.1_x2_table.png', 'Q5.2.1_x3.jpg',
                      'Q5.2.1_x3_table.png', 'Q5.2.1_x4.jpg', 'Q5.2.1_x4_table.png', 'Q5.2.2_x1.jpg',
                      'Q5.2.2_x1_table.png', 'Q5.2.2_x2.jpg', 'Q5.2.2_x2_table.png', 'Q5.2.2_x3.jpg',
                      'Q5.2.2_x3_table.png', 'Q5.2.2_x4.jpg', 'Q5.2.2_x4_table.png', 'Q4.2.3_list.txt',
                      'Q4.3.jpg', 'Q4.3_table.png', 'Q4.3_5_TEXT_other.txt', 'Q4.3.1.jpg',
                      'Q4.3.1_table.png', 'Q4.3.1_6_TEXT_other.txt']

    name_queue = ['Q2.1 - Since the start of the course, how would you describe your participation level?',
                  'Q2.1 Table', 'Q2.2.1 - Could you please describe the reason(s) why you did not start the course?',
                  'Q2.2.2 - Could you please describe which specific parts of '
                  'the course you were interested in and why?',
                  'Q3.1 - On a scale from 1 to 10, what overall grade would you give this course? '
                  '(1: very poor, 10: excellent)',
                  'Q3.3 - What was the most valuable in this course for you?',
                  'Q4.4 - Which aspects of this course would you like us to improve?',
                  'Q202 - What is your current type of enrollment in the course?', 'Q202 Table',
                  'Q204 - What additional value did you get from the verified track?',
                  'Q4.5 - How would you rate the following aspects of the course? The course was ...',
                  'Unique', 'Useful', 'Interesting',
                  'Q4.6 - How would you rate the difficulty level of the course?', 'Q4.6 Table',
                  'Q4.7 - How would you describe the amount of work required for the course?', 'Q4.7 Table',
                  'Q4.8 - How would you describe the breadth of topics covered in this course?', 'Q4.8 Table',
                  'Q4.9 - How would you describe the length of the course (i.e. number of weeks)?', 'Q4.9 Table',
                  'Q5.1 - On average, how many hours did you work on this course per week?',
                  'Q4.2 - Which elements of the course did you use or participate in?', 'Q4.2 Table',
                  'Q4.2.1 - How satisfied were you with the following elements of this course? - Videos', 'Table',
                  'Q4.2.1 - How satisfied were you with the following elements of this course? - Reading materials',
                  'Table',
                  'Q4.2.1 - How satisfied were you with the following elements of this course? - Forums', 'Table',
                  'Q4.2.1 - How satisfied were you with the following elements of this course? '
                  '- Exercises, quizzes, assignments', 'Table',
                  'Q4.2.2 - How valuable do you feel were the following elements of this course? - Videos', 'Table',
                  'Q4.2.2 - How valuable do you feel were the following elements of this course? '
                  '- Reading materials', 'Table',
                  'Q4.2.2 - How valuable do you feel were the following elements of this course? - Forums', 'Table',
                  'Q4.2.2 - How valuable do you feel were the following elements of this course? '
                  '- Exercises, quizzes, assignments', 'Table',
                  'Q4.2.3 - Why didnt you use or participate in [QID117-ChoiceGroup-UnselectedChoices]?',
                  'Q4.3 - What was the biggest challenge in completing this course?', 'Table', 'Other',
                  'Q4.3.1 - At the beginning of the survey you said that you participated in the course, but '
                  'stopped participating along the way. Why did you not participate in the course until the end? '
                  'Choose the answer that applies the most.', 'Table', 'Other']

    return resource_queue, name_queue


def find_profed_post_queue(course_id, run):
    resource_queue = ['Q2.1.jpg', 'Q2.1_table.png',
                      'Q2.2.1_list.txt',
                      'Q2.2.2_list.txt',
                      'Q3.1_1_statistics_table.png',
                      'Q3.3_list.txt',
                      'Q4.4_list.txt',
                      'Q4.5.jpg', 'Q4.5_1.1_table.png', 'Q4.5_2.1_table.png', 'Q4.5_3.1_table.png',
                      'Q4.6.jpg', 'Q4.6_table.png',
                      'Q4.7.jpg', 'Q4.7_table.png',
                      'Q4.8.jpg', 'Q4.8_table.png',
                      'Q4.9.jpg', 'Q4.9_table.png',
                      'Q5.1_1_statistics_table.png',
                      'Q4.2.jpg', 'Q4.2_table.png',
                      'Q4.2.1.jpg',
                      'Q4.2.2.jpg',
                      'Q4.2.3_list.txt',
                      'Q4.3.jpg', 'Q4.3_table.png', 'Q4.3_5_TEXT_other.txt',
                      'Q4.3.1.jpg',
                      'Q4.3.1_table.png', 'Q4.3.1_6_TEXT_other.txt']

    name_queue = ['Q2.1 - Since the start of the course, how would you describe your participation level?',
                  'Q2.1 Table',
                  'Q2.2.1 - Could you please describe the reason(s) why you did not start the course?',
                  'Q2.2.2 - Could you please describe which specific parts of '
                  'the course you were interested in and why?',
                  'Q3.1 - On a scale from 1 to 10, what overall grade would you give this course? '
                  '(1: very poor, 10: excellent)',
                  'Q3.3 - What was the most valuable in this course for you?',
                  'Q4.4 - Which aspects of this course would you like us to improve?',
                  'Q4.5 - How would you rate the following aspects of the course? The course was ...',
                  'Unique', 'Useful', 'Interesting',
                  'Q4.6 - How would you rate the difficulty level of the course?', 'Q4.6 Table',
                  'Q4.7 - How would you describe the amount of work required for the course?', 'Q4.7 Table',
                  'Q4.8 - How would you describe the breadth of topics covered in this course?', 'Q4.8 Table',
                  'Q4.9 - How would you describe the length of the course (i.e. number of weeks)?', 'Q4.9 Table',
                  'Q5.1 - On average, how many hours did you work on this course per week?',
                  'Q4.2 - Which elements of the course did you use or participate in?', 'Q4.2 Table',
                  'Q4.2.1 - How satisfied were you with the following elements of this course?',
                  'Q4.2.2 - How valuable do you feel were the following elements of this course?',
                  'Q4.2.3 - Why didnt you use or participate in [QID117-ChoiceGroup-UnselectedChoices]?',
                  'Q4.3 - What was the biggest challenge in completing this course?', 'Table', 'Other',
                  'Q4.3.1 - At the beginning of the survey you said that you participated in the course, but '
                  'stopped participating along the way. Why did you not participate in the course until the end? '
                  'Choose the answer that applies the most.',
                  'Table', 'Other']

    return resource_queue, name_queue
