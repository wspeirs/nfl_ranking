import pandas as pd

from collections import defaultdict
from statistics import mean, median


df = pd.read_csv('games.csv', header=0, engine='c')

years = dict()
max_mov = 0

for year in range(2002, 2018):
    movs = df.query('year == @year').eval('abs(home_score - away_score)')

    if max(movs) > max_mov:
        max_mov = max(movs)

    mov_histo = defaultdict(lambda: 0)

    for mov in movs:
        mov_histo[int(mov)] += 1

    years[year] = mov_histo


def accumulate(d, max):
    total = float(sum(d.values()))
    _sum = 0.0

    for mov in sorted(d.keys()):
        if mov > max:
            break

        _sum += d[mov]/total

    return round(_sum * 100.0, 2)


print(" & ".join(["MOV"] + list(map(lambda y: str(y), range(2002, 2010)))), "\\\\")
print("\\hline")

for mov in list(range(1, 11)) + list(range(14, int(max_mov), 7)):
    print("{} & ".format(mov), end='')
    vals = list(map(lambda v: "\\textbf{{{:0.1f}}}".format(v) if 23 <= v <= 27 or 48 <= v <= 52 else "{:0.1f}".format(v), [accumulate(years[year], mov) for year in range(2002, 2010)]))
    print(*vals, sep=" & ", end="\\\\\n")

print(" & ".join(["MOV"] + list(map(lambda y: str(y), range(2010, 2018)))), "\\\\")
print("\\hline")

for mov in list(range(1, 11)) + list(range(14, int(max_mov), 7)):
    print("{} & ".format(mov), end='')
    vals = list(map(lambda v: "\\textbf{{{:0.1f}}}".format(v) if 23 <= v <= 27 or 48 <= v <= 52 else "{:0.1f}".format(v), [accumulate(years[year], mov) for year in range(2010, 2018)]))
    print(*vals, sep=" & ", end="\\\\\n")

total = []
print("Year & Mean & Median\\\\")
for year in range(2002, 2018):
    movs = list(df.query('year == @year').eval('abs(home_score - away_score)'))
    total.extend(movs)

    print("{} & {:0.2f} & {:0.2f}\\\\".format(year, mean(movs), median(movs)))

print("Total & {:0.2f} & {:0.2f}".format(mean(total), median(total)))

#     means = list(map(lambda v: "{:0.2f}".format(v), [mean(m) for m in movs]))
#     meds = list(map(lambda v: "{:0.2f}".format(v), [median(m) for m in movs]))
# print("Mean & ", end='')
# print(*means, sep=" & ", end="\\\\\n")
# print("Median & ", end='')
# print(*meds, sep=" & ", end="\\\\\n")

