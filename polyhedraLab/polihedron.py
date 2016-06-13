#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sympy as sp
import numpy as np
import random
import itertools
from sympy.solvers.solveset import linsolve

class hasse_vertex:
    def __init__(self, value, previous_level, next_level):
        self.value = value
        self.previous_level = previous_level
        self.next_level = next_level


class hasse:
    def __init__(self, levels_number, inequalities):
        self.inequalities = inequalities
        self.levels = []
        for i in range(levels_number):
            self.levels.append([])


    def my_view(self):
        res = []
        for level in range(len(self.levels))[::-1]:
            res_line = ""
            line = []
            for vertex in self.levels[level]:
                if type(vertex.value) == str:
                    res_current = vertex.value
                else:
                    rows = vertex.value
                    dim = self.inequalities.cols
                    needed_eq_num = dim - level + 1

                    A = self.inequalities[rows,:]
                    b = sp.ones(needed_eq_num, 1)

                    x = sp.symbols(','.join(['x'+str(i) for i in range(dim)]))
                    res_current = linsolve(A.col_insert(A.cols, b),x)

                line.append(str(res_current))
                #for debug
                #line.append("[" + str(vertex.previous_level) + "]")
                #line.append("[" + str(vertex.next_level) + "]")
            res_line = ",".join(line)
            res.append(res_line)
        return "\n".join(res)


    def list_view(self):
        result = []
        index_magic_next = 0
        for level in range(len(self.levels)):
            index_magic_prev = '-'
            index_magic_next += len(self.levels[level])
            for element in range(len(self.levels[level])):
                first = {}#set(element.previous_level)
                if level == 0:
                    first = {}
                elif level == 1:
                    first = {element}
                else:
                    first = set()
                    index_magic_prev = index_magic_next - len(self.levels[level]) - len(self.levels[level-1])
                    temp_first = [i+index_magic_prev for i in self.levels[level][element].previous_level]
                    for i in temp_first:
                        first = first.union(result[i][0])

                second = set([i + index_magic_next for i in self.levels[level][element].next_level])
                result.append((first, second))
        return result


    def __str__(self):
        return str(self.list_view())


