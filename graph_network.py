from manim import *
import random 
import numpy as np
import networkx as nx
from colour import Color

class GraphIntroduction(Scene):
    def __init__(self, **kwargs):
        # Set the background color
        super().__init__(**kwargs)
        portfolio_colour = "#002040" 
        self.camera.background_color = Color(portfolio_colour)

    def graph_configure(self,graph,**kwargs):    
        # This is to configure the Graph object to wiggle the verts
        for submob in graph.vertices.values():
            submob.jiggling_direction = rotate_vector(
                RIGHT, np.random.random() * TAU *1.5,
            )
            submob.jiggling_phase = np.random.random() * TAU *1.5
            submob.set_opacity(0.9)
        for key, value in kwargs.items():
            setattr(graph, key, value)
            
    def set_graph_stroke(self,graph,**kwargs):
        for e in graph.edges.values():
            e.set_stroke(opacity= 0.8,**kwargs)
            
    
    def construct(self):
        
        def wiggle_graph_updater(graph, dt):
            # Updater to wiggle vertices of a given graph
            for key in graph.edges:
                edge=graph.edges[key]
                edge.start = graph.vertices[key[0]].get_center()
                edge.end = graph.vertices[key[1]].get_center()
            
            for submob in graph.vertices.values():
                submob.jiggling_phase += dt * graph.jiggles_per_second * TAU
                submob.shift(
                    graph.jiggle_amplitude *
                    submob.jiggling_direction *
                    np.sin(submob.jiggling_phase) * dt
                )
                
        random.seed(246)
        np.random.seed(4812)
        
        G = Graph.from_networkx(nx.newman_watts_strogatz_graph(20, 5, 0.1), layout="spring", layout_scale=3.2)
        G2 = Graph.from_networkx(nx.newman_watts_strogatz_graph(10, 6, 0.1), layout="spring", layout_scale=3.2)

        
        for graph in [G,G2]:
            self.graph_configure(graph, jiggle_amplitude=0.2, jiggles_per_second=0.1)
            graph.add_updater(wiggle_graph_updater)
            self.set_graph_stroke(graph,width=1)
            graph.shift(3.5*RIGHT+ 0.01*UP)

        G.rotate(PI/2)
        self.add(G, G2)
        # ANIMATION_TYPE = "VERTICES"  # Select whether to render only vertices or only edges (in order to colorize in After Effects separately)
        
        # if ANIMATION_TYPE=="VERTICES":
        #     # hiding edges
        #     for edge in G.edges.values():
        #         edge.set_stroke(width=0)

        # if ANIMATION_TYPE=="EDGES":
        #     for vert in G.vertices.values():
        #         vert.scale(0)
            
        self.wait(10)
        # self.play(G.animate.change_layout("circular"), run_time=3)
        # self.wait(5)

if __name__ == "__main__":
    graph = GraphIntroduction()
    graph.render() # construct is called inside render


