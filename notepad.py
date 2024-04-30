# Authors: Brian Griffith, Elijah Thomas, Drew Tweedale
# Last modified: April 27 2024

# Core module of the project, governing all visible UI and making all database calls relevant to populating, maintaining
# and updating said UI.

# Key elements:
"""
    TextBoxWithDefaultText
        Class used as a wrapper for the tkinter Text object. Used in very different ways either on the notepad screen
        or on the administrative server setup screen. This class is engineered to detect which screen it's on during
        instantiation and to change its behavior accordingly.

    server_setup(user)
        Essentially a wrapper for the config_handler module, which ensures that any server data entered is cached and
        can later be reconfigured by an admin user.

        On the program's first launch, the application has no knowledge of its sql server, so it is implied that the
        user should type in the necessary information.

        May serve as a launch point into select_user, or may require use of the back button, depending on how
        the function was called

    select_user()
        This function both validates the entered server configuration information, displaying a warning if it's not
        usable, making appropriate database queries if it is valid information, then populating the related UI with
        the results of those queries.

        Afterward, select_note is fired with the selected user as an argument.

    select_note(user)
        Opens a screen very similar to select_user(), except populated by a collection of the given user's note tables.

        Afterward, open_notepad is fired with several arguments collected from this function and select_user.

    open_notepad(user, note, connection, dicts)
        Arguments are defined at length in the related docstring

        Opens the notepad view, the main part of the program. If <note> refers to an existing note in the database,
        the entire structure of that note will be retrieved from the database, deserialized and placed in direct
        view of the user.

        Also contains a save button which manages serializing and sending data to the database.
"""

import tkinter as tk
from prompts import *
import note_storage
from tkinter import simpledialog
import config_handler
from os.path import isfile, abspath
from os import remove as os_remove

user_select_window = None       # Globally defined variables for tkinter windows
note_select_window = None
server_setup_window = None
notepad_window = None

prompt_box = None               # Global variable for the yellow prompt box in the notepad window
prompts_enabled = True          # Toggle variable determining said box's visibility
               
hide_button_frame = None        # All hide buttons get sent here - needs global definition because the
                                # TextBoxWithDefaultText class references it

host='ix.cs.uoregon.edu'        # Hardcoded for obvious reasons

port=None                       # Used for all database queries, loaded from config.txt file
username=None
password=None
database=None

note_boxes = []                 # List of tkinter objects for storing notes
admin_input_boxes = []          # List of the tkinter objects that capture admin inputs for database configuration
admin_inputs = []               # List of the actual strings submitted inside those boxes\

note_name = None                # Name of current note
exist_notes = None              # Existing notes in database, if applicable

