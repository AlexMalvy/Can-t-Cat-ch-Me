import pygame
import os

class image_loader:
    def load(path, scale):
        if len(path) == 1:
            img = pygame.image.load(path[0])
        else:
            path.reverse()
            true_path = path[0]
            for every in path[1:]:
                true_path = os.path.join(every, true_path)
            img = pygame.image.load(true_path)


        img = pygame.transform.scale(img, (img.get_width() * scale, img.get_height() * scale))

        return img