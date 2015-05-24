import numpy as np
import sympy as sp
import random


def get_matrix_B(cone_matrix): #TODO:
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


def adjacent(A, u1, u2):
    temp = sp.Matrix.zeros(0,A.cols)
    for i in range(A.rows):
        if (A[i,:]*u1)[0] == 0 and (A[i,:]*u2)[0] == 0:
            temp = temp.col_join(A[i,:])
    if temp.rank() == A.rank() - 2:
        return True
    return False


def step(A, new_row, Ut): #TODO: to come up with the name of the function
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
            if adjacent(A, Ut[:,iplus], Ut[:,iminus]):
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
        Ut = step(B.col_join(A) ,A[i,:], Ut)

    return np.matrix(Ut)


if __name__ == "__main__":
    a = sp.Matrix([[1,-1,0],[1,1,0],[1,0,1],[1,0,-1],[1,0,0]])
    res = double_description(a)
    print np.matrix(res)
