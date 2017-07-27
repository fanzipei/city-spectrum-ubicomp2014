#!/usr/bin/env python
# encoding: utf-8

import numpy as np
from numpy.linalg import inv
from numpy.linalg import norm

# Constant Definition
K = 10
LAMBDA = 0.5
MAXITER = 5
num_time = 48


def read_file(filename):

    # with open( filename , 'r' ) as f:
        # line = f.readline()
        # num_locations, num_time, num_days = [ int(n) for n in line.split() ]
        # tensor_list = np.zeros( [num_locations,num_time,num_days] )

        # # Read tensor from file
        # for i in range(num_locations):

            # # Read the coordinates
            # line = f.readline()
            # dis_lat, dis_lon = [ int(n) for n in line.split() ]

            # # Read the POI vector
            # line = f.readline()

            # # Read the people flow matrix of each location
            # for j in range(num_time):
                # line = f.readline()
                # tensor_list[i][j] = [ float(n) for n in line.split() ]
    tensor = np.genfromtxt(filename, dtype=np.float, delimiter=',')
    num_locations = tensor.shape[0]
    num_days = tensor.shape[1] / num_time
    tensor = tensor.reshapea([-1, num_time, num_days])

    return num_locations, num_time, num_days, tensor

def khatrirao(a, b):
    assert a.shape[1] == b.shape[1]
    return np.array( [np.outer(col_a,col_b).flatten().T for col_a, col_b in zip( a.T , b.T )] ).T


def cal_rec_error(y1, u, v, w):
    uvw = u.dot(khatrirao(w, v).T)
    return norm(y1 - uvw)


def cal_rec_error_loc(y1, u, v, w):
    uvw = u.dot(khatrirao(w, v).T)
    return norm(y1 - uvw, axis=1)


def cal_rec_error_time(y2, u, v, w):
    uvw = v.dot( khatrirao(w, u).T )
    return norm(y2 - uvw, axis=1)


def cal_rec_error_day(y3, u, v, w):
    uvw = w.dot(khatrirao(v, u).T)
    return norm(y3 - uvw, axis=1)


def ntf(tensor, num_locations, num_time, num_days, K, LAMBDA, MAXITER):
    # Normalize the tensor
    norm_t = tensor.sum(axis=0)
    for i in range(num_time):
        for j in range(num_days):
            tensor[:, i, j] /= norm_t[i][j]

    # Unfolding
    y_1 = np.concatenate([tensor[:, :, i] for i in range(num_days)], axis=1)
    y_2 = np.concatenate([tensor[:, :, i].T for i in range( num_days )], axis=1)
    y_3 = np.concatenate([tensor[:, i, :].T for i in range( num_time )], axis=1)

    # Initialize the best configuration
    u_best = np.zeros([num_locations, K])
    v_best = np.zeros([num_time, K])
    w_best = np.zeros([num_days, K])
    least_error = np.inf

    # N trial of Factorization
    for i in range(10):

        # Factorization initialization
        u = np.random.ranf( [num_locations, K] )
        v = np.random.ranf( [num_time, K] )
        w = np.random.ranf( [num_days, K] )

        # Factorization iteration
        for j in range(MAXITER):
            print 'Iteration %d' % (j+1)
            u = y_1.dot( khatrirao( w , v ) ).dot( inv( w.T.dot( w ) * v.T.dot( v ) + LAMBDA * np.identity(K) ) )
            # u = ( y_1.dot( khatrirao( w , v ) ) - LAMBDA ).dot( inv( w.T.dot( w ) * v.T.dot( v ) ) )
            u[u < 0] = 1e-10
            v = y_2.dot( khatrirao( w , u ) ).dot( inv( w.T.dot( w ) * u.T.dot( u ) + LAMBDA * np.identity(K) ) )
            v[v < 0] = 1e-10
            # v = ( y_2.dot( khatrirao( w , u ) ) - LAMBDA ).dot( inv( w.T.dot( w ) * u.T.dot( u ) ) )
            w = y_3.dot( khatrirao( v , u ) ).dot( inv( v.T.dot( v ) * u.T.dot( u ) + LAMBDA * np.identity(K) ) )
            w[w < 0] = 1e-10
            # w = ( y_3.dot( khatrirao( v , u ) ) - LAMBDA ).dot( inv( v.T.dot( v ) * u.T.dot( u ) ) )

        # Best configuration
        cur_error = cal_rec_error( y_1 , u, v, w )
        if cur_error < least_error:
            least_error = cur_error
            u_best = u
            v_best = v
            w_best = w

    # Calculate the error
    eu = cal_rec_error_loc( y_1 , u_best , v_best , w_best )
    ev = cal_rec_error_time( y_2 , u_best , v_best , w_best )
    ew = cal_rec_error_day( y_3 , u_best , v_best , w_best )

    return (u_best, v_best, w_best, eu, ev, ew)

def main():

    # Read file
    num_locations, num_time, num_days, tensor = read_file('./fukushima_coastal_pd.csv')

    # Decomposition
    (u, v, w, eu, ev, ew) = ntf( tensor , num_locations , num_time , num_days , K , LAMBDA , MAXITER )

    # Output
    np.savetxt( 'location.csv' , u.T , delimiter=',' )
    np.savetxt( 'time_slice.csv' , v.T , delimiter=',' )
    np.savetxt( 'days.csv' , w.T , delimiter=',' )
    np.savetxt( 'error_loc.csv' , eu.T , delimiter=',' )
    np.savetxt( 'error_time.csv' , ev.T , delimiter=',' )
    np.savetxt( 'error_day.csv' , ew.T , delimiter=',' )

if __name__ == '__main__':
    main()
