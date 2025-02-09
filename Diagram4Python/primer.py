from graphviz import Digraph

dot = Digraph()
dot.node('A', 'Start')
dot.node('B', 'Decision')
dot.edge('A', 'B')
dot.render('primer_output_graph', format='png', cleanup=True)