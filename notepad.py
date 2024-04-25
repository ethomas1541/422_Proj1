import tkinter as tk


#Make the window
window = tk.Tk()
window.title("User Selection")

# List of users
users = ["User 1", "User 2", "User 3" ]



#User selection
def select_user():
    global selected_user #stores the selected user
    selected_users = listbox.curselection() 
    if selected_users:
        selected_user_index = selected_users[0]
        selected_user = listbox.get(selected_user_index)
        print("Selected User:", selected_user)
        open_notepad(selected_user)


text_box_count = 1
#Opens the notepad
def open_notepad(user):
    window.destroy()

    # SAVE BUTTON
    def get_text():
        #CODE FOR SAVING
        #text = textbox.get("1.0", "end-1c")
        print("Text entered:")
        #print(text)

    def add_text_boxes():
        global text_box_count
        text_box_count += 1
        headingfont = ("Arial", 15)
        notesfont = ("Arial", 12)
        TextBoxWithDefaultText(notepad_frame, "Heading...", headingfont)
        TextBoxWithDefaultText(notepad_frame, "Notes...", notesfont, height=5)
        canvas.update_idletasks()  # Update the canvas to reflect the two new note pads
        canvas.config(scrollregion=canvas.bbox("all"))  # Rescales the region you can scroll in

    class TextBoxWithDefaultText:
        def __init__(self, master, default_text, font, width=65, height=2):
            self.default_text = default_text
            self.textbox = tk.Text(master, width=width, height=height, font= font)
            self.textbox.insert("1.0", self.default_text)
            self.textbox.bind("<FocusIn>", self.remove_default_text)
            self.textbox.bind("<FocusOut>", self.restore_default_text)
            self.textbox.pack(fill=tk.BOTH, expand=True)
        
        def remove_default_text(self, event):
            if self.textbox.get("1.0", "end-1c") == self.default_text:
                self.textbox.delete("1.0", tk.END)
        
        def restore_default_text(self, event):
            if not self.textbox.get("1.0", "end-1c"):
                self.textbox.insert("1.0", self.default_text)

    notepad_window = tk.Tk()
    notepad_window.title(f"{user} Notes") #Names the notepad


    scrollbar = tk.Scrollbar(notepad_window, orient=tk.VERTICAL)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    button = tk.Button(notepad_window, text="Get Text", command=get_text)
    button.pack()

    canvas = tk.Canvas(notepad_window, yscrollcommand=scrollbar.set)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    notepad_frame = tk.Frame(canvas)

    canvas.create_window((0, 0), window=notepad_frame, anchor="nw")
    canvas.config(yscrollcommand=scrollbar.set, scrollregion=canvas.bbox("all"))
    scrollbar.config(command=canvas.yview)

    chapterfont = ("Arial", 18)
    TextBoxWithDefaultText(notepad_frame, "Chapter...", chapterfont)

    add_button = tk.Button(notepad_window, text="Add Text Boxes", command=add_text_boxes)
    add_button.pack()

    #Runs the program
    notepad_window.mainloop()


#Makes a listbox so you can choose the user
listbox = tk.Listbox(window, selectmode=tk.SINGLE)
for user in users:
    listbox.insert(tk.END, user)
listbox.pack()

#Button for selecting user and switching to notepad
button = tk.Button(window, text="Select User", command=select_user)
button.pack()

#Runs the user selection program
window.mainloop()