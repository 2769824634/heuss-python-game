import tkinter
from game_ui import GameUI

def main():#启动！！！！！
    root = tkinter.Tk()
    app = GameUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()