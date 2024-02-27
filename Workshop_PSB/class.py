import tkinter as tk

class TeamSelectionPopup:
    def __init__(self, master):
        self.master = master
        self.master.title("选择队伍")

        self.team = []

        # Label and Entry for each team member
        self.member_entries = []
        for i in range(3):
            lbl = tk.Label(master, text=f"队员 {i+1} 姓名:")
            lbl.grid(row=i, column=0, padx=5, pady=5)
            entry = tk.Entry(master)
            entry.grid(row=i, column=1, padx=5, pady=5)
            self.member_entries.append(entry)

        # Radio buttons for selecting profession
        self.profession_var = tk.StringVar(master, "战士")
        warrior_radio = tk.Radiobutton(master, text="战士", variable=self.profession_var, value="战士")
        warrior_radio.grid(row=3, column=0, padx=5, pady=5)
        tanker_radio = tk.Radiobutton(master, text="坦克", variable=self.profession_var, value="坦克")
        tanker_radio.grid(row=3, column=1, padx=5, pady=5)

        # Button to submit team selection
        submit_btn = tk.Button(master, text="完成", command=self.submit_selection)
        submit_btn.grid(row=4, columnspan=2, padx=5, pady=10)

    def submit_selection(self):
        # Collect team member names and professions
        for entry in self.member_entries:
            name = entry.get().strip()
            if name:
                profession = self.profession_var.get()
                self.team.append((name, profession))
        
        # Close the popup window
        self.master.destroy()

def main():
    root = tk.Tk()
    popup = TeamSelectionPopup(root)
    root.mainloop()

    # After the popup is closed, you can access the selected team
    print("Selected Team:")
    for member in popup.team:
        print(member)

if __name__ == "__main__":
    main()
