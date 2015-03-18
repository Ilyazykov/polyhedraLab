from sympy import Matrix


#TODO
def gauss():
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

