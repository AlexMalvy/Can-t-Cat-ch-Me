from moviepy.editor import *
import pygame
from pygame.locals import QUIT, KEYDOWN

# opencv-python has to be installed !!!!!

# Class for playing video in a defined screen
class PlayedVideo:
    def __init__(self, screen, videoFileName, audioFileName):

        # Get clip
        video = VideoFileClip(videoFileName)
        #video.audio = AudioClip(audioFileName)

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

            # Calculate the new size to maintain the aspect ratio
            new_width = screen.get_width()
            new_height = int(video.h * (screen.get_width() / video.w))

            # Resize the frame to fit the screen
            resized_frame = pygame.transform.scale(pygame.surfarray.make_surface(frame.swapaxes(0, 1)), (new_width, new_height))
            
            # Calculate the position to center the video in the window
            x_offset = (screen.get_width() - new_width) // 2
            y_offset = (screen.get_height() - new_height) // 2

            # Blit the resized frame onto the Pygame window
            screen.blit(resized_frame, (x_offset, y_offset))

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

# # Create a Pygame window
# pygame.init()
# # Create screen
# pygame.display.set_caption("Video Preview")
# screen = pygame.display.set_mode((600, 480))
# # Play video
# PlayedVideo(screen, "test.mp4", "")
# # Quit game
# pygame.quit()