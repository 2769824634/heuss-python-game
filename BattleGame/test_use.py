import tkinter as tk
from tkinter import messagebox
import random
import constants
import characters
# from characters import Unit
from Logger import LogWriter
##########点击攻击之前和user_interface.py一样，就是这个UI代码点击攻击之后死机了，说是Unit.__init__()缺少defence这个数据，真懵逼了，和我之前的猜想一样，这个UI从一开始就没能从其他数据库里面提取到相应资料，完全就是个空壳子，我嘎了。
FRONTEND_UNIT_TYPES = {
    "Warrior": constants.UnitType.Warrior,
    "Tanker": constants.UnitType.Tanker
}

def show_main_window(player_team_info, ai_team_info):
    main_window = tk.Tk()
    main_window.title('Main Window')

    player_team_var = tk.StringVar(main_window)
    ai_team_var = tk.StringVar(main_window)

    # 显示玩家队伍成员
    player_team_var.set(None)
    for i, (name, unit_type) in enumerate(player_team_info):
        text = f"{name} ({unit_type})"
        tk.Radiobutton(main_window, text=text, variable=player_team_var, value=name).grid(row=i, column=0, padx=5, pady=5)

    # 显示AI队伍成员
    ai_team_var.set(None)
    for i, (name, unit_type) in enumerate(ai_team_info):
        text = f"{name} ({unit_type})"
        tk.Radiobutton(main_window, text=text, variable=ai_team_var, value=name).grid(row=i, column=1, padx=5, pady=5)

    # 创建攻击按钮
    attack_button = tk.Button(main_window, text="攻击", command=lambda: characters.Unit.attack(player_team_var.get(), ai_team_var.get())) #蒙蔽了
    attack_button.grid(row=len(player_team_info) // 2, column=2, padx=5, pady=5)
    

    # 主循环
    main_window.mainloop()

def on_finish_button_click(root):
    # 检查是否每个队员都已经填写了信息
    for i in range(3):
        if not entry_names[i].get():
            messagebox.showerror("错误", "请为每个队员选择名称和职业")
            return
    
    # 收集用户队伍信息
    user_team_info = []
    for i in range(3):
        name = entry_names[i].get()
        unit_type = selected_classes[i].get()  # 获取用户选择的职业
        user_team_info.append((name, unit_type))
        
    processed_team = []
    for name, unit_type in user_team_info:
        unit = characters.get_unit(name, FRONTEND_UNIT_TYPES[unit_type])
        processed_team.append((unit.name, unit_type))

    # 随机生成AI队伍信息
    ai_team_info = []
    for i in range(3):
        ai_name = f"AI_Player_{i+1}"
        ai_unit_type = random.choice(["Warrior", 'Tanker'])
        unit = characters.get_unit(ai_name, FRONTEND_UNIT_TYPES[ai_unit_type])
        ai_team_info.append((unit.name, ai_unit_type))

    # 跳转到主界面并传递处理后的队伍信息
    show_main_window(processed_team, ai_team_info)
    root.destroy()  # 销毁主窗口

root = tk.Tk()
root.title("选择队伍")

# 创建队员信息输入框和职业选项
entry_names = []
selected_classes = []

for i in range(3):
    label = tk.Label(root, text=f"队员{i+1}: ")
    label.grid(row=i, column=0, padx=5, pady=5)

    entry_name = tk.Entry(root)
    entry_name.grid(row=i, column=1, padx=5, pady=5)
    entry_names.append(entry_name)

    class_var = tk.StringVar(value='Warrior')  
    selected_class = tk.OptionMenu(root, class_var, 'Warrior', 'Tanker')
    selected_class.grid(row=i, column=2, padx=5, pady=5)
    selected_classes.append(class_var)

# 创建完成按钮
finish_button = tk.Button(root, text="完成", command=lambda: on_finish_button_click(root))
finish_button.grid(row=3, columnspan=3, padx=5, pady=10)

root.mainloop()
