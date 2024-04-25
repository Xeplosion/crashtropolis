# Foster Cavender
# CS 1400 - MWF - 8:30

import math
import pygame

SPEED = 10

class Player():
    def __init__(self, id, direction, start):
        self.id = id # id

        # for move
        self.start = start
        self.direction = direction
        self.last_dir = self.direction

        # for restart
        self.pos = self.start
        self.starting_direction = direction

    def move(self):
        # player coordinates
        self.pos[0] += math.sin(math.radians(self.direction)) * SPEED
        self.pos[1] += math.cos(math.radians(self.direction)) * SPEED

    def direction_change(self, inputs):
        prev_direction = self.direction
        if self.direction == 90 or self.direction == 270:
            # checking for vertical inputs
            if inputs[self.id][0]:
                self.direction = 180
            elif inputs[self.id][1]:
                self.direction = 0
        else:
            # check for horizontal inputs
            if inputs[self.id][2]:
                self.direction = 270
            elif inputs[self.id][3]:
                self.direction = 90

        if not prev_direction == self.direction:
            self.last_dir = prev_direction
            return True
        return False

    def offscreen(self, screen_width, screen_height):
        # check for offscreen
        if self.pos[0] < 0 or self.pos[0] > screen_width\
         or self.pos[1] < 0 or self.pos[1] > screen_height - 10:
            return True
        return False

    def reset(self):
        # reset to original values
        self.pos = self.start
        print(self.pos, self.start)
        self.direction = self.starting_direction
        self.last_dir = self.direction
