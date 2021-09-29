import matplotlib.pyplot as plt
import matplotlib.cm as cm
import seaborn as sns
import dataframe_image as dfi
import pandas as pd
import numpy as np


def bar_chart(db, q_nr):
    q_df = db[q_nr][2:].str.wrap(25)
    if len(q_df.dropna()) > 3:
        q_df_values = q_df.value_counts()
        sns.set(style='darkgrid')
        plt.figure(figsize=(10, 6))
        sns.countplot(y=q_df.index, data=q_df, order=q_df_values.index, color='red')
        plt.xlabel('Percentage')
        plt.xticks(np.arange(0, max(q_df_values) * 1.2, len(q_df.dropna()) / 10),
                   [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
        plt.tight_layout()
        plt.savefig('output/' + q_nr + '.jpg')
    else:
        plt.clf()
        plt.savefig('output/' + q_nr + '.jpg')


def standard_table(db, audit, verified, q_nr):
    table_total = db[q_nr][2:]
    table_verified = verified[q_nr].dropna()
    table_audit = audit[q_nr].dropna()

    db_q2_1_v2 = pd.concat([table_verified.value_counts().to_frame(),
                            table_verified.value_counts(normalize=True).to_frame().round(4) * 100,
                            table_audit.value_counts().to_frame(),
                            table_audit.value_counts(normalize=True).to_frame().round(4) * 100,
                            table_total.value_counts(),
                            table_total.value_counts(normalize=True).to_frame().round(4) * 100], axis=1, sort=True)

    db_q2_1_v2 = db_q2_1_v2.fillna(0)
    db_q2_1_v2.columns = ['Verified', '%', 'Audit', '%', 'Total', '%']
    db_q2_1_v2 = db_q2_1_v2.astype({'Verified': 'int', 'Audit': 'int', 'Total': 'int'})
    name = 'output/' + q_nr + '_table.png'
    dfi.export(db_q2_1_v2.sort_values(by='Total', ascending=False), name, max_rows=-1)


def standard_table_profed(db, q_nr):
    table_total = db[q_nr][2:]

    db_q2_1_v2 = pd.concat([table_total.value_counts(),
                            table_total.value_counts(normalize=True).to_frame().round(4) * 100], axis=1, sort=True)

    db_q2_1_v2 = db_q2_1_v2.fillna(0)
    db_q2_1_v2.columns = ['Total', '%']
    name = 'output/' + q_nr + '_table.png'
    dfi.export(db_q2_1_v2.sort_values(by='Total', ascending=False), name, max_rows=-1)


def other_audit(df, q_nr):
    other_aud = df[q_nr].dropna()
    f = open('output/'+q_nr+'_other_audit.txt', 'w+')
    if len(other_aud) > 0:
        other_aud = other_aud.to_string(index=False).splitlines()
        for i in other_aud:
            try:
                f.write('-' + i.strip() + '\n')
            except UnicodeEncodeError:
                pass
    else:
        f.write('No results')


def other_verified(df, q_nr):
    other_ver = df[q_nr].dropna()
    f = open('output/'+q_nr+'_other_verified.txt', 'w+')
    if len(other_ver) > 0:
        other_ver = other_ver.to_string(index=False).splitlines()
        for i in other_ver:
            try:
                f.write('-' + i.strip() + '\n')
            except UnicodeEncodeError:
                pass
    else:
        f.write('No results')


def other_list(audit, verified, q_nr):
    other_audit(audit, q_nr)
    other_verified(verified, q_nr)


def other_total(db, q_nr):
    other = db[q_nr][2:].dropna()
    f = open('output/' + q_nr + '_other.txt', 'w+')
    if len(other) > 0:
        other = other.to_string(index=False).splitlines()
        for i in other:
            try:
                f.write('-' + i.strip() + '\n')
            except UnicodeEncodeError:
                pass
    else:
        f.write('No results')


def count(db, q_nr):
    counts_db = db[q_nr][2:]

    count_df = pd.concat([counts_db.value_counts().to_frame(),
                          counts_db.value_counts(normalize=True).to_frame().round(4) * 100], axis=1, sort=True)

    count_df.columns = ['Total', '%']
    dfi.export(count_df.sort_values(by='Total', ascending=False), 'output/' + q_nr + '_table.png')


def normal_list(db, q_nr):
    normal = db[q_nr][2:].dropna()
    f = open('output/' + q_nr + '_list.txt', 'w+')
    if len(normal) > 0:
        normal = normal.to_string(index=False).splitlines()
        for i in normal:
            try:
                f.write('-' + i.strip() + '\n')
            except UnicodeEncodeError:
                pass
    else:
        f.write('No results')


def stacked_bar_pre(db, q_nr, first_column, last_column):
    db_v2 = db.loc[2:, first_column: last_column].dropna()

    db_v2_counts = pd.DataFrame(db_v2.iloc[:, 0].value_counts().to_frame())
    for i in range(1, len(db_v2.columns)):
        db_v2_counts[str(i)] = (db_v2.iloc[:, i].value_counts().to_frame())

    categories_list = ['Not at all important', 'Slightly important', 'Moderately important', 'Important',
                       'Very important']
    db_v2_counts = db_v2_counts.reindex(categories_list)

    db_v2_counts = round(db_v2_counts/db_v2_counts.sum()*100, 2)

    results = None

    if len(db_v2.columns) == 4:
        results = {'Uniqueness of this course': db_v2_counts.iloc[:, 0].values,
                   'Potential usefulness of this course': db_v2_counts.iloc[:, 1].values,
                   'Interesting topic of this course': db_v2_counts.iloc[:, 2].values,
                   'Lecturer(s) involved with this course': db_v2_counts.iloc[:, 3].values}

    if len(db_v2.columns) == 7:
        results = {'Uniqueness of this course': db_v2_counts.iloc[:, 0].values,
                   'Potential usefulness of this course': db_v2_counts.iloc[:, 1].values,
                   'Interesting topic of this course': db_v2_counts.iloc[:, 2].values,
                   'Lecturer(s) involved with this course': db_v2_counts.iloc[:, 3].values,
                   'University(ies) involved with this course': db_v2_counts.iloc[:, 4].values,
                   'That the course is offered online': db_v2_counts.iloc[:, 5].values,
                   'The possibility to receive a certificate or credentials': db_v2_counts.iloc[:, 6].values}

    labels = list(results.keys())
    data = np.nan_to_num(np.array(list(results.values())))
    data_cum = data.cumsum(axis=1)
    category_colors = cm.get_cmap('RdYlGn')(np.linspace(0.15, 0.85, data.shape[1]))

    fig, ax = plt.subplots(figsize=(13, 6))
    ax.invert_yaxis()
    ax.set_xlim(0, np.nanmax(np.sum(data, axis=1)))

    for i, (col_name, color) in enumerate(zip(categories_list, category_colors)):
        widths = data[:, i]
        starts = data_cum[:, i] - widths
        ax.barh(labels, widths, left=starts, height=0.5, label=col_name, color=color)
        x_centers = starts + widths / 2

        r, g, b, _ = color
        text_color = 'white' if r * g * b < 0.5 else 'darkgrey'
        for y, (x, c) in enumerate(zip(x_centers, widths)):
            ax.text(x, y, str(int(c)), ha='center', va='center', color=text_color)
            ax.legend(ncol=len(categories_list), bbox_to_anchor=(0, 1), loc='lower left')

    if np.nanmax(np.sum(data, axis=1)) > 0:
        plt.xticks(np.arange(0, np.nanmax(np.sum(data, axis=1)), np.nanmax(np.sum(data, axis=1)) / 10),
                   [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
    plt.xlabel('Percentages')
    plt.tight_layout()
    plt.savefig('output/' + q_nr + '.jpg')


def stacked_bar_post(db, q_nr, first_column, last_column):
    db_v2 = db.loc[2:, first_column: last_column].dropna()

    db_v2_counts = pd.DataFrame(db_v2.iloc[:, 0].value_counts().to_frame())
    for i in range(1, len(db_v2.columns)):
        db_v2_counts[str(i)] = (db_v2.iloc[:, i].value_counts().to_frame())

    categories_list = ['Strongly disagree', 'Somewhat disagree', 'Neither agree nor disagree', 'Somewhat agree',
                       'Strongly agree']
    db_v2_counts = db_v2_counts.reindex(categories_list)

    db_v2_counts = round(db_v2_counts / db_v2_counts.sum() * 100, 2)

    results = None

    if len(db_v2.columns) == 3:
        results = {'Unique': db_v2_counts.iloc[:, 0].values,
                   'Useful': db_v2_counts.iloc[:, 1].values,
                   'Interesting': db_v2_counts.iloc[:, 2].values}

    labels = list(results.keys())
    data = np.nan_to_num(np.array(list(results.values())))
    data_cum = data.cumsum(axis=1)
    category_colors = cm.get_cmap('RdYlGn')(np.linspace(0.15, 0.85, data.shape[1]))

    fig, ax = plt.subplots(figsize=(13, 6))
    ax.invert_yaxis()
    ax.set_xlim(0, np.nanmax(np.sum(data, axis=1)))

    for i, (col_name, color) in enumerate(zip(categories_list, category_colors)):
        widths = data[:, i]
        starts = data_cum[:, i] - widths
        ax.barh(labels, widths, left=starts, height=0.5, label=col_name, color=color)
        x_centers = starts + widths / 2

        r, g, b, _ = color
        text_color = 'white' if r * g * b < 0.5 else 'darkgrey'
        for y, (x, c) in enumerate(zip(x_centers, widths)):
            ax.text(x, y, str(int(c)), ha='center', va='center', color=text_color)
            ax.legend(ncol=len(categories_list), bbox_to_anchor=(0, 1), loc='lower left')

    plt.tight_layout()

    if np.nanmax(np.sum(data, axis=1)) > 0:
        plt.xticks(np.arange(0, np.nanmax(np.sum(data, axis=1)), np.nanmax(np.sum(data, axis=1)) / 10),
                   [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
    plt.xlabel('Percentages')
    plt.savefig('output/' + q_nr + '.jpg')


def stacked_bar_post_profed(db, q_nr, first_column, last_column):
    db_v2 = db.loc[2:, first_column: last_column].dropna()

    db_v2_counts = pd.DataFrame(db_v2.iloc[:, 0].value_counts().to_frame())
    for i in range(1, len(db_v2.columns)):
        db_v2_counts[str(i)] = (db_v2.iloc[:, i].value_counts().to_frame())

    categories_list = None
    if 'Q4.2.1' in q_nr:
        categories_list = ['Very dissatisfied', 'Somewhat dissatisfied', 'Neither satisfied nor dissatisfied',
                           'Somewhat satisfied', 'Very satisfied']
    elif 'Q4.2.2' in q_nr:
        categories_list = ['Not at all valuable', 'Somewhat valuable', 'Moderately valuable',
                           'Valuable', 'Very valuable']

    db_v2_counts = db_v2_counts.reindex(categories_list)

    db_v2_counts = round(db_v2_counts / db_v2_counts.sum() * 100, 2)

    results = None

    if len(db_v2.columns) == 4:
        results = {'Videos': db_v2_counts.iloc[:, 0].values,
                   'Reading materials': db_v2_counts.iloc[:, 1].values,
                   'Forums': db_v2_counts.iloc[:, 2].values,
                   'Exercises, quizzes, assignments': db_v2_counts.iloc[:, 3].values}

    labels = list(results.keys())
    data = np.nan_to_num(np.array(list(results.values())))
    data_cum = data.cumsum(axis=1)
    category_colors = cm.get_cmap('RdYlGn')(np.linspace(0.15, 0.85, data.shape[1]))

    fig, ax = plt.subplots(figsize=(13, 6))
    ax.invert_yaxis()
    ax.set_xlim(0, np.nanmax(np.sum(data, axis=1)))

    for i, (col_name, color) in enumerate(zip(categories_list, category_colors)):
        widths = data[:, i]
        starts = data_cum[:, i] - widths
        ax.barh(labels, widths, left=starts, height=0.5, label=col_name, color=color)
        x_centers = starts + widths / 2

        r, g, b, _ = color
        text_color = 'white' if r * g * b < 0.5 else 'darkgrey'
        for y, (x, c) in enumerate(zip(x_centers, widths)):
            ax.text(x, y, str(int(c)), ha='center', va='center', color=text_color)
            ax.legend(ncol=len(categories_list), bbox_to_anchor=(0, 1), loc='lower left')

    plt.tight_layout()

    if np.nanmax(np.sum(data, axis=1)) > 0:
        plt.xticks(np.arange(0, np.nanmax(np.sum(data, axis=1)), np.nanmax(np.sum(data, axis=1)) / 10),
                   [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
    plt.xlabel('Percentages')
    plt.savefig('output/' + q_nr + '.jpg')


def stacked_bar_post_split(audit, verified, q_nr):
    audit.dropna()
    verified.dropna()

    db_v2_counts = pd.concat([audit[q_nr].value_counts().to_frame(),
                              verified[q_nr].value_counts().to_frame()], axis=1, join='outer').fillna(0)

    db_v2_counts = round(db_v2_counts / db_v2_counts.sum() * 100, 2)

    categories_list = None

    if 'Q5.2.1' in q_nr:
        categories_list = ['Very dissatisfied', 'Somewhat dissatisfied', 'Neither satisfied nor dissatisfied',
                           'Somewhat satisfied', 'Very satisfied']

    if 'Q5.2.2' in q_nr:
        categories_list = ['Not at all valuable', 'Somewhat valuable', 'Moderately valuable',
                           'Valuable', 'Very valuable']

    db_v2_counts = db_v2_counts.reindex(categories_list)

    results = {'Audit': db_v2_counts.iloc[:, 0].values,
               'Verified': db_v2_counts.iloc[:, 1].values}

    labels = list(results.keys())
    data = np.nan_to_num(np.array(list(results.values())))
    data_cum = data.cumsum(axis=1)
    category_colors = cm.get_cmap('RdYlGn')(np.linspace(0.15, 0.85, data.shape[1]))

    fig, ax = plt.subplots(figsize=(13, 6))
    ax.invert_yaxis()
    ax.set_xlim(0, np.nanmax(np.sum(data, axis=1)))

    for i, (col_name, color) in enumerate(zip(categories_list, category_colors)):
        widths = data[:, i]
        starts = data_cum[:, i] - widths
        ax.barh(labels, widths, left=starts, height=0.5, label=col_name, color=color)
        x_centers = starts + widths / 2

        r, g, b, _ = color
        text_color = 'white' if r * g * b < 0.5 else 'darkgrey'
        for y, (x, c) in enumerate(zip(x_centers, widths)):
            ax.text(x, y, str(int(c)), ha='center', va='center', color=text_color)
            ax.legend(ncol=len(categories_list), bbox_to_anchor=(0, 1), loc='lower left')

    plt.tight_layout()

    if np.nanmax(np.sum(data, axis=1)) > 0:
        plt.xticks(np.arange(0, np.nanmax(np.sum(data, axis=1)), np.nanmax(np.sum(data, axis=1)) / 10),
                   [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
    plt.xlabel('Percentages')
    plt.savefig('output/' + q_nr + '.jpg')


def categories(db, audit, verified, q_nr, first_column, last_column, column_list):
    categories_total(db, q_nr, first_column, last_column, column_list)
    categories_audit(audit, q_nr, first_column, last_column, column_list)
    categories_verified(verified, q_nr, first_column, last_column, column_list)


def categories_total(db, q_nr, first_column, last_column, column_list):
    df = db.loc[2:, first_column: last_column].dropna()
    df_values = df.replace(
        to_replace=['Not at all important', 'Slightly important', 'Moderately important', 'Important',
                    'Very important'],
        value=[-2, -1, 0, 1, 2])

    if len(df_values.columns) == 4:
        df_values = df_values.rename(columns={'Q108_1': 'Uniqueness of this course',
                                              'Q108_2': 'Potential usefulness of this course',
                                              'Q108_3': 'Interesting topic of this course',
                                              'Q108_4': 'Lecturer(s) involved with this course'})

    if len(df_values.columns) == 7:
        df_values = df_values.rename(columns={'Q2.4_1': 'Uniqueness of this course',
                                              'Q2.4_2': 'Potential usefulness of this course',
                                              'Q2.4_3': 'Interesting topic of this course',
                                              'Q2.4_4': 'Lecturer(s) involved with this course',
                                              'Q2.4_5': 'University(ies) involved with this course',
                                              'Q2.4_6': 'That the course is offered online',
                                              'Q2.4_7': 'The possibility to receive a certificate or credentials'})

    x = df_values.drop(labels=df_values.columns.difference(column_list), axis=1)\
        .describe().T.drop(['min', '25%', '50%', '75%', 'max'], axis=1)
    x['var'] = x['std'] ** 2
    x = x[['mean', 'std', 'var', 'count']].round(2)
    x['count'] = x['count'].apply(np.int64)
    dfi.export(x, 'output/' + q_nr + '_total_table.png')


def categories_total_profed(db, q_nr, first_column, last_column, column_list):
    df = db.loc[2:, first_column: last_column].dropna()
    df_values = None

    if 'Q4.2.1' in q_nr:
        df_values = df.replace(
            to_replace=['Very dissatisfied', 'Somewhat dissatisfied', 'Neither satisfied nor dissatisfied',
                        'Somewhat satisfied', 'Very satisfied'],
            value=[-2, -1, 0, 1, 2])

        df_values = df_values.rename(columns={'Q5.2.1_x1': 'Videos',
                                              'Q5.2.1_x2': 'Reading materials',
                                              'Q5.2.1_x3': 'Forums',
                                              'Q5.2.1_x4': 'Exercises, quizzes, assignments'})

    if 'Q4.2.2' in q_nr:
        df_values = df.replace(
            to_replace=['Not at all valuable', 'Somewhat valuable', 'Moderately valuable',
                        'Valuable', 'Very valuable'],
            value=[-2, -1, 0, 1, 2])

        df_values = df_values.rename(columns={'Q5.2.2_x1': 'Videos',
                                              'Q5.2.2_x2': 'Reading materials',
                                              'Q5.2.2_x3': 'Forums',
                                              'Q5.2.2_x4': 'Exercises, quizzes, assignments'})

    x = df_values.drop(labels=df_values.columns.difference(column_list), axis=1)\
        .describe().T.drop(['min', '25%', '50%', '75%', 'max'], axis=1)
    x['var'] = x['std'] ** 2
    x = x[['mean', 'std', 'var', 'count']].round(2)
    x['count'] = x['count'].apply(np.int64)
    dfi.export(x, 'output/' + q_nr + '_total_table.png')


def categories_audit(audit, q_nr, first_column, last_column, column_list):
    db_audit = audit.loc[:, first_column:last_column].dropna()
    db_audit_values = db_audit.replace(
        to_replace=['Not at all important', 'Slightly important', 'Moderately important', 'Important',
                    'Very important'],
        value=[-2, -1, 0, 1, 2])
    if len(db_audit_values.columns) == 4:
        db_audit_values = db_audit_values.rename(columns={'Q108_1': 'Uniqueness of this course',
                                                          'Q108_2': 'Potential usefulness of this course',
                                                          'Q108_3': 'Interesting topic of this course',
                                                          'Q108_4': 'Lecturer(s) involved with this course'})

    if len(db_audit_values.columns) == 7:
        db_audit_values = db_audit_values.rename(columns={'Q2.4_1': 'Uniqueness of this course',
                                                          'Q2.4_2': 'Potential usefulness of this course',
                                                          'Q2.4_3': 'Interesting topic of this course',
                                                          'Q2.4_4': 'Lecturer(s) involved with this course',
                                                          'Q2.4_5': 'University(ies) involved with this course',
                                                          'Q2.4_6': 'That the course is offered online',
                                                          'Q2.4_7': 'The possibility to receive a certificate or '
                                                                    'credentials'})

    x = db_audit_values.drop(labels=db_audit_values.columns.difference(column_list), axis=1)\
        .describe().T.drop(['min', '25%', '50%', '75%', 'max'], axis=1)
    x['var'] = x['std'] ** 2
    x = x[['mean', 'std', 'var', 'count']].round(2)
    x['count'] = x['count'].apply(np.int64)
    dfi.export(x, 'output/' + q_nr + '_audit_table.png')


def categories_verified(verified, q_nr, first_column, last_column, column_list):
    db_verified = verified.loc[:, first_column:last_column].dropna()
    db_verified_values = db_verified.replace(
        to_replace=['Not at all important', 'Slightly important', 'Moderately important', 'Important',
                    'Very important'],
        value=[-2, -1, 0, 1, 2])
    if len(db_verified_values.columns) == 4:
        db_verified_values = db_verified_values.rename(columns={'Q108_1': 'Uniqueness of this course',
                                                                'Q108_2': 'Potential usefulness of this course',
                                                                'Q108_3': 'Interesting topic of this course',
                                                                'Q108_4': 'Lecturer(s) involved with this course'})

    if len(db_verified_values.columns) == 7:
        db_verified_values = db_verified_values.rename(columns={'Q2.4_1': 'Uniqueness of this course',
                                                                'Q2.4_2': 'Potential usefulness of this course',
                                                                'Q2.4_3': 'Interesting topic of this course',
                                                                'Q2.4_4': 'Lecturer(s) involved with this course',
                                                                'Q2.4_5': 'University(ies) involved with this course',
                                                                'Q2.4_6': 'That the course is offered online',
                                                                'Q2.4_7': 'The possibility to receive a certificate or '
                                                                          'credentials'})

    x = db_verified_values.drop(labels=db_verified_values.columns.difference(column_list), axis=1)\
        .describe().T.drop(['min', '25%', '50%', '75%', 'max'], axis=1)
    x['var'] = x['std'] ** 2
    x = x[['mean', 'std', 'var', 'count']].round(2)
    x['count'] = x['count'].apply(np.int64)
    dfi.export(x, 'output/' + q_nr + '_verified_table.png')


def standard_statistics_mooc(db, audit, verified, q_nr):
    df_audit = audit[q_nr].dropna().to_frame(name='Audit').reset_index(drop=True)
    df_ver = verified[q_nr].dropna().to_frame(name='Verified').reset_index(drop=True)
    df_total = db[q_nr][2:].dropna().to_frame(name='Total').reset_index(drop=True)

    df_audit['Audit'] = df_audit['Audit'].astype(int)
    df_ver['Verified'] = df_ver['Verified'].astype(int)
    df_total['Total'] = df_total['Total'].astype(int)

    df = pd.concat([df_audit, df_ver, df_total], axis=1)
    x = df.agg({'Audit': ['min', 'max', 'mean', 'std', 'count'],
                'Verified': ['min', 'max', 'mean', 'std', 'count'],
                'Total': ['min', 'max', 'mean', 'std', 'count']}).T
    x = x[['mean', 'std', 'min', 'max', 'count']].round(2)
    dfi.export(x, 'output/' + q_nr + '_statistics_table.png')


def standard_statistics_profed(db, q_nr):
    df = db[q_nr][2:].dropna().astype(int).to_frame(name='Total')

    x = df.agg({'Total': ['min', 'max', 'mean', 'std', 'count']}).T
    x = x[['mean', 'std', 'min', 'max', 'count']].round(2)
    dfi.export(x, 'output/' + q_nr + '_statistics_table.png')


def describing_the_course(db, q_nr):
    db_v2 = db.loc[2:, q_nr].dropna()

    db_v2_counts = pd.DataFrame(db_v2.value_counts().to_frame())

    if q_nr == 'Q4.6':
        categories_list = ['Far too difficult', 'Too difficult', 'About right', 'Too easy', 'Far too easy']
    elif q_nr == 'Q4.7':
        categories_list = ['Far too little', 'Too little', 'About right', 'Too much', 'Far too much']
    elif q_nr == 'Q4.8':
        categories_list = ['Far too narrow', 'Too narrow', 'About right', 'Too broad', 'Far too broad']
    elif q_nr == 'Q4.9':
        categories_list = ['Far too short', 'Too short', 'About right', 'Too long', 'Far too long']
    else:
        categories_list = ['Now', 'We', 'Are', 'Going', 'Wrong']

    db_v2_counts = db_v2_counts.reindex(categories_list)
    db_v2_counts = round(db_v2_counts/db_v2_counts.sum()*100, 2)

    # If we'd like to change the colors, use the lines below
    # colors = {'red', 'orange', 'wheat', 'limegreen', 'green'}
    # color_dict = dict(zip(categories_list, colors))

    # db_v2_counts.T.plot.barh(color=color_dict, stacked=True)
    db_v2_counts.T.plot.barh(stacked=True)

    plt.tight_layout()
    plt.xlabel('Percentages')
    plt.legend(loc='upper center', ncol=3)
    plt.savefig('output/' + q_nr + '.jpg')


def split_choose_all_that_apply_mooc(db, audit, verified, q_nr):
    plt.close()

    def counting(df):
        df = df.fillna('')
        videos = 0
        reading = 0
        forums = 0
        exercises = 0
        for i in df[q_nr]:
            i.split(",", maxsplit=3)
            if str('Videos') in i:
                videos += 1
            if str('Reading materials') in i:
                reading += 1
            if str('Forums') in i:
                forums += 1
            if str('Exercises, quizzes, assignments') in i:
                exercises += 1

        elements_frame = pd.DataFrame({'Elements': ['Videos', 'Reading materials', 'Forums',
                                                    'Exercises, quizzes, assignments'],
                                       'Count': [videos, reading, forums, exercises]})

        return elements_frame

    counting(db).plot.barh(x='Elements', y='Count', color='red')

    plt.tight_layout()
    plt.savefig('output/' + q_nr + '.jpg')

    elements = pd.concat([counting(audit),
                          round(counting(audit).iloc[:, 1] / counting(audit).iloc[:, 1].sum()*100, 2),
                          counting(verified).iloc[:, 1],
                          round(counting(verified).iloc[:, 1] / counting(verified).iloc[:, 1].sum() * 100, 2),
                          counting(db).iloc[:, 1],
                          round(counting(db).iloc[:, 1] / counting(db).iloc[:, 1].sum() * 100, 2)],
                         axis=1, join='inner')

    elements = elements.set_index('Elements')

    elements.columns = ['Audit', '%', 'Verified', '%', 'Total', '%']

    name = 'output/' + q_nr + '_table.png'
    dfi.export(elements.sort_values(by='Total', ascending=False), name)


def split_choose_all_that_apply_profed(db, q_nr):
    plt.close()

    def counting(df):
        df = df.fillna('')
        videos = 0
        reading = 0
        forums = 0
        exercises = 0
        for i in df[q_nr]:
            i.split(",", maxsplit=3)
            if str('Videos') in i:
                videos += 1
            if str('Reading materials') in i:
                reading += 1
            if str('Forums') in i:
                forums += 1
            if str('Exercises, quizzes, assignments') in i:
                exercises += 1

        elements_frame = pd.DataFrame({'Elements': ['Videos', 'Reading materials', 'Forums',
                                                    'Exercises, quizzes, assignments'],
                                       'Count': [videos, reading, forums, exercises]})

        return elements_frame

    counting(db).plot.barh(x='Elements', y='Count', color='red')

    plt.tight_layout()
    plt.savefig('output/' + q_nr + '.jpg')

    elements = pd.concat([counting(db), round(counting(db).iloc[:, 1] / counting(db).iloc[:, 1].sum() * 100, 2)],
                         axis=1, join='inner')

    elements = elements.set_index('Elements')

    elements.columns = ['Total', '%']

    name = 'output/' + q_nr + '_table.png'
    dfi.export(elements.sort_values(by='Total', ascending=False), name)


def nps_score(db, r_queue, n_queue):
    nps_db = db['Q182_NPS_GROUP'][2:].dropna()

    detractor = 0
    passive = 0
    promoter = 0
    for i in nps_db:
        if str('Detractor') in i:
            detractor += 1
        if str('Passive') in i:
            passive += 1
        if str('Promoter') in i:
            promoter += 1

    nps = pd.DataFrame({'': [detractor, passive, promoter]}, index=['Detractor', 'Passive', 'Promoter'])
    nps = round(nps / nps.sum() * 100, 2)

    nps.T.plot.barh(stacked=True)
    plt.xlabel('Percentage')
    plt.savefig('output/NPS.jpg')

    normal_list(db, 'Q184')

    r_queue.extend(['NPS.jpg', 'Q184_list.txt'])
    n_queue.extend(['NPS - Group percentages', 'Please explain your rating'])


def stacked_bar_programme_expectations(db, q_nr, first_column, last_column):
    db_v2 = db.loc[2:, first_column: last_column].dropna()

    db_v2_counts = pd.DataFrame(db_v2.iloc[:, 0].value_counts().to_frame())
    for i in range(1, len(db_v2.columns)):
        db_v2_counts[str(i)] = (db_v2.iloc[:, i].value_counts().to_frame())

    categories_list = ['Strongly disagree', 'Somewhat disagree', 'Neither agree nor disagree', 'Somewhat agree',
                       'Strongly agree']
    db_v2_counts = db_v2_counts.reindex(categories_list)

    db_v2_counts = round(db_v2_counts/db_v2_counts.sum()*100, 2)

    results = {'support my learning needs and help me to develop my skills': db_v2_counts.iloc[:, 0].values,
               'optimize my ability to learn this content': db_v2_counts.iloc[:, 1].values,
               'make me feel a part of the academic and social community of this course':
                   db_v2_counts.iloc[:, 2].values,
               'increase my expertise in the field': db_v2_counts.iloc[:, 3].values,
               'make me be perceived as an expert': db_v2_counts.iloc[:, 4].values,
               'aid me in my next career steps': db_v2_counts.iloc[:, 5].values,
               'bring me recognition through a certificate': db_v2_counts.iloc[:, 6].values,
               'support me in another way, namely...': db_v2_counts.iloc[:, 7].values}

    labels = list(results.keys())
    data = np.nan_to_num(np.array(list(results.values())))
    data_cum = data.cumsum(axis=1)
    category_colors = cm.get_cmap('RdYlGn')(np.linspace(0.15, 0.85, data.shape[1]))

    fig, ax = plt.subplots(figsize=(13, 6))
    ax.invert_yaxis()
    ax.set_xlim(0, np.nanmax(np.sum(data, axis=1)))

    for i, (col_name, color) in enumerate(zip(categories_list, category_colors)):
        widths = data[:, i]
        starts = data_cum[:, i] - widths
        ax.barh(labels, widths, left=starts, height=0.5, label=col_name, color=color)
        x_centers = starts + widths / 2

        r, g, b, _ = color
        text_color = 'white' if r * g * b < 0.5 else 'darkgrey'
        for y, (x, c) in enumerate(zip(x_centers, widths)):
            ax.text(x, y, str(int(c)), ha='center', va='center', color=text_color)
            ax.legend(ncol=len(categories_list), bbox_to_anchor=(0, 1), loc='lower left')

    if np.nanmax(np.sum(data, axis=1)) > 0:
        plt.xticks(np.arange(0, np.nanmax(np.sum(data, axis=1)), np.nanmax(np.sum(data, axis=1)) / 10),
                   [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
    plt.xlabel('Percentages')
    plt.tight_layout()
    plt.savefig('output/' + q_nr + '.jpg')


def stacked_bar_ib_questions(db, q_nr, first_column, last_column):
    db_v2 = db.loc[2:, first_column: last_column].dropna()

    db_v2_counts = pd.DataFrame(db_v2.iloc[:, 0].value_counts().to_frame())
    for i in range(1, len(db_v2.columns)):
        db_v2_counts[str(i)] = (db_v2.iloc[:, i].value_counts().to_frame())

    categories_list = ['First', 'Second', 'Third', 'Fourth']

    db_v2_counts = round(db_v2_counts/db_v2_counts.sum()*100, 2)

    results = {'Free upgrade to verified learner': db_v2_counts.iloc[:, 0].values,
               'A giant Micro Plushie': db_v2_counts.iloc[:, 1].values,
               'A question to a professor': db_v2_counts.iloc[:, 2].values,
               'Book: Microbiology for dummies': db_v2_counts.iloc[:, 3].values}

    labels = list(results.keys())
    data = np.nan_to_num(np.array(list(results.values())))
    data_cum = data.cumsum(axis=1)
    category_colors = cm.get_cmap('RdYlGn')(np.linspace(0.15, 0.85, data.shape[1]))

    fig, ax = plt.subplots(figsize=(13, 6))
    ax.invert_yaxis()
    ax.set_xlim(0, np.nanmax(np.sum(data, axis=1)))

    for i, (col_name, color) in enumerate(zip(categories_list, category_colors)):
        widths = data[:, i]
        starts = data_cum[:, i] - widths
        ax.barh(labels, widths, left=starts, height=0.5, label=col_name, color=color)
        x_centers = starts + widths / 2

        r, g, b, _ = color
        text_color = 'white' if r * g * b < 0.5 else 'darkgrey'
        for y, (x, c) in enumerate(zip(x_centers, widths)):
            ax.text(x, y, str(int(c)), ha='center', va='center', color=text_color)
            ax.legend(ncol=len(categories_list), bbox_to_anchor=(0, 1), loc='lower left')

    if np.nanmax(np.sum(data, axis=1)) > 0:
        plt.xticks(np.arange(0, np.nanmax(np.sum(data, axis=1)), np.nanmax(np.sum(data, axis=1)) / 10),
                   [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
    plt.xlabel('Percentages')
    plt.tight_layout()
    plt.savefig('output/' + q_nr + '.jpg')


def programme_expectations(db, r_queue, n_queue):
    bar_chart(db, 'Q179')
    standard_table_profed(db, 'Q179')

    bar_chart(db, 'Q180')
    standard_table_profed(db, 'Q180')

    normal_list(db, 'Q181')

    stacked_bar_programme_expectations(db, 'Q184', 'Q184_1', 'Q184_8')
    other_total(db, 'Q184_8_TEXT')

    r_queue.extend(['Q179.jpg', 'Q179_table.png', 'Q180.jpg', 'Q180_table.png', 'Q181_list.txt',
                    'Q184.jpg', 'Q184_8_TEXT_other.txt'])
    n_queue.extend(['Q179 - This course is part of a multi-course programme. Did you register for the full programme?',
                    'Table',
                    'Q180 - Is this your first course within the programme?', 'Table',
                    'Q181 - Why did you not register for the full programme?',
                    'Q184 - Please indicate how much you agree/disagree with the following statements: '
                    'I expect that the combination of courses in the programme will...', 'Namely'])


def programme_questions(db, r_queue, n_queue):
    bar_chart(db, 'Q243')
    standard_table_profed(db, 'Q243')

    stacked_bar_programme_expectations(db, 'Q239', 'Q239_1', 'Q239_8')
    other_total(db, 'Q239_8_TEXT')

    bar_chart(db, 'Q261_1')
    standard_table_profed(db, 'Q261_1')

    normal_list(db, 'Q262')

    normal_list(db, 'Q265')

    standard_statistics_profed(db, 'Q244_1')

    bar_chart(db, 'Q246_1')
    standard_table_profed(db, 'Q246_1')

    bar_chart(db, 'Q240')
    standard_table_profed(db, 'Q240')
    other_total(db, 'Q240_8_TEXT')

    normal_list(db, 'Q241')

    normal_list(db, 'Q266')

    r_queue.extend(['Q243.jpg', 'Q243_table.png', 'Q239.jpg', 'Q239_8_TEXT_other.txt', 'Q261_1.jpg', 'Q261_1_table.png',
                    'Q262_list.txt', 'Q265_list.txt', 'Q244_1_statistics_table.png', 'Q246_1.jpg', 'Q246_1_table.png',
                    'Q240.jpg', 'Q240_table.png', 'Q240_8_TEXT_other.txt', 'Q241_list.txt', 'Q266_list.txt'])
    n_queue.extend(['Q243 - Did you complete all the courses within this programme?', 'Table',
                    'Q239 - Completing all courses in this programme has...', 'Namely',
                    'Q261 - Programme structure', 'Table',
                    'Q262 - Please explain your answer',
                    'Q265 - What was the most valuable course of this programme for you? Please explain',
                    'Q244 - How much time did you take between courses on average in the programme?',
                    'Q246 - Course scheduling', 'Table',
                    'Q240 - What long term opportunities do you anticipate as a result of the programme certificate?',
                    'Table', 'Other opportunities, namely',
                    'Q241 - Please explain your answer',
                    'Q266 - Which aspects of this programme would you like us to improve upon? Please explain'])


def ib_questions(db, r_queue, n_queue):
    stacked_bar_ib_questions(db, 'Q251', 'Q251_1', 'Q251_4')
    # bar_chart(db, 'Q251_1')

    normal_list(db, 'Q252')

    bar_chart(db, 'Q247')
    standard_table_profed(db, 'Q247')

    bar_chart(db, 'Q248')
    standard_table_profed(db, 'Q248')

    bar_chart(db, 'Q249')
    standard_table_profed(db, 'Q249')

    normal_list(db, 'Q250')

    r_queue.extend(['Q251.jpg', 'Q252_list.txt', 'Q247.jpg', 'Q247_table.png', 'Q248.jpg', 'Q248_table.png',
                    'Q249.jpg', 'Q249_table.png', 'Q250_list.txt'])
    n_queue.extend(['Q251 - Rank the prizes from the best to least',
                    'Q252 - Do you have any other prize suggestions?',
                    'Q247 - Did you look on the Buddy up! forum?', 'Table',
                    'Q248 - Did you buddy up?', 'Table',
                    'Q249 - Did it help you?', 'Table',
                    'Q250 - How can we improve the Buddy up forum?'])
