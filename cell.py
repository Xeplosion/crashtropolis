# Foster Cavender
# CS 1400 - MWF - 8:30

import pygame


class Cell:
    def __init__(self, pos, size, images):
        # positional values
        self.pos = pos
        self.size = size

        self.images = images
        self.enter = False
        
        self.line = None
        self.line_rect = None
        self.line_rect_center = None
        self.head = None
        self.head_rect = None

        # change later
        self.direction = 0
        self.last_dir = self.direction

    def find_line(self, lid, change):
        if change:
            # make the corner images
            if self.last_dir == 180:
                if self.direction == 90:
                    return pygame.transform.rotate(self.images[lid][1], 0)
                return pygame.transform.rotate(self.images[lid][1], 270)
            elif self.last_dir == 0:
                if self.direction == 90:
                    return pygame.transform.rotate(self.images[lid][1], 90)
                return pygame.transform.rotate(self.images[lid][1], 180)
            elif self.last_dir == 90:
                if self.direction == 180:
                    return pygame.transform.rotate(self.images[lid][1], 180)
                return pygame.transform.rotate(self.images[lid][1], 270)
            else:
                if self.direction == 0:
                    return pygame.transform.rotate(self.images[lid][1], 0)
                return pygame.transform.rotate(self.images[lid][1], 90)

        # return line image
        return pygame.transform.rotate(self.images[lid][2], self.direction)  # make line image

    def get_head(self, hid):
        return pygame.transform.rotate(self.images[hid][0], self.direction + 180)  # create the player head image

    def update_cell(self, direction, last_dir, pid, change):
        # check for collision
        if self.line is not None:
            return True

        # player movement values
        self.direction = direction
        self.last_dir = last_dir
        self.enter = True  # the player is currently in this cell

        # create line image
        self.line = self.find_line(pid, change)
        self.line_rect = self.line.get_rect()
        self.line_rect.center = (self.pos[0]*self.size + self.size // 2, self.pos[1]*self.size + self.size // 2)

        # create head image
        self.head = self.get_head(pid)
        self.head_rect = self.head.get_rect()
        self.head_rect.center = self.line_rect.center

        return False  # game is not over

    def draw(self, screen):
        # we haven't entered this cell yet
        if self.line is None:
            return

        # currently in this cell draw head
        if self.enter:
            screen.blit(self.head, self.head_rect)
            self.enter = False
            return

        # not in the cell but entered draw line
        screen.blit(self.line, self.line_rect)

    def reset(self):
        self.enter = False
        self.line = None
        self.line_rect = None
        self.head = None
        self.head_rect = None
        self.direction = 0
        self.last_dir = self.direction



