import networkx as nx
import random
from math import *

def isbelong(l1,l2): # Checks if an item in list 1 exists in list 2
    x=0
    for i in l1:
        for j in l2:
            if i==j:
                x=1

    return x

def list_overlapping(g,communities_flipped):
	l_nodes = g.nodes()
	dict_membership_of_all_nodes=dict() # Prepare the dictionary to contain the membership of all nodes
	for i in l_nodes: # For each node
		dict_membership_of_all_nodes[i]=0
		for j in communities_flipped: # For each community x 
			for k in communities_flipped[j]: # For each node in that community x
				if i==k: # If the node i (starting node) occurs in community x, increment
					dict_membership_of_all_nodes[i]=dict_membership_of_all_nodes[i]+1
					
	list_overlapping_nodes=[] # Prepare the list to contain the nodes which only overlap
	for i in dict_membership_of_all_nodes: # For each node
		if dict_membership_of_all_nodes[i]>1: # If the membership is greater than 1, it is an overlapping node
			list_overlapping_nodes.append(i)


			
	dict_membership_of_overlapping_nodes=dict() # Prepare the dictionary to contain the membership of overlapping nodes only
	for i in list_overlapping_nodes: # For each overlapping node
		dict_membership_of_overlapping_nodes[i]=dict_membership_of_all_nodes[i] # Get its membership and put it in the dictionary


	return list_overlapping_nodes, dict_membership_of_all_nodes, dict_membership_of_overlapping_nodes
	
	
def remove_overlapping(g,list_overlapping_nodes,communities_flipped):

	# Copy the dictionary communities_flipped
	communities_flipped_copy=dict()
	for i in communities_flipped:
		communities_flipped_copy[i]=[]
	for i in communities_flipped:
		for j in communities_flipped[i]:
			communities_flipped_copy[i].append (j)
	 

	# Get the nodes and their neighbors in a dictionary `dict_graph`
	l_nodes = g.nodes()
	dict_graph = dict()  
	for i in l_nodes:
		dict_graph[i] = [] # nodes in the key and their neighbors in a list
	for i in l_nodes: # For each node
		iteri = g.neighbors(i) # Get the neighbors
		for j in iteri: # Access the neighbors
			dict_graph[i].append(j) # Append them to the list 
			
		
	# Remove the overlapping nodes from dict_graph
	for overlapping_node in list_overlapping_nodes: # For each overlapping node
		for i in dict_graph: # For each node (overlapping or not)
			for j in dict_graph[i]: # For the neighbor of each node
				if j == overlapping_node: # If the neighbor is an overlapping node
					dict_graph[i].remove(overlapping_node) # Remove it
		dict_graph.pop(overlapping_node) # Remove overlapping node from list when done

	# Remove the overlapping nodes from communities_flipped_copy
	for overlapping_node in list_overlapping_nodes: # For each overlapping node
		for i in communities_flipped_copy: # For each community
			for j in communities_flipped_copy[i]: # For each node in that community
				if j == overlapping_node: # If the node is an overalapping node, remove it
					communities_flipped_copy[i].remove(overlapping_node)

	# Construct the graph without overlapping nodes
	g_without_ov = nx.Graph()
	for i in dict_graph:
		g_without_ov.add_node(i) # Add the nodes first
	l_edges = []
	for i in dict_graph: # For each node that doesn't overlap
		for j in dict_graph[i]: # For the neighbors
			l_edges.append ((i, j)) # Create a list where they connect
	g_without_ov.add_edges_from(l_edges)

	return g_without_ov,dict_graph,communities_flipped_copy
	
	
