import tkinter
from tkinter import messagebox
import random
from main import Main

class GameUI:#玩家和ui界面的互动
    def __init__(self, master):
        self.master = master
        self.master.title("Turn-based Battle Game")

        self.main_game = Main()

        self.attack_button = tkinter.Button(self.master, text="Attack", command=self.player_turn)
        self.attack_button.pack()

        # 显示游戏状态信息的标签
        self.info_label = tk.Lable(master, text="Welocome to Turn-based Battle Game")
        self.info_label.pack()

        # 添加图像按钮
        self.attack_img = Image.open("attack.png")
        self.attack_img = self.attack_img.resize((100, 50), Image.ANTIALIAS)
        self.attack_img = ImageTk.PhotoImage(self.attack_img)
        self.attack_button = tk.Button(master, image=self.attack_img, command=self.player_turn, borderwidth=0)
        self.attack_button.pack()

    def player_turn(self):
        # 玩家回合
        result = self.main_game.player_turn()
        self.update_info(result)

        # 敌人回合
        enemy_result = self.main_game.enemy_turn()
        self.update_info(enemy_result)

    def update_info(self, result):
        # 更新游戏状态信息
        self.info_label.config(text=result)

if __name__ == "__main__":
    root = tkinter.Tk()
    app = GameUI(root)
    root.mainloop()