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

    def __str__(self):
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
        return self.hasse


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
        res = []
        for i in self.hasse.levels[1]:
            res.append(self.get_faset_from_rows(i.value, 1))

        return res

    #public
    def facets(self):
        res = []
        for i in self.hasse.levels[3]:
            res.append(self.get_faset_from_rows(i.value, 3))

        return res

    #public
    def affine_hull(self):
        return self.inequalities

    #public
    def bounded_facets(self):
        pass

    #public
    def unbounded_facets(self):
        pass

    #public
    def is_bounded(self, first, second, level):
        res = []
        first = self.hasse.levels[level][first]
        second = self.hasse.levels[level][second]

        previos_level_first = first.previous_level
        previos_level_second = second.previous_level

        intersection = set(previos_level_first).intersection(set(previos_level_second))

        return len(intersection) > 0

    #public
    def vertex_number(self):
        return len(self.hasse.levels[1])


def main():
    P1 = polyhedron(name = "cube", dim = 3)
    print P1.skeleton()
    print
    print P1.hasse_diagram()
    print
    print P1.vertices()
    print
    print P1.facets()
    print

    print
    A = sp.Matrix([[1,0], [-1, 0], [0,  1], [0, -1]])
    P2 = polyhedron(inequalities = A)
    print P2.hasse_diagram()
    print
    print P2.is_bounded(0, 1, 2) #true
    print
    print P2.is_bounded(0, 3, 2) #false
    print
    print P2.vertex_number()



if __name__ == "__main__":
    main()
