# -*- coding: utf-8 -*-
"""
Created on Fri Jan 27 16:25:16 2023

@author: Surender Harsha
"""
import networkx

from TOIGraph import *

a=TOH(3,3)

d = {1: [1,2,3], 2: [], 3: []}
print(a.check_validity(d))
g = GameState()
g.tower_state = d
f = {1: [], 2: [], 3: [1,2,3]}
gt = GraphConstructor(a)
gt.initial_state(g)
fg = GameState()
fg.tower_state = f

gt.final_state(fg)
gt.populate_nodes()
gt.populate_edges()
print(gt.check_possibility())
#gt.draw()
route = gt.get_shortest_route()
gt.draw_shortest_route()
path = gt.get_path_dict()

