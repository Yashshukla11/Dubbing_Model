from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import SRTFormatter
import pytube
from pytube.helpers import safe_filename
from tkinter.filedialog import *
import moviepy.editor
import speech_recognition as sr
from text_to_audio import *
from audiovideomerger import *
import tkinter as tk
from tkinter import ttk
from tkinter import font
import threading
from os import startfile
from googletrans import Translator
from sub import *
# Language code to language name mapping
language_names = {
    "en": "English",
    "ta": "Tamil",
    "bn": "Bengali",
    "mr": "Marathi",
    "hi": "Hindi",
    "gu": "Gujarati",
    "te": "Telugu",
    "ml": "Malayalam",
    "kn": "Kannada",
    "ur": "Urdu"
}

# Create a custom Entry widget with rounded corners
class RoundedEntry(tk.Entry):
    def __init__(self, master=None, **kwargs):
        tk.Entry.__init__(self, master, **kwargs)
        self.config(relief=tk.FLAT)
        self.bind("<FocusIn>", self.on_focus_in)
        self.bind("<FocusOut>", self.on_focus_out)
        self.rounded = False
        self.update_shape()

    def on_focus_in(self, event):
        self.rounded = True
        self.update_shape()

    def on_focus_out(self, event):
        self.rounded = False
        self.update_shape()

    def update_shape(self):
        if self.rounded:
            self.configure({"relief": "flat", "borderwidth": 1.5})
            self.config(bg="#5470b3")
        else:
            bg_color = self.master.cget("bg")
            if bg_color:
                self.config(bg=bg_color)
            else:
                self.config(bg="white")

# Create a canvas with a gradient background
class GradientCanvas(tk.Canvas):
    def __init__(self, master=None, **kwargs):
        tk.Canvas.__init__(self, master, **kwargs)
        self.bind("<Configure>", self.draw_gradient)

    def draw_gradient(self, event):
        width = self.winfo_width()
        height = self.winfo_height()
        gradient = tk.PhotoImage(width=width, height=height)

        for y in range(height):
            color = interpolate_colors("#0922de", "#7193eb", y / height)
            gradient.put("{" + " ".join(color for _ in range(width)) + "} ", to=(0, y))

        self.create_image(0, 0, anchor="nw", image=gradient)
        self.image = gradient

def interpolate_colors(color1, color2, weight):
    r1, g1, b1 = int(color1[1:3], 16), int(color1[3:5], 16), int(color1[5:7], 16)
    r2, g2, b2 = int(color2[1:3], 16), int(color2[3:5], 16), int(color2[5:7], 16)

    r = int(r1 * (1 - weight) + r2 * weight)
    g = int(g1 * (1 - weight) + g2 * weight)
    b = int(b1 * (1 - weight) + b2 * weight)

    return f"#{r:02X}{g:02X}{b:02X}"


def func():
    progress_bar.place(relx=0.5, rely=0.65, anchor="center")
    url = youtube_entry.get()
    langk = list(language_names.keys())
    langv = list(language_names.values())
    index=langv.index(language_var.get())
    lang = langk[index]
    sep = 'channel'
    urlshrt = url.split(sep,1)[0]
    urlshrt = urlshrt[32:-1]
    my_video = pytube.YouTube(url)
    my_video = my_video.streams.get_highest_resolution()
    my_video.download('Downloads')
    input_video="Downloads/" + safe_filename(my_video.title)+".mp4"
    text_file = "subtitles\\"+ urlshrt+".txt"
    video = moviepy.editor.VideoFileClip(input_video)
    
    try:
        srt = YouTubeTranscriptApi.get_transcript(urlshrt)
        text = ""
        with open(text_file, "w") as file:
            for i in srt:
                text += i["text"] + "\n"    
            file.write(text)
        formatter = SRTFormatter()
        srt_formatted = formatter.format_transcript(srt)
        with open("subtitles\\" + urlshrt+".srt", 'w', encoding='utf-8') as srt_file:
            srt_file.write(srt_formatted)
        with open("subtitles\\" + urlshrt+".srt", 'r', encoding='utf-8') as file:
            srt_contents = file.read()
        # Initialize the translator
        translator = Translator()
        # Translate the English subtitles to Hindi
        translated_srt = translator.translate(srt_contents, src='en', dest=lang)
        # Save the translated SRT to a new file
        with open("subtitles\\" + urlshrt+lang+".srt", 'w', encoding='utf-8') as file:
            file.write(translated_srt.text)
        progress_bar['value']=15            
    except:
        audio = video.audio
        audio.write_audiofile("audio\\"+my_video.title+".wav")
        sound = ("audio\\" + my_video.title+".wav")
        rec = sr.Recognizer()
        with sr.AudioFile(sound) as source:
            audio=rec.listen(source)
            try:
                text = rec.recognize_google(audio)
                with open("subtitles\\" + urlshrt+".txt" , "w") as  file:
                    file.write(text)
            except:
                print("Sorry couldn't hear that")
    progress_bar['value'] = 25
    progress_bar['value']=30
    convert_text_to_target_language(text_file,lang, text_file[:-4]+lang+".txt")
    progress_bar['value']=40
    convert_text_file_to_audio(text_file[:-4]+lang+".txt" , lang,"audio/" + my_video.title+language_var.get()+".mp3")
    progress_bar['value']=60
    merge_audio_and_video(input_video,"audio\\" + my_video.title+language_var.get()+".mp3","final\\"+my_video.title+language_var.get()+"final.mp4")
    progress_bar['value']=70
    video = VideoFileClip("final\\"+my_video.title+language_var.get()+"final.mp4")
    subtitles = pysrt.open("subtitles\\" + urlshrt+lang+".srt")
    # Extract the filename without the extension
    output_video_file = "final\\"+my_video.title+language_var.get()+ '_subtitled.mp4' 
    # Create subtitle clips
    subtitle_clips = create_subtitle_clips(subtitles, video.size,language_var.get())
    # Add subtitles to the video
    final_video = CompositeVideoClip([video] + subtitle_clips)
    # Write output video file
    final_video.write_videofile(output_video_file)
    progress_bar['value']=100 
    global path
    path = output_video_file
    play()
