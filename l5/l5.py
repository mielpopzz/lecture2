import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation
import random


def stp_reader(file_name):
    arcs = []
    with open(file_name) as f:
        for line in f:
            if line[0] == "A" and line[1] != "r":
                l = line.split()
                l.remove("A")
                arcs.append(l)
    return arcs


def arcs_list_convert(list, type):
    ss = {}
    if type == "SS":
        for a in list:
            if a[0] in ss:
                ss[a[0]].append([a[1], a[2]])
            else:
                ss[a[0]] = [[a[1], a[2]]]
        return ss
    if type == "SI":
        for a in list:
            if a[0] in ss:
                ss[a[0]].append([a[0] + a[1], a[2]])
            else:
                ss[a[0]] = [[a[0] + a[1], a[2]]]
            if a[1] in ss:
                ss[a[1]].append([a[0] + a[1], a[2]])
            else:
                ss[a[1]] = [[a[0] + a[1], a[2]]]
        return ss


elist = stp_reader("simple.stp")
G = nx.DiGraph()
G.add_weighted_edges_from(elist)

pos = nx.spring_layout(G, seed=23, k=1, iterations=20)
fig, ax = plt.subplots()


def update(idx):
    node_dist_to_color = {
        1: "red",
        2: "orange",
        3: "olive",
        4: "green",
        5: "blue",
        6: "purple",
    }
    ax.clear()
    nx.draw_networkx_nodes(G, pos, ax=ax, node_size=100, node_color=node_dist_to_color[idx % 6 + 1])
    nx.draw_networkx_labels(G, pos, ax=ax)

    arc_rad = 0
    nx.draw_networkx_edges(G, pos, ax=ax, edgelist=[elist[idx]], connectionstyle=f'arc3, rad = {arc_rad}',
                           edge_color="b", style='dashed')

    nx.draw_networkx_edges(G, pos, ax=ax, edgelist=elist[:idx] + elist[idx + 1:])

    edge_labels = dict([((u, v,), d['weight'])
                        for u, v, d in G.edges(data=True)])
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, label_pos=0.3, font_size=7)

    ax.set_title(f'Frame {idx}')


ani = matplotlib.animation.FuncAnimation(fig, update, frames=len(elist), interval=1000, repeat=True)
plt.show()
print("Cписок ребер: " + str(elist))
print("Cписок cмежности: " + str(arcs_list_convert(elist, "SS")))
print("Cписок инцедентности: " + str(arcs_list_convert(elist, "SI")))
