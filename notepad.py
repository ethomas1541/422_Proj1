import tkinter as tk
import db

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

#Opens the notepad
def open_notepad(user):
    window.destroy()

    # Makes a Tkinter window
    notepad_window = tk.Tk()
    notepad_window.title(f"{user} Notes") #Names the notepad

    # Creates the textbox and puts it in the window
    textbox = tk.Text(notepad_window, width=40, height=30)
    textbox.pack()  #adds box to window

    # Returns the text thats in the textbox to console probably unnecessary
    def get_text():
        text = textbox.get("1.0", "end-1c")
        print("Text entered:")
        db.save(text)
        print(text)
        db.load()

    #Creates and adds button that calls get_text
    button = tk.Button(notepad_window, text="Get Text", command=get_text)
    button.pack()

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