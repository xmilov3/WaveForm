import tkinter as tk
from tkinter import filedialog, messagebox
import librosa
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def analyze_song(file_path=None):
    try:
        if not file_path:
            root = tk.Tk()
            root.withdraw()
            
            file_path = filedialog.askopenfilename(
                title="Select a File to Analyze",
                filetypes=(
                    ("Audio Files", "*.mp3;*.wav;"),
                    ("All Files", "*.*")
                )
            )
            
            if not file_path:
                print("No file selected.")
                return None

        audio_data, sample_rate = librosa.load(file_path)
        
        tempo, _ = librosa.beat.beat_track(y=audio_data, sr=44100)
        tempo_float = float(tempo)
        tempo_rounded = round(tempo_float, 1)
        
        spectogram = librosa.amplitude_to_db(
            np.abs(librosa.stft(
                audio_data,
                n_fft=2048,
                hop_length=512,
                win_length=1024,
                window='hann'
            )), 
            ref=np.max)
        
        plot_window = tk.Toplevel()
        plot_window.title("Basic Audio Analysis Results")
        plot_window.geometry("1300x700")
        
        
        fig = Figure(figsize=(12, 7))
        ax = fig.add_subplot(111)
        
        img = librosa.display.specshow(
            spectogram, 
            x_axis='time', 
            y_axis='log', 
            sr=44100,
            hop_length=1024,
            fmin=20,
            fmax=20000,
            ax=ax)
        
        fig.suptitle(f'Tempo: {tempo_rounded:.1f} BPM')
        ax.set_title('Basic Spectrogram')
        fig.colorbar(img, ax=ax, format="%+2.f dB")
        
        fig.tight_layout(rect=[0, 0.03, 1, 0.95])
        
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