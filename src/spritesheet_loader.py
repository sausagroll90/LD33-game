import pygame

def load_spritesheet(spritesheet, rectsize, width, height):
	spritelist = []
	for row in range(height):
		for square in range(width):
			sprite = pygame.Surface((rectsize, rectsize))
			loadrect = pygame.Rect(square * rectsize, row * rectsize, rectsize, rectsize)
			sprite.blit(spritesheet, (0, 0), loadrect)
			spritelist.append(sprite)
	return spritelist