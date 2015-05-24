import double_description
import sympy as sp

class polihedron:
    _edges = sp.Matrix()

    def __init__(self, inequalities = 0, edges = 0):
        if inequalities != 0:
            _edges = double_description(inequalities)
        elif edges != 0:
            _edges = edges

    def facets(self):
        print "will be soon"

    def hasse_diagram(self):
        print "will be soon"

    def verticles(self):
        print "will be soon"

    def affine_hull(self):
        print "will be soon"

    def dim(self):
        return _edges.cols-1

    def is_feasible(self):
        return _edges

    def is_pointed(self):
        print "will be soon"

    def bounded_facets(self):
        print "will be soon"

    def unbounded_facets(self):
        print "will be soon"

    def is_bounded(self):
        print "will be soon"

    def N_points(self):
        print "will be soon"

    def N_vertices(self):
        print "will be soon"

    def N_bounded_vertices(self):
        print "will be soon"

    def N_rays(self):
        print "will be soon"

    def Vertices_in_facet(self):
        print "will be soon"

    def Facets_thru_vertex(self):
        print "will be soon"

    def Hasse_diagram(self):
        print "will be soon"

    def Graph(self):
        print "will be soon"

    def Dual_graph(self):
        print "will be soon"

    def N_edges(self):
        print "will be soon"

    def N_ridges(self):
        print "will be soon"

    def Vertex_degrees(self):
        print "will be soon"

    def Facet_degrees(self):
        print "will be soon"

    def F_vector(self):
        print "will be soon"

    def H_vector(self):
        print "will be soon"

    def Is_simplicial(self):
        print "will be soon"

    def Is_simple(self):
        print "will be soon"
