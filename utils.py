import json
import os
import matplotlib.pyplot as plt
import pandas as pd
from datetime import date
from collections import Counter
import bar_chart_race as bcr


rootdir = 'messages/inbox'


def get_person():
    with open('messages/autofill_information.json', 'r') as f:
        return dict(json.load(f))[
            "autofill_information_v2"]["FULL_NAME"][0].encode('latin1').decode('utf8')


def get_participant_count(data):
    return len(data[0]['participants'])


def get_recipent(data, person):
    for name_ in data[0]['participants']:
        if name_['name'].encode('latin1').decode('utf8') != person:
            return name_['name'].encode('latin1').decode('utf8')


def load_folder(folder):
    data = []
    path = f'{rootdir}/{folder}'

    message_files = [f for f in os.listdir(path) if f.endswith('.json')]

    data = []
    for file_ in sorted(message_files):
        with open(f'{path}/{file_}', 'r') as f:
            data.append(dict(json.load(f)))

    return data


def create_message_dataframe(data, recipent):
    ts = []
    for data_ in data:
        for message_info in data_['messages']:
            if message_info["type"] == 'Generic':
                ts.append(date.fromtimestamp(message_info['timestamp_ms'] / 1000))

    counts = Counter(ts)
    counts = {date_: [count] for date_, count in counts.items()}
    df = pd.DataFrame.from_dict(counts, orient='index', columns=[recipent]).sort_index()

    return df


def agg(df, days=180):
    df = df.rolling(days, min_periods=1).sum()
    return df


def rolling_sum_race(df, days):

    for column in df.columns.unique():
        sum_ = df[[column]].sum(axis=1)
        df = df.drop(columns=[column])
        df[column] = sum_

    df = agg(df, days=days)

    df.index = df.index.rename('date')
    df = df.reset_index()
    df['date'] = pd.to_datetime(df['date'])

    df = df[(df['date'].dt.day == 1) | (df['date'].dt.day == 10) | (df['date'].dt.day == 20)]
    df = df[df['date'] > '2015-01-01']
    df = df.set_index('date')

    bcr.bar_chart_race(
        df=df,
        title=f'Messages sent past {days} days',
        filename='rolling_message_count.mp4',
        n_bars=9,
        filter_column_colors=True)


def total_count_race(df):
    for column in df.columns.unique():
        sum_ = df[[column]].sum(axis=1)
        df = df.drop(columns=[column])
        df[column] = sum_.cumsum()

    df.index = df.index.rename('date')
    df = df.reset_index()
    df['date'] = pd.to_datetime(df['date'])

    df = df[(df['date'].dt.day == 1)]
    df = df.set_index('date')

    bcr.bar_chart_race(
        df=df,
        title='Total Messages Sent',
        filename='total_message_count.mp4',
        n_bars=9,
        filter_column_colors=True)


def process():
    dataframes = []

    person = get_person()

    for folder in os.listdir(rootdir):
        if folder not in ['.DS_Store']:
            data = load_folder(folder)

            if get_participant_count(data) == 2:

                recipent = get_recipent(data, person)

                df = create_message_dataframe(data, recipent)
                dataframes.append(df)

    df = pd.concat(dataframes, axis=1).sort_index()
    df = df.fillna(0)
    return df
