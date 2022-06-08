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
            if line[0] == "E":
                if line[1] == " ":
                    l = line.split()
                    l.remove("E")
                    arcs.append(l)
    return arcs


def arcs_list_convert(list, type):
    ss = {}
    if type == "SS":
        for a in list:
            if a[0] in ss:
                ss[a[0]].append([a[1], a[2]])
            else:
                ss[a[0]] = [0, [a[1], a[2]]]
    if type == "SI":
        for a in list:
            if a[0] in ss:
                ss[a[0]].append([[a[0], a[1]], a[2]])
            else:
                ss[a[0]] = [[[a[0], a[1]], a[2]]]
            if a[1] in ss:
                ss[a[1]].append([[a[0], a[1]], a[2]])
            else:
                ss[a[1]] = [[[a[0], a[1]], a[2]]]

    return ss


elist = stp_reader(input("File name: "))
G = nx.DiGraph()
G.add_weighted_edges_from(elist)

pos = nx.shell_layout(G)
fig, ax = plt.subplots()
slist = arcs_list_convert(elist, "SS")

first = input("Start Node: ")
queue = [first]

if first not in slist:
    slist[first] = [1, []]
else:

    slist[first][0]=1
def bfs(node):
    slist[node][0] = 2
    for n in slist[node]:
        if n != 0 and n != 2 and n != 3 and slist[node][1] != []:

            if n[0] in slist:
                if slist[n[0]][0] == 0:
                    queue.append(n[0])

                    slist[n[0]][0] = 1
            else:
                slist[n[0]] = [1, []]
                queue.append(n[0])

    del queue[0]


def update(idx):
    node_dist_to_color = {
        0: "white",
        1: "grey",
        2: "black"
    }
    ax.clear()

    nx.draw_networkx_nodes(G, pos, ax=ax, node_size=200, node_color=node_dist_to_color[0], edgecolors="black")
    nx.draw_networkx_labels(G, pos, ax=ax)
    if idx != 0:
        for node in slist:
            nx.draw_networkx_nodes(G, pos, ax=ax, node_size=200, node_color=node_dist_to_color[slist[node][0]],
                                   edgecolors="black", nodelist=[node])


    nx.draw_networkx_labels(G, pos, ax=ax)
    nx.draw_networkx_edges(G, pos, ax=ax, edgelist=elist)

    edge_labels = dict([((u, v,), d['weight'])
                        for u, v, d in G.edges(data=True)])
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, label_pos=0.3, font_size=7)

    if queue != [] and idx != 0:
        ax.set_title(f'Next Node {queue[0]}')
        bfs(queue[0])



ani = matplotlib.animation.FuncAnimation(fig, update, frames=len(elist)**2, interval=1000, repeat=True)
plt.show()
