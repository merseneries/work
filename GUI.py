from tkinter import *

root = Tk()

entry_1 = Entry(width=20)
button_1 = Button(text='Press me', width=20, height=4, bg='yellow', activebackground='red', borderwidth=3)
label_1 = Text(bg='orange', fg='black', width=20, height=5)


def reverse_number(event):
    result = int(entry_1.get())
    result = [i for i in range(0, result)]
    label_1.insert(1.0, result)


button_1.bind('<Button>', reverse_number)

entry_1.pack(expand=1)
button_1.pack(expand=1)
label_1.pack(expand=1, fill=X)

root.mainloop()
