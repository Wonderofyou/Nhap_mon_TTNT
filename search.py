
import utils

from statespace import StateSpace
import sys
from collections import deque
import copy
import heapq
from queue import PriorityQueue


class Search:
    def __init__(self, search_alg, state, moves):
        self.search_alg = search_alg
        self.start = state
        self.moves = moves  
        

    def search(self):
        StateSpace.open_close_set.clear()
        if self.search_alg == 'DFS':
            stack = deque([(self.start, [], 0, [])])  # Stack holds tuples of (state, path, weight, flag)
            StateSpace.open_close_set.add(self.start.to_string())
            node = 1
            size = sys.getsizeof(self.start)

            while stack:
                current_state, path, current_weight, flag = stack.pop()

                if current_state.is_completed():
                    return current_weight, size/(1024**2) , path, flag, node
                
                is_deadlock = utils.check_deadlock(current_state)
                
                if(is_deadlock):
                    continue


                for move in self.moves:
                    if current_state.can_move_or_push(move[0], move[1]):
                        child = copy.deepcopy(current_state)
                        res = child.get_child(move[0], move[1])

                        

                        size += sys.getsizeof(self.start)
                        child_string = child.to_string()

                        # Chỉ tiến hành nếu trạng thái chưa được thăm
                        if child_string not in StateSpace.open_close_set:
                            node += 1
                            StateSpace.open_close_set.add(child_string)

                            if child.is_completed():
                                # Nếu trạng thái hoàn thành, không cần thêm vào ngăn xếp
                                return current_weight+res[0], size/(1024**2) , path + [move], flag + [res[0]], node

                            # Thêm trạng thái con vào ngăn xếp với trọng số
                            stack.append((child, path + [move], current_weight+res[0], flag + [res[0]]))


            return 0, size /(1024**2), [], flag, node

        if self.search_alg == 'BFS':
            queue = deque([(self.start, [], 0, [])])  # Queue holds tuples of (state, path, weight, flag)
            StateSpace.open_close_set.add(self.start.to_string())
            node = 1
            size = sys.getsizeof(self.start)

            while queue:
                current_state, path, current_weight, flag = queue.popleft()

                if current_state.is_completed():
                    return current_weight, size / (1024**2), path, flag, node
                
                is_deadlock = utils.check_deadlock(current_state)
                
                if(is_deadlock):
                    continue

                for move in self.moves:
                    if current_state.can_move_or_push(move[0], move[1]):
                        child = copy.deepcopy(current_state)
                        res = child.get_child(move[0], move[1])

                        size += sys.getsizeof(self.start)
                        child_string = child.to_string()

                        # Only proceed if the state has not been visited
                        if child_string not in StateSpace.open_close_set:
                            node += 1
                            StateSpace.open_close_set.add(child_string)

                            if child.is_completed():
                                # If state is completed, no need to add to the queue
                                return current_weight + res[0], size / (1024**2), path + [move], flag + [res[0]], node

                            # Add child state to the queue with weight
                            queue.append((child, path + [move], current_weight + res[0], flag + [res[0]]))

            return 0, size / (1024**2), [], flag, node


        elif self.search_alg == "UCS":
            pq = PriorityQueue()
            switches = utils.get_positions(self.start.matrix)
            weight = 0
            cost = 0 
            counter = 0
            pq.put((cost, counter, weight, self.start, [], []))
            counter += 1
            StateSpace.open_close_set.add(self.start.to_string())
            node = 1
            size = sys.getsizeof(self.start)
            while not pq.empty():
                cost, _, current_weight, current_state, path, flag = pq.get()
        
                if current_state.is_completed():
                    return current_weight, size/(1024**2), path, flag, node
                
                is_deadlock = utils.check_deadlock(current_state)
                
                if(is_deadlock):
                    continue

            
                for move in self.moves:
                    if current_state.can_move_or_push(move[0], move[1]):
                        child = copy.deepcopy(current_state)
                        res = child.get_child(move[0], move[1])
                        size+=sys.getsizeof(child)

                        
                        child_string = child.to_string()
                
                        if child_string not in StateSpace.open_close_set:
                            node += 1
                            StateSpace.open_close_set.add(child_string)
                            child_cost = 0
                            
                            child_cost = cost + res[0] + 1  # Chi phí thực tế từ start đến node hiện tại
                            pq.put((child_cost, counter, current_weight+ res[0], child, path + [move], flag + [res[0]]))

                            counter += 1                  
            return 0, size/(1024**2), [], flag, node

        elif self.search_alg == 'A*':
            pq = PriorityQueue()
            switches = utils.get_positions(self.start.matrix)
            h_score = utils.calculate_heuristic(self.start.box, switches)
            weight = 0
            g_score = 0 
            f_score = g_score + h_score
            counter = 0
            pq.put((f_score, g_score, counter, weight, self.start, [], []))
            counter += 1
            StateSpace.open_close_set.add(self.start.to_string())
            node = 1
            size = sys.getsizeof(self.start)
            while not pq.empty():
                f_score, g_score, _, current_weight, current_state, path, flag = pq.get()
        
                if current_state.is_completed():
                    return current_weight, size/(1024**2), path, flag, node
                
                is_deadlock = utils.check_deadlock(current_state)
                
                if(is_deadlock):
                    continue

            
                for move in self.moves:
                    if current_state.can_move_or_push(move[0], move[1]):
                        child = copy.deepcopy(current_state)
                        res = child.get_child(move[0], move[1])
                        size+=sys.getsizeof(child)

                        
                        child_string = child.to_string()
                
                        if child_string not in StateSpace.open_close_set:
                            node += 1
                            StateSpace.open_close_set.add(child_string)
                            # Tính f_score mới = g(n) + h(n)
                            child_g_score = 0
                            
                            child_g_score = g_score + res[0] + 1  # Chi phí thực tế từ start đến node hiện tại
                            
                            child_h_score = 0
                            if(res[1]):
                                child_h_score = utils.calculate_heuristic(child.box, switches)  # Ước lượng chi phí từ node hiện tại đến goal
                            else:
                                child_h_score = f_score - g_score
                            
                            child_f_score = child_g_score + child_h_score
                            pq.put((child_f_score, child_g_score, counter, current_weight+ res[0], child, path + [move], flag + [res[0]]))

                            counter += 1                  
            return 0, size/(1024**2), [], flag, node
        


