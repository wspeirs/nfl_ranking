import pandas as pd

df = pd.read_csv('games.csv', header=0, engine='c')

total_upsets = 0
total_count = 0
for year in range(2002, 2018):
    upsets = 0
    count = 0

    for _, game in df.query('year == @year').sort_values(by=['week']).iterrows():
        if game['home_team'] == game['spread_team'] and game['home_score'] < game['away_score']:
            upsets += 1
        elif game['away_team'] == game['spread_team'] and game['home_score'] > game['away_score']:
            upsets += 1

        count += 1

    print("{} & {} & {:0.02f}\\\\".format(year, upsets, (1-upsets/count) * 100.0))
    total_count += count
    total_upsets += upsets

print("Total & {} & {:0.02f}\\\\".format(total_upsets, (1 - total_upsets/total_count) * 100.0))
