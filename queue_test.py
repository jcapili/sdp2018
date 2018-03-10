# python3 source code
from tkinter import *
from tkinter.ttk import *
import threading
import time
import queue


root = Tk()
msg = StringVar()
Label(root, textvariable=msg).pack()

# This is our own event queue, each element should be in this form:
# (function_to_be_called_from_gui_thread, function_arguments)
# In python, functions are objects and can be put in a queue.
my_event_queue = queue.Queue()


def worker():
    """
    This is a time consuming worker, it takes 1 second for each task.
    If you put such a worker in the GUI thread, the GUI will be blocked.
    """
    task_counter = 0
    while True:
        time.sleep(1)  # simulate a time consuming task

        # show how many tasks finished in the Label. We put this action in my_event_queue instead of handle
        # it from this worker thread which is not safe. This action will be handled by my_event_handler which is
        # called from GUI thread.
        my_event_queue.put((msg.set, '{} tasks finished.'.format(task_counter)))
        task_counter += 1


def my_event_handler():
    """
    Query my_event_queue, and handle one event per time.
    """
    try:
        func, *args = my_event_queue.get(block=False)
    except queue.Empty:
        pass
    else:
        func(*args)

    # At last schedule handling for next time.
    # Every 100 ms, my_event_handler will be called
    root.after(100, my_event_handler)


threading.Thread(target=worker, daemon=True).start()  # start worker in new thread

my_event_handler()  # start handler, after root.mainloop(), this method will be called every 100ms. Or you can use root.after(100, my_event_handler)

root.mainloop()