import tkinter as tk
import random

COLS, ROWS, MINES, CELL = 10, 10, 12, 32

class Game:
    def __init__(self, root):
        self.c = tk.Canvas(root, width=COLS*CELL, height=ROWS*CELL,
                           bg='#bdbdbd', highlightthickness=0)
        self.c.pack()
        self.c.bind('<Button-1>', self.left)
        self.c.bind('<Button-3>', self.right)
        self.reset()

    def reset(self):
        self.open = [[False]*COLS for _ in range(ROWS)]
        self.flag = [[False]*COLS for _ in range(ROWS)]
        self.mine = [[False]*COLS for _ in range(ROWS)]
        self.placed = False
        self.over = False
        self.draw()

    def neighbors(self, x, y):
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                if dx or dy:
                    nx, ny = x+dx, y+dy
                    if 0 <= nx < COLS and 0 <= ny < ROWS:
                        yield nx, ny

    def count(self, x, y):
        return sum(self.mine[ny][nx] for nx, ny in self.neighbors(x, y))

    def place(self, sx, sy):
        safe = {(sx+dx, sy+dy) for dx in (-1,0,1) for dy in (-1,0,1)}
        cells = [(x, y) for y in range(ROWS) for x in range(COLS)
                 if (x, y) not in safe]
        for x, y in random.sample(cells, MINES):
            self.mine[y][x] = True

    def reveal(self, x, y):
        if self.open[y][x] or self.flag[y][x]:
            return
        self.open[y][x] = True
        if self.mine[y][x]:
            self.over = True
            return
        if self.count(x, y) == 0:
            for nx, ny in self.neighbors(x, y):
                self.reveal(nx, ny)

    def left(self, e):
        if self.over: return
        x, y = e.x // CELL, e.y // CELL
        if not self.placed:
            self.place(x, y)
            self.placed = True
        self.reveal(x, y)
        if all(self.open[y][x] or self.mine[y][x]
               for y in range(ROWS) for x in range(COLS)):
            self.over = True
        self.draw()

    def right(self, e):
        if self.over: return
        x, y = e.x // CELL, e.y // CELL
        if not self.open[y][x]:
            self.flag[y][x] = not self.flag[y][x]
        self.draw()

    def draw(self):
        c = self.c
        c.delete('all')
        colors = ['', '#1976d2', '#388e3c', '#d32f2f', '#7b1fa2',
                  '#ff8f00', '#0097a7', '#424242', '#000']
        for y in range(ROWS):
            for x in range(COLS):
                x0, y0, x1, y1 = x*CELL, y*CELL, x*CELL+CELL, y*CELL+CELL
                if self.open[y][x]:
                    c.create_rectangle(x0, y0, x1, y1,
                                       fill='#d6d6d6', outline='#9e9e9e')
                    if self.mine[y][x]:
                        c.create_oval(x0+8, y0+8, x1-8, y1-8, fill='#000')
                    else:
                        n = self.count(x, y)
                        if n:
                            c.create_text(x0+CELL/2, y0+CELL/2, text=str(n),
                                          font=('Helvetica', 14, 'bold'),
                                          fill=colors[n])
                else:
                    c.create_rectangle(x0, y0, x1, y1,
                                       fill='#bdbdbd', outline='#9e9e9e')
                    c.create_line(x0, y0, x1, y0, fill='#f0f0f0')
                    c.create_line(x0, y0, x0, y1, fill='#f0f0f0')
                    c.create_line(x1, y1, x1, y0, fill='#7a7a7a')
                    c.create_line(x1, y1, x0, y1, fill='#7a7a7a')
                    if self.flag[y][x]:
                        c.create_text(x0+CELL/2, y0+CELL/2, text='🚩',
                                      font=('Helvetica', 16))
                    if self.over and self.mine[y][x]:
                        c.create_oval(x0+8, y0+8, x1-8, y1-8, fill='#d32f2f')
        if self.over:
            c.create_text(COLS*CELL/2, ROWS*CELL/2, text='GAME OVER',
                          font=('Helvetica', 26, 'bold'), fill='#fff')

root = tk.Tk()
root.title('Minesweeper')
Game(root)
root.mainloop()
