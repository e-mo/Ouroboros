import tkinter as tk
import time

class testclass(tk.Frame):

    def meow(self, event):
        print('meow')

def printstuff(event):
    print('stuff')

window = tk.Tk()
tc = testclass()
frame = tk.Frame(window, width=100, height=100)
text = tk.Text(width=100, height=100)
text.pack()
while True:
    try:
        window.update()
        time.sleep(0.02)
    except:
        break