class TextBoxWithDefaultText:
    """
    Most important class in the project - used both for taking notes and for supplying admin input for database
    configuration

    Attributes:
        default_text:   string containing the default text of this box
        mode:           string of form TITLE, NOTES OR BULLET_LIST
        textbox:        tkinter textbox object that takes input
                        most arguments to __init__ get passed into here

    Methods:
        toggle_hidden()
            Hides the corresponding text box, if applicable

        remove_default_text()
            Make way for user input, removing default text from the box

        restore_default_text()
            Place the text defined by __init__ into the text box if it's empty

        add_bullets()
            Prepend a unicode dot character to each line in the input
            applies only if self.mode == "BULLET_LIST"

            Fires whenever the user presses enter

    """
    def __init__(self, master, default_text, font, width=29, height=1, mode="TITLE", is_on_notepad=False):
        self.default_text = default_text
        self.mode=mode
        self.textbox = tk.Text(master, width=width, height=height, font= font, wrap="word")
        self.textbox.insert("1.0", self.default_text)

        # Describe generic behaviors for default text textboxes
        # i.e., shooing away the default text when the user focuses
        self.textbox.bind("<FocusIn>", self.remove_default_text)
        self.textbox.bind("<FocusOut>", self.restore_default_text)

        # Behavior is more defined if we're in the notepad view
        # We need to add a button to hide fields
        if is_on_notepad:
            self.hidden = False
            # Need this padding to synchronize the scrolling
            self.hide_button = tk.Button(hide_button_frame, text="👁", command=self.toggle_hidden, pady=30)
            self.hide_button.pack(side=tk.TOP)

        # Bind pressing enter to forcing bullet-list formatting
        if self.mode == "BULLET_LIST":
            self.textbox.bind("<Key>", self.add_bullets)
        self.textbox.pack(fill=tk.BOTH, expand=True)

        # note_boxes will be used to serialize data and send it to the database
        if is_on_notepad:
            global note_boxes
            note_boxes.append(self)

        # If not on the notepad, assume we're in database configuration view
        else:
            global admin_input_boxes
            admin_input_boxes.append(self.textbox)
            # print(admin_inputs)

    # Toggle the hidden attribute, then make the text in said textbox camouflage or un-camouflage
    def toggle_hidden(self):
        self.hidden = not self.hidden
        if self.hidden:
            self.textbox.config(fg="#fff")
        else:
            self.textbox.config(fg="#000")

    # Self-explanatory
    def remove_default_text(self, event):
        if self.textbox.get("1.0", "end-1c") == self.default_text:
            self.textbox.delete("1.0", tk.END)
    
    # See line 104
    def restore_default_text(self, event):
        if not self.textbox.get("1.0", "end-1c"):
            self.textbox.insert("1.0", self.default_text)

    # Take input and replace it with a bulleted list
    def add_bullets(self, event):
        # Check if it's the return key
        if(event.keysym == "Return"):
            # Unfiltered text that's in the box
            raw_text = self.textbox.get("1.0", "end-1c")
            # Reset the box, akin to restore_default_text
            if not raw_text:
                self.textbox.insert("1.0", self.default_text)
            else:
                # Split lines into an array
                lines = raw_text.split("\n")
                # Array which will hold bulleted results
                bulleted_lines = []
                # Remove unformatted text
                self.textbox.delete("1.0", tk.END)
                # print("\n".join(lines))
                # Format the text
                for x in lines:
                    try:
                        # Prepend the dot only if it's not already there
                        if x[0] != "●":
                            bulleted_lines.append("● " + x)
                        else:
                            bulleted_lines.append(x)
                    except:
                        pass
                # Insert the now-formatted text
                self.textbox.insert("1.0", "\n".join(bulleted_lines))

#User selection
def select_user():
    """
    No args, no return value

    All code governing user selection is here. This function manages retrieving a list of users from the database,
    properly reflecting the retrieved list in the tkinter UI, and creating new users to be added to the database.

    Lastly, it handles staging what the user needs to advance to the window where they select one of their notes to
    edit or chooses to create a new note.
    """
    # Check for originating windows that may have opened this one
    # ...And kill them all
    try:
        server_setup_window.destroy()
    except:
        pass
    try:
        note_select_window.destroy()
    except:
        pass

    #Make the window
    global user_select_window
    user_select_window = tk.Tk()
    user_select_window.title("User Selection")
    user_select_window.geometry("200x300")

    # Uses calls to note_storage to populate the users listbox, which will appear later
    def fetch_users():
        users = []
        try:
            # Connect to the database
            connection = note_storage.connect_to_database(host, port, username, password, database)
            if connection:
                cursor = connection.cursor()
                cursor.execute("SHOW TABLES")
                # Fetch table names (users)
                tables = cursor.fetchall()
                users = [table[0].split('_')[0] for table in tables]  # Extract usernames from table names
                connection.close()
        except note_storage.Error as err:
            print(f"Error fetching users: {err}")
        return users

    # Use calls to note_storage to create a user with a new table in the database
    def create_new_user(user_name):
        try:
            # Connect to the specific database
            connection = note_storage.connect_to_database(host, port, username, password, database)
            if connection:
                # Check if user table exists or create new one
                note_storage.check_or_create_user_table(connection, user_name)
                connection.close()
                print("New user created successfully.")
                return True
        except note_storage.Error as err:
            print(f"Error creating new user: {err}")
        return False
    
    users = fetch_users()

    # It is VERY BAD if this gets set to true - it means that somehow the database cannot be reached.
    # If so, the app will behave in an undefined way, so I'll put this scary red banner here
    if note_storage.error_flag:
        tk.Label(bg="red", wraplength=200, width=30, height=3, text="Database connection error; please check the console and restart the application").pack()
        # If the error flag is set, chances are the user entered un-workable database information
        # Delete the config file so they have a chance to renew their information without manually
        # editing config.txt
        os_remove("config.txt")

    # Makes a listbox so you can choose the user
    listbox = tk.Listbox(user_select_window, selectmode=tk.SINGLE)
    # Iterates through the list of users we got from the earlier database query
    # And adds them each as an accessible list item
    for user in users:
        listbox.insert(tk.END, user)
    listbox.pack()

    # This function gets fired by the button below
    def get_selection():
        selected_user = listbox.curselection()
        if selected_user:
            selected_user_string = listbox.get(selected_user[0])
            print("Selected User:", selected_user_string)
            # Pass the string from the selected listbox item as an argument to the next window
            select_note(selected_user_string)

    #Button for selecting user and switching to notepad
    button = tk.Button(user_select_window, text="Select User", command=get_selection)
    button.pack()

    # Button for creating a new user
    def create_new_user_handler():
        # Small separate popup for typing in the username
        user_name = tk.simpledialog.askstring("Create New User", "Enter new user name:")
        if user_name:
            success = create_new_user(user_name)
            # We've got the new username right here, why go to the database again to retrieve it?
            if success:
                listbox.insert(tk.END, user_name)

    # Button for calling the function above manually
    create_user_button = tk.Button(user_select_window, text="Create New User", command=create_new_user_handler)
    create_user_button.pack()

    # Finalizes the window
    user_select_window.mainloop()