def play():
    progress_bar.place(relx=-1, rely=-1, anchor="center")
    play_button = tk.Button(widget_frame, text="PLAY ▸", command=threading.Thread(target=openvid).start, width=70,bg="green")
    play_button.grid(row=2, column=0, columnspan=2, pady=0)
    play_button['font'] = font.Font(size=25)
def openvid():
    startfile(path)
    root.destroy()
    quit()
# Create the main window
root = tk.Tk()
'''root.attributes('-fullscreen', True)  # Enable full screen'''
root.state("zoomed")
root.title("YouTube Dubbing Tool")


# Create a gradient canvas as the background
gradient_bg = GradientCanvas(root)
gradient_bg.place(relx=0.5, rely=0.5, anchor="center", relwidth=1, relheight=1)
gradient_bg.pack

# Load the raw.png image
raw_image = tk.PhotoImage(file="img\\x.png", height=100, width=100)


# Create a label for the image and place it on the canvas
raw_label = tk.Label(gradient_bg, image=raw_image)
raw_label.image = raw_image  # Keep a reference to prevent garbage collection
raw_label.place(relx=0.01, rely=0.02, anchor="nw")
raw_label.pack

# Create a frame for other widgets (buttons, labels, entry)
widget_frame = tk.Frame(root, bg="#d4e4fa", bd=100)
widget_frame.place(relx=0.5, rely=0.5, anchor="center")
widget_frame.pack


# Create a label and entry for the YouTube link
label_font_a = font.Font(size=30)
youtube_label = tk.Label(widget_frame, text="Enter YouTube URL:", font=label_font_a, bg="#84a0e3")
youtube_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
youtube_label.pack

# Create a custom rounded entry widget
youtube_entry = RoundedEntry(widget_frame, justify="center", font=("Helvetica", 20), insertbackground="#5470b3")
youtube_entry.grid(row=0, column=1, padx=10, pady=10)
youtube_entry.pack

# Create a label and dropdown for selecting the target language
label_font_b = font.Font(size=30)
language_label = tk.Label(widget_frame, text="Select Target Language:", font=label_font_b , bg="#84a0e3")
language_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
language_label.pack

language_var = tk.StringVar()
language_dropdown = tk.OptionMenu(widget_frame, language_var, *language_names.values())
language_dropdown.grid(row=1, column=1, padx=5, pady=10)
language_dropdown.pack

# Create a button to trigger the dubbing process
convert_button_font = font.Font(size = 20)
convert_button = tk.Button(widget_frame, text="Convert", command=threading.Thread(target=func).start, width=10, bg="#5470b3",font = convert_button_font)
convert_button.grid(row=2, column=0, columnspan=2, pady=20)
convert_button.pack 

# Create a heading frame
heading_frame = tk.Frame(root, bg="#d4e4fa", bd=0 )
heading_frame.place(relx=0.5, rely=0.1, anchor="n")
heading_frame.pack

# Create a label for the heading
heading_label_font = font.Font(size=40, weight="bold")
heading_label = tk.Label(heading_frame, text="Video Dubber", font=heading_label_font, fg="black", bg="#d4e4fa")
heading_label.pack()

# Load and place the "b.png" image to the right-hand top corner
b_image = tk.PhotoImage(file="img\\b.png")
b_label = tk.Label(root, image=b_image)
b_label.image = b_image
b_label.place(relx=0.99, rely=0.02, anchor="ne")
b_label.pack



# Create a transparent progress bar

progress_bar = ttk.Progressbar(root, orient="horizontal", length=500, mode="determinate", style="TProgressbar")
style = ttk.Style()
style.layout("TProgressbar",
             [("Horizontal.Progressbar.trough", {"children":
                 [("Horizontal.Progressbar.pbar", {"side": "left", "sticky": "ns"})],
                 "sticky": "nswe"})])
style.configure("TProgressbar",
                troughcolor="red",
                troughrelief="flat",
                pbarrelief="flat",
                backgroundcolor = "black",
                foregroundcolor = "#2b2b2c"
                )

progress_bar.place(relx=-1, rely=-1, anchor="center") # Center-align the progress bar
root.mainloop()

