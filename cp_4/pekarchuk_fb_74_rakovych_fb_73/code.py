from numba import cuda, jit, njit, vectorize, types
from numba.typed import List, Dict
import numpy as np
import random
from collections import defaultdict
import asyncio

@njit()
def lfsr(init_state, curr_state, polynom, period):
    counter = 0
    prev_list = List()
    while True:
        for i in range(0, curr_state.size):
            prev_list.append(curr_state[i])

        for i in range(0, curr_state.size):
            if curr_state[i] == prev_list[i]:
                # for j in range(0, curr_state.size):
                for i in range(0, curr_state.size):
                    prev_list.append(curr_state[i])

        new_bit = 0
        for item in polynom:
            if item != init_state.size:
                new_bit ^= curr_state[item]

        counter += 1
        if counter > curr_state.size:
            print(counter)

        for j in range(curr_state.size-1):
            curr_state[j] = curr_state[j+1]
        curr_state[-1] = new_bit

        validated = True
        for j in range(curr_state.size):
            if curr_state[j] != init_state[j]:
                validated = False
                break

        if validated:
            period[0] = counter
            return prev_list

    return None


async def get_polygrams(prev, num, out_file):
    result = defaultdict(int)
    poly_counter = 0
    poly_string = ''

    for item in prev:
        poly_string += str(item)
        if len(poly_string) == num:
            result[poly_string] += 1
            poly_string = poly_string[1::1]
            poly_counter -= -1 # oh yeah baby

    message = f"{num}-gramm: total count = {poly_counter}: \n{result}\n\n"
    print(message)
    out_file.write(message)
    return poly_counter


def runner(polynom, out_file):

    initial_message = f"Polynom: {polynom}\nq ** (n) - 1: {2 ** (polynom[0]) - 1}"
    print(initial_message)
    out_file.write(initial_message)
    
    init_state = [1] + [0] * (polynom[0] - 1)
    for i in range(polynom[0]):
        if i < polynom[0] - 1:
            init_state = [0] + init_state[:-1]
            continue

        initial_array = np.array(init_state, np.int64)
        polynom_array = np.array(polynom, np.int64)
        current_array = np.copy(initial_array)
        autocorr_dict = defaultdict(int)

        period = np.ones(1, dtype=np.int64)
        res = lfsr(  # linear feedback shift register runs here
            initial_array,
            current_array,
            polynom_array,
            period
        )

        print(period[0], autocorr_dict)
        for d in range(1, 11):
            for i in range(0, period[0]):
                autocorr_dict[d] += (res[i] ^ res[(i+d) % period[0]]) % 2

        message = (
            f"\nInitial state: {''.join([str(i) for i in initial_array])}\n"
            f"period: {period[0]}\n"
            f"result state: {''.join([str(i) for i in current_array])}\n"
            f"autocorrection values: {autocorr_dict}\n" + "=" * 40 + "\n"
        )
        print(message)
        out_file.write(message)

        # running getting polygrams in async
        loop = asyncio.get_event_loop()
        futures = list()
        for i in range(1, 6):
            futures.append(get_polygrams(res, i, out_file))

        results = loop.run_until_complete(asyncio.gather(*futures))
        loop.close()

        for result in results:
            print(result)

        init_state = [0] + init_state[:-1]

    return


def main():
    polynoms = [
        (20,18,11,10,8,7,6,5,0),
    ]
    for i in range(0, len(polynoms)):
        filename = f"out{i}.txt"
        out_file = open(filename, "w") 
        runner(polynoms[i], out_file)
        out_file.close()


if __name__ == "__main__":
    main()