def setup_server(user):
    """
    Arg: user
        used solely to determine the corresponding user's note select screen to which we return if the back
        button is pressed and whether or not we're to create a new user table
    
    No return value

    This function is very important - it both handles the initial connection procedure to the mySQL database
    and ensures that admin-privileged users can reconfigure the database or switch to a different one (or even a
    different port on ixdev altogether)

    Of course, it also handles the UI for such things
    """

    # Reference global variable for holding the relevant text objects
    global admin_input_boxes
    # CLEAR THAT LIST! Otherwise old inputs may be reused, which is very bad.
    admin_input_boxes = []
    # We can tell whether this is at program startup or not by determining the presence of this other
    # window that may have preceded it
    initial_setup = not bool(note_select_window)
    title_string = "Configure mysql Server"
    global server_setup_window
    server_setup_window = tk.Tk()
    server_setup_window.geometry("300x140")
    if not initial_setup:
        # Destroy existing window if applicable
        try:
            note_select_window.destroy()
        except:
            pass
        # Have to use lambda here, because we NEED to pass an argument to select_note()
        # ...but tkinter does not allow this on its own, so lambda is the workaround
        # lambdas are treated as nothing more than function references even though you can pass arguments to them
        back_button = tk.Button(server_setup_window, text="<<", command=lambda:select_note(user))
        back_button.pack(side=tk.LEFT, anchor=tk.NW)
    else:
        title_string = "Connect to mysql Server"
    server_setup_window.title(title_string)
    
    # Default text to put in the boxes
    fields = ["Port Number", "Username", "Password", "New Database Name"]
    # ...Except this one, which is hardcoded.
    host_label = tk.Label(server_setup_window, text="Hostname: ix.cs.uoregon.edu", font=("Courier", 12))
    host_label.pack()
    # Make a TBw/DT (TextBoxWithDefaultText) for each field in fields
    for x in fields:
        # The objects created by instantiation here get appended to admin_input_boxes
        TextBoxWithDefaultText(server_setup_window, x, ("Courier", 12), width=20, height=1)

    def db_main():
        """
        No args, no return value

        The fundamental function for connecting to the mySQL database, and for ensuring that connection configurations
        are stored and don't need to be reiterated every time
        """
        # Same general idea as our use of admin_input_boxes above
        global admin_inputs
        admin_inputs = []
        for x in admin_input_boxes:
            # Populate w/ the contents of the admin input boxes
            admin_inputs.append(x.get("1.0", "end-1c"))

        # Ensure that no fields still have their default text
        for i in range(0, 4):
            if admin_inputs[i] == fields[i]:
                print("All fields are required")
                return
            
        # Save this config so it can be automatically referenced on relaunch
        config_handler.write_config({
            "Port": admin_inputs[0],
            "Username": admin_inputs[1],
            "Password": admin_inputs[2],
            "Database Name": admin_inputs[3]
        })

        # Attempt a connection to the database with the given inputs
        # mySQL won't allow spaces in ara_username so replace them with _'s
        note_storage.main(admin_inputs[0], admin_inputs[1], admin_inputs[2], admin_inputs[3], str.replace(user, " ", "_"))
        global port, username, password, database

        # Change global variables to the most recent admin inputs
        # Because these variables are used elsewhere throughout this file
        port = admin_inputs[0]
        username = admin_inputs[1]
        password = admin_inputs[2]
        database = admin_inputs[3]
        # If this was their initial setup, advance to user selection
        if initial_setup:
            select_user()
        # Otherwise, switch into the admin user on the new database
        # (it should exist by default)
        else:
            select_note(user)

    # Button for firing db_main
    button = tk.Button(server_setup_window, text="Submit", command=db_main)
    button.pack()
    server_setup_window.mainloop()

