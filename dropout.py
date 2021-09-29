import pandas as pd
import matplotlib.pyplot as plt


def counts(date):
    filename = '2019T1_General_Pre-course+survey_' + date + '.csv'
    db = pd.read_csv(filename)

    courses = db['course_code'].unique()
    courses = courses[~pd.isna(courses)][2:]

    for i in range(len(courses)):
        courses[i] = courses[i].partition(' ')[2]

    my_df = pd.DataFrame(columns=['Question', 'Count'])

    for column in db.columns:
        count = len(db[column].dropna())-2
        row = {'Question': column, 'Count': count}

        my_df = my_df.append(row, ignore_index=True)

    print(my_df)

    plt.plot(my_df['Question'], my_df['Count'])
    plt.xticks(rotation=90)

    plt.show()
