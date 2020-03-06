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
            self.images = None

    def __contains__(self, item):
        return item in self.images

    def __iter__(self):
        return iter(self.images)

    def __len__(self):
        return self.number_of_imgs()

    def __del__(self):
        del self.images
