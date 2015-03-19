from sympy import Matrix


#TODO
def gauss( a, f, e, q ,r, perm, intarith, eps):
    m = a.rows
    n = a.cols

    f.assign_eye(n) #TODO what is assign_eye?
    e.resize(0, n) #TODO

    q = transpose(a) #TODO

    for i in range(min(q.cols, q.rows)):
        q_pivot = abs(q[i][i]) #TODO
        j_pivot = i
        for j in range(i+1, m): #TODO
            if abs(q[i][j] > q_pivot: #TODO
                j_pivot = j
                q_pivot = abs(q[i][j])
    if q_pivot <= eps:
        # it's a zero row
        q.erase_row(i) #TODO
        e.insert_row(e.rows, f.take_row(i)) #TODO
        continue

    if i != j_pivot:
        q.swap_cols(i, j_pivot) #TODO swap?
        perm.swap_els(i, j_pivot) #TODO swap?

    if q[i][i] < 0:
        q.mult_row(i, -1) #TODO
        f.mult_row(i, -1) #TODO
    #TODO ...
    # branch test
    print "test gauss"


#TODO
def do_ddm( ineq, 
            eq, 
            ext, 
            bas, 
            dis, 
            edges_ind, 
            totalnumrays, 
            totalnumedges, 
            edgesflag, 
            order, 
            prefixed_order, 
            graphadj, 
            plusplus, 
            intarith, 
            eps,
            logonstdout,
            logfileflag,
            logfile ):
    print "test do_ddm"


def ddm( ineq, 
         eq, 
         ext, 
         bas, 
         dis, 
         edges_ind, 
         totalnumrays, 
         totalnumedges, 
         edgesflag, 
         order, 
         prefixed_order, 
         graphadj, 
         plusplus, 
         intarith, 
         eps,
         logonstdout,
         logfileflag,
         logfile ):
    if (eq.rows == 0):
        do_ddm()#TODO
    else:
        bus_sub = Matrix()
        f = Matrix()
        q = Matrix()

        m = ineq.rows
        perm = []
        for j in range(m):
            perm.append(j)
        gauss()#TODO
        do_ddm()#TODO

        ext = ext*bas_sub
        bas = bas*bas_sub

        ext_nrows = ext.rows
        bas_nrows = bas.rows

        for ii in range(ext_nrows):
            if (intarith):
                print "test intarith true"
                #delta = gcd(ext.copy_row(ii))#TODO copy_row in cympy
            else:
                print "test intarith false"
                #delta = firstnonzero(ext.copy_row(ii), eps)#TODO the same as below
            #bas.div_row(ii, delta)#TODO div_row
        print "test ddm"


def main():
    ineq = Matrix()
    eq = Matrix()
    ext = Matrix()
    bas = Matrix()
    dis = Matrix()
    edges_ind = Matrix()
    totalnumrays = 10
    totalnumedges = 5
    edgesflag = 1
    order = 1
    prefixed_order = 1
    graphadj = 1
    plusplus = 1
    intarith = 1
    eps = 0.1
    logonstdout = 1
    logfileflag = 1
    logfile = ""
    ddm(ineq, 
        eq, 
        ext, 
        bas, 
        dis, 
        edges_ind, 
        totalnumrays, 
        totalnumedges,
        edgesflag,
        order,
        prefixed_order,
        graphadj,
        plusplus,
        intarith,
        eps,
        logonstdout,
        logfileflag,
        logfile)

if __name__ == "__main__":
    main()

