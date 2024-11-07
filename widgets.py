from events import *
from pygame_widgets.button import Button
def sidebar_widgets(window):
    def create_click_handler(event_type, algo_name):
        def handler():
            event = pygame.event.Event(event_type)
            pygame.event.post(event)
        return handler
    
    astar_button = Button(
		window, 1055, 100, 130, 40, text='A*', radius=5,
		font=pygame.font.SysFont('Verdana', 14, bold=True),
		onClick= create_click_handler(SOLVE_ASTAR_EVENT, 'A*'),
		borderColor='black', borderThickness=2,
	)
    bfs_button = Button(
		window, 1055, 200, 130, 40, text='BFS', radius=5,
		font=pygame.font.SysFont('Verdana', 14, bold=True),
		onClick=create_click_handler(SOLVE_BFS_EVENT, 'BFS'),
		borderColor='black', borderThickness=2,
	)
    dfs_button = Button(
		window, 1055, 300, 130, 40, text='DFS', radius=5,
		font=pygame.font.SysFont('Verdana', 14, bold=True),
		onClick=create_click_handler(SOLVE_DFS_EVENT, 'DFS'),
		borderColor='black', borderThickness=2,
	)
    ucs_button = Button(
		window, 1055, 400, 130, 40, text='UCS', radius=5,
		font=pygame.font.SysFont('Verdana', 14, bold=True),
		onClick=create_click_handler(SOLVE_UCS_EVENT, 'UCS'),
		borderColor='black', borderThickness=2,
	)
    
    return [bfs_button, dfs_button, ucs_button, astar_button]