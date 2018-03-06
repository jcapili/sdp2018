from tkinter import *
import os
import threading

# Create Tk window
window = Tk()

# Add text to the window via a label
label = Label(window, text="Hello World")
label.pack() # Make the label visible

top = Frame(window)
top.pack()
bottom = Frame(window)
bottom.pack(side=BOTTOM)

#   Separate imports for server because mutual imports are bad according to the Internet
def start_eeg():
    import server
    server.begin_server()

#   Separate imports for server because mutual imports are bad according to the Internet
def stop_eeg():
    import server
    server.end_server()


# Put the window in a loop so that it doesn't just open, print the label, and then close
def main():
    # use lambdas so the command functions don't run on button initialization
    button1 = Button(top, text="Start EEG data", fg="red", command=lambda : start_eeg())
    button2 = Button(bottom, text="Stop EEG data", fg="green", command=lambda : stop_eeg())

    button1.pack()
    button2.pack()
    
    window.mainloop()
