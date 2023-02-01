# -*- coding: utf-8 -*-
"""
Created on Fri Jan 27 16:33:16 2023

@author: Surender Harsha
"""
from typing import List,Dict
import copy
import networkx
from networkx.algorithms import bipartite

#States
class GameState:
    tower_state : Dict = None
    
#Moves
class Moves:
    disk_moved : int = None
    from_tower : int = None
    to_tower : int = None

#Edges
class Edge:
    from_state : GameState = None
    to_state : GameState = None
    move : Moves = None

#Vertices
class Vertex:
    init_state : GameState = None
    all_edges : List[Edge] = None



class TOH:
    
    def __init__(self, n_disks: int, n_towers: int):
        self.n_disks = n_disks
        self.n_towers = n_towers
        self.disks = list(range(1,n_disks+1))
        
    def check_validity(self, towers: dict):
        
        if not isinstance(towers,dict):
            return False
        
        if list(towers.keys()) != list(range(1,self.n_towers+1)):
            return False
           
        disk_list = self.disks.copy()
        
        for t in towers:
            l = towers[t]
            prev = -1
            
            
            for disk in l:
                try:
                    disk_list.remove(disk)
                except:
                    return False
    
                if prev > disk:
                    return False
                prev = disk
        
        if len(disk_list) > 0:
            return False
        
        return True
            
    def get_possible_states(self, game_state: GameState) -> Vertex:
        possible_edges = []
        
        
        tower_state = game_state.tower_state
        copy_ts = copy.deepcopy(tower_state)
        
        for i in copy_ts:
            other_towers = list(copy_ts.keys())
            other_towers.remove(i)
            if len(copy_ts[i]):
                disk = copy_ts[i].pop()
                for j in other_towers:
                    copy_ts[j].append(disk)
                    if self.check_validity(copy_ts):
                        n_state = GameState()
                        n_state.tower_state = copy.deepcopy(copy_ts)
                        n_move = Moves()
                        n_move.disk_moved = disk
                        n_move.from_tower = i
                        n_move.to_tower = j
                        n_edge = Edge()
                        n_edge.from_state = copy.deepcopy(game_state)
                        n_edge.to_state = n_state
                        n_edge.move = n_move
                        possible_edges.append(n_edge)
                    disk = copy_ts[j].pop()
                copy_ts[i].append(disk)
        v = Vertex()
        v.init_state = copy.deepcopy(game_state)
        v.all_edges = possible_edges
        return v
    
class Metrics:
    def __init__(self, GC):
        self.GC = GC
        try:
            if GC.route:
                pass
        except:
            raise Exception("Your graph constructor did not calculate the shortest route yet!")
    
    def route_length(self):
        return len(self.GC.route) - 1
    
    def adjacency_matrix(self):
        self.adj_mat = networkx.adjacency_matrix(self.GC.G)
        return self.adj_mat
    
    def incidence_matrix(self):
        self.inc_mat = networkx.incidence_matrix(self.GC.G)
        return self.inc_mat
    
    def eigenvector_centrality(self):
        self.eigen_cent = networkx.eigenvector_centrality(self.GC.G)
        self.eigen_cent = {k: v for k, v in sorted(self.eigen_cent.items(), key=lambda item: item[1])[::-1]}
        
        return self.eigen_cent
    
    def is_eulerian(self):
        self.is_eul = networkx.is_eulerian(self.GC.G)
        return self.is_eul
        

class GraphConstructor:
    
    def __init__(self, toh : TOH):
        self.toh = toh
        
        self.G = networkx.Graph()
        
        self.populated_states = []
        self.populated_edges = {}
        self.node_idx = []
        
        
    def initial_state(self, init_state: GameState):
        if self.toh.check_validity(init_state.tower_state):    
            self.init_state = init_state
        else:
            raise Exception("Check tower state before setting it! Invalid state provided!")
    def final_state(self, final_state: GameState):
        if self.toh.check_validity(final_state.tower_state):    
            self.final_state = final_state
        else:
            raise Exception("Check tower state before setting it! Invalid state provided!")
    
    def check_possibility(self):
        if self.final_state.tower_state in self.populated_states:
            return True
        else:
            return False
    
    def populate_nodes(self):
        idx = 0
        population_stack = [self.init_state]
        while len(population_stack) != 0:
            state = population_stack.pop(0)
            if state.tower_state in self.populated_states:
                continue
            self.populated_states.append(state.tower_state)
            self.node_idx.append(idx)
            v = self.toh.get_possible_states(state)
            self.G.add_node(v,label=idx)
            #bipartite_switch ^= 1 
            idx+=1
            for e in v.all_edges:
                population_stack.append(e.to_state)
    
    def search_vertex(self, game_state: GameState):
        for n in self.G.nodes:
            if n.init_state.tower_state == game_state.tower_state:
                return n
        return None
    
    def populate_edges(self):
        idx = 0
        for node in self.G.nodes:
            for edges in node.all_edges:
                next_s = edges.to_state
                next_v = self.search_vertex(next_s)
                if next_v is None:
                    continue
                if not self.G.has_edge(node, next_v):
                    self.G.add_edge(node, next_v, name=idx)
                    self.populated_edges[idx] = [node.init_state.tower_state, next_v.init_state.tower_state]
                    idx+=1
                    
    def get_vertex(self, idx):
        g = GameState()
        g.tower_state = self.populated_states[idx]
        return self.search_vertex(g)
    def draw(self):
        self.G = networkx.convert_node_labels_to_integers(self.G)
        networkx.draw_kamada_kawai(self.G, with_labels=True)
    def get_shortest_route(self):
        self.G = networkx.convert_node_labels_to_integers(self.G)
        self.i_idx = self.populated_states.index(self.init_state.tower_state)
        self.f_idx = self.populated_states.index(self.final_state.tower_state)
        self.route = networkx.shortest_path(self.G, source=self.i_idx, target=self.f_idx)
        return self.route
    def get_path_dict(self):
        path = []
        for i in self.route:
            path.append(self.populated_states[i])
        return path
    def draw_shortest_route(self, font_s):
        route = self.get_shortest_route()
        node_size = []
        color_map = []
        #top_nodes = []
        width = []
        for i in self.node_idx:
            if i ==  self.i_idx:
                color_map.append('yellow')
                node_size.append(120)
                #top_nodes.append(i)
                continue
            if i == self.f_idx:
                color_map.append('cyan')
                node_size.append(120)
                #top_nodes.append(i)
                continue
            if i in route:
                node_size.append(120)
                color_map.append('pink')
                #top_nodes.append(i)
                continue
            color_map.append('grey')
            node_size.append(10)
        for e in self.G.edges:
            if e[0] in route and e[1] in route:
                width.append(1)
            else:
                width.append(0.1)
        self.G = networkx.convert_node_labels_to_integers(self.G)
        networkx.draw_kamada_kawai(self.G,width = width,node_color = color_map,node_size=node_size,font_size = font_s, with_labels=True)
        
        

