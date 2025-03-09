import os
import tkinter as tk
from tkinter import filedialog, Listbox, ttk
import pygame

class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Music Player")
        self.root.geometry("500x450")
        self.root.configure(bg="#282c34")
        
        pygame.mixer.init()
        self.playlist = []
        self.current_index = 0
        
        # UI Components
        self.label = tk.Label(root, text="No song loaded", wraplength=400, fg="white", bg="#282c34", font=("Arial", 12))
        self.label.pack(pady=10)
        
        self.playlist_box = Listbox(root, bg="#1e1e1e", fg="white", selectbackground="#ff9800", width=60, height=10)
        self.playlist_box.pack(pady=10)
        
        self.controls_frame = tk.Frame(root, bg="#282c34")
        self.controls_frame.pack(pady=10)
        
        self.load_button = tk.Button(self.controls_frame, text="Load Songs", command=self.load_songs, bg="#61afef", fg="white", font=("Arial", 10), padx=10)
        self.load_button.grid(row=0, column=0, padx=5)
        
        self.play_button = tk.Button(self.controls_frame, text="Play", command=self.play_song, bg="#98c379", fg="white", font=("Arial", 10), padx=10)
        self.play_button.grid(row=0, column=1, padx=5)
        
        self.pause_button = tk.Button(self.controls_frame, text="Pause/Resume", command=self.pause_song, bg="#e5c07b", fg="black", font=("Arial", 10), padx=10)
        self.pause_button.grid(row=0, column=2, padx=5)
        
        self.stop_button = tk.Button(self.controls_frame, text="Stop", command=self.stop_song, bg="#e06c75", fg="white", font=("Arial", 10), padx=10)
        self.stop_button.grid(row=0, column=3, padx=5)
        
        self.prev_button = tk.Button(self.controls_frame, text="Previous", command=self.previous_song, bg="#56b6c2", fg="white", font=("Arial", 10), padx=10)
        self.prev_button.grid(row=0, column=4, padx=5)
        
        self.next_button = tk.Button(self.controls_frame, text="Next", command=self.next_song, bg="#56b6c2", fg="white", font=("Arial", 10), padx=10)
        self.next_button.grid(row=0, column=5, padx=5)
        
        self.progress = ttk.Progressbar(root, orient=tk.HORIZONTAL, length=400, mode='determinate')
        self.progress.pack(pady=10)
        
        self.volume_scale = tk.Scale(root, from_=0, to=1, resolution=0.1, orient=tk.HORIZONTAL, command=self.set_volume, bg="#61afef", fg="white")
        self.volume_scale.set(0.5)
        self.volume_scale.pack(pady=10)
        
        self.update_progress()
        
    def load_songs(self):
        files = filedialog.askopenfilenames(filetypes=[("MP3 Files", "*.mp3")])
        if files:
            self.playlist = list(files)
            self.current_index = 0
            self.playlist_box.delete(0, tk.END)
            for song in self.playlist:
                self.playlist_box.insert(tk.END, os.path.basename(song))
            self.label.config(text=os.path.basename(self.playlist[self.current_index]))
    
    def play_song(self):
        if self.playlist:
            pygame.mixer.music.load(self.playlist[self.current_index])
            pygame.mixer.music.play()
            self.label.config(text=os.path.basename(self.playlist[self.current_index]))
            self.playlist_box.select_clear(0, tk.END)
            self.playlist_box.select_set(self.current_index)
    
    def pause_song(self):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.unpause()
    
    def stop_song(self):
        pygame.mixer.music.stop()
    
    def next_song(self):
        if self.playlist:
            self.current_index = (self.current_index + 1) % len(self.playlist)
            self.play_song()
    
    def previous_song(self):
        if self.playlist:
            self.current_index = (self.current_index - 1) % len(self.playlist)
            self.play_song()
    
    def set_volume(self, volume):
        pygame.mixer.music.set_volume(float(volume))
        
    def update_progress(self):
        if pygame.mixer.music.get_busy():
            self.progress.step(1)
        self.root.after(1000, self.update_progress)


if __name__ == "__main__":
    root = tk.Tk()
    app = MusicPlayer(root)
    root.mainloop()
