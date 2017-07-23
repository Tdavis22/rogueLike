import numpy as np

#sigmoid function
def nonlin(x, deriv = False):
    if(deriv == True): #we want the derivative when we calculate error
        return(x * (1 - x ))

    return 1/(1 + np.exp(-x))


#test data
x = np.array([[0,0,1],
[0,1,1],
[1,0,1],
[1,1,1]])

#testing data results. [0,0,1] = 0 a failure
# [0,1,1] = 1 a success
y = np.array([[0], [1], [1], [0]])

#SCREEN_WIDTH
np.random.seed(1)

#synapses

syn0 = 2 * np.random.random((3,4)) - 1 #1 is our bias
syn1 = 2 * np.random.random((4,1)) - 1 #four nodes for one output?

#layers aren't actual strucutres just abstractions of probobility

#training
#continuously inputting data.

for j in range(0, 6000):
    l0 = x
    l1 = nonlin(np.dot(l0, syn0))
    l2 = nonlin(np.dot(l1, syn1))

#back propogation
    l2_error = y - l2 #arbitrary error
    if (j % 5000) == 0:
        print( "error:" + str(np.mean(np.abs(l2_error))))

    l2_delta = l2_error * nonlin(l2, deriv=True)

    l1_error = l2_delta.dot(syn1.T) #matrix transposed

    l1_delta = l1_error * nonlin(l1, deriv = True)

    #use these deltas to update our weights/Synapses from sigmoid function
    syn1 += l1.T.dot(l2_delta) #first layer transposed multiplied by second layer deltas
    syn0 += l0.T.dot(l1_delta)
print ("output after training")
print(l2)
