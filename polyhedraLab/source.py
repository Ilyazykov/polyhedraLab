import numpy as np
import sympy as sp


def get_matrix_B(cone_matrix): #TODO: rename
    size = cone_matrix.rank()
    B = cone_matrix[:size,:]
    A = cone_matrix[size:,:]
    if (B.rank() != size):
        raise ValueError('Degenerate matrix')
    return A, B


def adjacent(plus, minus): #TODO realize function!!!
    #DEBUG: print plus
    #DEBUG: print minus
    return True


def step(new_row, Ut): #TODO: rename
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
            if adjacent(Ut[:,iplus], Ut[:,iminus]):
                newU = aiu[iplus]*Ut[:,iminus] - aiu[iminus]*Ut[:,iplus]
                uplusminus.append(newU)

    #DEBUG: print uminus[::-1]
    for i in uminus[::-1]:
        Ut.col_del(i)

    #DEBUG: print np.matrix(Ut)

    for i in uplusminus:
        Ut = Ut.col_insert(Ut.rows, sp.Matrix([i]))

    #DEBUG: print np.matrix(Ut)
    return Ut

def double_description(cone_matrix):
    A, B = get_matrix_B(cone_matrix)
    size = B.rank()

    Ut = B.inv()

    #DEBUG: print np.matrix(Ut)

    for i in range(A.rows):
        Ut = step(A[i,:], Ut)

    #DEBUG: print np.matrix(Ut)


if __name__ == "__main__":
    a = sp.Matrix([[1,-1,0],[1,1,0],[1,0,1],[1,0,-1],[1,0,0]])
    double_description(a)
