import utils
from statespace import StateSpace
import sys
from collections import deque
import copy
import heapq
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
                    return current_weight, size , path, flag, node

                for move in self.moves:
                    if current_state.can_move_or_push(move[0], move[1]):
                        child = copy.deepcopy(current_state)
                        res = child.get_child(move[0], move[1])
                        node += 1

                        if res is not None:
                            child_string = child.to_string()

                            # Chỉ tiến hành nếu trạng thái chưa được thăm
                            if child_string not in StateSpace.open_close_set:
                                StateSpace.open_close_set.add(child_string)

                                if child.is_completed():
                                    # Nếu trạng thái hoàn thành, không cần thêm vào ngăn xếp
                                    return current_weight+res[0], size , path + [move], flag + [res[1]], node

                                # Thêm trạng thái con vào ngăn xếp với trọng số
                                stack.append((child, path + [move], current_weight+res[0], flag + [res[1]]))


            return 0, size , [], flag, node
        
        elif self.search_alg == 'BFS':
            queue = deque([(self.start, [], 0, [])])  # Queue holds tuples of (state, path, weight, flag)
            StateSpace.open_close_set.add(self.start.to_string())
            node = 1
            size = sys.getsizeof(self.start)

            while queue:
                current_state, path, current_weight, flag = queue.popleft()  # Pop from the front of the queue

                if current_state.is_completed():
                    return current_weight, size , path, flag, node

                for move in self.moves:
                    if current_state.can_move_or_push(move[0], move[1]):
                        child = copy.deepcopy(current_state)
                        res = child.get_child(move[0], move[1])
                        node += 1
                        if res is not None:
                            child_weight = res[0]  # Weight of the child state
                            child_string = child.to_string()

                            # Only proceed if the state has not been visited
                            if child_string not in StateSpace.open_close_set:
                                StateSpace.open_close_set.add(child_string)

                                if child.is_completed():
                                    # If the state is complete, return immediately without adding it to the queue
                                    return current_weight + res[0], size , path + [move], flag + [res[1]], node
                            # Add the child state to the queue with the accumulated weight
                            queue.append((child, path + [move], current_weight + res[0], flag + [res[1]]))

            return 0, size , [], flag, node
        elif self.search_alg == "UCS":
            heap_states = [(0, self.start.to_string(), self.start, [], 0, [])] # heap holds the same things above, first element is priority level
            StateSpace.open_close_set.add(self.start.to_string())
            node = 1
            switches = utils.get_positions(self.start.matrix)
            size = sys.getsizeof(self.start)
            while heap_states:
                cost, child_string, current_state, path, current_weight, flag = heapq.heappop(heap_states)
                print(cost)
                if current_state.is_completed():
                    return current_weight, size / (1024 * 1024), path, flag, node
                for move in self.moves:
                    child = copy.deepcopy(current_state)
                    res = child.get_child(move[0], move[1])
                    cost = utils.cost_g(switches, child.box, child.weights)
                    node += 1

                    if res is not None:
                        child_weight = res[0]  # Weight of the child state
                        child_string = child.to_string()

                        # Only proceed if the state has not been visited
                        if child_string not in StateSpace.open_close_set:
                            StateSpace.open_close_set.add(child_string)

                            if child.is_completed():
                                # If the state is complete, return immediately without adding it to the queue
                                return current_weight + res[0], size / (1024 * 1024), path + [move], flag + [res[1]], node

                            # Add the child state to the heap with the accumulated weight
                            heapq.heappush(heap_states, (cost, child.to_string(), child, path + [move], current_weight + res[0], flag + [res[1]]))
            return 0, size , [], flag, node
