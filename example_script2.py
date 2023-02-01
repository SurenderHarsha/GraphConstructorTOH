# -*- coding: utf-8 -*-
"""
Created on Sun Jan 29 05:20:02 2023

@author: Surender Harsha
"""

from TOIGraph import *


first_game = TOH(3, 3)

d = {1: [1,2,3], 2: [], 3: []}

#first_game.check_validity(d)
initial_game_state  = GameState()
initial_game_state.tower_state = d

f = {1: [], 2: [], 3: [1,2,3]}

final_game_state = GameState()
final_game_state.tower_state = f

gt = GraphConstructor(first_game)


gt.initial_state(initial_game_state)
gt.final_state(final_game_state)
gt.populate_nodes()
gt.populate_edges()
route = gt.get_shortest_route()
#Change font_s to 1 when drawing larger graphs
gt.draw_shortest_route(font_s = 10)
m  = Metrics(gt)
print(m.route_length())
n = m.adjacency_matrix()
i = m.incidence_matrix()
e = m.eigenvector_centrality()
print(m.is_eulerian())