import matplotlib.pyplot as plt

import networkx as nx
from networkx.drawing.nx_agraph import graphviz_layout


def create_network(psstc):

    G = nx.Graph()
    for gen in psstc.gen_name:
        G.add_node(gen, attr_dict={'type': 'gen'})
        bus = psstc.gen.loc[gen, 'GEN_BUS']
        G.add_node(bus, attr_dict={'type': 'bus'})
        G.add_edge(gen, bus)

    for branch in psstc.branch_name:
        f_bus, t_bus = psstc.branch.loc[branch, ['F_BUS', 'T_BUS']]
        G.add_edge(f_bus, t_bus)

    return G


def plot(psstc):
    G = create_network(psstc)

    fig, axs = plt.subplots(1, 1, figsize=(16, 10))
    ax = axs
    pos = graphviz_layout(G, prog='sfdp')
    nx.draw_networkx_nodes(G, pos, ax=ax, node_size=50, node_color='red', nodelist=[n for n, d in G.nodes(data=True) if d.get('type', None) == 'gen'])
    nx.draw_networkx_nodes(G, pos, ax=ax, node_size=50, node_color='blue', nodelist=[n for n, d in G.nodes(data=True) if d.get('type', None) != 'gen'])
    nx.draw_networkx_edges(G, pos, ax=ax)
    ax.axis('off')
