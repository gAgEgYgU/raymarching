
import pygame
import random
from sceneManager import SceneManager
import numpy as np

class GameManager :
	def __init__(self) :
		pygame.init()
		self.SCREEN_WIDTH = 700
		self.SCREEN_HEIGHT = 394
		self.screen_size = (self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
		self.screen = pygame.display.set_mode(self.screen_size)
		self.game_launched = True
		self.sceneManager = SceneManager()
		self.clock = None
		self.scale = 13
		pygame.display.set_caption('RayMarching')
	
	def event(self) :
		for event in pygame.event.get():
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						self.game_launched = False
						exit(0)
				elif event.type == pygame.QUIT:
					self.game_launched = False
					exit(0)

	def start(self, loop = True, resolution = 0) :
		if resolution != 0 :
			self.scale = resolution
		
		self.clock = pygame.time.Clock()
		pygame.display.flip()
		first = True

		while self.game_launched:
			#self.clock.tick(60)

			self.event()
			
			if loop==True or first==True :
				mouseRPso = pygame.mouse.get_pos()
				for x in range(int(self.SCREEN_WIDTH / self.scale)+1):
					self.event()
					for y in range(int(self.SCREEN_HEIGHT / self.scale)+1):
						surf = pygame.Surface((self.scale, self.scale))
						color = self.sceneManager.getColor(np.array([x*self.scale, y*self.scale]), np.array([self.SCREEN_WIDTH, self.SCREEN_HEIGHT]), mouseRPso)
						if color[0] < 0 :
							color[0] = 0
						elif color[0] > 255 :
							color[0] = 255
						if color[1] < 0 :
							color[1] = 0
						elif color[1] > 255 :
							color[1] = 255
						if color[2] < 0 :
							color[2] = 0
						elif color[2] > 255 :
							color[2] = 255
						surf.fill(( int(color[0]), int(color[1]), int(color[2]) ))
						self.screen.blit(surf, (x*self.scale, self.SCREEN_HEIGHT - (y+1)*self.scale))
						current = y+x*(int(self.SCREEN_HEIGHT / self.scale)+1)
						total = (int(self.SCREEN_WIDTH / self.scale)+1) * (int(self.SCREEN_HEIGHT / self.scale)+1)
						short_float = float("{:.2f}".format(current*100/total))
						print(str(short_float)+"%")

				print("Update Screen !!!")
				pygame.display.flip()
				
			first = False
