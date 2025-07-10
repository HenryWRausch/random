'''Scheduling for summer league'''

import networkx as nx
from collections import defaultdict

# Teams and their prior opponents (play history) by team ID
teams = {
    1: 'B.O.B.',
    2: 'Lady Vikings',
    3: 'Rebels',
    4: 'Cats',
    5: 'Spartans',
    6: 'Killer Rays',
    7: 'Groovy Goats',
    8: 'Varsity Gold',
    9: 'Cavaliers',
}

# Play history: each team maps to a set of opponents they've played
play_history = {
    1: {2, 3, 4, 7},
    2: {1, 3, 5, 8},
    3: {1, 2, 6, 9},
    4: {1, 5, 6, 7},
    5: {2, 4, 6, 8},
    6: {3, 4, 5, 9},
    7: {1, 4, 8, 9},
    8: {2, 5, 7, 9},
    9: {3, 6, 7, 8},
}

# Seed order: order of team in standings
seed_order = [4, 7, 3, 5, 9, 8, 2, 6, 1]

def build_weighted_graph(teams, history, seed_order):
    G = nx.Graph()
    seed_by_team = {tid: seed for seed, tid in enumerate(seed_order, start=1)}
    for team_id in teams:
        G.add_node(team_id)
    for t1 in teams:
        for t2 in teams:
            if t1 < t2:
                if t2 not in history[t1]:
                    seed_dist = abs(seed_by_team[t1] - seed_by_team[t2])
                    weight = 1 / (seed_dist if seed_dist != 0 else 1)
                    G.add_edge(t1, t2, weight=weight)
    return G

def find_weighted_2_factor(G):
    edges = list(G.edges(data=True))
    # Sort edges descending by weight to prioritize closer seeds
    edges.sort(key=lambda e: e[2]['weight'], reverse=True)

    degree_count = defaultdict(int)
    selected_edges = []

    def backtrack(idx):
        # If all edges considered, verify degree condition
        if idx == len(edges):
            return all(degree_count[node] == 2 for node in G.nodes)
        # Prune: any node degree exceeds 2 invalidates this path
        if any(degree_count[node] > 2 for node in G.nodes):
            return False

        u, v, data = edges[idx]
        # Option 1: Include this edge
        degree_count[u] += 1
        degree_count[v] += 1
        selected_edges.append((u, v))
        if backtrack(idx + 1):
            return True
        # Backtrack
        selected_edges.pop()
        degree_count[u] -= 1
        degree_count[v] -= 1

        # Option 2: Exclude this edge
        if backtrack(idx + 1):
            return True

        return False

    if backtrack(0):
        return selected_edges
    else:
        return None

def main():
    G = build_weighted_graph(teams, play_history, seed_order)
    solution = find_weighted_2_factor(G)
    if solution is None:
        print("No valid weighted schedule found respecting history and two matches per team.")
    else:
        print("Valid weighted schedule found:")
        for u, v in solution:
            print(f"{u} vs {v}")

if __name__ == "__main__":
    main()
