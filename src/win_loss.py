import pandas as pd

from collections import defaultdict

df = pd.read_csv('games.csv', header=0, engine='c')


def compute_ratios(records, home, away):
    home_ret = records[home]['w'] + records[home]['l']
    home_ret = records[home]['w'] / home_ret if home_ret != 0 else 0

    away_ret = records[away]['w'] + records[away]['l']
    away_ret = records[away]['w'] / away_ret if away_ret != 0 else 0

    return home_ret, away_ret

total_upsets = 0
total_count = 0
for year in range(2002, 2018):
    records = defaultdict(lambda: {'w': 0, 'l': 0})
    upsets = 0
    count = 0

    for _, game in df.query('year == @year').sort_values(by=['week']).iterrows():
        home_team = game['home_team']
        away_team = game['away_team']
        home_ratio, away_ratio = compute_ratios(records, home_team, away_team)
        count += 1

        if game['home_score'] > game['away_score']:
            records[home_team]['w'] += 1
            records[away_team]['l'] += 1

            if home_ratio < away_ratio:
                upsets += 1
        elif game['home_score'] < game['away_score']:
            records[home_team]['l'] += 1
            records[away_team]['w'] += 1

            if home_ratio > away_ratio:
                upsets += 1

    print("{} & {} & {:0.02f}\\\\".format(year, upsets, (1 - upsets/count) * 100.0))
    total_count += count
    total_upsets += upsets

print("Total & {} & {:0.02f}\\\\".format(total_upsets, (1 - total_upsets/total_count) * 100.0))