def select_note(user):
    """
    Arg: user
        The user whose notes we're to retrieve. Because of the structure of this code, this can ONLY EVER be
        an actual user who is actually present in the database at the time of the function call.
    
    No return value

    Once the user given by user's list of notes has been retreived, the next step is to ask the user which
    notes table they would like to access. This function handles that entire process and wraps it all in UI.
    """
    if user:
        global note_select_window, exist_notes

        # Function to fetch notes from the database
        def fetch_notes(connection, user):
            # Focus on the corresponding table in the database, named with the convention shown in note_storage.py
            table_name = f"{user}_notes"
            cursor = connection.cursor()
            try:
                # SQL query
                cursor.execute(f"SELECT note_name FROM {table_name}")
                result = cursor.fetchall()
                note_names = [note_name[0] for note_name in result] if result else []
                return note_names
            except note_storage.Error as err:
                print(f"Error fetching notes: {err}")
                return []
            finally:
                cursor.close()

        # See relevant commentary in note_storage
        connection = note_storage.connect_to_database(host, port, username, password, database)
        
        # There are a lot of originator windows that can reach this one, so we need to slaughter the whole lot of them
        # unless we want the screen to get crowded really quickly
        try:
            user_select_window.destroy()
        except:
            pass
        try:
            server_setup_window.destroy()
        except:
            pass
        try:
            notepad_window.destroy()
        except:
            pass

        # Make overarching window
        note_select_window = tk.Tk()
        note_select_window.geometry("250x250")
        note_select_window.title(f"Select Note for {user}")

        # Insert back button with function for previous window attached
        back_button = tk.Button(note_select_window, text="<<", command=select_user)
        back_button.pack(side=tk.LEFT, anchor=tk.NW)

        note_listbox = tk.Listbox(note_select_window, selectmode=tk.SINGLE)
        
        # Populate note_listbox with the notes we've retrieved for the user from the database
        exist_notes = fetch_notes(connection, user)
        for note in exist_notes:
            note_listbox.insert(tk.END, note)
        
        # Option to create a new note will be at the bottom
        note_listbox.insert(tk.END, "Create a new note")
        note_listbox.pack()
        
        # Master function for loading a note from the database back into the actual application where it can then
        # be edited, expanded, saved or renamed at the user's will
        def fetch_note_details(connection, username, note_name):
            # Find the table associated with the user, just as in fetch_notes
            table_name = f"{username}_notes"
            cursor = connection.cursor()
            try:
                # SQL query to said table
                cursor.execute(f"""
                    SELECT headers, notes, bullets FROM {table_name} WHERE note_name = %s
                """, (note_name,))
                result = cursor.fetchone()
                if result:
                    return list(result) # Convert the tuple to a list and return it
                # This case will fire if "Create new note" is selected
                else:
                    print(f"No note found with the name '{note_name}'.")
                    return []
            except note_storage.Error as err:
                print(f"Failed to fetch note data: {err}")
                return []
            finally:
                cursor.close()

        # Function to be bound to the select note button
        def get_selection():
            connection = note_storage.connect_to_database(host, port, username, password, database)
            selected_note = note_listbox.curselection()
            if selected_note:
                selected_note_string = note_listbox.get(selected_note[0])
                print("Selected Note", selected_note_string)
                connection = note_storage.connect_to_database(host, 3854, username, password, database)
                dictionaries = fetch_note_details(connection, user, selected_note_string)
                # print(dictionaries)
                # dictionaries stores a serialized data structure that we will use to load the
                # data back into the notepad
                open_notepad(user, selected_note_string, connection, dictionaries)

        button = tk.Button(note_select_window, text="Select Note", command=get_selection)
        button.pack()

        # Not exactly a secure check to see if the user's an admin, but it works for now.
        # Only give the user any permission to influence the database configuration if they're an admin
        # Lambda is used here for the same reasons it was used on line ~290
        if user == "Admin":
            button = tk.Button(note_select_window, text="Server Setup", command=lambda:setup_server(user))
            button.pack()

    # This should be unreachable, and is only here for debugging
    else:
        print(user)

