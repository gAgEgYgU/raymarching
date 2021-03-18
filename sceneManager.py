
import numpy as np
import pygame
import math

class SceneManager :
	def __init__(self) :
		self.max_dist = 20
	
	def dPlane(self, p:np.ndarray, h:float, i:float) -> np.ndarray : 
		return np.array([i, p[1] - h])
	
	def dSphere(self, p:np.ndarray, r:float, i:float) -> np.ndarray :
		return np.array([i, self.length(p) - r])

	def minVec2(self, a:np.ndarray, b:np.ndarray) -> np.ndarray :
		if a[1] < b[1] :
			return a
		else :
			return b

	def scene(self, p:np.ndarray) -> np.ndarray :
		dp = self.dPlane(p, -0.5, 0.0)
		ds = self.dSphere(p - np.array([0,-0.5,2]), 0.5, 1.0)
		ds2 = self.dSphere(p - np.array([0.5, -0.5, 1.5]), 0.5, 2.0)
		return self.minVec2(dp, self.minVec2(ds, ds2))

	def march(self, rO:np.ndarray, rD:np.ndarray) -> np.ndarray :
		cP = rO
		d = 0.0
		s = np.array([0.0, 0.0])
		for i in range(50) :
			cP = rO + rD * d
			s = self.scene(cP)
			d += s[1]

			if s[1] < 0.001 :  # Object toucher
				break

			if d > self.max_dist :  # Décor (trop loin)
				return np.array([100, self.max_dist+10])
		
		s[1] = d
		return s
	
	def normal(self, p:np.ndarray) -> np.ndarray :
		dP = self.scene(p)[1]
		off = 0.001
		dX = self.scene(p+np.array([off, 0, 0]))[1] - dP
		dY = self.scene(p+np.array([0, off, 0]))[1] - dP
		dZ = self.scene(p+np.array([0, 0, off]))[1] - dP
		return self.normalize(np.array([dX, dY, dZ]))
	
	def lighting(self, p:np.ndarray, n:np.ndarray) -> float :
		lP = np.array([3, 2, -0.5])
		lD = lP - p
		lN = self.normalize(lD)

		if self.march(p + n*0.01, lN)[1] < self.length(lD) :
			return 0

		return max(0, np.dot(n, lN))
	
	def material(self, i:float) -> np.ndarray :
		
		col = np.array([0,0,0])

		if i < 0.5 :
			col = np.array([1, 2, 2])
		elif i < 1.5 :
			col = np.array([1, 0.2, 0.3])
		elif i < 2.5 :
			col = np.array([0.3, 0.2, 5])
		
		return col * np.array([0.2, 0.2, 0.2])

	def getColor(self, fragCoord:np.ndarray, screenResolution:np.ndarray, mouseRPso:np.ndarray) -> np.ndarray :
		fragColor = None

		uv = np.array([ (fragCoord[0] - (screenResolution[0] * 0.5)) / screenResolution[1], 
						(fragCoord[1] - (screenResolution[1] * 0.5)) / screenResolution[1] ])
		
		mouse = np.array([ mouseRPso[0] / screenResolution[0], 
						mouseRPso[1] / screenResolution[1] ])
		mouse[1] = 1 - mouse[1]

		rO = np.array([0,mouse[1]*0.2,0])
		rD = np.array([uv[0], uv[1], 1]) - rO
		rD = self.normalize(rD)

		s = self.march(rO, rD)
		d = s[1]
		sCol = np.array([0.5, 0.8, 1])   # sky color
		col = self.mix(sCol, np.array([0.08, 0.3, 1]) , pow(uv[1]+0.5, 2.5))  # applique la sky color

		if d < self.max_dist :
			col = self.material(s[0])   # overide with material color
			p = rO + rD*d
			nor = self.normal(p)
			l = self.lighting(p, nor)

			a = np.array([5, 0, 10]) * 0.03  # global ambient

			aS = (nor[1] * sCol) * 0.2  # sky ambient
			
			col = col * (a + l + aS)


		col = pow(col, np.array([0.4545, 0.4545, 0.4545]))
		fragColor = col
		fragColor = fragColor*255
		"""
		if self.length(uv) < 0.2 :
			fragColor = np.array([1,1,1])
		"""

		return fragColor
	
	def length(self, vecteur) :
		return np.linalg.norm(vecteur)
	
	def normalize(self, vecteur) :
		return (vecteur / (self.length(vecteur) + 1e-16))
	
	def mix(self, x, y, a) :
		return x * (1-a) + y*a
