#Universidad del Valle de Guatemala
#CARLOS CHEW - 17507 .

import struct 

		def __init__(self, width, height):
		
			self.width = abs(int(width))
			self.height = abs(int(height))
			self.framebuffer = []
			self.zbuffer = []
			self.clear()
			
		def color(self, r=0, g=0, b=0):
		
			if (r > 255 or g > 255 or b > 255 or r < 0 or g < 0 or b <0):
				r = 0
				g = 0
				b = 0
			return bytes([b, g, r])
			
		def clear(self, r=0, b=0, g=0):
			
			self.framebuffer = [
				[
					self.color(r, b, g)
						for x in range(self.width)
				]
				for y in range(self.height)
			]

			self.zbuffer = [ [-float('inf') for x in range(self.width)] for y in range(self.height)]
			
		def point(self, x, y, color):
		
			if(x < self.width and y < self.height):
				self.framebuffer[x][y] = color
				
		def write(self, filename, zbuffer=False):
		
			BLACK = self.color(0,0,0)
			import os
			os.makedirs(os.path.dirname(filename), exist_ok=True)
			file = open(filename, "bw")
			pWidth =  self.__padding(4, self.width)
			pHeight = self.__padding(4, self.height)

			
			file.write(self.__char("B"))
			file.write(self.__char("M")) 
			file.write(self.___dword(14 + 40 + pWidth * pHeight)) 
			file.write(self.___dword(0))
			file.write(self.___dword(14 + 40))

			
			file.write(self.___dword(40))
			file.write(self.___dword(self.width))
			file.write(self.___dword(self.height))
			file.write(self.___word(1))
			file.write(self.___word(24))
			file.write(self.___dword(0))
			file.write(self.___dword(pWidth * pHeight))
			file.write(self.___dword(0))
			file.write(self.___dword(0))
			file.write(self.___dword(0))
			file.write(self.___dword(0))

			
			for x in range(pWidth):
				for y in range(self.height):
					if(x < self.width and y < self.height):
						if zbuffer:
							if self.zbuffer[y][x] == -float("inf"):
								file.write(BLACK)
							else:
								z = abs(int(self.zbuffer[y][x]*255))
								file.write(self.color(z,z,z))
						else:
							file.write(self.framebuffer[y][x])
					else:
						file.write(self.__char("c"))

			file.close()		
			
		def __padding(self, base, c):
			
			if(c %  base == 0):
				return c
			else:
				while (c % base):
					c += 1
				return c	
				
		def __char(self, c):
			return struct.pack("c", c.encode("ascii"))		
			
		def ___word(self, c):			
			return struct.pack("h", c)	
			
		def ___dword(self, c):			
			return struct.pack("l", c)	
			
		def getZbufferValue(self, x, y):		
			if x < self.width and y < self.height:
				return self.zbuffer[x][y]
			else:
				return -float("inf")	
				
		def setZbufferValue(self, x, y, z):			
			if x < self.width and y < self.height:
				self.zbuffer[x][y] = z
				return 1
			else:
				return 0		