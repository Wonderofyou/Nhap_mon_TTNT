
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
                
                solvable = utils.check_deadlock(current_state)
                
                if(solvable):
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
                                return current_weight+res[0], size/(1024**2) , path + [move], flag + [res[1]], node

                            # Thêm trạng thái con vào ngăn xếp với trọng số
                            stack.append((child, path + [move], current_weight+res[0], flag + [res[1]]))


            return 0, size /(1024**2), [], flag, node
        
        elif self.search_alg == 'BFS':
            queue = deque([(self.start, [], 0, [])])  # Queue holds tuples of (state, path, weight, flag)
            StateSpace.open_close_set.add(self.start.to_string())
            node = 1
            size = sys.getsizeof(self.start)
            while queue:
                current_state, path, current_weight, flag = queue.popleft()  # Pop from the front of the queue
                if current_state.is_completed():
                    return current_weight, size/(1024**2) , path, flag, node
                
                
                solvable = utils.check_deadlock(current_state)
                
                if(solvable):
                    continue


                for move in self.moves:
                    if current_state.can_move_or_push(move[0], move[1]):
                        child = copy.deepcopy(current_state)
                        res = child.get_child(move[0], move[1])
                        size+=sys.getsizeof(current_state)                     
                        child_weight = res[0]  # Weight of the child state
                        child_string = child.to_string()

                        # Only proceed if the state has not been visited
                        if child_string not in StateSpace.open_close_set:
                            node += 1
                            StateSpace.open_close_set.add(child_string)

                            if child.is_completed():
                                # If the state is complete, return immediately without adding it to the queue
                                return current_weight + res[0], size/(1024**2) , path + [move], flag + [res[1]], node
                        # Add the child state to the queue with the accumulated weight
                        queue.append((child, path + [move], current_weight + res[0], flag + [res[1]]))

            return 0, size/(1024**2) , [], flag, node

        elif self.search_alg == "UCS":
            heap_states = [(0, "", self.start, [], 0, [])] # heap holds the same things above, first element is priority level
            StateSpace.open_close_set.add(self.start.to_string())
            node = 1
            size = sys.getsizeof(self.start)
            while heap_states:
                cost, child_string, current_state, path, current_weight, flag = heapq.heappop(heap_states)
                if current_state.is_completed():
                    print(node, cost)
                    return current_weight, size/(1024**2), path, flag, node
                
                solvable = utils.check_deadlock(current_state)
                
                if(solvable):
                    continue
                

                for move in self.moves:
                    if current_state.can_move_or_push(move[0], move[1]):
                        child = copy.deepcopy(current_state)
                        res = child.get_child(move[0], move[1])
                        child_cost = 0
                        child_cost = cost + 1 + res[0]
                        size+=sys.getsizeof(self.start)

                        child_weight = res[0]  # Weight of the child state
                        child_string = child.to_string()

                        # Only proceed if the state has not been visited
                        if child_string not in StateSpace.open_close_set:
                            node += 1
                            StateSpace.open_close_set.add(child_string)

                            # if child.is_completed():
                            #     # If the state is complete, return immediately without adding it to the queue
                            #     return current_weight + res[0], size, path + [move], flag + [res[1]], node

                            # Add the child state to the heap with the accumulated weight
                            print(node, child_cost, move[0]*0.5 + move[1], move[0], move[1])
                            heapq.heappush(heap_states, (child_cost, child_string, child, path + [move], current_weight + res[0], flag + [res[1]]))
            return 0, size/(1024**2) , [], flag, node

        # (0, 1) (0, -1), (1, 0), (-1, 0)
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
                    print(node, g_score)
                    return current_weight, size/(1024**2), path, flag, node
                
                solvable = utils.check_deadlock(current_state)
                
                if(solvable):
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
                    
                            # if child.is_completed():
                            #     return current_weight + res[0], size, path + [move], flag + [res[1]], node


                    
                            # Tính f_score mới = g(n) + h(n)
                            child_g_score = 0
                            
                            child_g_score = g_score + res[0] + 1  # Chi phí thực tế từ start đến node hiện tại
                            
                            child_h_score = 0
                            
                            # if(res[1]):
                            #     child_h_score = utils.calculate_heuristic(child.box, switches)  # Ước lượng chi phí từ node hiện tại đến goal
                            #     #h_score = utils.simple_heuristic(child.box, switches)
                            # else:
                            #     child_h_score = f_score - g_score
                            
                            child_h_score = utils.calculate_heuristic(child.box, switches)
                            
                            child_f_score = child_g_score + child_h_score
                            print(node, child_g_score, move[0]*0.5 + move[1], move[0], move[1])
                            pq.put((child_f_score, child_g_score, counter, current_weight+ res[0], child, path + [move], flag + [res[1]]))
                            counter += 1
                    
            return 0, size/(1024**2), [], flag, node