def intra_wo(dict_graph_wo,communities_flipped):

	dict_node_communities_flipped = dict() 
	for i in dict_graph_wo: # Get the non-overlapping nodes and the communities they participate in 
		dict_node_communities_flipped[i] = []
		for j in communities_flipped:
			for k in communities_flipped[j]:
				if i == k:
					dict_node_communities_flipped[i].append(j)
					
	d_copy=dict_graph_wo.copy() 
	dict_graph_intra_wo=dict() # Get the non-overlapping node and its neighbors which are non overlapping in `dict_graph_intra_wo`
	for i in d_copy:
		dict_graph_intra_wo[i] =[]
		for j in d_copy[i]:
			k=isbelong(dict_node_communities_flipped[i],dict_node_communities_flipped[j])
			if k==1:
				dict_graph_intra_wo[i].append(j)
				
	# Construct dict_graph_intra_wo into graph_intra_wo
	graph_intra_wo = nx.Graph ()
	for i in dict_graph_intra_wo:
		graph_intra_wo.add_node (i)

	for i in dict_graph_intra_wo:
		for j in dict_graph_intra_wo[i]:
			graph_intra_wo.add_edges_from ([(i, j)])
    
	return dict_graph_intra_wo, graph_intra_wo
	
def intra_o(g,communities_flipped,list_overlapping_nodes):

	dict_node_communities_flipped = dict () 
	for i in g: # Get all the nodes and the communities they participate in 
		dict_node_communities_flipped[i] = []
		for j in communities_flipped:
			for k in communities_flipped[j]:
				if i == k:
					dict_node_communities_flipped[i].append(j)
	g_copy=g.copy()
	dict_graph_intra_o=dict()

	# Find the list of communities to delete
	#print(list_overlapping_nodes)
	#print(dict_node_communities_flipped)

	c=set() # Will contain the communities of the overlapping nodes
	for i in list_overlapping_nodes: # For each overlapping node
		for j in dict_node_communities_flipped[i]: # For each community of the overlapping node
			c.add(j) # Add the community
			
	c_sup=set() # Will contain all of the communities to be later processed to contain only communities with non-overlapps in it
	for i in communities_flipped: # For each community
		c_sup.add(i) # Add the community

	for i in c: # Remove communities which have overlaps in them
		c_sup.remove(i)
		
	#Remove the nodes in the communities with no overlaps --> We want overlapping intra nodes only
	for i in c_sup:
		for j in communities_flipped[i]:
			g_copy.remove_node(j) # May be nothing removed if all communities have overlaps in them

	# Build the dictionary of the overlapping intra 
	for i in g_copy: #g_copy not g
		dict_graph_intra_o[i] =[]
		for j in g[i]:
			k=isbelong(dict_node_communities_flipped[i],dict_node_communities_flipped[j])
			if k==1:
				dict_graph_intra_o[i].append(j)

	# Construct the overlapping intra graph
	graph_intra_o = nx.Graph ()
	for i in dict_graph_intra_o:
		graph_intra_o.add_node(i)

	for i in dict_graph_intra_o:
		for j in dict_graph_intra_o[i]:
			graph_intra_o.add_edges_from ([(i, j)])
			
	return dict_graph_intra_o, graph_intra_o

def inter_wo_o(g,communities_flipped):

	dict_node_communities_flipped = dict ()
	for i in g: # Get all the nodes and the communities they participate in 
		dict_node_communities_flipped[i] = []
		for j in communities_flipped:
			for k in communities_flipped[j]:
				if i == k:
					dict_node_communities_flipped[i].append(j)

	dict_graph_inter=dict() # dict of overlapping and non-overlapping
	for i in  g:
		dict_graph_inter[i]=[]
		for j in g[i]:
			k=isbelong(dict_node_communities_flipped[i],dict_node_communities_flipped[j])
			if k==0:
				dict_graph_inter[i].append(j)

	graph_inter = nx.Graph() # Graph of inter overlapping + non-overlapping
	for i in dict_graph_inter:
		graph_inter.add_node (i)

	for i in dict_graph_inter:
		for j in dict_graph_inter[i]:
			graph_inter.add_edges_from ([(i, j)])
	return dict_graph_inter, graph_inter


