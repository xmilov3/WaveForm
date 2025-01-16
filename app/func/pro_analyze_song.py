import tkinter as tk
from tkinter import filedialog, messagebox
import librosa
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def pro_analyze_song(file_path=None):
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

        audio_data_temp, _ = librosa.load(file_path)
        temp_tempo, _ = librosa.beat.beat_track(y=audio_data_temp, sr=44100)

        if temp_tempo < 100:
            audio_data, sample_rate = librosa.load(file_path)
        else:
            audio_data, sample_rate = librosa.load(
                file_path, 
                sr=44100, 
                res_type='kaiser_best'
            )

        tempo, beat_frames = librosa.beat.beat_track(
            y=audio_data, 
            sr=44100,
            units='frames',
            tightness=100,
            trim=False,
            hop_length=512
        )

        if temp_tempo < 100 and tempo > 100:
            tempo = tempo / 2
        elif temp_tempo >= 100 and tempo < 100:
            tempo = tempo * 2

                
        beat_times = librosa.frames_to_time(beat_frames, sr=44100)
        tempo_rounded = round(float(tempo), 1)
        
        if temp_tempo < 100:
            audio_data, sample_rate = librosa.load(file_path)
            hop_length = 256
        else:
            audio_data, sample_rate = librosa.load(
                file_path, 
                sr=44100, 
                res_type='kaiser_best'
            )
            hop_length = 512

        
        spectogram = librosa.amplitude_to_db(
            np.abs(librosa.stft(
                audio_data,
                n_fft=8192,
                hop_length=hop_length,
                win_length=8192,
                window='blackmanharris',
                center=True,
                pad_mode='reflect'
            )), 
            ref=np.max,
            top_db=100
        )
        
        plot_window = tk.Toplevel()
        plot_window.title("Advanced Audio Analysis Results")
        plot_window.geometry("1300x700")
        
        fig = Figure(figsize=(12, 7))
        ax = fig.add_subplot(111)
        
        img = librosa.display.specshow(
            spectogram, 
            x_axis='time', 
            y_axis='log', 
            sr=44100,
            hop_length=512,
            fmin=20,
            fmax=20000,
            cmap='magma',
            ax=ax
        )
        
        ax.vlines(beat_times, 0, spectogram.shape[0], color='w', alpha=0.1, 
                 linestyle='--', label='Beats')
        
        fig.suptitle(f'Tempo: {tempo_rounded:.1f} BPM | Beat Frames: {len(beat_frames)}')
        ax.set_title('Advenced Spectrogram with Beat Detection')
        fig.colorbar(img, ax=ax, format="%+2.f dB")
        
        fig.tight_layout(rect=[0, 0.03, 1, 0.95])
        
        canvas = FigureCanvasTkAgg(fig, master=plot_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        print(f"Analyzed file: {file_path}")
        print(f"BPM: {tempo_rounded}")
        print(f"Number of detected beats: {len(beat_frames)}")
        print(f"Average time between beats: {np.mean(np.diff(beat_times)):.3f} seconds")
        
        return True
        
    except Exception as e:
        messagebox.showerror(
            "Error",
            f"An error occurred while analyzing the file:\n{str(e)}"
        )
        print(f"Error: {str(e)}")
        return None
if __name__ == "__main__":
    pro_analyze_song()