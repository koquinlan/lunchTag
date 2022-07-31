import networkx as nx
from django.db import models
from django.contrib.auth.models import User
from .models import Edge

def make_pairings():
    G = nx.Graph()

    edge_list = []
    for edge in Edge.objects.all():
        edge_list.append((edge.user1.username, edge.user2.username, edge.weight))

    print(edge_list)
    G.add_weighted_edges_from(edge_list)