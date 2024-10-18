# I used simulated annealing instead of sweeping the values.
# All the SA parameters can be found below.
# The heuristic was the lowest value of id1 + id2.

# I swept wl1 and wl2 between 1-10000 for the first result here:

# Final result:
# id1 + id2: 1.9531252573591942 mA
# vov1: 0.2
# wl1: 1464.4298150661193
# wl2: 8.678107178689256
# rd: 2048
# id1: 0.0014644298150661196
# vds1: 2.000847738744587
# vov2: 1.500847738744587
# id2: 0.0004886954422930747
# vds2: 3.999151734183783

# And between 1-100 (more realistic) for this result here:

# Final result:
# id1 + id2: 2.4458095841147434 mA
# vov1: 0.8918315781864689
# wl1: 100
# wl2: 100
# rd: 2048
# id1: 0.001988408909626419
# vds1: 0.9277385530850939
# vov2: 0.4277385530850939
# id2: 0.0004574006744883242
# vds2: 4.063243418647912

import random
def initialize():
    vov1 = random.random() * 4.3 + 0.2 # 0.2-4.5
    wl1 = random.random() * 9999 + 1 # 1-10000
    wl2 = random.random() * 9999 + 1 # 1-10000
    rd = random.random() * 2048 # 0-2048
    return vov1, wl1, wl2, rd

def heuristic(vov1, wl1, wl2, rd):
    id1 = 0.5 * (50 * 10 ** -6) * wl1 * (vov1 ** 2)
    vds1 = 5 - id1 * rd
    vov2 = vds1 - 0.5
    id2 = 0.5 * (50 * 10 ** -6) * wl2 * (vov2 ** 2)
    return id1 + id2

def check_validity(vov1, wl1, wl2, rd):
    id1 = 0.5 * (50 * 10 ** -6) * wl1 * (vov1 ** 2)
    vds1 = 5 - id1 * rd
    if vds1 < 0.7 or vds1 < vov1:
        return False
    vov2 = vds1 - 0.5
    id2 = 0.5 * (50 * 10 ** -6) * wl2 * (vov2 ** 2)
    vds2 = 5 - id2 * rd
    if vds2 < vov2:
        return False
    if ((id1 * id2) / (vov1 * vov2)) * (rd ** 2) < 10:
        return False
    return True

def clamp(val, lower, upper):
    return max(lower, min(val, upper))

def print_result(vov1, wl1, wl2, rd):
    print(f'id1 + id2: {1000 * heuristic(vov1, wl1, wl2, rd)} mA')
    id1 = 0.5 * (50 * 10 ** -6) * wl1 * (vov1 ** 2)
    vds1 = 5 - id1 * rd
    vov2 = vds1 - 0.5
    id2 = 0.5 * (50 * 10 ** -6) * wl2 * (vov2 ** 2)
    vds2 = 5 - id2 * rd
    print(f'vov1: {vov1}')
    print(f'wl1: {wl1}')
    print(f'wl2: {wl2}')
    print(f'rd: {rd}')
    print(f'id1: {id1}')
    print(f'vds1: {vds1}')
    print(f'vov2: {vov2}')
    print(f'id2: {id2}')
    print(f'vds2: {vds2}')
    print('\n')

def update_vals(vov1, wl1, wl2, rd, temp):
    vov1 = vov1 + vov1 * (random.random() - 0.5) * temp
    vov1 = clamp(vov1, 0.2, 4.5)
    wl1 = wl1 + wl1 * (random.random() - 0.5) * temp
    wl1 = clamp(wl1, 1, 10000)
    wl2 = wl2 + wl2 * (random.random() - 0.5) * temp
    wl2 = clamp(wl2, 1, 10000)
    rd = rd + rd * (random.random() - 0.5) * temp
    rd = clamp(rd, 0, 2048)
    return vov1, wl1, wl2, rd

if __name__ == '__main__':
    current_min = 10000
    best_vov1 = None
    best_wl1 = None
    best_wl2 = None
    best_rd = None
    for j in range(100):
        while True:
            vov1, wl1, wl2, rd = initialize()
            if check_validity(vov1, wl1, wl2, rd):
                break
        temp = 1
        while True:
            temp = temp * 0.99
            for i in range(100000):
                vov1m, wl1m, wl2m, rdm = update_vals(vov1, wl1, wl2, rd, temp)
                if check_validity(vov1m, wl1m, wl2m, rdm) and heuristic(vov1, wl1, wl2, rd) > heuristic(vov1m, wl1m, wl2m, rdm):
                    vov1, wl1, wl2, rd = vov1m, wl1m, wl2m, rdm
                    break
            if i == 99999:
                break
        if heuristic(vov1, wl1, wl2, rd) < current_min:
            current_min = heuristic(vov1, wl1, wl2, rd)
            best_vov1, best_wl1, best_wl2, best_rd = vov1, wl1, wl2, rd
        print_result(vov1, wl1, wl2, rd)
    print("Final result:")
    print_result(best_vov1, best_wl1, best_wl2, best_rd)
