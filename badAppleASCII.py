import pywhatkit
import time
import vlc
import cv2
import os

#bad apple video file
badapple_mp4dir = "bad_apple.mp4"

#bad apple frame director
bad_apple_frames_dir = 'bad-apple-frames'


#if frame directory doesn't exist, create it
if not os.path.exists(bad_apple_frames_dir):
    os.makedirs(bad_apple_frames_dir)
#if frame directory doesn't have enough frames, create frames
if len(os.listdir(bad_apple_frames_dir)) < 6500:
    video = cv2.VideoCapture(badapple_mp4dir)
    count = 0
    while True:
        try:
            success, badapp_frame = video.read()
            cv2.imshow("badappframe", badapp_frame)
            frame_save_dir = os.path.join(bad_apple_frames_dir, "frame%s.jpg" % (count))
            cv2.imwrite(frame_save_dir, badapp_frame)
            count += 1
        except:
            break

#if frame directory doesn't have enough frames, create frames
bad_apple_frames = os.listdir(bad_apple_frames_dir)

fps = 30
spf = 1/fps
tot_time = 0
cortime = .003

#You might have to change this depending on the speed of your pc
video_start_offset = 0.14
frames_ps = []

#start up VLC player
badapp_vlc = vlc.Media(badapple_mp4dir)
vlc_player = vlc.MediaPlayer()
vlc_player.set_media(badapp_vlc)
vlc_player.audio_set_volume(70)
vlc_player.video_set_scale(0.65)
vlc_player.audio_set_delay(100)
vlc_player.play()

#give a time offset to sync vlc with text
time.sleep(video_start_offset)
global_start_time = time.time()
for i in range(len(bad_apple_frames)):
    tstart = time.time()
    full_path = os.path.join(bad_apple_frames_dir,'frame%s.jpg'%(i))
    text_file_name = 'frame%s.txt'%(i)
    pywhatkit.image_to_ascii_art(full_path, text_file_name)

    contents = open(text_file_name + '.txt')

    #this is a hack, but this made the text stop flickering
    os.system('dfdff\n')

    #print out the frame
    for w in contents:
        print(w.strip('\n'))
    contents.close()
    os.remove(text_file_name + '.txt')
    tend = time.time()
    runtime = tend-global_start_time
    current_fps = (i+1)/runtime
    frames_ps.append(current_fps)
    draw_time = tend-tstart

    # make frame speed corrections dependent on a global clock
    if current_fps < fps: sleep_time = spf - draw_time - cortime
    elif current_fps > fps: sleep_time = spf - draw_time + cortime

    if sleep_time < 0: continue
    else: time.sleep(sleep_time)


