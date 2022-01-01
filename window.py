import pygame
from pygame.locals import *
import time
import random
print("Rasende Roboter")


DICO = {"b":"bleu", "v":"vert", "r":"rouge", "j":"jaune"}

CORRESP = {	"wnes": ["wnes", "swne", "eswn", "nesw"],
			"nse": ["esn", "sen", "nse", "sne"],
			"swe": ["esw", "wes", "swe"],
			"new": ["wne", "ewn", "new", "ews"],
			"nsw": ["wns", "nws", "nsw", "snw"],
			"se": ["es", "se"],
			"sw": ["ws", "sw"],
			"ns": ["sn", "ns"],
			"ne": ["en", "ne"],
			"ew": ["ew", "we"],
			"nw": ["wn", "nw"],
			"0": "0"
}

SHAPES = "icotYicot"
COLORS = "brjv"


class Board:
	# Objet représentant le plateau.
	def __init__(self):
		self.tab_a = [["se","sw","se","swe","ew","swe","swe","swe"],
					["nse","swen","swen","swen","ovsw","nse","swen","swen"],
					["nse","swen","swen","swen","swen","swen","swen","swen"],
					["ns","trne","swen","swen","swen","swen","swen","swen"],
					["nse","swe","swen","swen","swen","new","swen","swen"],
					["ne","swen","swen","swen","nsw","cjes","swen","swen"],
					["se","swen","swen","ibnw","nse","swen","swen","new"],
					["nse","swen","swen","swe","swen","swen","nsw","0"]]

		self.tab_b = [["nse","swen","swen","swen","swen","swen","nsw","0"],
					["nse","swen","swen","swen","nsw","cvne","swen","swe"],
					["nse","obnw","nse","swen","swen","swe","swen","swen"],
					["nse","swe","swen","swen","new","swen","swen","swen"],
					["ne","swen","new","swen","irsw","nse","swen","swen"],
					["se","swen","YYsw","nse","swen","swen","new","swen"],
					["nse","swen","swen","swen","swen","nsw","tjes","swen"],
					["ne","new","new","nw","ne","new","new","new"]]

		self.tab_c = [["sw","se","swe","ew","swe","swe","swe","sw"],
					["swen","swen","nsw","ores","swen","swen","swen","nw"],
					["swen","swen","swen","swen","swen","swen","new","sw"],
					["swen","swen","swen","swen","swen","swen","tvsw","ns"],
					["swen","cbnw","nse","swen","swen","swen","swen","nsw"],
					["swen","swe","swen","swen","swen","swen","swen","nsw"],
					["new","swen","swen","nsw","ijne","swen","swen","nsw"],
					["0","nse","swen","swen","swe","swen","swen","nsw"]]

		self.tab_d = [["0","nse","swen","swen","swen","swen","swen","nsw"],
					["swe","swen","swen","new","swen","swen","swen","nsw"],
					["swen","swen","nsw","ives","swen","swen","swen","nsw"],
					["swen","swen","new","swen","nsw","crne","swen","nw"],
					["swen","swen","tbsw","nse","swen","swe","swen","sw"],
					["swen","swen","swen","swen","ojnw","nse","swen","nsw"],
					["swen","swen","swen","swen","swe","swen","swen","nsw"],
					["new","nw","ne","new","new","new","new","nw"]]

		self.to_draw = {
					"Robot vert" : [(1064, 100), (140, 40), (34,177,76), "bot_v", False],
					"Robot rouge": [(1244, 100), (140, 40), (237,28,36), "bot_r", False],
					"Robot bleu" : [(1064, 200), (140, 40), (0,162,232), "bot_b", False],
					"Robot jaune": [(1244, 200), (140, 40), (255,242,0), "bot_j", False],
					"Reset":       [(1154, 400), (140, 40), (195,195,195), "but_R", None],
					"Submit":      [(1154, 600), (140, 40), (195,195,195), "but_S", None]
				}


		self.south = False
		self.north = False
		self.west = False
		self.east = False

		self.board = []

		self.movements = 0

		self.moving_bot = None

		self.target_pos = [int(), int(), str()]



	def display_board(self, fenetre):
		# Fonction qui affiche le plateau de jeu sur la fenêtre et le rectangle autour du bouton séléctionné

		fenetre.fill((0,0,0))

		# Affichage du plateau
		for Y, line in enumerate(self.board):
			for X, case in enumerate(line):
				if case[0] in SHAPES:
					img = pygame.transform.scale(pygame.image.load(f"img/{case[0:2]}_.png"), (64, 64))
				else:
					img = pygame.transform.scale(pygame.image.load(f"img/{case}.png"), (64, 64))
				fenetre.blit(img, (X*64, Y*64))

		# Affichage du rectangle autour du bouton de robot séléctionné.
		for i in self.to_draw:
			if self.to_draw[i][4]:
				coord = self.to_draw[i][0]
				size = self.to_draw[i][1]
				pygame.draw.rect(fenetre, (255,255,255), (coord[0] - 5, coord[1] - 5, size[0] + 10, size[1] + 10), width=2)
		
		# Affichage de la cible à atteindre au milieu du plateau
		display_anything(fenetre, (480, 480), (64, 64), f"img/{self.target}.png")




	def fusion_tab(self):
		# Fonction qui assemble les 4 tableau de 8x8 cases en un grand plateau de jeu de 16x16

		tab1 = []
		tab2 = []
		for i in range(8):
			tab1.append(self.tab_a[i] + self.tab_c[i])
			tab2.append(self.tab_b[i] + self.tab_d[i])
		return tab1 + tab2



	def init_board(self, fenetre):
		# Initialisation du plateau de jeu et choix aléatoire de la cible

		self.board = self.fusion_tab()
		self.target = SHAPES[random.randint(0, 8)] + COLORS[random.randint(0, 3)]
		if "Y" in self.target:
			self.target = "YY"

		for Y, line in enumerate(self.board):
			for X, tile in enumerate(line):
				if self.target in tile:
					self.target_pos = [X, Y, self.target[1]]

		
		


	def record_keys(self, robots):
		# Fonction qui enregistre les touches de clavier préssées et les clics de souris

		a = False
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_s:
					self.south = True
					a = True
				elif event.key == pygame.K_z:
					self.north = True
					a = True
				elif event.key == pygame.K_d:
					self.east = True
					a = True
				elif event.key == pygame.K_q:
					self.west = True
					a = True
			
			# Si un clic gauche est fait, on exécute la fonction qui gère les clic
			if event.type == pygame.MOUSEBUTTONDOWN:
				ret = self.buttons(robots)
				if ret == "end":
					return "end"

		# Si une touche de mouvement est préssée, on exécute la fonction de mouvement de robot.
		if a:
			if self.moving_bot != None:
				self.bot_movement(robots)
			else:
				print("Veuilles sélectionner un robot.")



	def allowed_movement(self, mvt):
		# Vérifie si, sur la case courante, le mouvement mvt (s, n, e ou w) est présent

		place = self.board[self.moving_bot.position[1]][self.moving_bot.position[0]] # receives the letters of the case the bot is located on. like 'ives' or 'nsw'
		if mvt in place:
			return True
		else:
			return False
			



	def next_pos(self, direc, robots):
		# Fonction qui va chercher la prochaine position du robot en mouvement 
		# en fonction de l'argument direc qui indique la direction du robot

		X, Y = self.moving_bot.position[0], self.moving_bot.position[1]
		returning = []
		robots_positions = []
		for robot in robots:
			robots_positions.append(robot.position[0:2])

		if direc == "s":
			# La direction SUD indique que l'on va jouer sur l'axe Y. 
			# Puisque qu'on descend, on ne va vérifier que les cases en dessous de la position du robot
			for i in range(1, 16 - Y):
				place = self.board[Y + i][X]
				# Si 's' n'est pas dans la case courrante, on ne peut pas continuer
				if "s" not in place:
					returning = [X, Y + i]
				# Si la case courrante est une case occupée par un robot, on ne peut pas continuer
				if [X, Y + i] in robots_positions:
					returning = [X, Y + i - 1]
				# En retour, on obtient les coordonnées de la case de destination du robot
				if returning != []:
					return returning

		if direc == "n":
			for i in range(1, Y + 1):
				place = self.board[Y - i][X]
				if "n" not in place:
					returning = [X, Y - i]
				if [X, Y - i] in robots_positions:
					returning = [X, Y - i + 1]
				if returning != []:
					return returning

		if direc == "e":
			for i in range(1, 16 - X + 1):
				place = self.board[Y][X + i]
				if "e" not in place:
					returning = [X + i, Y]
				if [X + i, Y] in robots_positions:
					returning = [X + i - 1, Y]
				if returning != []:
					return returning

		if direc == "w":
			for i in range(1, X + 1):
				place = self.board[Y][X - i]
				if "w" not in place:
					returning = [X - i, Y]
				if [X - i, Y] in robots_positions:
					returning = [X - i + 1, Y]
				if returning != []:
					return returning






	def bot_movement(self, robots):
		# Fonction qui gére les mouvements des robots, en vérifiant qu'ils ne traversent pas de mur, ou d'autres robots.
		next_position = self.moving_bot.position
		ret = next_position
		if self.south: # Si la direction est sud, on vérifie que le mouvement est possible et on va chercher la prochaine position du robot en mouvement.
			self.south = False
			if self.allowed_movement("s"):
				ret = self.next_pos("s", robots)

		elif self.north:
			self.north = False
			if self.allowed_movement("n"):
				ret = self.next_pos("n", robots)

		elif self.east:
			self.east = False
			if self.allowed_movement("e"):
				ret = self.next_pos("e", robots)

		elif self.west:
			self.west = False
			if self.allowed_movement("w"):
				ret = self.next_pos("w", robots)

		if ret != next_position:
			self.movements += 1

		self.moving_bot.position = ret
		print(f"\rNumber of moves: {self.movements}\t\t\t\t\t\t\t\t\t\t", end='')





	def display_inputs(self, fenetre):
		# Fonction qui affiche les boutons
		font = pygame.font.SysFont("Arial", 24)
		for text in self.to_draw:
			coords = self.to_draw[text][0]
			size = self.to_draw[text][1]
			color = self.to_draw[text][2]
			
			text = font.render(text, 1, pygame.Color("White"))
			text_size = text.get_size()
			surface = pygame.Surface(size)
			surface.fill(color)
			surface.blit(text, ((size[0] - text_size[0]) / 2, (size[1] - text_size[1]) / 2))
			fenetre.blit(surface, coords)



	def buttons(self, robots):
		"""
		Fonction gérant les boutons et leurs différentes actions.
		Il y a trois types de boutons: les robots, reset et submit
		"""
		x, y = pygame.mouse.get_pos() # coordonnées du clic
		if pygame.mouse.get_pressed()[0]:
			for name in self.to_draw:
				coords = self.to_draw[name][0]
				size = self.to_draw[name][1]
				var = self.to_draw[name][3]

				# on vérifie si le clic sur l'un des boutons avec le jeu de coordonnées défini dans __init__
				if (coords[0] <= x <= coords[0] + size[0]) and (coords[1] <= y <= coords[1] + size[1]):

					# Si le clic est sur un bouton d'activation d'un robot:
					if "Robot" in name:
						for i in self.to_draw:
							self.to_draw[i][4] = False
						color = var.split('_')[1]
						# on défini que le robot de la couleur corespondante au bouton cliqué peut bouger
						for robot in robots:
							if robot.color == color:
								robot.moving = True
								self.moving_bot = robot
						self.to_draw[name][4] = True

					elif name == "Submit":
						if self.submit(robots):
							return "end"

					elif name == "Reset":
						self.reset_board(robots)





	def reset_board(self, robots):
		# Fonction permettant de remettre les robots à leur position d'origine, en remttatn le compteur de mouvements a 0
		for robot in robots:
			robot.position = robot.spawn_position
		self.movements = 0


	def submit(self, robots):
		# Fonction qui intervient lorsque l'on appuie sur le bouton submit
		# Elle vérifie si le robot de la bonne couleur a atteint la bonne cible.
		end = False
		for robot in robots:
			X = robot.position[0]
			Y = robot.position[1]
			if self.target in self.board[Y][X] and (robot.color in self.target or "Y" in self.target):
				print(f"\nLe robot {DICO[robot.color]} à atteint la cible en {self.movements} coup(s).")
				end = True
		if not end:
			print("\nVous n'avez pas atteint la cible.")
			return False
		else:
			for key in self.to_draw:
				if self.to_draw[key][4] == True:
					self.to_draw[key][4] = False
			return True


