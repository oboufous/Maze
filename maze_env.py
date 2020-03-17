"""
Reinforcement learning maze example.
Red rectangle:          explorer.
Black rectangles:       hells       [reward = -1].
Yellow bin circle:      paradise    [reward = +1].
All other states:       ground      [reward = 0].
This script is the environment part of this example. The RL is in RL_brain.py.
View more on my tutorial page: https://morvanzhou.github.io/tutorials/
"""

import numpy as np
import random
import time
import sys
if sys.version_info.major == 2:
    import Tkinter as tk
else:
    import tkinter as tk

UNIT = 40   # pixels
MAZE_H = 8  # grid height
MAZE_W = 8  # grid width
origin = np.array([20, 20]) # create origin (center) of the squares
number_of_hells = 6
number_of_paradises = 3

# Generate number_of_hells cells randomly
hell_positions = [(random.randrange(0, 7), random.randrange(0, 7)) for i in range(number_of_hells)]
hell_coord = []
paradises_positions = [(random.randrange(0, 7), random.randrange(0, 7)) for i in range(number_of_paradises)]
paradises_coord = []
paradises = []

while (0,0) in hell_positions:
    hell_positions = [(random.randrange(0, 7), random.randrange(0, 7)) for i in range(number_of_hells)]
for e in hell_positions:
    while (0,0) in paradises_positions or e in paradises_positions:
        paradises_positions = [(random.randrange(0, 7), random.randrange(0, 7)) for i in range(number_of_paradises)]

class Maze(tk.Tk, object):
    def __init__(self):
        super(Maze, self).__init__()
        self.action_space = ['u', 'd', 'l', 'r']
        self.n_actions = len(self.action_space)
        self.title('Garden')
        self.geometry('{0}x{1}'.format(MAZE_H * UNIT, MAZE_H * UNIT))
        self._build_maze()

    def _build_maze(self):
        self.canvas = tk.Canvas(self, bg='white',
                           height=MAZE_H * UNIT,
                           width=MAZE_W * UNIT)
        # Create grids
        for c in range(0, MAZE_W * UNIT, UNIT):
            x0, y0, x1, y1 = c, 0, c, MAZE_H * UNIT
            self.canvas.create_line(x0, y0, x1, y1)
        for r in range(0, MAZE_H * UNIT, UNIT):
            x0, y0, x1, y1 = 0, r, MAZE_W * UNIT, r
            self.canvas.create_line(x0, y0, x1, y1)

        # Create hell
        for i in range(number_of_hells):
            hell_center = origin + np.array([UNIT * hell_positions[i][0], UNIT*hell_positions[i][1]])
            self.hell = self.canvas.create_rectangle(
                hell_center[0] - 15, hell_center[1] - 15,
                hell_center[0] + 15, hell_center[1] + 15,
                fill='black')
            hell_coord.append(self.canvas.coords(self.hell))

        # Create ovals
        for i in range(number_of_paradises):
            oval_center = origin + np.array([UNIT * paradises_positions[i][0], UNIT*paradises_positions[i][1]])
            self.i = self.canvas.create_oval(
                oval_center[0] - 15, oval_center[1] - 15,
                oval_center[0] + 15, oval_center[1] + 15,
                fill='green')
            paradises.append(self.canvas.coords(self.i))
            paradises_coord.append(self.canvas.coords(self.i))

        # Create red rect
        self.rect = self.canvas.create_rectangle(
            origin[0] - 15, origin[1] - 15,
            origin[0] + 15, origin[1] + 15,
            fill='blue')

        # Pack all
        self.canvas.pack()

    def reset(self):
        self.update()
        time.sleep(0.5)
        self.canvas.delete(self.rect)
        origin = np.array([20, 20])
        self.rect = self.canvas.create_rectangle(
            origin[0] - 15, origin[1] - 15,
            origin[0] + 15, origin[1] + 15,
            fill='blue')
        # Return observation
        return self.canvas.coords(self.rect)

    def step(self, action):
        visited = []
        s = self.canvas.coords(self.rect)
        base_action = np.array([0, 0])
        if action == 0:   # up
            if s[1] > UNIT:
                base_action[1] -= UNIT
        elif action == 1:   # down
            if s[1] < (MAZE_H - 1) * UNIT:
                base_action[1] += UNIT
        elif action == 2:   # right
            if s[0] < (MAZE_W - 1) * UNIT:
                base_action[0] += UNIT
        elif action == 3:   # left
            if s[0] > UNIT:
                base_action[0] -= UNIT

        self.canvas.move(self.rect, base_action[0], base_action[1])  # move agent

        s_ = self.canvas.coords(self.rect)  # next state
        visited.append(s_)

        # Reward function
        if s_ in paradises_coord:
            if len(paradises_coord) != 0:
                if s_ in visited:
                    reward = -5
                else:
                    reward = 5
                print('- - - - - - - - -> paradises_positions', paradises_positions)
                oval_position = paradises_coord.index(s_)
                print('- - - - - - - - -> oval_position', oval_position)
                paradise_obj = paradises[oval_position] # oval position in list
                self.canvas.delete(paradise_obj) # oval object
                del paradises_coord[oval_position]
                del paradises_positions[oval_position]
                del paradises[oval_position]
                done = False
            else:
                reward = 10
                done = True
                s_ = 'terminal'
        elif s_ in hell_coord:
            if s_ in visited:
                reward = -5
            else:
                reward = -1
            done = True
            s_ = 'terminal'
        else:
            if s_ in visited:
                reward = -5
            else:
                reward = 0
            done = False

        return s_, reward, done

    def render(self):
        time.sleep(0.1)
        self.update()

def update():
    for t in range(10):
        s = env.reset()
        while True:
            env.render()
            a = 1
            s, r, done = env.step(a)
            if done:
                break

if __name__ == '__main__':
    env = Maze()
    env.after(100, update)
    env.mainloop()