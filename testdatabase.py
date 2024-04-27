import tkinter as tk
from prompts import *

user_select_window = None
note_select_window = None
prompt_box = None
prompts_enabled = True

#User selection
def select_user():
    #Make the window
    global user_select_window
    user_select_window = tk.Tk()
    user_select_window.title("User Selection")
    user_select_window.geometry("150x200")

    # List of users
    users = ["User 1", "User 2", "User 3" ]

    #Makes a listbox so you can choose the user
    listbox = tk.Listbox(user_select_window, selectmode=tk.SINGLE)
    for user in users:
        listbox.insert(tk.END, user)
    listbox.pack()

    selected_user = None
    def get_selection():
        selected_user = listbox.curselection()
        if selected_user:
            selected_user_string = listbox.get(selected_user[0])
            print("Selected User:", selected_user_string)
            select_note(selected_user_string)

    #Button for selecting user and switching to notepad
    button = tk.Button(user_select_window, text="Select User", command=get_selection)
    button.pack()

    #Runs the user selection program
    user_select_window.mainloop()

def select_note(user):
    if user:
        global note_select_window
        user_select_window.destroy()
        note_select_window = tk.Tk()
        note_select_window.geometry("150x200")
        note_select_window.title(f"Select Note for {user}")

        note_listbox = tk.Listbox(note_select_window, selectmode=tk.SINGLE)
        note_listbox.insert(tk.END, "Sample Note")
        note_listbox.insert(tk.END, "New Note")
        note_listbox.pack()

        selected_note = None
        def get_selection():
            selected_note = note_listbox.curselection()
            if selected_note:
                selected_note_string = note_listbox.get(selected_note[0])
                print("Selected Note", selected_note_string)
                open_notepad(user, selected_note_string)

        button = tk.Button(note_select_window, text="Select Note", command=get_selection)
        
        button.pack()
    else:
        print(user)

text_box_count = 1
#Opens the notepad
def open_notepad(user, note):
    global note_select_window
    note_select_window.destroy()

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

    def add_bullet():
        global text_box_count
        text_box_count += 1
        headingfont = ("Arial", 15)
        notesfont = ("Arial", 12)
        TextBoxWithDefaultText(notepad_frame, "Heading...", headingfont)
        TextBoxWithDefaultText(notepad_frame, "Bulleted List", notesfont, height=5)
        canvas.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

    def toggle_prompts():
        global prompts_enabled, prompt_box
        prompts_enabled = not prompts_enabled
        if prompts_enabled:
            prompt_box.pack(pady=5)
        else:
            prompt_box.pack_forget()

    def cycle_prompts():
        prompt_box.config()

    class TextBoxWithDefaultText:
        def __init__(self, master, default_text, font, width=29, height=1):
            self.default_text = default_text
            self.textbox = tk.Text(master, width=width, height=height, font= font, wrap="word")
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
    notepad_window.title(f"{user}: {note}") #Names the notepad


    scrollbar = tk.Scrollbar(notepad_window, orient=tk.VERTICAL)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Use this to submit text into the database
    button = tk.Button(notepad_window, text="Save Note", command=get_text)
    button.pack()

    canvas = tk.Canvas(notepad_window, yscrollcommand=scrollbar.set)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    notepad_frame = tk.Frame(canvas)

    canvas.create_window((0, 0), window=notepad_frame, anchor="nw")
    canvas.config(yscrollcommand=scrollbar.set, scrollregion=canvas.bbox("all"))
    scrollbar.config(command=canvas.yview)

    chapterfont = ("Arial", 18)
    TextBoxWithDefaultText(notepad_frame, "Note Name", chapterfont)

    add_button = tk.Button(notepad_window, text="Add Text Boxes", command=add_text_boxes)
    add_button.pack(pady=5)

    bullet_button = tk.Button(notepad_window, text="Add Bulleted Points", command=add_bullet)
    bullet_button.pack(pady=5)

    toggle_prompts_button = tk.Button(notepad_window, text="Toggle Prompts", command=toggle_prompts)
    toggle_prompts_button.pack(pady=5)

    global prompt_box
    prompt_box = tk.Label(notepad_window, text=get_prompt(), width=20, wraplength=140, bg="yellow", borderwidth=3, relief="sunken")
    prompt_box.pack(pady=5)

    #Runs the program
    
    notepad_window.mainloop()

if __name__ == "__main__":
    select_user()