class polyhedron:
    #public
    def __init__(self, inequalities = -1, points = -1, name = -1, dim = -1):
        if (inequalities != -1):
            self.inequalities = inequalities
        elif (points != -1):
            pass
        elif (name != -1 and dim != -1):
            if name == "cube":
                self.inequalities = sp.zeros(dim*2, dim)
                for i in range(dim):
                    self.inequalities[2*i, i] = 1
                    self.inequalities[2*i+1, i] = -1
        self.get_hasse_diagram()
        return
        print "wrong parameters"

    def get_matrix_B(self, cone_matrix):
        size = cone_matrix.rank()
        B = cone_matrix[:size,:]
        A = cone_matrix[size:,:]
        while (B.rank() != size):
            b = random.randint(0, size-1)
            a = random.randint(0, A.rows-1)
            temp = A[a,:]
            A[a,:] = B[b,:]
            B[b,:] = temp
        return A, B

    def adjacent(self, A, u1, u2):
        temp = sp.Matrix.zeros(0, A.cols)
        for i in range(A.rows):
            if (A[i,:]*u1)[0] == 0 and (A[i,:]*u2)[0] == 0:
                temp = temp.col_join(A[i,:])
        if temp.rank() == A.rank() - 2:
            return True
        return False

    def skeleton_step(self, A, new_row, Ut):
        aiu = new_row*Ut

        uplus = []
        uminus = []
        uzero = []

        uplusminus = []

        for j in range(aiu.cols):
            if aiu[j] > 0:
                uplus.append(j)
            elif aiu[j] < 0:
                uminus.append(j)
            else:
                uzero.append(j)

        for iplus in uplus:
            for iminus in uminus:
                if self.adjacent(A, Ut[:,iplus], Ut[:,iminus]):
                    newU = aiu[iplus]*Ut[:,iminus] - aiu[iminus]*Ut[:,iplus]
                    uplusminus.append(newU)

        for i in uminus[::-1]:
            Ut.col_del(i)

        for i in uplusminus:
            Ut = Ut.col_insert(Ut.rows, sp.Matrix([i]))

        return Ut

    #public
    def skeleton(self):
        cone_matrix = self.inequalities.row_insert(0, sp.Matrix.zeros(1, self.inequalities.cols)).\
            col_insert(0, sp.ones(self.inequalities.rows+1, 1))
        A, B = self.get_matrix_B(cone_matrix)
        size = B.rank()

        Ut = B.inv()

        for i in range(A.rows):
            Ut = self.skeleton_step(B.col_join(A), A[i,:], Ut)

        return Ut.T


    def intersectIsNotEmpty(self, top, bottom):
        for i in top:
            if i not in bottom:
                return False
        return True


    def get_vertices(self):
        dim = self.inequalities.cols
        eq_num = self.inequalities.rows

        res = []

        x = sp.symbols(','.join(['x'+str(i) for i in range(dim)]))
        for rows in itertools.combinations(range(eq_num), dim):
            A = self.inequalities[rows,:]
            b = sp.ones(dim, 1)

            res_current = linsolve(A.col_insert(A.cols, b),x)
            if res_current != sp.EmptySet():
                res.append(rows)

        return res


    def get_facets_n_level(self, level):
        dim = self.inequalities.cols
        eq_num = self.inequalities.rows
        needed_eq_num = dim - level + 1

        res = []

        x = sp.symbols(','.join(['x'+str(i) for i in range(dim)]))
        for rows in itertools.combinations(range(eq_num), needed_eq_num):
            A = self.inequalities[rows,:]
            b = sp.ones(needed_eq_num, 1)
            res_current = linsolve(A.col_insert(A.cols, b),x)
            if res_current != sp.EmptySet():
                res.append(rows)

        return res


    #public
    def get_hasse_diagram(self):
        self.hasse = hasse(self.inequalities.cols + 2, self.inequalities)
        for level in range(len(self.hasse.levels)):
            if level == 0:
                #vertexes
                empty = hasse_vertex('O', [], [])
                self.hasse.levels[level] = [empty]
            elif level == 1:
                #vertexes
                vertexes = self.get_vertices()
                for i in range(len(vertexes)):
                    temp = hasse_vertex(vertexes[i], [0], [])
                    self.hasse.levels[1].append(temp)
                #edges
                for i in range(len(self.hasse.levels[1])):
                    self.hasse.levels[1][i].previous_level = [0]
                    self.hasse.levels[0][0].next_level.append(i)
            #last vertex
            elif level == self.inequalities.cols + 1:
                #vertexes
                all = hasse_vertex('polyhedron', [], [])
                self.hasse.levels[level] = [all]
                #edges
                for i in range(len(self.hasse.levels[self.inequalities.cols])):
                    self.hasse.levels[self.inequalities.cols+1][0].previous_level.append(i)
                    self.hasse.levels[self.inequalities.cols][i].next_level = [0]
            else:
                #vertexes
                facets = self.get_facets_n_level(level)
                for i in range(len(facets)):
                    temp = hasse_vertex(facets[i], [], [])
                    self.hasse.levels[level].append(temp)
                #edges
                for i in range(len(self.hasse.levels[level])):
                    for j in range(len(self.hasse.levels[level-1])):
                        top = self.hasse.levels[level][i].value
                        bottom = self.hasse.levels[level-1][j].value
                        if self.intersectIsNotEmpty(top, bottom):
                            self.hasse.levels[level][i].previous_level.append(j)
                            self.hasse.levels[level-1][j].next_level.append(i)


    def hasse_diagram(self):
        return self.hasse.list_view()


    def get_faset_from_rows(self, rows, level):
        dim = self.inequalities.cols
        needed_eq_num = dim - level + 1

        A = self.inequalities[rows,:]
        b = sp.ones(needed_eq_num, 1)

        x = sp.symbols(','.join(['x'+str(i) for i in range(dim)]))
        res = linsolve(A.col_insert(A.cols, b),x)
        return res


    #public
    def vertices(self):
        res = sp.Matrix([])
        for i in self.hasse.levels[1]:
            current_res = sp.Matrix(list(self.get_faset_from_rows(i.value, 1)))
            if res.rows > 0:
                res = res.row_insert(res.rows, current_res)
            else:
                res = current_res

        return res

    #public
    def facets(self):
        res = sp.Matrix([])
        for i in self.hasse.levels[3]:
            current_res = sp.Matrix(list(self.get_faset_from_rows(i.value, 3)))
            if res.rows > 0:
                res = res.row_insert(res.rows, current_res)
            else:
                res = current_res

        return res

    #public
    def affine_hull(self):
        return self.inequalities

    #public
    def dim(self):
        return self.inequalities.cols

    #public
    def is_feasible(self):
        return self.dim() > 0

    #public
    def is_pointed(self):
        pass

    #public
    def bounded_facets(self):
        #посчитать 2^уровень в диаграме хасе,
        #вывести элементы со стольким количеством вершин
        pass

    #public
    def unbounded_facets(self):
        pass

    #public
    def is_bounded(self):
        skeleton_matrix = self.skeleton()
        for i in range(skeleton_matrix.rows):
            if skeleton_matrix[i,0] == 0:
                return False
        return True

    #public
    def N_points(self):
        return len(self.hasse.levels[1])

    #public
    def N_vertices_and_rays(self):
        return self.skeleton().rows

    #public
    def N_vertices(self):
        return len(self.hasse.levels[1])

    #public
    def N_rays(self):
        return self.skeleton().rows - self.N_vertices()

    #public
    def vertex_in_facet(self):
        pass

    def facets_thru_vertex(self):
        pass

    def graph(self):
        res = []
        for vertex in range(len(self.hasse.levels[1])):
            res.append([])
            current_res = set()
            for edge in self.hasse.levels[1][vertex].next_level:
                current_res = current_res |\
                    (set(self.hasse.levels[2][edge].previous_level) - \
                    set([vertex]))
            res[vertex] += (list(current_res))
        return res


    def dual_graph(self):
        pass

    def n_edges(self):
        return len(self.hasse.levels[2])

    def n_ridges(self):
        return len(self.hasse.levels[self.dim()])

    def vertex_degrees(self):
        return [len(i.next_level) for i in self.hasse.levels[1]]

    def facet_degrees(self):
        if self.dim() != 2:
            return [len(i.next_level) for i in self.hasse.levels[3]]
        else:
            return 0

    def f_vector(self):
        return [len(i) for i in self.hasse.levels]

    def is_simplical(self):
        pass

    def is_simple(self):
        pass


def main():
    P1 = polyhedron(name = "cube", dim = 3)
    #print P1.skeleton()
    #print
    #print P1.hasse_diagram()
    #print
    #print P1.vertices()
    #print
    #print P1.facets()
    #print
    #print P1.dim()

    #print
    A2 = sp.Matrix([[1,0], [-1, 0], [0,  1], [0, -1]])
    P2 = polyhedron(inequalities = A2)
    print P2.skeleton()
    print
    print P2.hasse_diagram()
    print
    print P2.f_vector()
    print
    print P2.graph()

    #print
    #A3 = sp.Matrix([[1,0], [-1, 0], [0, -1]])
    #P3 = polyhedron(inequalities = A3)
    #print P3.vertices()
    #print
    #for i in P3.hasse_diagram():
    #    print list(i[0]), list(i[1])
    #print
    #print P3.skeleton()
    #print P3.is_bounded()
    #print P3.vertex_degrees()

    #print
    #A4 = sp.Matrix([[1,0], [0, 1]])
    #P4 = polyhedron(inequalities = A4)
    #print P4.skeleton()



if __name__ == "__main__":
    main()
