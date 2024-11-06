from events import *
from pygame_widgets.button import Button
def sidebar_widgets(window):
    astar_button = Button(
		window, 1055, 200, 130, 40, text='A*', radius=5,
		font=pygame.font.SysFont('Verdana', 14, bold=True),
		onClick=lambda: pygame.event.post(pygame.event.Event(SOLVE_ASTAR_EVENT)),
		borderColor='black', borderThickness=2,
	)
    bfs_button = Button(
		window, 1055, 300, 130, 40, text='BFS', radius=5,
		font=pygame.font.SysFont('Verdana', 14, bold=True),
		onClick=lambda: pygame.event.post(pygame.event.Event(SOLVE_BFS_EVENT)),
		borderColor='black', borderThickness=2,
	)
    dfs_button = Button(
		window, 1055, 400, 130, 40, text='DFS', radius=5,
		font=pygame.font.SysFont('Verdana', 14, bold=True),
		onClick=lambda: pygame.event.post(pygame.event.Event(SOLVE_DFS_EVENT)),
		borderColor='black', borderThickness=2,
	)
    ucs_button = Button(
		window, 1055, 500, 130, 40, text='UCS', radius=5,
		font=pygame.font.SysFont('Verdana', 14, bold=True),
		onClick=lambda: pygame.event.post(pygame.event.Event(SOLVE_UCS_EVENT)),
		borderColor='black', borderThickness=2,
	)
    return [bfs_button, dfs_button, ucs_button, astar_button]