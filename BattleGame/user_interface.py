import tkinter as tk
from tkinter import messagebox
import random
import constants
import characters

######## 以奇怪方式陷入了死循环，角色创建好后，按攻击键屁用没有，（这破玩意是个空壳，最终还是没有连上接口，无能狂怒中）。
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
        tk.Radiobutton(main_window, text=name, variable=player_team_var, value=name).grid(row=i, column=0, padx=5, pady=5)

    # 显示AI队伍成员
    ai_team_var.set(None)
    for i, (name, unit_type) in enumerate(ai_team_info):
        tk.Radiobutton(main_window, text=name, variable=ai_team_var, value=name).grid(row=i, column=1, padx=5, pady=5)

    # 创建攻击按钮
    attack_button = tk.Button(main_window, text="攻击", command=lambda: characters.Unit.attack(player_team_var.get(), ai_team_var.get()))
    attack_button.grid(row=len(player_team_info) // 2, column=2, padx=5, pady=5)

    # 主循环
    main_window.mainloop()

def on_finish_button_click():
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
    
    # if selected_classes[i].get() == "Warrior": #不知道有没有用的史山代码
    #     unit_type= constants.UnitType.Warrior 
    # else: 
    #     unit_type = constants.UnitType.Tanker
    # 获取用户选择职业对应的角色信息
        
    processed_team = []
    for name, unit_type in user_team_info:
        unit = characters.get_unit(name, unit_type)
        processed_team.append((unit.name, unit_type)) #没能成功接入character里的数据

    # 随机生成AI队伍信息
    ai_team_info = []
    for i in range(3):
        ai_name = f"AI_Player_{i+1}"
        ai_unit_type = random.choice(["Warrior", 'Tanker'])
        unit = characters.get_unit(ai_name, ai_unit_type)
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
finish_button = tk.Button(root, text="完成", command=on_finish_button_click)
finish_button.grid(row=3, columnspan=3, padx=5, pady=10)

root.mainloop()
