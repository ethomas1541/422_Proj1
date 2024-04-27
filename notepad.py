# note_gui.py
import tkinter as tk
from tkinter import messagebox
from testdatabase import ensure_database_exists, ensure_table_exists, connect_to_database, fetch_users, fetch_notes, save_or_update_note

# Database credentials
HOST = 'ix.cs.uoregon.edu'
USER = 'dtweedale'
PASSWORD = 'password'
DATABASE = 'Notes'
PORT = 3854

connection = ensure_database_exists(HOST, USER, PASSWORD, DATABASE, PORT)

def select_user():
    global user_select_window
    user_select_window = tk.Tk()
    user_select_window.title("User Selection")

    users = fetch_users(connection)

    listbox = tk.Listbox(user_select_window, selectmode=tk.SINGLE)
    for user in users:
        listbox.insert(tk.END, user)
    listbox.pack()

    def get_selection():
        selection_index = listbox.curselection()
        if selection_index:
            selected_user = listbox.get(selection_index[0])
            user_select_window.destroy()
            select_note(selected_user)

    button = tk.Button(user_select_window, text="Select User", command=get_selection)
    button.pack()
    user_select_window.mainloop()

def select_note(user):
    ensure_table_exists(connection, user)
    note_select_window = tk.Tk()
    note_select_window.title(f"Select Note for {user}")

    notes = fetch_notes(connection, user)
    listbox = tk.Listbox(note_select_window, selectmode=tk.SINGLE)
    for note in notes:
        listbox.insert(tk.END, note)
    listbox.insert(tk.END, "Create New Note")
    listbox.pack()

    def get_selection():
        selection_index = listbox.curselection()
        if selection_index:
            selected_note = listbox.get(selection_index[0])
            if selected_note == "Create New Note":
                selected_note = ""  # Create a new note entry
            note_select_window.destroy()
            open_notepad(user, selected_note)

    button = tk.Button(note_select_window, text="Select Note", command=get_selection)
    button.pack()
    note_select_window.mainloop()

def open_notepad(user, note_name):
    notepad_window = tk.Tk()
    notepad_window.title(f"{user}: {note_name}")

    subject_label = tk.Label(notepad_window, text="Subject:")
    subject_label.pack()
    subject_entry = tk.Entry(notepad_window)
    subject_entry.pack()

    text_box = tk.Text(notepad_window, width=80, height=20)
    text_box.pack(padx=10, pady=10)

    # Load existing note
    if note_name:
        notes = fetch_notes(connection, user)
        if note_name in notes:
            cursor = connection.cursor()
            cursor.execute(f"SELECT note, subject FROM {user} WHERE note_name = %s", (note_name,))
            note_text, note_subject = cursor.fetchone()
            if note_text:
                text_box.insert(tk.END, note_text)
            if note_subject:
                subject_entry.insert(tk.END, note_subject)
            cursor.close()

    def save_note():
        text = text_box.get("1.0", tk.END)
        subject = subject_entry.get()  # Get subject from entry field
        save_or_update_note(connection, user, note_name, subject, text)
        messagebox.showinfo("Save", "Your note has been saved successfully!")
        notepad_window.destroy()
        select_note(user)

    button = tk.Button(notepad_window, text="Save Note", command=save_note)
    button.pack()

    notepad_window.mainloop()

if __name__ == "__main__":
    select_user()
