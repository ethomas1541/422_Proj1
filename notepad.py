import tkinter as tk


# Makes a Tkinter window
window = tk.Tk()
window.title("Notes")

# Creates the textbox and puts it in the window
textbox = tk.Text(window, width=40, height=30)
textbox.pack()  #adds box to window

# Returns the text thats in the textbox to console probably unnecessary
def get_text():
    text = textbox.get("1.0", "end-1c")
    print("Text entered:")
    print(text)

#Creates and adds button that calls get_text
button = tk.Button(window, text="Get Text", command=get_text)
button.pack()

#Runs the program
window.mainloop()
