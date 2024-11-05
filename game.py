
import sys
import queue

from statespace import StateSpace

class game:

    def is_valid_value(self,char):
        if ( char == ' ' or #floor
            char == '#' or #wall
            char == '@' or #worker on floor
            char == '.' or #dock
            char == '*' or #box on dock
            char == '$' or #box
            char == '+' ): #worker on dock
            return True
        else:
            return False

    def __init__(self,level):
        self.queue = queue.LifoQueue()
        #if level < 1 or level > 50:
        if level < 1:
            print("ERROR: Level "+str(level)+" is out of range")
            sys.exit(1)
        else:
            formatted_level = f"{level:02}"
            self.start_state = StateSpace(f"input-{formatted_level}.txt")
            
            

    def load_size(self):
        x = 0
        y = len(self.start_state.get_matrix())
        for row in self.start_state.get_matrix():
            if len(row) > x:
                x = len(row)
        return (x * 32, y * 32)
    
    def load_move_from_file(self, output_file):
        # Initialize the dictionary to store results
        result = {'algorithm': [], 'path': [], 'instruction':[]}

        # Open and read the file
        with open(output_file, 'r') as file:
            # Initialize variables to keep track of current algorithm and path
            current_algorithm = None
            current_path = None

            # Read through each line in the file
            for line in file:
                # Check if the line indicates a new algorithm
                if line.startswith('BFS') or line.startswith('DFS') or line.startswith('A*') or line.startswith('UCS'):
                    # Extract algorithm name and store it
                    current_algorithm = line.split()[0]
                    result['algorithm'].append(current_algorithm)

                # Check if the line represents a path (assumes paths do not start with 'Steps')
                elif not line.startswith('Steps') and current_algorithm:
                    # Extract and store the path for the current algorithm

                    current_path = line.strip()
                    instruction = []
                    for command in current_path:
                        if command.lower() == 'l':
                            instruction.append((0, -1))
                        elif command.lower() == 'r':
                            instruction.append((0, 1))
                        elif command.lower() == 'u':
                            instruction.append((-1, 0))
                        elif command.lower() == 'd':
                            instruction.append((1, 0))
                    
                    result['path'].append(current_path)
                    result['instruction'].append(instruction)

        # Print the dictionary
        return result
#     def unmove(self): 
#         if not self.queue.empty():
#             movement = self.queue.get()
#             if movement[2]:
#                 current = self.worker()
#                 self.move(movement[0] * -1,movement[1] * -1, False)
#                 self.move_box(current[0]+movement[0],current[1]+movement[1],movement[0] * -1,movement[1] * -1)
#             else:
#                 self.move(movement[0] * -1,movement[1] * -1, False)