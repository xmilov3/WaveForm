from tkinter import *
import pygame
#import os

# Manipulate song functions
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
    
#def changevolume(volume):
    #pygame.mixer.music.set_volume(volume)
    
# Main window            
root = Tk()
root.title("WaveForm")
root.geometry("1500x1000")
root.configure(bg='#1E052A')


# Background and icon images
img = PhotoImage(file='/Users/bartek/Desktop/Politechnika/Praca inżynierska/WaveForm/WaveForm/Pictures/Logo.png')
logo_top = PhotoImage(file='/Users/bartek/Desktop/Politechnika/Praca inżynierska/WaveForm/WaveForm/Pictures/TopLogo.png')

root.iconphoto(False, img)
#background = PhotoImage(file='/Users/bartek/Desktop/Politechnika/Praca inżynierska/WaveForm/WaveForm/Pictures/Background.png')

# Background with canvas
#canvas=Canvas(root, width=500, height=400)
#canvas.grid(row=0, column=0, columnspan=4, rowspan=2, sticky="nsew")
#canvas_background = canvas.create_image(0, 0, image=background, anchor="nw")

# Initiate pygame mixer
pygame.mixer.init()
pygame.mixer.init(channels=2)
playlist = Listbox(root,selectmode=SINGLE)
#playlist_window = canvas.create_window(50,50, anchor="nw", window=playlist, width=400, height=100)

# Catalog with music
#os.chdir('/Users/bartek/Desktop/Politechnika/Praca inżynierska/WaveForm/WaveForm/Music')
#song = os.listdir()
#for s in song:
    #playlist.insert(END,s)
    
# Panels
# Main pannel
main_frame = Frame(root, bg='black')
main_frame.grid(row=0, column=0, sticky='nsew')
# Grid settings
#main_frame.grid_rowconfigure(0, weight=1)
main_frame.grid_rowconfigure(1, weight=1)
main_frame.grid_rowconfigure(2, weight=0)
main_frame.grid_columnconfigure(0, weight=1)
main_frame.grid_columnconfigure(1, weight=3)
main_frame.grid_columnconfigure(2, weight=1)
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
# Top pannel
top_frame = Frame(main_frame, bg='#1E052A')
top_frame.grid(row=0, column=0, columnspan=3, sticky='ew')

logo_label = Label(top_frame, image=logo_top, bg='#1E052A')
logo_label.grid(row=0, column=1, sticky='e', padx=10, pady=5)
Label(top_frame, bg='#1E052A').grid(row=0, column=0, sticky='w')
top_frame.grid_columnconfigure(0, weight=1)
#image.place(relx=1.0, rely=0.5, anchor='ne')

#image_label = root.Label(root, img)
#image_label.pack()

#Left pannel
left_frame = Frame(main_frame, bg='#240745')
left_frame.grid(row=1, column=0, sticky='nsew', padx=10, pady=10)

Label(left_frame, text="Playlists", font=("Arial", 14), fg='white', bg='#240745').pack(pady=5)
playlist1 = Button(left_frame, text="Liked songs", width=20, height=2, bg='#3A0C60', fg='white')
playlist1.pack(pady=5)
playlist2 = Button(left_frame, text="UK Dubstep", width=20, height=2, bg='#3A0C60', fg='white')
playlist2.pack(pady=5)

# Mid pannel
middle_frame = Frame(main_frame, bg='#3C0F64')
middle_frame.grid(row=1, column=1, sticky='nsew', padx=10, pady=10)

Label(middle_frame, text='Playlist: UK Bassline', font=("Arial", 14), fg='white', bg='#3C0F64').pack(pady=10)
playlist = Listbox(middle_frame, selectmode=SINGLE, bg='#1E052A', fg='white', height=15, width=40)
playlist.pack(padx=10, pady=10)
# Now songs are static, in future they will be dynamic
for song in ["Gimmie More", "Bandman Sound", "Really Tight"]:
    playlist.insert(END, song)
    
# Right pannel
right_frame = Frame(main_frame, bg='#3A0C60')
right_frame.grid(row=1, column=2, sticky='nsew', padx=10, pady=10)

Label(right_frame, text="Now Playing", font=("Arial", 14), fg='white', bg='#3A0C60').pack(pady=5)
now_playing_label = Label(right_frame, text="Gimmie More - Distinkt", font=("Arial", 12), fg='white', bg='#3A0C60')
now_playing_label.pack(pady=5)

#  Bottom pannel
bottom_frame = Frame(main_frame, bg='#1E052A')
bottom_frame.grid(row=2, column=0, columnspan=3, sticky='ew')

# Bottom pannel Buttons    
Button(bottom_frame, text="Play", width=10, command=playsong, bg='#6A1B9A', fg='white').pack(side=LEFT, padx=10, pady=10)
Button(bottom_frame, text="Pause", width=10, command=pausesong, bg='#6A1B9A', fg='white').pack(side=LEFT, padx=10, pady=10)
Button(bottom_frame, text="Stop", width=10, command=stopsong, bg='#6A1B9A', fg='white').pack(side=LEFT, padx=10, pady=10)
Button(bottom_frame, text="Resume", width=10, command=resumesong, bg='#6A1B9A', fg='white').pack(side=LEFT, padx=10, pady=10)



root.mainloop()