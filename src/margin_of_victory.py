import pandas as pd

from collections import defaultdict


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
