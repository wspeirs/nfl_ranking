import pandas as pd
import networkx as nx

from collections import defaultdict


def construct_graph(game_df):
    """
    Constructs the graph, and returns a dictionary of wins
    :param game_df: a DataFrame with ONLY one year
    :return:
    """
    teams = df['home_team'].unique()

    wins = defaultdict(lambda: 0)
    G = nx.MultiDiGraph()

    G.add_nodes_from(teams)

    for game in game_df.itertuples():
        if game.home_score > game.away_score:
            G.add_edge(game.home_team, game.away_team)
            wins[game.home_team] += 1
        elif game.away_score > game.home_score:
            G.add_edge(game.away_team, game.home_team)
            wins[game.away_team] += 1

    # remove any teams that have degree zero; some teams not in all seasons
    remove_teams = [t[0] for t in G.degree(G.nodes()) if t[1] == 0]
    G.remove_nodes_from(remove_teams)

    return G, wins


def compute_rank(G, s1, s2):
    """
    Computes a ranking using the algo by Eades, Lin, and Smyth
    :param G:
    :return:
    """
    rankings = []

    # while G != None
    while len(G.nodes) != 0:
        # while G has sink
        sink_nodes = [node for node, outdegree in G.out_degree(G.nodes()) if outdegree == 0]
        while len(sink_nodes) != 0:
            for sink in sink_nodes:
                s2.insert(0, sink)
                G.remove_node(sink)

            sink_nodes = [node for node, outdegree in G.out_degree(G.nodes()) if outdegree == 0]

        # while G has source
        source_nodes = [node for node, indegree in G.in_degree(G.nodes()) if indegree == 0]
        while len(source_nodes) != 0:
            for source in source_nodes:
                s1.append(source)
                G.remove_node(source)

            source_nodes = [node for node, indegree in G.in_degree(G.nodes()) if indegree == 0]

        # if G is not None, pick u
        if len(G.nodes) != 0:
            nodes = list(G.nodes)
            max_node = nodes[0]
            max_sig = G.out_degree(max_node) - G.in_degree(max_node)

            for node in nodes:
                sig = G.out_degree(node) - G.in_degree(node)

                if sig > max_sig:
                    max_node = node
                    max_sig = sig

            count = 0
            for node in nodes:
                if count < 4 and node != max_node and max_sig == G.out_degree(node) - G.in_degree(node):
                    # recurse and find the ranking picking this node to remove
                    new_G = G.copy()
                    new_G.remove_node(node)
                    s1_new = list(s1 + [node])
                    s2_new = list(s2)

                    for rank in compute_rank(new_G, s1_new, s2_new):
                        rankings.append(rank)
                        count += 1

            s1.append(max_node)
            G.remove_node(max_node)

    rankings.append(s1 + s2)

    return rankings


def compute_upsets(G, ranking):
    upsets = 0

    matrix = nx.adjacency_matrix(G, ranking).toarray()

    row_num = 0
    for row in matrix:
        upsets += sum(row[:row_num])
        row_num += 1

    return upsets

if __name__ == '__main__':
    df = pd.read_csv('games.csv', header=0, engine='c')

    years = df['year'].unique()

    # for year in years:
    for year in range(2002, 2018):
        game_df = df.query('year == @year')
        G, wins = construct_graph(game_df)

        rankings = compute_rank(G.copy(), [], [])
        print("RANKINGS: {}".format(len(rankings)))

        min_upsets = 1000
        min_ranking = None

        for ranking in rankings:
            upsets = compute_upsets(G, ranking)

            if upsets < min_upsets:
                min_upsets = upsets
                min_ranking = list(ranking)

        games = len(game_df)
        print("{} UPSETS: {} {:.2f}".format(year, min_upsets, (1 - float(min_upsets/games))*100.0))
        print(min_ranking)


