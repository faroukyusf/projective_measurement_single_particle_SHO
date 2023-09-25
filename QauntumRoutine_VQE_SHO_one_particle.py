#!/usr/bin/env python
# coding: utf-8

# In[3]:


# function that takes any n cpomonent vector and map it to 2^n component vector 
def map_2n_vec(state):
    psi = [0] * (2**len(state))
    num = '0' * (len(state)-1)
    for i in range(len(state)):
        nthcomp = state[i]
        binum = num[:i] + "1" + num[i:]
        m = int(binum, 2)
        psi[m] = nthcomp
    return psi


# This is the quatum routine of the VQE algorithm for this problem.
# It's worth mentioning that the following function 'Projective_Expected' does the quantum routine part on qiskit. 
# And by that I mean, later on ahead, if the VQE algorithm is to be run on fake simulators or real qubits then 
# the function 'Projective_Expected' won't be useful. Only then, we will have to use Estimator class.
# That class enables the computation of expectation values on real or semi-real setup of qubits. 

# In[4]:


##==================## THE PROJECTVIE MEASUREMENTS CURCUIT [QUANTUM ROUTINE] ##==================##
simulator = Aer.get_backend('aer_simulator')

def Projective_Expected(psi, h, l):
    E_ = 0.0
    trials = 10**5
    
    state = map_2n_vec(psi)

    ##==== <X0 ⊗ X1> measurement ====## 
    for i in range(len(psi)-1):
        qc = QuantumCircuit(len(psi), 2) 
        qc.initialize(state)
        qc.h(i)
        qc.h(i+1)
        qc.measure([i, i+1], [0, 1])
        
        job = execute(qc, simulator, shots = trials, seed = 3567)
        result = job.result()
        counts = result.get_counts(qc)
        
        list = counts
        
        E_ += -h*(list.get('00', 0) + list.get('11', 0) - list.get('10', 0) - list.get('01', 0))/trials/2
     
    ##==== <Y0 ⊗ Y1> measurement ====## 
    for i in range(len(psi)-1):
        qc = QuantumCircuit(len(psi), 2) 
        qc.initialize(state)
        qc.p(-np.pi/2, i)
        qc.h(i)
        qc.p(-np.pi/2, i+1)
        qc.h(i+1)
        qc.measure([i, i+1], [0, 1])
        
        job = execute(qc, simulator, shots = trials, seed = 3567)
        result = job.result()
        counts = result.get_counts(qc)
        
        list = counts
        
        E_ += -h*(list.get('00', 0) + list.get('11', 0) - list.get('10', 0) - list.get('01', 0))/trials/2
    
    
#     ##==== <Z> measurement ====## 
    for i in range(len(psi)):
        qc = QuantumCircuit(len(psi), 1) 
        qc.initialize(state)
        qc.measure([i], [0])
        
        job = execute(qc, simulator, shots = trials, seed = 3567)
        result = job.result()
        counts = result.get_counts(qc)
        
        list = counts
        
        x = i-((len(psi)-1)/2)

        E_ += -l*x**2*(list.get('0', 0) - list.get('1', 0))/trials/2
        E_ += l*x**2/2
    
    E_ += 2*h

    return E_

