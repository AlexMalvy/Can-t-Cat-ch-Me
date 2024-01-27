from moviepy.editor import *
from moviepy.video.fx.resize import resize
import pygame
from pygame.locals import QUIT, KEYDOWN

# opencv-python has to be installed !!!!!

# Class providing a videoclip from video file and audio file, resized to fit a related screen
class VideoClip:
    def __init__(self, screen, videoFileName, audioFileName):
        # Files importation
        rawClip = VideoFileClip(videoFileName)

        # Get duration
        self.duration = rawClip.duration

        # Get FPS
        self.fps = rawClip.fps

        # Get frame func
        self.get_frame = rawClip.get_frame

        # Get new dimensions values
        self.resizedWidth = screen.get_width()
        self.resizedHeight = screen.get_height()

        # Import the clip and resize to the window size
        self.clip = resize(rawClip, width=self.resizedWidth, height=self.resizedHeight)

""""""""""""""""""""""""""""""
# Class for playing video in a defined screen
class PlayedVideo:
    def __init__(self, surface, videoFileName, audioFileName):

        # Get clip
        video = VideoClip(surface, videoFileName, audioFileName)

        # Current time
        clock = pygame.time.Clock()

        # Video starting time
        start_time = pygame.time.get_ticks()

        # Playing flag
        playing = True

        # Video loop
        while playing:
            # Get the current time in milliseconds
            current_time = (pygame.time.get_ticks() - start_time) / 1000

            # Get the current frame
            frame = video.get_frame(pygame.time.get_ticks() / 1000)

            # Resize the frame to fit the screen
            resized_frame = pygame.transform.scale(pygame.surfarray.make_surface(frame.swapaxes(0, 1)), (video.resizedWidth, video.resizedHeight))

            # Blit the resized frame onto the Pygame window
            surface.blit(resized_frame, (0, 0))
            pygame.display.flip()

            # Control the frame rate
            clock.tick(video.fps)

            # Video ending
            if current_time > video.duration:
                playing = False

            # Other exit cases events handler
            for event in pygame.event.get():
                # Exit cases
                if event.type == QUIT:
                    playing = False
                elif event.type == KEYDOWN and event.key == pygame.K_SPACE:
                    playing = False
                elif event.type == KEYDOWN and event.key == pygame.K_ESCAPE:
                    playing = False
                else:
                    playing = True

"""""""""""""""""""""""""""""" 
# Tests part here

# Create a Pygame window
pygame.init()
# Create screen
pygame.display.set_caption("Video Preview")
screen = pygame.display.set_mode((600, 480))
# Play video
PlayedVideo(screen, "test.mp4", "")
# Quit game
pygame.quit()