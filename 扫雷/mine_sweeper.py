"""
命令行扫雷
题目：
实现扫雷游戏。
该游戏在一个10*10的棋盘中，随机分布着15个雷。
棋盘由以下符号表示：
‘#’ 表示该格子未揭开
‘ ‘ 表示该格子附近8个格子没有雷
‘1-8’ 数字表示该格子附近有多少个雷
‘*’ 表示该格子是地雷
玩家可以按 WASD 进行上下左右移动光标，按空格揭开格子。当揭开的格子是地雷时，打印’you lose’；当揭开格子附近有地雷时，显示附近有多少个雷；
当揭开格子附近无地雷时，显示为空格并上下左右四周扩散；当揭开格子后剩余格子全是地雷时，打印 ‘you win’。

示例图：https://media.giphy.com/media/xUA7b5A0LyBXULNdtu/giphy.gif

实现扫雷程序完成 生成棋盘、响应用户操作、更新界面 的一个完整程序。

"""

import random


class Cell(object):
    def __init__(self, x, y, value):
        self.x = x
        self.y = y
        self.value = value
        self.side_bombs = 0
        self.clicked = False
        self.is_showed = False

    def is_bomb(self):
        return self.value == 1

    def __repr__(self):
        if not self.clicked:
            if self.is_showed:
                return str(self.side_bombs)
            else:
                return '#'
        elif self.is_bomb():
            return '*'
        elif self.side_bombs > 0:
            return str(self.side_bombs)
        else:
            return ' '

    def side_cells(self, w=10, h=10):
        ms = []
        if self.x > 0:
            ms.append((self.x - 1, self.y))
        if self.x < w - 1:
            ms.append((self.x + 1, self.y))
        if self.y > 0:
            ms.append((self.x, self.y - 1))
        if self.y < h - 1:
            ms.append((self.x, self.y + 1))
        return ms

    def count_side_bombs(self, game):
        bs = self.side_cells(game.w, game.h)
        count = 0
        for ix, iy in bs:
            cm = game.bombs[iy][ix]
            if cm == 1:
                count += 1
        return count

    def click(self, game):
        if not self.clicked:
            self.clicked = True
            game.clicked_cell += 1
            if self.is_bomb():
                return True
            else:
                if self.side_bombs == 0:
                    ms = self.side_cells(game.w, game.h)
                    for ix, iy in ms:
                        m = game.mines[iy][ix]
                        if m.side_bombs == 0:
                            m.click(game)
                        else:
                            m.is_showed = True

                return False


class Game(object):
    def __init__(self, count=15, w=10, h=10):
        self.w = w
        self.h = h
        self.count = count
        self.total = w * h
        self.bombs = self.bomb_map(count, w, h)
        self.mines = self.mine_map()
        self.clicked_cell = 0
        self.step = 0
        self.is_finished = False
        self.result = 0
        self.message = ''

    @staticmethod
    def bomb_map(count=15, w=10, h=10):
        ds = [[0 for i in range(w)] for y in range(h)]
        ms = random.sample(range(w * h), count)
        for m in ms:
            ix = m % w
            iy = m // h
            ds[iy][ix] = 1
        return ds

    def mine_map(self):
        ms = []
        for iy, row in enumerate(self.bombs):
            line = []
            for ix, value in enumerate(row):
                m = Cell(ix, iy, value)
                if value == 0:
                    m.side_bombs = m.count_side_bombs(self)
                line.append(m)
            ms.append(line)
        return ms

    def _click(self, x, y):
        self.step += 1
        c = self.mines[y][x]
        m = c.click(self)
        if m:
            self.is_finished = True
            self.message = 'you lose ({},{})'.format(x, y)
        elif self.clicked_cell >= self.total - self.count:
            self.is_finished = True
            self.result = 1
            self.message = 'you win'
        else:
            self.message = 'step {} at (横{},竖{}) '.format(self.step, x, y)

    def click(self, x, y):
        if not self.is_finished:
            self._click(x, y)
        else:
            print('游戏已经结束')
        self.display()

    def display(self):
        print(' {}  \n'.format(self.message))
        for row in self.mines:
            print(row)
        print('\n')

    def debug(self):
        print('------bombs-----\n')
        for row in self.bombs:
            print(row)
        print('----- debug ----\n')
        for row in self.mines:
            m = list(zip((c.value, c.side_bombs) for c in row))
            print(m)
        print('---------------\n')


def mine_game(debug=True):
    g = Game()
    if debug:
        g.debug()
    g.display()
    while not g.is_finished:
        m = input('以0开始计算，横x，竖y. \n(以逗号隔开) 请输入 x,y >> \t')
        x, y = m.split(',')
        g.click(int(x), int(y))
    print('游戏结束')


if __name__ == '__main__':
    mine_game()
