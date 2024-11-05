
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
        if self.search_alg == 'DFS':
            stack = deque([(self.start, [], 0, [])])  # Stack holds tuples of (state, path, weight, flag)
            StateSpace.open_close_set.add(self.start.to_string())
            node = 1
            size = sys.getsizeof(self.start)

            while stack:
                current_state, path, current_weight, flag = stack.pop()

                if current_state.is_completed():
                    return current_weight, size/(1024**2) , path, flag, node

                for move in self.moves:
                    if current_state.can_move_or_push(move[0], move[1]):
                        child = copy.deepcopy(current_state)
                        res = child.get_child(move[0], move[1])
                        node += 1
                        size += sys.getsizeof(self.start)

                        child_string = child.to_string()

                        # Chỉ tiến hành nếu trạng thái chưa được thăm
                        if child_string not in StateSpace.open_close_set:
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

                for move in self.moves:
                    if current_state.can_move_or_push(move[0], move[1]):
                        child = copy.deepcopy(current_state)
                        res = child.get_child(move[0], move[1])
                        node += 1
                        size+= sys.getsizeof(self.start)
                        child_string = child.to_string()

                        # Only proceed if the state has not been visited
                        if child_string not in StateSpace.open_close_set:
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
                    return current_weight, size/(1024**2), path, flag, node
                for move in self.moves:
                    if current_state.can_move_or_push(move[0], move[1]):
                        child = copy.deepcopy(current_state)
                        res = child.get_child(move[0], move[1])
                        size+=sys.getsizeof(self.start)

                        if res[1]:
                            cost += (1 + res[0])
                        else:
                            cost += 1
                        node += 1
                        child_weight = res[0]  # Weight of the child state
                        child_string = child.to_string()

                        # Only proceed if the state has not been visited
                        if child_string not in StateSpace.open_close_set:
                            StateSpace.open_close_set.add(child_string)

                            if child.is_completed():
                                # If the state is complete, return immediately without adding it to the queue
                                return current_weight + res[0], size/(1024**2), path + [move], flag + [res[1]], node

                            # Add the child state to the heap with the accumulated weight
                            #print(node, cost, move[0]*0.5 + move[1], move[0], move[1])
                            heapq.heappush(heap_states, (cost, child_string, child, path + [move], current_weight + res[0], flag + [res[1]]))
            return 0, size/(1024**2) , [], flag, node
        # (0, 1) (0, -1), (1, 0), (-1, 0)
        elif self.search_alg == 'AStar':
            pq = PriorityQueue()
            counter = 0
            initial_h = 0
            pq.put((initial_h, 0, counter, self.start, [], []))
            counter += 1
            StateSpace.open_close_set.add(self.start.to_string())
            node = 1
            switches = utils.get_positions(self.start.matrix)
            size = sys.getsizeof(self.start)
            while not pq.empty():
                f_score, current_weight, _, current_state, path, flag = pq.get()
        
                if current_state.is_completed():
                    return current_weight, size/(1024**2), path, flag, node
            
                for move in self.moves:
                    if current_state.can_move_or_push(move[0], move[1]):
                        child = copy.deepcopy(current_state)
                        res = child.get_child(move[0], move[1])
                        node += 1
                        size+=sys.getsizeof(child)
                        
                        child_string = child.to_string()
                
                        if child_string not in StateSpace.open_close_set:
                            StateSpace.open_close_set.add(child_string)
                    
                            if child.is_completed():
                                return current_weight + res[0], size/(1024**2), path + [move], flag + [res[1]], node
                    
                            # Tính f_score mới = g(n) + h(n)
                            
                            g_score = current_weight + res[0] + 1  # Chi phí thực tế từ start đến node hiện tại
                            
                            if(res[1]):
                                h_score = utils.calculate_heuristic(child.box, switches)  # Ước lượng chi phí từ node hiện tại đến goal
                            else:
                                h_score = f_score - current_weight
                            f_score = g_score + h_score
                    
                            pq.put((f_score, g_score, counter, child, path + [move], flag + [res[1]]))
                            counter += 1
                    
            return 0, size/(1024**2), [], flag, node
