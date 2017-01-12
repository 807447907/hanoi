#!/usr/bin/python
# -*- coding: UTF-8 -*-
import Tkinter as Tk
from tkMessageBox import *


class Hanoi(Tk.Frame):
    description = "    在世界中心贝拿勒斯（在印度北部）的圣庙里，一块黄铜板上插着三根宝石针。印度教的主神梵天在创造世界的时候，在其中一根针上从下到上地穿好了由大到小的64片金片，这就是所谓的汉诺塔。" + "不论白天黑夜，总有一个僧侣在按照下面的法则移动这些金片：一次只移动一片，不管在哪根针上，小片必须在大片上面。" + "僧侣们预言，当所有的金片都从梵天穿好的那根针上移到另外一根针上时，世界就将在一声霹雳中消灭，而梵塔、庙宇和众生也都将同归于尽。"

    canvas_width = 200#画布宽度
    canvas_height = canvas_width
    maxLevel = 64#最大层数

    canvas_hanoi = []
    hanoi = [[], [], []]
    button_move = []

    def __init__(self, master=None):
        Tk.Frame.__init__(self, master)
        self.grid()
        self._create_widgets()
        self.focus = None#标记当前选中状态

    def _create_widgets(self):
        self.label = Tk.Label(self, wraplength=self.canvas_width * 3, text=self.description, justify="left")
        self.label.grid(row=0, column=0, columnspan=3)

        for i in range(0, 3):#绘制画布
            canvas = Tk.Canvas(self, width=self.canvas_width, height=self.canvas_height, background="#E4E4E4")
            canvas.grid(row=1, column=i)
            self.canvas_hanoi.append(canvas)

        button = Tk.Button(self, text="From", state="disabled", command=lambda: self._move_handler(0))#绘制按钮，并绑定事件
        button.grid(row=2, column=0)
        self.button_move.append(button)

        button = Tk.Button(self, text="From", state="disabled", command=lambda: self._move_handler(1))
        button.grid(row=2, column=1)
        self.button_move.append(button)

        button = Tk.Button(self, text="From", state="disabled", command=lambda: self._move_handler(2))
        button.grid(row=2, column=2)
        self.button_move.append(button)

        self.label = Tk.Label(self, text="请输入汉诺塔层数(1-" + str(Hanoi.maxLevel) + ")")
        self.label.grid(row=3, column=0)

        self.entry_level = Tk.Entry(self, validate="all", validatecommand=(self.register(self.is_number), "%S"))#绑定验证事件
        self.entry_level.grid(row=3, column=1)

        self.button_confirm = Tk.Button(self, text="确定", command=self._new_game)
        self.button_confirm.grid(row=3, column=2)

    @staticmethod
    def _draw_one_hanoi(canvas, hanoi, level):#绘制一个汉诺塔
        canvas.delete("all")#清空画布

        canvas_width = Hanoi.canvas_width
        canvas_height = Hanoi.canvas_height - 5

        scale = canvas_width / level / 2.5;#自动缩放比例

        for i in range(0, len(hanoi)):#逐次绘制每层
            w = hanoi[i] * scale
            x0 = canvas_width / 2 - w
            x1 = canvas_width / 2 + w
            y0 = canvas_height - (i + 1) * scale
            y1 = canvas_height - i * scale
            canvas.create_rectangle(x0, y0, x1, y1)

    def _show_hanoi(self):#绘制所有汉诺塔
        for i in range(0, 3):
            Hanoi._draw_one_hanoi(self.canvas_hanoi[i], self.hanoi[i], self.level)

    def _new_game(self):
        entry_value = self.entry_level.get()#获得文本框内容
        if entry_value is '':
            return
        try:
            level = int(entry_value)
            if level < 1 or level > Hanoi.maxLevel:
                showwarning("警告", "请输入1-" + str(Hanoi.maxLevel) + "之间的层数")
                return
            self.level = level
            self.hanoi[0] = range(self.level, 0, -1)
            self.hanoi[1] = []
            self.hanoi[2] = []
            self.focus = None
            self._show_hanoi()
            self.button_move[0].config(state="normal")
            self.button_move[1].config(state="disabled")
            self.button_move[2].config(state="disabled")
        except ValueError, Argument:
            showwarning("警告", "请输入正确的数字" + Argument)

    def _move_handler(self, pos):#处理move操作，并改变button状态
        button_move = self.button_move
        if self.focus is None:
            for i in range(0, 3):
                if i is pos:
                    button_move[i].config(state="normal")
                    button_move[i].config(text="Cancel")
                else:
                    button_move[i].config(text="To")
                    if Hanoi.can_move(self.hanoi[pos], self.hanoi[i]):
                        button_move[i].config(state="normal")
                    else:
                        button_move[i].config(state="disabled")
            self.focus = pos
        else:
            if self.focus is not pos:
                _from = self.hanoi[self.focus]
                _to = self.hanoi[pos]
                if Hanoi.can_move(_from, _to):
                    _to.append(_from[-1])
                    _from.pop()
                    self._show_hanoi()
                    if self.is_success():
                        showinfo("世界毁灭", "世界就将在一声霹雳中被消灭，梵塔、庙宇和众生也都也同归于尽。")
            self.focus = None
            for i in range(0, 3):
                if len(self.hanoi[i]) is 0:
                    button_move[i].config(state="disabled", text="From")
                else:
                    button_move[i].config(state="normal", text="From")

    def is_success(self):#判断是否游戏结束
        return len(self.hanoi[0]) is 0 and len(self.hanoi[1]) is 0

    @staticmethod
    def can_move(_from, _to):#判断能否移动
        if len(_from) is 0:
            return False
        if len(_to) is 0:
            return True
        return _from[-1] < _to[-1]

    @staticmethod
    def is_number(what):#判断是否是unicode的数字
        return unicode(what, "UTF-8").isdecimal()

app = Hanoi()
app.master.title('Hanoi')
app.master.resizable(width=False, height=False)
app.mainloop()
