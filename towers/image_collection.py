import pygame
import os


class ImageCollection:
    def __init__(self, path, count, start_index, image_size, directory, identifier):
        self.images = []
        self.number_of_imgs = count
        self.load_index = start_index
        self.path = path
        self.image_size = image_size
        self.directory = directory
        self.identifier = identifier
        self.loaded = False

    def download_images(self):
        try:
            for index in range(self.number_of_imgs):
                add_str = str(index)
                if index < 10:
                    add_str = "0" + add_str

                path = os.path.join("../game_assets/" + self.path + str(self.directory), str(self.directory) + self.identifier + add_str + ".png")
                self.images.append(pygame.transform.scale(pygame.image.load(path), (self.image_size, self.image_size)))
            self.loaded = True
        except pygame.error:
            self.loaded = False
            raise pygame.error("Images does not loaded!")

    def download_tower(self):
        try:
            for x in range(self.load_index, self.load_index + self.number_of_imgs):
                add_str = str(x)
                self.images.append(
                    pygame.transform.scale(pygame.image.load(self.path + self.identifier + add_str + ".png"), (self.image_size, self.image_size)))
            self.loaded = True
        except pygame.error:
            self.loaded = False
            raise pygame.error("Images does not loaded!")

    def __contains__(self, item):
        return item in self.images

    def __iter__(self):
        return iter(self.images)

    def __len__(self):
        return self.number_of_imgs()

    def __del__(self):
        del self.images


class ControlImageCollection:
    def __init__(self, path, width, height):
        self.image = None
        self.path = path
        self.width = width
        self.height = height

    def download_image(self):
        try:
            self.image = pygame.transform.scale(pygame.image.load(self.path), (self.width, self.height))
            return self.image
        except pygame.error:
            raise pygame.error("Images does not loaded!")
