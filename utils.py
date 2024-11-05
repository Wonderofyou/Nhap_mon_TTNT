import numpy as np
from scipy.optimize import linear_sum_assignment

def get_positions(map_matrix):
    switches = []
    
    for row in range(len(map_matrix)):
        for col in range(len(map_matrix[row])):
            if map_matrix[row][col] in (".", "+", "*"):
                switches.append((row, col))
    
    return switches


def get_manhattan_distance(point1, point2):
    return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])


def calculate_heuristic(stones, switches):
        cost_matrix = np.zeros((len(stones), len(switches)))
        
        for i,stone in enumerate(stones):
            for j,switch in enumerate(switches):
                # Chi phí = trọng số * khoảng cách Manhattan
                cost = stone[2] * get_manhattan_distance((stone[0], stone[1]), switch)
                cost_matrix[i][j] = cost
                
                
        stone_indices, switch_indices = linear_sum_assignment(cost_matrix)
        
        min_weighted_distance = cost_matrix[stone_indices, switch_indices].sum()
    
        return min_weighted_distance  