class Robot(object):
	# Obejt représentant 1 robot.
	# Le Robot est caractérisé par sa couleur, sa position de départ et actuelle
	# et s'il est en mouvement ou non
	def __init__(self, color, position):
		self.position = position
		self.spawn_position = position
		self.color = color
		self.moving = False



def set_robot_false(robots):
	# Indique que tout les robots ne bougent pas
	for robot in robots:
		robot.moving = False




def init_robots(game):
	# Fonction qui initialise la position des robots. 
	# Leur couleurs respectives sont données dans le fichier main.py
	robots = []
	for i in range(4):
		x = random.randint(0, 15)
		y = random.randint(0, 15)
		bot_tile = game.board[y][x]
		bot = [x, y]

		# Vérifie qu'un robot ne tombe pas sur une cible ou sur un autre robot
		while ((bot in robots) or ("0" in bot_tile) or (bot_tile[0] in SHAPES)):
			x = random.randint(0, 15)
			y = random.randint(0, 15)
			bot_tile = game.board[y][x]
			bot = [x, y]
		robots.append([x, y])

	return robots



def disp_robots(robots, fenetre):
	# Affiche uniquement les robots sur le plateau
	for robot in robots:
		img = pygame.transform.scale(pygame.image.load("img/pion_{}.jpg".format(DICO[robot.color])), (46, 48))
		fenetre.blit(img, (robot.position[0]*64 + 9, robot.position[1]*64 + 8))




def display_anything(fenetre, coords, scale, image):
	# Permet d'afficher ce que l'on veut, ou l'on veut sur l'écran.
	img = pygame.transform.scale(pygame.image.load(image), scale)
	fenetre.blit(img, coords)




