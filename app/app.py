from tkinter import *
import pygame
import os


def playsong():
    currentsong = playlist.get(ACTIVE)
    print(currentsong)
    pygame.mixer.music.load(currentsong)
    pygame.mixer.music.play()
def pausesong():
    pygame.mixer.music.pause()
def stopsong():
    pygame.mixer.music.stop()
def resumesong():
    pygame.mixer.music.unpause()
def changevolume(volume):
    pygame.mixer.music.set_volume(volume)
            
root = Tk()
img = PhotoImage(file='/Users/bartek/Desktop/Politechnika/Praca inżynierska/WaveForm/WaveForm/Pictures/Logo.png')
background = PhotoImage(file='/Users/bartek/Desktop/Politechnika/Praca inżynierska/WaveForm/WaveForm/Pictures/Background.png')
#favicon = PhotoImage(file='/Users/bartek/Desktop/Politechnika/Praca inżynierska/WaveForm/WaveForm/Pictures/favicon.ico')
root.iconphoto(False, img)
#root.wm_iconbitmap(False, favicon)

canvas=Canvas(root, width=500, height=400)
canvas.grid(row=0, column=0, columnspan=4, rowspan=2, sticky="nsew")
canvas_background = canvas.create_image(0, 0, image=background, anchor="nw")

root.title("WaveForm")
root.geometry("500x400")
root.iconbitmap("/Users/bartek/Desktop/Politechnika/Praca inżynierska/WaveForm/WaveForm/Pictures/favicon2.ico")
pygame.mixer.init()
pygame.mixer.init(channels=2)
playlist = Listbox(root,selectmode=SINGLE)
#playlist.grid(row=0, column=0, columnspan=4, sticky="nsew")
playlist_window = canvas.create_window(50,50, anchor="nw", window=playlist, width=400, height=100)
os.chdir('/Users/bartek/Desktop/Politechnika/Praca inżynierska/WaveForm/WaveForm/Music')
song = os.listdir()
for s in song:
    playlist.insert(END,s)
    
Button(root,width=10,text="play", command = playsong).grid(row=1, column=0, sticky="nsew")
Button(root,width=10,text="pause", command = pausesong).grid(row=1, column=1, sticky="nsew")
Button(root,width=10,text="stop", command = stopsong).grid(row=1, column=2, sticky="nsew")
Button(root,width=10,text="resume", command = resumesong).grid(row=1, column=3, sticky="nsew")

root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=0)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)
root.grid_columnconfigure(3, weight=1)

mainloop()