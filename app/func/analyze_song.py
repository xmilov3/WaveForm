import tkinter as tk
from tkinter import filedialog, messagebox
import librosa
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def analyze_song(file_path=None):
    try:
        # Open file dialog if no file path is provided
        if not file_path:
            root = tk.Tk()
            root.withdraw()
            
            file_path = filedialog.askopenfilename(
                title="Select a File to Analyze",
                filetypes=(
                    ("Audio Files", "*.mp3;*.wav;*.flac"),
                    ("All Files", "*.*")
                )
            )
            
            if not file_path:
                print("No file selected.")
                return None

        # Load audio file
        y, sr = librosa.load(file_path)
        
        # Count BPM
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
        tempo_float = float(tempo)
        tempo_rounded = round(tempo_float, 1)
        
        # Create a spectrogram
        D = librosa.amplitude_to_db(np.abs(librosa.stft(y)), ref=np.max)
        
        # Open a new window for the plot
        plot_window = tk.Toplevel()
        plot_window.title("Audio Analysis Results")
        plot_window.geometry("800x600")
        
        # Create a frame for the song info
        info_frame = tk.Frame(plot_window)
        info_frame.pack(pady=10)
        
        # Add song BPM Label
        bpm_label = tk.Label(info_frame, text=f"Tempo (BPM): {tempo_rounded}", font=('Arial', 12, 'bold'))
        bpm_label.pack()
        
        # Create a figure
        fig = Figure(figsize=(10, 6))
        ax = fig.add_subplot(111)
        
        # Draw the spectrogram
        img = librosa.display.specshow(D, x_axis='time', y_axis='log', ax=ax)
        ax.set_title('Spectrogram')
        fig.colorbar(img, ax=ax, format="%+2.f dB")
        
        # Add the plot to the window
        canvas = FigureCanvasTkAgg(fig, master=plot_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        print(f"Analyzed file: {file_path}")
        print(f"BPM: {tempo_rounded}")
        
        return tempo_rounded
        
    except Exception as e:
        messagebox.showerror(
            "Error",
            f"An error occurred while analyzing the file:\n{str(e)}"
        )
        print(f"Error: {str(e)}")
        return None

if __name__ == "__main__":
    analyze_song()