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

DICO = {"b":"bleu", "v":"vert", "r":"rouge", "j":"jaune"}

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
ROTATE_MATRIX_16 = [
		240, 224, 208, 192, 176, 160, 144, 128, 112, 96, 80, 64, 48, 32, 16, 0, 
		241, 225, 209, 193, 177, 161, 145, 129, 113, 97, 81, 65, 49, 33, 17, 1, 
		242, 226, 210, 194, 178, 162, 146, 130, 114, 98, 82, 66, 50, 34, 18, 2, 
		243, 227, 211, 195, 179, 163, 147, 131, 115, 99, 83, 67, 51, 35, 19, 3, 
		244, 228, 212, 196, 180, 164, 148, 132, 116, 100, 84, 68, 52, 36, 20, 4, 
		245, 229, 213, 197, 181, 165, 149, 133, 117, 101, 85, 69, 53, 37, 21, 5, 
		246, 230, 214, 198, 182, 166, 150, 134, 118, 102, 86, 70, 54, 38, 22, 6, 
		247, 231, 215, 199, 183, 167, 151, 135, 119, 103, 87, 71, 55, 39, 23, 7, 
		248, 232, 216, 200, 184, 168, 152, 136, 120, 104, 88, 72, 56, 40, 24, 8, 
		249, 233, 217, 201, 185, 169, 153, 137, 121, 105, 89, 73, 57, 41, 25, 9, 
		250, 234, 218, 202, 186, 170, 154, 138, 122, 106, 90, 74, 58, 42, 26, 10, 
		251, 235, 219, 203, 187, 171, 155, 139, 123, 107, 91, 75, 59, 43, 27, 11, 
		252, 236, 220, 204, 188, 172, 156, 140, 124, 108, 92, 76, 60, 44, 28, 12, 
		253, 237, 221, 205, 189, 173, 157, 141, 125, 109, 93, 77, 61, 45, 29, 13, 
		254, 238, 222, 206, 190, 174, 158, 142, 126, 110, 94, 78, 62, 46, 30, 14, 
		255, 239, 223, 207, 191, 175, 159, 143, 127, 111, 95, 79, 63, 47, 31, 15
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

SHAPES = "icotYicot"
COLORS = "bvrj"



class Board:
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




	def display_board(self, fenetre):
		fenetre.fill((0,0,0))
		for Y, line in enumerate(self.board):
			for X, case in enumerate(line):
				try:
					if case[0] in SHAPES:
						img = pygame.transform.scale(pygame.image.load(f"img/{case[0:2]}_.png"), (64, 64))
					else:
						img = pygame.transform.scale(pygame.image.load(f"img/{case}.png"), (64, 64))
				except Exception as e:
					"""
					print("|"+case+"|")
					print(self.board)
					"""
					print(e)
					quit()
				fenetre.blit(img, (X*64, Y*64))

		for i in self.to_draw:
			if self.to_draw[i][4]:
				coord = self.to_draw[i][0]
				size = self.to_draw[i][1]
				pygame.draw.rect(fenetre, (255,255,255), (coord[0] - 5, coord[1] - 5, size[0] + 10, size[1] + 10), width=2)
		# display the target in the middle of the board
		display_anything(fenetre, (480, 480), (64, 64), f"img/{self.target}.png")




	def fusion_tab(self):
		tab1 = []
		tab2 = []
		for i in range(8):
			tab1.append(self.tab_a[i] + self.tab_c[i])
			tab2.append(self.tab_b[i] + self.tab_d[i])
		return tab1 + tab2



	def init_board(self, fenetre):

		self.board = self.fusion_tab()
		self.target = SHAPES[random.randint(0, 8)] + COLORS[random.randint(0, 3)]
		if "Y" in self.target:
			self.target = "Y"
		





	def record_keys(self, robots):
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
				self.buttons(robots)

		if a:
			if self.moving_bot != None:
				self.bot_movement(robots)
			else:
				print("Veuilles sélectionner un robot.")



	def allowed_movement(self, mvt):
		place = self.board[self.moving_bot.position[1]][self.moving_bot.position[0]] # receives the letters of the case the bot is located on. like 'ives' or 'nsw'
		if mvt in place:
			return True
		else:
			return False
			



	def next_pos(self, direc, robots):
		X, Y = self.moving_bot.position[0], self.moving_bot.position[1]
		returning = []
		robots_positions = []
		for robot in robots:
			robots_positions.append(robot.position)


		if direc == "s":
			for i in range(1, 16 - Y):
				place = self.board[Y + i][X]
				if "s" not in place or [X, Y + i] in [robot_pos for robot_pos in robots_positions]:
					returning = [X, Y + i]
				if [X, Y + i] in [robot_pos for robot_pos in robots_positions]:
					returning = [X, Y + i - 1]
				if returning != []:
					return returning

		if direc == "n":
			for i in range(1, Y + 1):
				place = self.board[Y - i][X]
				if "n" not in place or [X, Y - i] in [robot_pos for robot_pos in robots_positions]:
					returning = [X, Y - i]
				if [X, Y - i] in [robot_pos for robot_pos in robots_positions]:
					returning = [X, Y - i + 1]
				if returning != []:
					return returning

		if direc == "e":
			for i in range(1, 16 - X + 1):
				place = self.board[Y][X + i]
				if "e" not in place:
					returning = [X + i, Y]
				if [X + i, Y] in [robot_pos for robot_pos in robots_positions]:
					returning = [X + i - 1, Y]
				if returning != []:
					return returning

		if direc == "w":
			for i in range(1, X + 1):
				place = self.board[Y][X - i]
				if "w" not in place or [X - i, Y] in [robot_pos for robot_pos in robots_positions]:
					returning = [X - i, Y]
				if [X - i, Y] in [robot_pos for robot_pos in robots_positions]:
					returning = [X - i + 1, Y]
				if returning != []:
					return returning






	def bot_movement(self, robots):
		next_position = self.moving_bot.position
		if self.south:
			self.south = False
			if self.allowed_movement("s"):
				self.movements += 1
				next_position = self.next_pos("s", robots)

		elif self.north:
			self.north = False
			if self.allowed_movement("n"):
				self.movements += 1
				next_position = self.next_pos("n", robots)

		elif self.east:
			self.east = False
			if self.allowed_movement("e"):
				self.movements += 1
				next_position = self.next_pos("e", robots)

		elif self.west:
			self.west = False
			if self.allowed_movement("w"):
				self.movements += 1
				next_position = self.next_pos("w", robots)

		self.moving_bot.position = next_position
		print(f"\rNumber of moves: {self.movements}\t\t\t\t\t\t\t\t\t\t", end='')





	def display_inputs(self, fenetre):
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
		x, y = pygame.mouse.get_pos()
		if pygame.mouse.get_pressed()[0]:
			for name in self.to_draw:
				coords = self.to_draw[name][0]
				size = self.to_draw[name][1]
				var = self.to_draw[name][3]

				# when the click is done, check if the click is in one of the boxes.
				if (coords[0] <= x <= coords[0] + size[0]) and (coords[1] <= y <= coords[1] + size[1]):
					if "Robot" in name:
						self.set_draw_rect_false()
						color = var.split('_')[1]
						for robot in robots:
							if robot.color == color:
								robot.moving = True
								self.moving_bot = robot
						self.to_draw[name][4] = True
					elif name == "Submit":
						self.submit(robots)
					elif name == "Reset":
						pass
						self.reset_board(robots)

	def set_draw_rect_false(self):
		for i in self.to_draw:
			self.to_draw[i][4] = False


	def reset_board(self, robots):
		for robot in robots:
			robot.position = robot.spawn_position
		self.movements = 0


	def submit(self, robots):
		end = False
		for robot in robots:
			X = robot.position[0]
			Y = robot.position[1]
			if self.target in self.board[Y][X] and robot.color in self.target:
				print(f"\nLe robot {DICO[robot.color]} à atteint la cible en {self.movements} coup(s).")
				end = True
		if not end:
			print("\nVous n'avez pas atteint la cible.")
		else:
			pygame.quit()
			quit()




class Robot(object):
	#this will be one robot
	def __init__(self, color, position):
		self.position = position
		self.spawn_position = position
		self.color = color
		self.moving = False



def set_robot_false(robots):
	for robot in robots:
		robot.moving = False




def init_robots(game):
	robots = []
	for i in range(4):
		x = random.randint(0, 15)
		y = random.randint(0, 15)
		bot_tile = game.board[y][x]
		bot = [x, y]
		while ((bot in robots) or ("0" in bot_tile) or (bot_tile[0] in SHAPES)):
			x = random.randint(0, 15)
			y = random.randint(0, 15)
			bot_tile = game.board[y][x]
			bot = [x, y]
		robots.append([x, y])

	return robots


def disp_robots(robots, fenetre):
	for robot in robots:
		img = pygame.transform.scale(pygame.image.load("img/pion_{}.jpg".format(DICO[robot.color])), (46, 48))
		fenetre.blit(img, (robot.position[0]*64 + 9, robot.position[1]*64 + 8))




def display_anything(fenetre, coords, scale, image):
	img = pygame.transform.scale(pygame.image.load(image), scale)
	fenetre.blit(img, coords)





def main():

	pygame.init()
	largeur = 1424
	hauteur = 1024
	fenetre = pygame.display.set_mode((largeur, hauteur))
	pygame.display.set_caption('Rasende roboter')

	fenetre.fill((0,0,0))

	board = Board()
	board.init_board(fenetre)

	robots = []
	for index, bot_pos in enumerate(init_robots(board)):
		robots.append(Robot(COLORS[index], bot_pos)) # creates a list of the 4 robots with different positions and colors.

	
	while True:
		set_robot_false(robots)
		board.display_board(fenetre)
		board.display_inputs(fenetre)
		disp_robots(robots, fenetre)
		board.record_keys(robots)
		pygame.display.update()
		


if __name__ == '__main__':
	main()

#  / modifier le design des sprites? trait gris ? bords ronds ?
#! / pour thomas: couleur du symbole, le type de symbole, 
#  / permettre a thomas de l'utiliser comme un outil: acces au tableau, a la position de pions...
#! O implémenter les 3 autres robots /!\ les robots ont des hitbox (issou)
#  O générer une cible aléatoire
#  O faire la cible joker
#! O compter les points
#! O bouton revenir a la case départ?
#! / timer qui s'affiche ? en lien avec au-dessus
#! / faire tourner les boards a,b,c,d
#! / Faire tourner les cases en fonction du nombre de rotations !
#! O Arranger les lettres des cases pour charger les images