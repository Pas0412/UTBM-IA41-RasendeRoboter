import pygame
from pygame.locals import *
import time
import random


"""
colors:
j: yellow
r: red
v: green
b: blue

shapes:
o: circle
i: star
c: square
t: triangle

directions:
n: north
e: east
s: south
w: west

other:
0: empty (middle square)
Y: Joker ?
"""

ROTATE_MATRIX = [
    56, 48, 40, 32, 24, 16,  8,  0, 
    57, 49, 41, 33, 25, 17,  9,  1, 
    58, 50, 42, 34, 26, 18, 10,  2, 
    59, 51, 43, 35, 27, 19, 11,  3, 
    60, 52, 44, 36, 28, 20, 12,  4, 
    61, 53, 45, 37, 29, 21, 13,  5, 
    62, 54, 46, 38, 30, 22, 14,  6, 
    63, 55, 47, 39, 31, 23, 15,  7,
]

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




class Window:
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
					"Robot vert" : [(1064, 100), (140, 40), (34,177,76), "bot_v",],
					"Robot rouge": [(1244, 100), (140, 40), (237,28,36), "bot_r"],
					"Robot bleu" : [(1064, 200), (140, 40), (0,162,232), "bot_b"],
					"Robot jaune": [(1244, 200), (140, 40), (255,242,0), "bot_j"],
					"Reset":       [(1154, 400), (140, 40), (195,195,195), "but_R"],
					"Submit":      [(1154, 600), (140, 40), (195,195,195), "but_S"]
				}

		self.forms = "icotYicot"
		self.colors = "bvjr"
		self.directions = "swen"

		self.south = False
		self.north = False
		self.west = False
		self.east = False
		self.direc = None

		self.bot_v = False
		self.bot_b = True
		self.bot_j = False
		self.bot_r = False

		self.fenetre = None

		self.angle = 0

		# case de 64*64 pixels

		self.board_a = (self.tab_a, self.tab_c)
		self.board_b = (self.tab_b, self.tab_d)
		self.board = []
		self.bot_position = []

		self.movements = 0




	def rotate_tabs(self, tab, times):

		new_board = []
		line = []
		for _ in range(times):
			if _ != 0:
				tab = new_board
				new_board = []
			for index in ROTATE_MATRIX:
				line.append(tab[index // 8][index % 8])
				if len(line) == 8:
					new_board.append(line)
					line = []

		new_board = self.rotate_tiles(times, new_board)

		return new_board 




	def rotate_tiles(self, rotation, new_board):
		reference = "neswnesw"
		new_tile = ""
		final_tile = ""
		for Y, line in enumerate(new_board):
			for X, tile in enumerate(line):
				if tile != "swen":
					for letter in tile:
						if letter in reference:
							new_tile += reference[reference.find(letter) + rotation]
						else:
							new_tile += letter
					
					# tiles will have the letter inverted after a rotation, thus not found because the images don't have the right name
					entered = True
					key = ""
					for key in CORRESP:
						condition = new_tile[0] in self.forms or new_tile == "0"
						if condition:
							final_tile = new_tile
						else:
							if new_tile in CORRESP[key]:
								entered = True
								final_tile = key
							elif new_tile not in CORRESP[key] and not entered:
								final_tile = new_tile
					entered = False

					new_board[Y][X] = final_tile
					new_tile = ""
		return new_board

	a=[['se', 'swe', 'sw', 'se', 'swe', 'swe', 'swe', 'swe', 'swe', 'sw', 'se', 'swe', 'swe', 'swe', 'swe', 'sw'], 
	['nse', 'swen', 'swen', 'swen', 'nse', 'nse', 'swen', 'swen', 'swen', 'swen', 'swen', 'sw', 'sw', 'swen', 'swen', 'nw'], 
	['nse', 'swen', 'nse', 'nse', 'swen', 'swe', 'swen', 'swen', 'swen', 'swen', 'swen', 'swen', 'swen', 'swen', 'swen', 'sw'], 
	['ne', 'swen', 'swe', 'swen', 'swen', 'swen', 'swen', 'swen', 'sw', 'sw', 'swen', 'swen', 'swen', 'swen', 'swen', 'sw'], 
	['se', 'swen', 'swen', 'se', 'nse', 'swen', 'new', 'swen', 'swen', 'swe', 'new', 'swen', 'swen', 'swen', 'new', 'ns'], 
	['nse', 'new', 'swen', 'swe', 'swen', 'swe', 'swe', 'swen', 'swen', 'swen', 'ns', 'nse', 'swen', 'swen', 'swe', 'swe'], 
	['nse', 'nse', 'nse', 'swen', 'swen', 'swen','swen', 'new', 'new', 'swen', 'swen', 'swen', 'swen', 'swen', 'swen', 'new'], 
	['nse', 'swen', 'swen', 'swen', 'swen', 'swen', 'nse', 'nse', 'new', 'nse', 'swen', 'swen', 'swen', 'swen', 'swen', 'nse'], 
	['nse', 'swen', 'swen', 'swen', 'swen', 'swen', 'nse', 'nse', '', 'nse', 'swen', 'swen', 'swen', 'swen', 'swen', 'nw'], 
	['ne', 'swen', 'swen', 'swen', 'swen', 'swen', 'swen', 'swe', 'swe', 'swen', 'swe', 'swe', 'swen', 'swen', 'swen', 'sw'], 
	['se', 'swen', 'swen', 'se', 'nse', 'new', 'swen', 'swen', 'swen', 'swen', 'swen', 'swe', 'swen', 'swen', 'new', 'new'], 
	['nse', 'swen', 'swen', 'swe', 'swen', 'swe', 'nse', 'swen', 'swen', 'new', 'swen', 'swen', 'swen', 'swen', 'new', 'ns'], 
	['nse', 'nse', 'nse', 'swen', 'new', 'swen', 'swen', 'swen', 'ns', 'ns','swen', 'swen', 'swen', 'swen', 'swen', 'ns'], 
	['nse', 'swen', 'swe', 'swe', 'swe', 'swen', 'swen', 'swen', 'swen', 'swen', 'swen', 'swen', 'swen', 'swen', 'swen', 'ns'], 
	['nse', 'swen', 'swen', 'swen', 'swen', 'swen', 'swen', 'swen', 'swen', 'swen', 'swen', 'swen', 'ns', 'nse', 'swen', 'nse'], 
	['ne', 'new', 'new', 'nw', 'ne', 'new', 'new', 'new', 'new', 'new', 'new', 'new', 'new', 'nw', 'ne', 'nw']]

	tmp=[['sw', 'se', 'swe', 'ew', 'swe', 'swe', 'swe', 'sw'], 
	['swen', 'swen', 'nsw', 'ores', 'swen', 'swen', 'swen', 'nw'], 
	['swen', 'swen', 'swen', 'swen', 'swen', 'swen', 'new', 'sw'], 
	['swen', 'swen', 'swen', 'swen', 'swen', 'swen', 'tvsw', 'ns'],
	['swen', 'cbnw', 'nse', 'swen', 'swen', 'swen', 'swen', 'nsw'], 
	['swen', 'swe', 'swen', 'swen', 'swen', 'swen', 'swen', 'nsw'], 
	['new', 'swen', 'swen', 'nsw', 'ijne', 'swen', 'swen', 'nsw'], 
	['0', 'nse', 'swen', 'swen', 'swe', 'swen', 'swen', 'nsw']]



	def display_board(self, fenetre, angle):

		for Y, line in enumerate(self.board):
			for X, case in enumerate(line):
				try:
					if case[0] in self.forms:
						img = pygame.transform.scale(pygame.image.load(f"img/{case[0:2]}_.png"), (64, 64))
					else:
						img = pygame.transform.scale(pygame.image.load(f"img/{case}.png"), (64, 64))
				except Exception as e:
					"""
					print("erreur")
					print("f"+case+"f")
					print(self.board)
					"""
					print(e)
					quit()
				if angle != 0:
					img = pygame.transform.rotate(img, angle)
					#new_rect = img.get_rect(center = img.get_rect(topleft = topleft).center)
				fenetre.blit(img, (X*64, Y*64))

		# display the target in the middle of the board
		self.display_anything(self.fenetre, (480, 480), (64, 64), f"img/{self.to_reach}.png")




	def fusion_tab(self, rotations):
		order = []
		if rotations == 1:
			order = (self.tab_b, self.tab_a, 
					self.tab_d, self.tab_c)

		elif rotations == 2:
			order = (self.tab_d, self.tab_b, 
					self.tab_c, self.tab_a)

		elif rotations == 3:
			order = (self.tab_c, self.tab_d, 
					self.tab_a, self.tab_b)

		elif rotations == 0:
			order = (self.tab_a, self.tab_c, 
					self.tab_b, self.tab_d)

		tab1 = []
		tab2 = []
		for i in range(8):
			tab1.append(order[0][i] + order[1][i])
			tab2.append(order[2][i] + order[3][i])

		return tab1 + tab2



	def init_board(self):
		rotations = random.randint(0, 3)
		#rotations = 0
		self.angle = rotations * 90 # angle of rotation for when I will blit the picture
		print("Nombre de rotations: ", rotations)

		if rotations != 0:
			self.tab_a = self.rotate_tabs(self.tab_a, rotations)
			self.tab_b = self.rotate_tabs(self.tab_b, rotations)
			self.tab_c = self.rotate_tabs(self.tab_c, rotations)
			self.tab_d = self.rotate_tabs(self.tab_d, rotations)
		self.board = self.fusion_tab(rotations)

		self.to_reach = self.forms[random.randint(0, 8)] + self.colors[random.randint(0, 3)]
		if "Y" in self.to_reach:
			self.to_reach = "Y"




	def record_keys(self):
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
			
			if event.type == pygame.MOUSEBUTTONDOWN:
				self.button_behavior()

		if a:
			self.bot_movement()



	def allowed_movement(self, mvt):
		place = self.board[self.bot_position[1]][self.bot_position[0]] # receives the letters of the case the bot is located on. like 'ives' or 'nsw'
		print(place)
		if mvt in place:
			return True
		else:
			return False



	def next_pos(self, direc):
		X, Y = self.bot_position[0], self.bot_position[1]
		print("Number of moves: ", self.movements)

		if direc == "s":
			for i in range(1, 16 - Y):
				place = self.board[Y + i][X]
				if "s" not in place:
					self.bot_pos_before = self.bot_position
					return [X, Y + i]

		if direc == "n":
			for i in range(1, Y + 1):
				place = self.board[Y - i][X]
				if "n" not in place:
					self.bot_pos_before = self.bot_position
					return [X, Y - i]

		if direc == "e":
			for i in range(1, 16 - X + 1):
				place = self.board[Y][X + i]
				if "e" not in place:
					self.bot_pos_before = self.bot_position
					return [X + i, Y]

		if direc == "w":
			for i in range(1, X + 1):
				place = self.board[Y][X - i]
				if "w" not in place:
					self.bot_pos_before = self.bot_position
					return [X - i, Y]






	def bot_movement(self):
		next_position = self.bot_position
		if self.south:
			self.south = False
			if self.allowed_movement("s"):
				print("PROCHAIN DEPLACEMENT: s")
				self.movements += 1
				next_position = self.next_pos("s")

		elif self.north:
			self.north = False
			if self.allowed_movement("n"):
				print("PROCHAIN DEPLACEMENT: n")
				self.movements += 1
				next_position = self.next_pos("n")

		elif self.east:
			self.east = False
			if self.allowed_movement("e"):
				print("PROCHAIN DEPLACEMENT: e")
				self.movements += 1
				next_position = self.next_pos("e")

		elif self.west:
			self.west = False
			if self.allowed_movement("w"):
				print("PROCHAIN DEPLACEMENT: w")
				self.movements += 1
				next_position = self.next_pos("w")

		self.bot_position = next_position



	def init_robot(self):
		x = random.randint(0, 15)
		y = random.randint(0, 15)
		self.bot_position = [x, y]
		place = self.board[y][x]
		# tests to make sure the robot doesn't spawn on a shape or in the middle
		for i in self.forms:
			if i in place:
				return False
		if "0" in place:
			return False
		return True



	def disp_robot(self, fenetre):
		img = pygame.transform.scale(pygame.image.load(f"img/pion_bleu.jpg"), (46, 48))
		fenetre.blit(img, (self.bot_position[0]*64 + 6, self.bot_position[1]*64 + 6))



	def init_inputs(self, fenetre):
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



	def button_behavior(self):
		x, y = pygame.mouse.get_pos()
		if pygame.mouse.get_pressed()[0]:
			for name in self.to_draw:
				coords = self.to_draw[name][0]
				size = self.to_draw[name][1]
				var = self.to_draw[name][3]
				# when the click is done, check if the click in one of the boxes.
				if (coords[0] <= x <= coords[0] + size[0]) and (coords[1] <= y <= coords[1] + size[1]):
					if "Robot" in name:
						self.set_robot_false()
						locals()[var] = True # sets the bot of the corresponding color of the button clicked to True so it can start moving
					elif name == "Submit":
						# exit the programm or something and check if the player is on the requetes tile
						pass
					elif name == "Reset":
						pass
						self.reset_board() # à coder
					print(f"Bouton {var} pressé.")




	def set_robot_false(self):
		self.bot_v = False
		self.bot_b = False
		self.bot_j = False
		self.bot_r = False



	def display_anything(self, fenetre, coords, scale, image):
		img = pygame.transform.scale(pygame.image.load(image), scale)
		fenetre.blit(img, coords)




	def reset_board(self):
		self.movements = 0
		# stocker les coordonnées initiales des robots pour les remettres à zéro ici.



def main():

	pygame.init()
	largeur = 1424
	hauteur = 1024
	fenetre = pygame.display.set_mode((largeur, hauteur))
	pygame.display.set_caption('Rasende roboter')

	win = Window()
	fenetre.fill((0,0,0))

	win.init_board()
	win.fenetre = fenetre
	result = win.init_robot()
	while not result:
		result = win.init_robot()


	while True:
		win.display_board(fenetre, win.angle)
		win.disp_robot(fenetre)
		win.record_keys()
		win.init_inputs(fenetre)
		pygame.display.update()






if __name__ == '__main__':
	main()

#  / modifier le design des sprites? trait gris ? bords ronds ?
#! / pour thomas: couleur du symbole, le type de symbole, 
#  / permettre a thomas de l'utiliser comme un outil: acces au tableau, a la position de pions...
#! / implémenter les 3 autres robots /!\ les robots ont des hitbox (issou)
#  / mettre des boites de dialogue
#  O générer une cible aléatoire
#  O faire la cible joker
#! / compter les points
#! / bouton revenir a la case départ?
#! / timer qui s'affiche ? en lien avec au-dessus
#! O faire tourner les boards a,b,c,d
#! O Faire tourner les cases en fonction du nombre de rotations !
#! O Arranger les lettres des cases pour charger les images
#! / rotation pas bonne pour certaines tiles (presque toutes en fait)
