import time
import pygame
import subprocess
import json

from IA import *
from window import *



def init_display(fps):
	pygame.init()
	largeur = 1424
	hauteur = 1024
	fenetre = pygame.display.set_mode((largeur, hauteur))
	pygame.display.set_caption('Rasende roboter')
	clock = pygame.time.Clock()
	clock.tick(fps)
	fenetre.fill((0,0,0))

	return fenetre

def check_ia_finish(p2):
	status = p2.poll()
	if status == 0:
		return True
	else:
		return False


def sequence_mouvement(mvt):
	etat_precedent = mvt[0]
	for etat in mvt:
		for i, bot in enumerate(etat[0:4]):
			if bot not in etat_precedent:
				print(str(etat_precedent[i]) + " -> " + str(bot))
		etat_precedent = etat



def recup_coup_ia():
	with open("reponse", 'r') as f:
		fichier = f.read().replace("'", '"').replace("(", "[").replace(")", "]")
	ret = json.loads(fichier)

	return ret

def choix_difficulte():
	difficulte = "a"
	while difficulte not in "fmd":
		difficulte = str(input("Veuillez choisir la difficultée: Facile, Moyen ou Difficile ? (f/m/d) -> "))
	if difficulte == "f":
		temps_dispo = 180
	elif difficulte == "m":
		temps_dispo = 120
	elif difficulte == "d":
		temps_dispo = 30

	print(f"Vous avez {temps_dispo} secondes pour trouver une solution. Bonne chance !")
	return temps_dispo


def main():

	temps_dispo = choix_difficulte()

	fenetre = init_display(60)
	board = Board()
	board.init_board(fenetre)
	robots = []
	movements = []
	bots = []

	for index, bot_pos in enumerate(init_robots(board)):
		robots.append(Robot(COLORS[index], bot_pos)) # creates a list of the 4 robots with different positions and colors.
	for i in robots:
		a=i.position
		a.append(i.color)
		bots.append(tuple(a))

	#print("BFS({}, {})".format(bots, tuple(board.target_pos)))

	with open("transfert", "w") as f:
		f.write(str(bots) + "||" + str(tuple(board.target_pos)))
	time_init = time.time()
	p2 = subprocess.Popen('py ".\\IA.py"', shell=True)
	ia_fini = False
	premier_qui_trouve = False
	joueur_fini = False
	temps_ecoule = False
	time_ia = 10**8
	pas_fini = True

	while pas_fini:

		set_robot_false(robots)
		board.display_board(fenetre)
		board.display_inputs(fenetre)
		disp_robots(robots, fenetre)
		pygame.display.update()
		ret = board.record_keys(robots)
		if ret == "end":
			joueur_fini = True


		if check_ia_finish(p2) and not ia_fini:
			time_ia = time.time()
			ia_fini = True
			print("L'ia a terminé et a trouvé en {} secondes !".format(int(time_ia - time_init)))
			movements = recup_coup_ia()

		if ((time.time() - time_init) >= temps_dispo) and not temps_ecoule:
			temps_ecoule = True
			print("\nLe temps est écoulé ! Le premier qui trouve une solution gagne la partie !")

		if (ret == "end" or joueur_fini) and (temps_ecoule or ia_fini):

			if movements != []:
				sequence_mouvement(movements)

			temps_joueur = time.time()
			ia_moves = len(movements)-1
			if ia_moves == -1:
				print("L'IA n'a pas trouvé de réponse à temps.")
				alors = "non"
				p2.terminate()
			else:
				alors = str(input(f"L'IA a trouvé une réponse en {ia_moves} coups.\nMontrer les coups joués ? (oui/non) -> "))

			fin_de_jeu(ia_fini, movements, board, temps_joueur, time_ia, temps_ecoule)
			
			if alors == "oui":
				pygame.display.quit()
				fenetre = init_display(60)
				board.init_board(fenetre)
				board.display_board(fenetre)
				pygame.display.update()
				show_ia_moves(movements, robots, fenetre, board)

			
			#time.sleep(len(movements)*3/5)
			pas_fini = False





def fin_de_jeu(ia_fini, movements, board, temps_joueur, temps_ia, premier_qui_trouve):
	if premier_qui_trouve:
		if ia_fini:
			print("Vous n'avez pas trouver avant l'IA, vous avez donc perdu.")
		else:
			print("Vous avez trouvé avant l'IA, vous avez donc gagné.")
	else:
		if board.movements > len(movements)-1 and len(movements) != 0:
			mot = "perdu."
		elif board.movements == len(movements)-1 and temps_ia < temps_joueur:
			mot = "perdu."
		elif board.movements < len(movements)-1:
			mot = "gagné !"
		elif board.movements == len(movements)-1 and temps_ia >= temps_joueur:
			mot = "gagné !"

		print("Vous avez trouvé en {} coups et vous avez {}".format(board.movements, mot))



def show_ia_moves(movements, robots, fenetre, board):
	# Cette fonction intervient pour montrer les mouvements des robots de l'IA,
	# après qu'elle ai fini de trouver la réponse.
	for i in range(len(movements)):
		for y in range(len(movements[i])):
			if type(movements[i][y]) == tuple:
				movements[i][y] = list(movements[i][y])

	for index, etat in enumerate(movements):
		for i, mov in enumerate(etat[0:4]):
			movements[index][i][2] = COLORS[i]
	movements = [movements[0]] + movements + [movements[-1]]
	#movements = movements + movements + movements

	for state in movements:
		for new_bot_pos in state[0:4]:
			for bot in robots:
				if bot.color == new_bot_pos[2]:
					bot.position = [new_bot_pos[0], new_bot_pos[1]]
					board.display_board(fenetre)
					disp_robots(robots, fenetre)
					pygame.display.update()
					pygame.time.wait(150)




if __name__ == '__main__':
	main()

