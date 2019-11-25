from numba import njit
import numpy as np

global global_period

@njit
def lfsr(init_state, curr_state, polynom, period):
    i=0
    
    while True:    
        if i <= 10:
            summ = 0
            for j in range(curr_state.size):
                summ += curr_state[j] ^ init_state[j]
            print("AutoCorr.", i,": ", summ, curr_state)

        new_bit = 0
        for elem in polynom:
            new_bit ^= curr_state[elem]

        i += 1

        for j in range(curr_state.size - 1):
            curr_state[j] = curr_state[j+1]
        curr_state[-1] = new_bit

        check = True

        for j in range(curr_state.size):
            if curr_state[j] != init_state[j]:
                check = False
                break

        if check == True:
            period[0] = i
            return


def lab_experiments2(polynom):
    print("Polynom: {}\nq^(n)-1: {}".format(polynom, 2**(polynom[0]+1)-1))
    init_state = (1,) + (0,) * polynom[0]
    
    for i in range(polynom[0] + 1):
        init_stateArr = np.array(init_state, np.int64)
        polynomArr = np.array(polynom, np.int64)
        curr_stateArr = np.copy(init_stateArr)
        
        period = np.ones(1, dtype=np.int64)
        
        lfsr(init_stateArr, curr_stateArr, polynomArr, period)
        '''
        if period > global_period:
            global_period = period  
        '''
        print(f"\nInit State: {''.join(map(str, init_stateArr))}\nPeriod: {period[0]}\nCurr State: {''.join(map(str, curr_stateArr))}\n")
        init_state = (0,) + init_state[:-1]


def main():
    lab_experiments2((20, 18, 11, 10, 8, 7, 6, 5, 0))
    # lab_experiments2((24, 17, 14, 13, 12, 9, 6, 0))
    
    

if __name__ == "__main__":
    main()
