import tkinter as tk
from tkinter import messagebox
import characters
import random
import constants

def show_main_window(team_info):
    # 这里是跳转到主界面的操作
    print("跳转到主界面，队伍信息：", team_info)

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
        user_team_info.append((name))
    
    ai_team_info = []
    for i in range(3):
        ai_name = f"AI_Player_{i+1}"
        unit_type = random.choice([constants.UnitType.Warrior, constants.UnitType.Tanker])
        ai_team_info.append((ai_name, unit_type))
    

    processed_team = [
        characters.get_unit(unit_type, name) \
        for name, unit_type \
        in zip(entry_names, selected_classes)\
    ]
    
    # 跳转到主界面并传递处理后的队伍信息
    show_main_window(processed_team)
    show_main_window(ai_team_info)
    root.destroy()


root = tk.Tk()
root.title("选择队伍")

# 创建队员信息输入框和职业选项
entry_names = []
selected_classes = []
for i in range(3):
    label = tk.Label(root, text=f"队员{i+1}：")
    label.grid(row=i, column=0, padx=5, pady=5)

    entry_name = tk.Entry(root)
    entry_name.grid(row=i, column=1, padx=5, pady=5)
    entry_names.append(entry_name)

    class_var = tk.StringVar()
    class_var.set('Warrior')  # 默认选中战士
    selected_class = tk.OptionMenu(root, class_var, "Warrior", "Tanker")
    selected_class.grid(row=i, column=2, padx=5, pady=5)
    selected_classes.append(class_var)

selected_classes = [
    constants.UnitType.Warrior if class_var == 'Warrior' else constants.UnitType.Tanker for unit_type in selected_classes
]


# 创建完成按钮
finish_button = tk.Button(root, text="完成", command=on_finish_button_click)
finish_button.grid(row=3, columnspan=3, padx=5, pady=10)

root.mainloop()

