"""
Methods for network analysis.
"""

import networkx as nx
import tethne.networks as nt
import tethne.data as ds

# [#60463184]
def closeness_introgression(papers, node, start, end, chunk, normalize = False):
    """
    Analyzes the global closeness centrality of a node over time.
    
    Parameters
    ----------
    papers : list
        A list of :class:`Paper` instances.
    node : any
        Handle of the node to analyze.
    start : int
        Year to start analysis.
    end : int
        Start year of final time-window.
    chunk : int
        Size of time-window.
    normalize : bool
        If True, normalizes global closeness centrality for each year against
        the average closeness centrality for that year. This will require
        substantially more processing time, and values will usually be >> 0.
        
    Returns
    -------
    trajectory : list
        Global closeness centrality for node over specified period.
    
    """
    
    trajectory = []
    for i in xrange(start, end):
        slice = [ m for m in papers if i <= m['date'] < i+chunk ]
        g = nt.nx_coauthors(slice)
        c = 0
        try:   
            for pl in nx.shortest_path_length(g, node).values():
                if pl != 0:     # Ignore self-loops.
                    c += 1/float(pl)
            c = c/len(g)
        except:
            c = 0.
            
        if normalize:
            ac = 0
            for sg in nx.connected_component_subgraphs(g):
                if len(sg.nodes()) > 1:
                    ac += (1/nx.average_shortest_path_length(sg)) * (float(len(sg)) / float(len(g))**2 )
            c = c/ac
        trajectory.append(c)

    return trajectory