import tkinter as tk
from prompts import *
import testdatabase

user_select_window = None
note_select_window = None
prompt_box = None
prompts_enabled = True

note_boxes = []
notes = []
admin_input_boxes = []
admin_inputs = []

class TextBoxWithDefaultText:
    def __init__(self, master, default_text, font, width=29, height=1, mode="TITLE", is_on_notepad=False):
        self.default_text = default_text
        self.textbox = tk.Text(master, width=width, height=height, font= font, wrap="word")
        self.textbox.insert("1.0", self.default_text)
        self.textbox.bind("<FocusIn>", self.remove_default_text)
        self.textbox.bind("<FocusOut>", self.restore_default_text)
        self.textbox.pack(fill=tk.BOTH, expand=True)
        if is_on_notepad:
            global note_boxes
            note_boxes.append(self.textbox)
            print(note_boxes)
        else:
            global admin_input_boxes
            admin_input_boxes.append(self.textbox)
            print(admin_inputs)
    
    def remove_default_text(self, event):
        if self.textbox.get("1.0", "end-1c") == self.default_text:
            self.textbox.delete("1.0", tk.END)
    
    def restore_default_text(self, event):
        if not self.textbox.get("1.0", "end-1c"):
            self.textbox.insert("1.0", self.default_text)

#User selection
def select_user():
    #Make the window
    global user_select_window
    user_select_window = tk.Tk()
    user_select_window.title("User Selection")
    user_select_window.geometry("150x200")

    # List of users
    users = ["Admin 1", "User 2", "User 3"]

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

def setup_server(user):
    note_select_window.destroy()
    server_setup_window = tk.Tk()
    server_setup_window.geometry("300x140")
    server_setup_window.title("mysql Server Setup")
    fields = ["Port Number", "Username", "Password", "New Database Name"]
    host_label = tk.Label(server_setup_window, text="Hostname: ix.cs.uoregon.edu", font=("Courier", 12))
    host_label.pack()
    for x in fields:
        TextBoxWithDefaultText(server_setup_window, x, ("Courier", 12), width=20, height=1)

    def db_main():
        global admin_inputs
        admin_inputs=[]
        for x in admin_input_boxes:
            admin_inputs.append(x.get("1.0", "end-1c"))
        print("db main")
        for i in range(0, 4):
            print(admin_inputs[i], fields[i])
            if admin_inputs[i] == fields[i]:
                return
        print("db main 2")
        testdatabase.main(admin_inputs[0], admin_inputs[1], admin_inputs[2], admin_inputs[3], str.replace(user, " ", "_"))

    button = tk.Button(server_setup_window, text="Submit", command=db_main)
    button.pack()

def select_note(user):
    if user:
        global note_select_window
        user_select_window.destroy()
        note_select_window = tk.Tk()
        note_select_window.geometry("150x220")
        note_select_window.title(f"Select Note for {user}")

        note_listbox = tk.Listbox(note_select_window, selectmode=tk.SINGLE)
        # Redo these next couple lines, make sure these note names are loaded in from the database
        # These hard-coded ones need to be replaced with actual content
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

        # Very stupid little check to see if the user is an admin
        # The predefined usernames we have only provide one admin account, and the user can't change the usernames
        # So it works - for now
        if user[0] == "A":
            button = tk.Button(note_select_window, text="Server Setup", command=lambda:setup_server(user))
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

    def add_text_boxes(box_type):
        mode = "NOTES"
        if box_type[0] == "B":
            mode = "BULLET_LIST"
        global text_box_count
        text_box_count += 1
        headingfont = ("Arial", 15)
        notesfont = ("Arial", 12)
        TextBoxWithDefaultText(notepad_frame, "Heading...", headingfont, mode="HEADING", is_on_notepad=True)
        TextBoxWithDefaultText(notepad_frame, box_type, notesfont, height=5, mode=mode, is_on_notepad=True)
        canvas.update_idletasks()  # Update the canvas to reflect the two new note pads
        canvas.config(scrollregion=canvas.bbox("all"))  # Rescales the region you can scroll in

    def toggle_prompts():
        global prompts_enabled, prompt_box
        prompts_enabled = not prompts_enabled
        if prompts_enabled:
            prompt_box.pack(pady=5)
        else:
            prompt_box.pack_forget()

    def cycle_prompts():
        global prompt_box   
        prompt_box.config(text=get_prompt())
        prompt_box.after(10000, cycle_prompts)

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
    TextBoxWithDefaultText(notepad_frame, "Note Name", chapterfont, is_on_notepad=True)

    add_button = tk.Button(notepad_window, text="Add Text Boxes", command=lambda:add_text_boxes("Notes..."))
    add_button.pack(pady=5)

    bullet_button = tk.Button(notepad_window, text="Add Bulleted Points", command=lambda:add_text_boxes("Bulleted List..."))
    bullet_button.pack(pady=5)

    toggle_prompts_button = tk.Button(notepad_window, text="Toggle Prompts", command=toggle_prompts)
    toggle_prompts_button.pack(pady=20)

    global prompt_box
    prompt_box = tk.Label(notepad_window, text=get_prompt(), width=20, wraplength=140, bg="yellow", borderwidth=3, relief="sunken")
    prompt_box.pack(pady=5)

    #Runs the program
    
    cycle_prompts()
    notepad_window.mainloop()

if __name__ == "__main__":
    select_user()