import os              
import time
        

def write_to_file(inputfile, outputfile, algorithms, moves=[(0, -1), (0, 1), (-1, 0), (1, 0)]):
        start_state = StateSpace(filename=inputfile)
        
        # Clear previous content if needed
        with open(outputfile, 'w') as f:
            pass  # Just open in write mode to clear content
        
        for algorithm in algorithms:
            search_engine = Search(search_alg=algorithm, state=start_state, moves=moves)
            start_time = time.time()
            total_weight, size, path, flag, node = search_engine.search()
            end_time = time.time()
            print(path)
            total_time = 1000 * (end_time - start_time)
            
            path_str = []
            for (i, move) in enumerate(path):
                if move == (0, -1):
                    path_str.append('L' if flag[i] else 'l')
                elif move == (0, 1):
                    path_str.append('R' if flag[i] else 'r')
                elif move == (-1, 0):
                    path_str.append('U' if flag[i] else 'u')
                elif move == (1, 0):
                    path_str.append('D' if flag[i] else 'd')
                    
            path_str = "".join(path_str)
            print(len(path), total_weight)
            
            # Append results to output file
            with open(outputfile, 'a') as f:
                f.write(algorithm + '\n')
                f.write(f"Steps: {len(flag)}, Weight: {total_weight}, Node: {node}, Time (ms): {total_time}, Memory(MB): {size}\n")
                f.write(path_str + '\n')




from game import *
if __name__ =="__main__":

    for i in range (7,11):
        start_state = StateSpace(filename=f"input-{i:02}.txt")
        write_to_file(f"input-{i:02}.txt",f"output-{i:02}.txt",['UCS','A*','BFS','DFS'])
        Game = game(i)

        result = Game.load_move_from_file(f"output-{i:02}.txt")
        for(j,alg) in enumerate(result['algorithm']):
            start = StateSpace(f'input-{i:02}.txt')
            for move in result['instruction'][j] :
                start.get_child(move[0],move[1])

            if start.is_completed():
                print(f"YES {i}")