text_box_count = 1
#Opens the notepad
def open_notepad(user, note, connection, dicts):
    """
    args:
        user:
            A string containing the username of the user for which the note is being retrieved/newly created

        note:
            The name of the note being opened

        connection:
            mysql object referring to an existing connection to the database

        dicts:
            Serialized data containing the information contained in the database for the given note
            If the user has selected "create a new note", this will be []

    No return value

    The main workhorse of the entire project, and the most complex window. This is where the database, the
    TextBoxWithDefaultText class, its subordinate hide buttons and the prompts library all come together
    in the main feature.

    Text boxes can be added manually, two-at-a-time with respect to the fact that each note/bullet point field
    is created with a header field immediately preceding it

    All fields have hide buttons associated with them regardless of their <mode> parameter

    Text boxes cannot currently be removed, however those not saved manually with the save button will be
    entirely forgotten when reloaded from the database, allowing for some superficial "temporary" note-taking
    """
    global note_name, note_boxes
    # Empty out this global array, otherwise notes from a previous session might creep in
    # which will almost certainly cause a runtime error
    note_boxes = []

    # Destroy the note select window where applicable
    try:
        note_select_window.destroy()
    except:
        pass

    # Small helper function that calls a generic tkinter get function
    def get_note_name_text():
        if note_name:
            return note_name.textbox.get("1.0", "end-1c")
        else:
            return None
    
    # Serialize the data entered into the boxes, allowing easy transportation to the database
    def get_text():
        headers = {}
        notes = {}
        bullets = {}
        note_name = get_note_name_text()
        cur_header = 0
        # Sort all note boxes except the title into dictionaries
        # These will represent couplings between headings and subordinate note/bullet fields
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

        # Make a call to note_storage, inserting the serialized data into the database
        note_storage.insert_note_data(connection, user, note_name, str(headers), str(notes), str(bullets))
    
    # Very important function, both for the user and for loading in data from the database
    def add_text_boxes(box_type):
        # Assume a default mode
        mode = "NOTES"
        # Switch to bulleted list if we're proven wrong
        if box_type[0] == "B":
            mode = "BULLET_LIST"
        global text_box_count
        text_box_count += 1
        headingfont = ("Arial", 15)
        notesfont = ("Arial", 12)
        # Whenever boxes are added, a heading field gets added inevitably. Here it is, with its default text hard-coded.
        TextBoxWithDefaultText(notepad_frame, "Heading...", headingfont, mode="HEADING", is_on_notepad=True)
        TextBoxWithDefaultText(notepad_frame, box_type, notesfont, height=5, mode=mode, is_on_notepad=True)
        canvas.update_idletasks()  # Update the canvas to reflect the two new note pads
        canvas.config(scrollregion=canvas.bbox("all"))  # Rescales the region you can scroll in
        # We need references to the two newly-created text boxes, in case they're going to be populated with
        # incoming text from the database
        # Unfortunately we can't get a return value from TextBoxWithDefaultText.__init__(), but since that very
        # same function appends the boxes to the note_boxes list, we can use some clever indexing to find out where
        # they are and return them as a tuple
        return (note_boxes[-2], note_boxes[-1])

    # Fairly self-explanatory. When the user clicks this, invert the prompts_enabled global bool and pack or unpack
    # the prompt_box tkinter object accordingly
    def toggle_prompts():
        global prompts_enabled, prompt_box
        prompts_enabled = not prompts_enabled
        if prompts_enabled:
            prompt_box.pack(pady=5)
        else:
            prompt_box.pack_forget()

    # Runs "asynchronously", though not in the usual Python way
    def cycle_prompts():
        global prompt_box
        # This function gets a random prompt as described in prompts.py
        prompt_box.config(text=get_prompt())
        # This makes a recursive call to the function every 10 seconds
        prompt_box.after(10000, cycle_prompts)

    # Air this as a global variable so it can be destroyed by another window if we choose to go back
    global notepad_window
    notepad_window = tk.Tk()
    notepad_window.title(f"{user}: {note}") #Names the notepad

    # Another lambda, see lines 290-300
    back_button = tk.Button(notepad_window, text="<<", command=lambda:select_note(user))
    back_button.pack(side=tk.LEFT, anchor=tk.NW)

    # Scrollbar
    scrollbar = tk.Scrollbar(notepad_window, orient=tk.VERTICAL)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Use this to submit text into the database
    button = tk.Button(notepad_window, text="Save Note", command=get_text)
    button.pack()

    # The element that will hold the frame for the notes and corresponding hide buttons
    canvas = tk.Canvas(notepad_window, yscrollcommand=scrollbar.set)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    notepad_frame = tk.Frame(canvas)

    canvas.create_window((0, 0), window=notepad_frame, anchor="nw")
    canvas.config(yscrollcommand=scrollbar.set, scrollregion=canvas.bbox("all"))
    scrollbar.config(command=canvas.yview)

    # Vertical frame on the left-side margin that is used to hide corresponding notes
    # (turn the text white)
    global hide_button_frame
    hide_button_frame = tk.Frame(notepad_frame)
    hide_button_frame.pack(side=tk.LEFT, anchor="ne")

    chapterfont = ("Arial", 18)
    # Instantiate TBw/DT
    note_name = TextBoxWithDefaultText(notepad_frame, "Note Name", chapterfont, is_on_notepad=True)

    # Button for adding coupled note box and its title
    add_button = tk.Button(notepad_window, text="Add Text Boxes", command=lambda:add_text_boxes("Notes..."))
    add_button.pack(pady=5)

    # Same thing for bullet list box and its title
    bullet_button = tk.Button(notepad_window, text="Add Bulleted Points", command=lambda:add_text_boxes("Bulleted List..."))
    bullet_button.pack(pady=5)

    # This is where the prompt box can be toggled on and off
    toggle_prompts_button = tk.Button(notepad_window, text="Toggle Prompts", command=toggle_prompts)
    toggle_prompts_button.pack(pady=20)

    # Prompt box
    global prompt_box
    prompt_box = tk.Label(notepad_window, text=get_prompt(), width=20, wraplength=140, bg="yellow", borderwidth=3, relief="sunken")
    prompt_box.pack(pady=5)

    # Must be fired manually
    cycle_prompts()

    # This conditional is true if the database contains an existing record with the given note name
    # If this is the case, we need some special code to load them into new text boxes.
    if len(dicts):
        print("You are loading an EXISTING note")
        # There's only one title field, so we access that directly
        note_boxes[0].textbox.delete("1.0", tk.END)
        note_boxes[0].textbox.insert("1.0", note)

        # Right now, dicts contains strings that "look" like dictionaries. eval python-ifies them, turning them into
        # actual dictionaries.
        true_dicts = [eval(dicts[x]) for x in range(3)]
        print(true_dicts)

        # Will be needed for ascertaining if this is a note field or a bullet field
        note_keys = true_dicts[1].keys()
        for key in true_dicts[0]:
            # If there's a key match between the 0th and 1st dictionaries, that means we have a header
            # paired with a note field
            if key in note_keys:
                new_boxpair = add_text_boxes("Notes...")
                #               ^^^ this will return a tuple with two TBw/DT objects in it
                # So here we override the textbox text in those objects with whatever we got from the database
                new_boxpair[0].textbox.delete("1.0", tk.END)
                new_boxpair[0].textbox.insert("1.0", true_dicts[0][key])
                new_boxpair[1].textbox.delete("1.0", tk.END)
                new_boxpair[1].textbox.insert("1.0", true_dicts[1][key])
            else:
                # Exact same code, but with slight numeric/symantic adjustments for alternatively loading in a bullet
                # point field
                new_boxpair = add_text_boxes("Bullets...")
                #print(new_boxpair)
                new_boxpair[0].textbox.delete("1.0", tk.END)
                new_boxpair[0].textbox.insert("1.0", true_dicts[0][key])
                new_boxpair[1].textbox.delete("1.0", tk.END)
                new_boxpair[1].textbox.insert("1.0", true_dicts[2][key])

    # Run the window, at long last...
    notepad_window.mainloop()

if __name__ == "__main__":
    # If there's a config file, try to load it. The validation check will happen in select_user momentarily.
    print(abspath("config.txt"))
    if(isfile(abspath("config.txt"))):
        config_lines = config_handler.read_config()
        # Load the config file into our global variables
        port = config_lines[0]
        username = config_lines[1]
        password = config_lines[2]
        database = config_lines[3]
        # Move to user select
        select_user()
    else:
        # Without a config file, the program has no idea how to reach the mysql server.
        # So, make the user give us one!

        # setup_server will later make a call to select_user which will check for validation, so the mysql
        # validation check is functionally unavoidable
        setup_server("Admin")
