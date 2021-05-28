import cv2
import numpy as np

from char import ASCII_CHARS

import time
import os , sys , cursor

# Video_Path 、 ASCII_Code
class Source:
    def __init__(self):
        self.video_path = 'BadApple.mp4'
        self.ASCII_Codes = [" ", "0", "1", "2", "3", "4", "5", "6", "7", "8" , "9"]

# Information of each frame , and Transformer
class Ascii_Frame:
    def __init__(self , number , frame , source):
        self.number = number # Frame number
        self.frame  = frame  # CV2 object
        self.source = source # Source Class
        
        self.text = []       # list[string]
        self.Transform()     # Start Transform

    # Transform process
    def Transform(self):
        img  = self.Resized(self.frame)
        img  = self.Grayscale(img)
        self.Frame_To_Ascii(img) 

    # To resize , we set it to 92 * 62
    # Because we don't want the edge
    # So the result will be 90 * 60
    def Resized(self , frame):
        return cv2.resize(frame , (92 , 62) , interpolation = cv2.INTER_NEAREST)

    # From 3 Channels to 1 Channel (Grayscale) 
    def Grayscale(self , frame):
        return cv2.cvtColor(frame , cv2.COLOR_BGR2GRAY)

    # Generate Text
    def Frame_To_Ascii(self , frame):
        #Since we don't wnat the edge , so we start from 1 to end - 1
        characters = ''
        for j in range(1 , 62 - 1):     # Up   to Down : Height
            for i in range(1 , 92 - 1): # Left to Right : Width
                pixel = frame[j][i]
                # Map each pixel to a certain ASCII_CODE
                characters += self.source.ASCII_Codes[pixel // 25]

            self.text.append(characters) # Text is a list of string
            characters = ''              # Reset the string     

# Information of Original Video
class Video:
    def __init__(self , source):
        self.capture = cv2.VideoCapture(source.video_path) # Open the Video

        self.total_frames = int(self.capture.get(cv2.CAP_PROP_FRAME_COUNT)) # Get total Frame count
        self.FPS = self.capture.get(cv2.CAP_PROP_FPS) # Get FPS

        self.source = source # Source Class
        self.Frame_LIST = [] # list[ list[string] ] : We append ASCII_Frame.text into it

    # Extract each frames
    def Extract_Frames(self):
        # For Test, We don't use it though
        # self.total_frames = int(input('How many frames do you want? (All {})\nFrames: '.format(int(self.total_frames))))
        
        current_frame = 1

        print('\nExtracting Video...')
        start = time.time()

        while(current_frame <= self.total_frames):
            ret , frame = self.capture.read()

            if ret != True:
                break

            # Turn each frame to ASCII_Frame Object
            frame = Ascii_Frame(current_frame , frame , self.source)

            # Append ASCII_Frame.text to Frame_List
            self.Frame_LIST.append(frame.text)

            # Show the progress
            self.progress_bar(current_frame , self.total_frames)

            current_frame += 1

        end = time.time()
        # Show the time we spend , and release the Video
        print('\nSpend :' , int((end-start) // 60) , 'm' , int((end-start) % 60) , 's')
        self.capture.release()

    # Generate Ascii Video !!! The video is video only !!!
    def Generate_Ascii_Video(self):
        # Set resolution 1440 * 1080
        width , height = 1440 , 1080
        img = np.zeros((height , width) , np.uint8)

        # Create a Video
        out = cv2.VideoWriter(
            'Bad Apple Ascii.mp4' , 
            cv2.VideoWriter_fourcc(*'mp4v') , 
            self.FPS , 
            (width , height), 
            False)

        print('\nMaking Video...')
        start = time.time()

        # Start write Frames into the Video
        for current_frame in range(self.total_frames):
            self.put_char(img , current_frame)
            out.write(img)

            self.progress_bar(current_frame + 1 , self.total_frames) 

        end = time.time()

        print('\nSpend :' , int((end-start) // 60) , 'm' , int((end-start) % 60) , 's')
        out.release()

    # Put on Ascii
    def put_char(self , img , index):
        # I have no idea how to make it better 
        # Please tell if we have any idea
        # How can I put the ASCII on the img ????

        text = self.Frame_LIST[index]
        img.fill(0)

        # We have 90 * 60 chars, if the char is space then we pass
        for height in range(0 , 60):
            for width in range(0 , 90):
                if text[height][width] != ' ':
                    Char = ASCII_CHARS[int(text[height][width])] # Get the char form the code
                    self.draw_char(Char , img , height , width)

    # Draw the Char on the image
    def draw_char(self , char , img , height , width):
        for x in range(0 , 16):
            for y in range(0 , 16):
                if char[x][y] == 1:
                    img[height * 18 + x][width * 16 + y] = 255

    # The Progress
    def progress_bar(self , current , total , barLength = 25):
        progress = float(current) * 100 / total
        arrow = '▇' * int(progress / 100 * barLength - 1)
        spaces = ' ' * (barLength - len(arrow))
        sys.stdout.write('\rProgress: [%s%s] %d%% Frame %d of %d frames' % (arrow, spaces, progress, current, total))
   
# Extract then Generate
def Generate_Ascii_Video():
    source = Source()
    video  = Video(source)

    cursor.hide() # 隱藏游標
    video.Extract_Frames()
    video.Generate_Ascii_Video()
    cursor.show() # 顯示回來

# Choose Mode
def main():
    os.system('cls')
    print('Hi,')
    print('Choose A Mode')
    print('\n==========================================')
    print('(1) Generate Ascii Video')
    print('(2) Exit')
    print('==========================================\n')

    # Mode : Generate or Exit
    mode = input('Slect: ')
    if mode == '1':
        Generate_Ascii_Video()
    elif mode == '2':
        pass
    else:
        print('You Shall Not Pass')

    print('\nFinished')
    print('Have A Good Day :)')
    print('See You Next Time\n')

if __name__ == '__main__':
    main()            
