import tkinter as tk
from prompts import *
import testdatabase
from tkinter import simpledialog


user_select_window = None
note_select_window = None
prompt_box = None
prompts_enabled = True
port=3854
host='ix.cs.uoregon.edu'
username='dtweedale'
password='password'
database='theREALREALREALdatabase'

note_boxes = []
admin_input_boxes = []
admin_inputs = []
note_name = None
exist_notes = None

class TextBoxWithDefaultText:
    def __init__(self, master, default_text, font, width=29, height=1, mode="TITLE", is_on_notepad=False):
        self.default_text = default_text
        self.mode=mode
        self.textbox = tk.Text(master, width=width, height=height, font= font, wrap="word")
        self.textbox.insert("1.0", self.default_text)
        self.textbox.bind("<FocusIn>", self.remove_default_text)
        self.textbox.bind("<FocusOut>", self.restore_default_text)
        self.textbox.pack(fill=tk.BOTH, expand=True)
        if is_on_notepad:
            global note_boxes
            note_boxes.append(self)
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
    user_select_window.geometry("200x250")

    def fetch_users():
        users = []
        try:
            # Connect to the database
            connection = testdatabase.connect_to_database(host, port, username, password, database)
            if connection:
                cursor = connection.cursor()
                cursor.execute("SHOW TABLES")
                # Fetch table names (users)
                tables = cursor.fetchall()
                users = [table[0].split('_')[0] for table in tables]  # Extract usernames from table names
                connection.close()
        except testdatabase.Error as err:
            print(f"Error fetching users: {err}")
        return users

    def create_new_user(user_name):
        try:
            # Connect to the specific database
            connection = testdatabase.connect_to_database(host, port, username, password, database)
            if connection:
                # Check if user table exists or create new one
                testdatabase.check_or_create_user_table(connection, user_name)
                connection.close()
                print("New user created successfully.")
                return True
        except testdatabase.Error as err:
            print(f"Error creating new user: {err}")
        return False
    
    users = fetch_users()

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

        # Button for creating a new user
    def create_new_user_handler():
        user_name = tk.simpledialog.askstring("Create New User", "Enter new user name:")
        if user_name:
            success = create_new_user(user_name)
            if success:
                listbox.insert(tk.END, user_name)

    
    create_user_button = tk.Button(user_select_window, text="Create New User", command=create_new_user_handler)
    create_user_button.pack()

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
        global note_select_window, exist_notes

        # Function to fetch notes from the database
        def fetch_notes(connection, user):
            table_name = f"{user}_notes"
            cursor = connection.cursor()
            try:
                cursor.execute(f"SELECT note_name FROM {table_name}")
                result = cursor.fetchall()
                note_names = [note_name[0] for note_name in result] if result else []
                return note_names
            except testdatabase.Error as err:
                print(f"Error fetching notes: {err}")
                return []
            finally:
                cursor.close()

        connection = testdatabase.connect_to_database(host, port, username, password, database)
        user_select_window.destroy()
        note_select_window = tk.Tk()
        note_select_window.geometry("150x220")
        note_select_window.title(f"Select Note for {user}")

        note_listbox = tk.Listbox(note_select_window, selectmode=tk.SINGLE)
        # Redo these next couple lines, make sure these note names are loaded in from the database
        # These hard-coded ones need to be replaced with actual content
        exist_notes = fetch_notes(connection, user)
        for note in exist_notes:
            note_listbox.insert(tk.END, note)
        
        note_listbox.insert(tk.END, "Create a new note")
        note_listbox.pack()
        
        def fetch_note_details(connection, username, note_name):
            table_name = f"{username}_notes"
            cursor = connection.cursor()
            try:
                cursor.execute(f"""
                    SELECT headers, notes, bullets FROM {table_name} WHERE note_name = %s
                """, (note_name,))
                result = cursor.fetchone()
                if result:
                    return list(result) # Convert the tuple to a list and return it
                else:
                    print(f"No note found with the name '{note_name}'.")
                    return []
            except testdatabase.Error as err:
                print(f"Failed to fetch note data: {err}")
                return []
            finally:
                cursor.close()
        
        selected_note = None
        def get_selection():
            connection = testdatabase.connect_to_database(host, port, username, password, database)
            selected_note = note_listbox.curselection()
            if selected_note:
                selected_note_string = note_listbox.get(selected_note[0])
                print("Selected Note", selected_note_string)
                connection = testdatabase.connect_to_database(host, 3854, username, password, database)
                dictionaries = fetch_note_details(connection, user, selected_note_string)
                print(dictionaries)
                open_notepad(user, selected_note_string, connection, dictionaries)

        button = tk.Button(note_select_window, text="Select Note", command=get_selection)
        button.pack()

        # Very stupid little check to see if the user is an admin
        # The predefined usernames we have only provide one admin account, and the user can't change the usernames
        # So it works - for now
        if user == "Admin":
            button = tk.Button(note_select_window, text="Server Setup", command=lambda:setup_server(user))
            button.pack()

    else:
        print(user)

text_box_count = 1
#Opens the notepad
def open_notepad(user, note, connection, dicts):
    global note_select_window, note_name
    note_select_window.destroy()
    # SAVE BUTTON
    def get_note_name_text():
        if note_name:
            return note_name.textbox.get("1.0", "end-1c")
        else:
            return None
    def get_text():
        headers = {}
        notes = {}
        bullets = {}
        note_name = get_note_name_text()
        cur_header = 0
        # Sort all note boxes except the title into dictionaries
        # These will represent couplings between titles and subordinate note/bullet fields
        for i in range(1, len(note_boxes)):
            ith_box = note_boxes[i]
            ith_box_text = ith_box.textbox.get("1.0", "end-1c")
            cur_header_str = str(cur_header)
            # Send these to the header dictionary
            if ith_box.mode == "HEADING":
                headers[cur_header_str] = ith_box_text
            # In both cases below, we know a note field or a bullet field must be immediately followed
            # by a header field. So increment cur_header by 1.

            # Send these to notes dict
            elif ith_box.mode == "NOTES":
                notes[cur_header_str] = ith_box_text
                cur_header += 1

            # Send these to bullets dict
            else:
                bullets[cur_header_str] = ith_box_text
                cur_header += 1

        testdatabase.insert_note_data(connection, user, note_name, str(headers), str(notes), str(bullets))
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
    note_name = TextBoxWithDefaultText(notepad_frame, "Note Name", chapterfont, is_on_notepad=True)

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