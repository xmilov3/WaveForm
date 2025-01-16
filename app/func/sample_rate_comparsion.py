import tkinter as tk
from tkinter import filedialog, messagebox
import librosa
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def analyze_song_comparison(file_path=None):
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

        audio_data_22k, sr_22k = librosa.load(file_path, sr=22050)
        audio_data_44k, sr_44k = librosa.load(file_path, sr=44100)
        
        tempo_22k, _ = librosa.beat.beat_track(y=audio_data_22k, sr=sr_22k)
        tempo_44k, _ = librosa.beat.beat_track(y=audio_data_44k, sr=sr_44k)
        
        tempo_22k_rounded = float(tempo_22k)
        tempo_44k_rounded = float(tempo_44k)
        
        spectrogram_22k = librosa.amplitude_to_db(
            np.abs(librosa.stft(audio_data_22k, n_fft=4096, hop_length=1024)), 
            ref=np.max
        )
        spectrogram_44k = librosa.amplitude_to_db(
            np.abs(librosa.stft(
                audio_data_44k, 
                n_fft=8192, 
                hop_length=1024,
                win_length=4096,
                window='hann'
            )), 
            ref=np.max
        )
        
        plot_window = tk.Toplevel()
        plot_window.title("Spectrogram Comparison")
        plot_window.geometry("1600x900")
        
        fig = Figure(figsize=(18, 8))
        
        ax1 = fig.add_subplot(211)
        img1 = librosa.display.specshow(
            spectrogram_22k, 
            x_axis='time', 
            y_axis='log', 
            sr=22050,
            hop_length=1024,
            ax=ax1
        )
        ax1.set_title(f'Spectrogram (22050 Hz) - {tempo_22k_rounded:.1f} BPM')
        fig.colorbar(img1, ax=ax1, format="%+2.f dB")
        
        ax2 = fig.add_subplot(212)
        img2 = librosa.display.specshow(
            spectrogram_44k, 
            x_axis='time', 
            y_axis='log', 
            sr=44100,
            hop_length=1024,
            fmin=20,
            fmax=20000,
            ax=ax2
        )
        ax2.set_title(f'Spectrogram (44100 Hz) - {tempo_44k_rounded:.1f} BPM')
        fig.colorbar(img2, ax=ax2, format="%+2.f dB")
        
        fig.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, master=plot_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        print(f"Analyzed file: {file_path}")
        print(f"Sample rates compared: 22050 Hz vs 44100 Hz")
        print(f"BPM at 22050 Hz: {tempo_22k_rounded:.1f}")
        print(f"BPM at 44100 Hz: {tempo_44k_rounded:.1f}")
        
        return True
        
    except Exception as e:
        messagebox.showerror(
            "Error",
            f"An error occurred while analyzing the file:\n{str(e)}"
        )
        print(f"Error: {str(e)}")
        return None