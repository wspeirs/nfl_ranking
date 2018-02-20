import pandas as pd

from collections import defaultdict

df = pd.read_csv('games.csv', header=0, engine='c')

total_same = 0
total_diff = 0
for year in range(2002, 2018):
    records = defaultdict(lambda: 0)

    for _, game in df.query('year == @year').sort_values(by=['week']).iterrows():
        if game['home_team'] < game['away_team']:
            if game['home_score'] > game['away_score']:
                records["{},{}".format(game['home_team'], game['away_team'])] += 1
            elif game['home_score'] < game['away_score']:
                records["{},{}".format(game['home_team'], game['away_team'])] -= 1
        else:
            if game['home_score'] < game['away_score']:
                records["{},{}".format(game['away_team'], game['home_team'])] += 1
            elif game['home_score'] > game['away_score']:
                records["{},{}".format(game['away_team'], game['home_team'])] -= 1

    same = len(list(filter(lambda v: v == 2 or v == -2, records.values())))
    diff = len(list(filter(lambda v: v == 0, records.values())))

    total_same += same
    total_diff += diff

    print("{} & {:0.02f}\\\\".format(year, (same / (same + diff))* 100.0))

print("Total & {:0.02f}\\\\".format((total_same / (total_same + total_diff))* 100.0))
