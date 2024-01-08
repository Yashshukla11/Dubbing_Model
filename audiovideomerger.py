from moviepy.editor import VideoFileClip, AudioFileClip

# Function to merge audio and video
def merge_audio_and_video(video_file, audio_file, output_file):
    try:
        
        video_clip = VideoFileClip(video_file)
        audio_clip = AudioFileClip(audio_file)
        
        # Set the audio of the video clip to the provided audio
        video_clip = video_clip.set_audio(audio_clip)

        # Write the merged video with audio to the output file
        video_clip.write_videofile(output_file, codec='libx264', audio_codec='aac')
        print("Video and audio merged successfully!")

    except Exception as e:
        print(f"Error merging video and audio: {str(e)}")

# Example usage
#merge_audio_and_video("input_video.mp4", "output.mp3", "finalvideo.mp4")
