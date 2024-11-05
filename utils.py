import numpy as np
from scipy.optimize import linear_sum_assignment

def get_positions(map_matrix):
    switches = []
    
    for row in range(len(map_matrix)):
        for col in range(len(map_matrix[row])):
            if map_matrix[row][col] in (".", "+", "*"):
                switches.append((row, col))
    
    return switches

def min_weighted_distance(stones, switches, weights):

    # Tạo ma trận chi phí dựa trên khoảng cách Manhattan có trọng số giữa các stones và switches
    cost_matrix = np.zeros((len(stones), len(switches)))

    for i, (stone_row, stone_col) in enumerate(stones):
        weight = weights[i]  # Trọng lượng của viên đá i
        for j, (switch_row, switch_col) in enumerate(switches):
            # Tính khoảng cách Manhattan và nhân với trọng lượng
            distance = abs(stone_row - switch_row) + abs(stone_col - switch_col)
            cost_matrix[i][j] = weight * distance
    
    # Áp dụng thuật toán Hungarian để tìm cách gán tối ưu
    stone_indices, switch_indices = linear_sum_assignment(cost_matrix)
    
    # Tổng khoảng cách có trọng số tối thiểu
    min_weighted_distance = cost_matrix[stone_indices, switch_indices].sum()


    return min_weighted_distance  
  
def get_first_two_elements(arrays):
    return [array[:2] for array in arrays]
<<<<<<< HEAD

=======
>>>>>>> 9876863e0b981fa2360546ab4dc2410c6f8e5aac
def cost_g(switches, stones, weights):
    stones_postions = get_first_two_elements(stones)
    return min_weighted_distance(stones_postions, switches, weights)


<<<<<<< HEAD


def get_manhattan_distance(point1, point2):
    return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])


def calculate_heuristic(stones, switches):
        # Lấy vị trí các target
        cost_matrix = np.zeros((len(stones), len(switches)))
        
        for i,stone in enumerate(stones):
            for j,switch in enumerate(switches):
                # Chi phí = trọng số * khoảng cách Manhattan
                cost = stone[2] * get_manhattan_distance((stone[0], stone[1]), switch)
                cost_matrix[i][j] = cost
                
                
        stone_indices, switch_indices = linear_sum_assignment(cost_matrix)
        
        min_weighted_distance = cost_matrix[stone_indices, switch_indices].sum()
    
        return min_weighted_distance  
=======
>>>>>>> 9876863e0b981fa2360546ab4dc2410c6f8e5aac
