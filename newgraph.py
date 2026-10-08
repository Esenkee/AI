import random
import networkx as nx
import matplotlib.pyplot as plt


def is_validcoloring(graph, coloring):
    for u, v in graph.edges():
        if coloring[u] == coloring[v]:
            return False
    return True


def available_colors(graph, coloring, node, k):
    used = {coloring[nb] for nb in graph.neighbors(node) if nb in coloring}
    return [c for c in range(k) if c not in used]


def select_node(graph, coloring, k):
    best_node, best_colors = None, None

    for node in graph.nodes():
        if node in coloring:
            continue

        colors = available_colors(graph, coloring, node, k)

        if best_node is None or len(colors) < len(best_colors):
            best_node, best_colors = node, colors
        elif (len(colors) == len(best_colors)
              and graph.degree[node] > graph.degree[best_node]):
            best_node, best_colors = node, colors

    return best_node, best_colors


def order_colors(graph, coloring, node, colors, k):
    scores = []

    for color in colors:
        constraints = 0
        for nb in graph.neighbors(node):
            if nb in coloring:
                continue
            if color in available_colors(graph, coloring, nb, k):
                constraints += 1
        scores.append((constraints, color))

    scores.sort()
    return [color for _, color in scores]


def backtrack(graph, coloring, k):
    if len(coloring) == len(graph.nodes()):
        return True

    node, colors = select_node(graph, coloring, k)

    if not colors:
        return False

    for color in order_colors(graph, coloring, node, colors, k):
        coloring[node] = color

        if backtrack(graph, coloring, k):
            return True

        del coloring[node]

    return False


def mrv_degree_lcv_backtracking(graph):
    for k in range(1, len(graph.nodes()) + 1):
        coloring = {}
        if backtrack(graph, coloring, k):
            return coloring, k


n_nodes = 20

while True:
    G = nx.Graph()
    G.add_nodes_from(range(n_nodes))

    for i in range(n_nodes):
        for j in range(i + 1, n_nodes):
            if random.random() < 0.2:
                G.add_edge(i, j)

    if nx.is_connected(G):
        break

coloring_result, k = mrv_degree_lcv_backtracking(G)

print("Edges:", list(G.edges()))
print("Coloring:", coloring_result)
print("Valid:", is_validcoloring(G, coloring_result))
print("K:", k)

color_map = [coloring_result[node] for node in G.nodes()]

nx.draw(G, node_color=color_map, with_labels=True,
        font_weight="bold", node_size=800)
plt.show()