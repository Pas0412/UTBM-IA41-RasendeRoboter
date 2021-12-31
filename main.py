import time
import pygame

from IA import *
from window import *

[(0,0,"b"),(7,2,"r"),(15,4,"j"),(1,9,"v")]
(0,12,'b')

def init_display():
	pygame.init()
	largeur = 1424
	hauteur = 1024
	fenetre = pygame.display.set_mode((largeur, hauteur))
	pygame.display.set_caption('Rasende roboter')

	fenetre.fill((0,0,0))

	return fenetre



def main():

	fenetre = init_display()

	board = Board()
	board.init_board(fenetre)

	robots = []
	
	for index, bot_pos in enumerate(init_robots(board)):
		robots.append(Robot(COLORS[index], bot_pos)) # creates a list of the 4 robots with different positions and colors.

	movements = []
	bots = []
	for i in robots:
		a=i.position
		a.append(i.color)
		bots.append(tuple(a))


	while True:
		set_robot_false(robots)
		board.display_board(fenetre)
		board.display_inputs(fenetre)
		disp_robots(robots, fenetre)
		ret = board.record_keys(robots)
		pygame.display.update()

		if ret == "end":
			pygame.display.quit()
			movements = BFS(bots , tuple(board.target_pos), board.board)
			
			alors = str(input("L'IA à trouvée une réponse en {} coups.\nMontrer les coups joués ? (oui/non) -> ".format(len(movements)-1)))
			if alors == "oui":
				fenetre = init_display()
				board.display_board(fenetre)
				board.display_inputs(fenetre)
				show_ia_moves(movements, robots, fenetre, board)
			print("Vous avez trouvé en {} coups, vous avez donc {}".format(board.movements, "perdu." if board.movements > len(movements)-1 else "gagné !"))
			pygame.quit()
			quit()




def show_ia_moves(movements, robots, fenetre, board):
	for state in movements:
		for new_bot_pos in state[0:4]:
			for bot in robots:
				if bot.color == new_bot_pos[2]:
					bot.position = [new_bot_pos[0], new_bot_pos[1]]
					board.display_board(fenetre)
					disp_robots(robots, fenetre)
					pygame.display.update()
					time.sleep(0.2)




if __name__ == '__main__':
	main()

