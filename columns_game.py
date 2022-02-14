# Derek Naing 70307889

# NOTE: There is a lot of input lag for keys so it only moves
#       if holding down spacebar or right arrow or left arrow


import pygame
import columns
import random

HEIGHT = 500
WIDTH = 800
FRAME_RATE = 120
BACKGROUND_COLOR = pygame.Color(0, 0, 0) 
BOARD_ROWS = 13
BOARD_COLUMNS = 6


class ColumnsGame:
    """Class for the columns game view."""

    def __init__(self) -> None:
        """Initializes attributes needed."""

        self._running = True
        self._state = columns.GameState()
        self._x_counter = 0
        self._y_counter = 0

    def run(self) -> None:
        """Runs the columns game."""
        
        pygame.init()
        clock = pygame.time.Clock()
        MS = pygame.USEREVENT
        pygame.time.set_timer(MS,200)
        try:
            self._make_screen((WIDTH, HEIGHT))
            w, h = pygame.display.get_surface().get_size() 
            self.x = int(w / 2.5)
            self.y = int(h / 18.571)


            self._background = pygame.image.load('C:/Users/derek/OneDrive/Documents/Python Projects/Columns/anakin_v_obiwan.jpg') # 39 KB


            self._drop_sound = pygame.mixer.Sound('C:/Users/derek/OneDrive/Documents/Python Projects/Columns/arrow.wav')          # 82 KB
            self._land_sound = pygame.mixer.Sound('C:/Users/derek/OneDrive/Documents/Python Projects/Columns/drop.wav')           # 57 KB
            self._match_sound = pygame.mixer.Sound('C:/Users/derek/OneDrive/Documents/Python Projects/Columns/lightsaber.wav')    # 67 KB

                                                                        # Total: 245 KB                                                                  

            while self._running:
                
                if self._state.game_ended == True:
                    print('GAME OVER')
                    self._finish_game()
                else:
                    clock.tick(FRAME_RATE)
                    self._handle_events(MS)
                    self._draw_frame()

        except (GameOver):
            print('GAME OVER')

        finally:
            pygame.quit()

    def _handle_events(self, MS) -> None:
        """Handles all game events in columns."""
        
        for event in pygame.event.get():

            if event.type == pygame.VIDEORESIZE:
                self._make_screen(event.size)

            elif event.type == pygame.QUIT:
                self._finish_game()


            if self._state.faller_exists == False:
                self._column, self._first, self._second, self._third = self._randomize()
                self._state.create_faller(self._column, self._first, self._second, self._third)

            if event.type == MS and self._state.faller_exists == True:
                
                keys = pygame.key.get_pressed()

                if keys[pygame.K_RIGHT]:
                    self._state.move_right(self._column, self._first, self._second, self._third)

                if keys[pygame.K_LEFT]:
                    self._state.move_left(self._column, self._first, self._second, self._third)

                if keys[pygame.K_SPACE]:
                    self._first, self._second, self._third = self._state.rotate(self._column, self._first, self._second, self._third)


                self._state.drop(self._column, self._first, self._second, self._third)
                self._drop_sound.play()

    def _randomize(self) -> None:
        """Randomizes the jewels in each faller and also the column that it drops."""
        
        jewels = ['S', 'T', 'V', 'W', 'X', 'Y', 'Z']
        column = random.randrange(1, 7)
        first = random.choice(jewels)
        second = random.choice(jewels)
        third = random.choice(jewels)

        return column, first, second, third       

    def _make_screen(self, size) -> None:
        """Makes the window screen for the game."""
        
        self._screen = pygame.display.set_mode(size, pygame.RESIZABLE)
        self._scaled_background = None

    def _finish_game(self) -> None:
        """Ends game."""
        
        self._running = False

    def _draw_frame(self) -> None:
        """Draws the frame that is being considered."""

        self._draw_background()
        self._draw_column_background()
        self._draw_game_state()
        pygame.display.update()
        pygame.display.flip()

    def _draw_background(self) -> None:
        """Draws the columns game background which is the Anakin vs Obiwan picture."""
        
        if self._scaled_background == None:
            w, h = pygame.display.get_surface().get_size()
            self._scaled_background = pygame.transform.scale(self._background, (w, h))

        self._screen.blit(self._scaled_background, (0, 0))

    def _draw_game_state(self) -> None:
        """Looks at the gamestate of columns and draws the appropriate graphic version of it."""
        
        for j in range(len(self._state.game)):
            for i in range(1, len(self._state.game[j]), 3):
                    
                if self._state.game[j][i] == '':

                    if self._state.game[j][i - 1] == '*' and self._state.game[j][i + 1] == '*':
                        pass

                    else:
                        self._draw_cell('EMPTY')
                        

                elif self._state.game[j][i] == 'S':

                    if self._state.game[j][i - 1] == '*' and self._state.game[j][i + 1] == '*':
                        self._draw_matching_cell('RED')
                        self._match_sound.play()

                    elif self._state.game[j][i - 1] == '|' and self._state.game[j][i + 1] == '|':
                        self._draw_landing('RED')
                        self._land_sound.play()

                    else:
                        self._draw_cell('RED')

                elif self._state.game[j][i] == 'T':

                    if self._state.game[j][i - 1] == '*' and self._state.game[j][i + 1] == '*':
                        self._draw_matching_cell('ORANGE')
                        self._match_sound.play()

                    elif self._state.game[j][i - 1] == '|' and self._state.game[j][i + 1] == '|':
                        self._draw_landing('ORANGE')
                        self._land_sound.play()

                    else:
                        self._draw_cell('ORANGE')

                elif self._state.game[j][i] == 'V':

                    if self._state.game[j][i - 1] == '*' and self._state.game[j][i + 1] == '*':
                        self._draw_matching_cell('YELLOW')
                        self._match_sound.play()

                    elif self._state.game[j][i - 1] == '|' and self._state.game[j][i + 1] == '|':
                        self._draw_landing('YELLOW')
                        self._land_sound.play()

                    else:
                        self._draw_cell('YELLOW')

                elif self._state.game[j][i] == 'W':

                    if self._state.game[j][i - 1] == '*' and self._state.game[j][i + 1] == '*':
                        self._draw_matching_cell('GREEN')
                        self._match_sound.play()

                    elif self._state.game[j][i - 1] == '|' and self._state.game[j][i + 1] == '|':
                        self._draw_landing('GREEN')
                        self._land_sound.play()

                    else:
                        self._draw_cell('GREEN')

                elif self._state.game[j][i] == 'X':

                    if self._state.game[j][i - 1] == '*' and self._state.game[j][i + 1] == '*':
                        self._draw_matching_cell('CYAN')
                        self._match_sound.play()

                    elif self._state.game[j][i - 1] == '|' and self._state.game[j][i + 1] == '|':
                        self._draw_landing('CYAN')
                        self._land_sound.play()

                    else:
                        self._draw_cell('CYAN')

                elif self._state.game[j][i] == 'Y':

                    if self._state.game[j][i - 1] == '*' and self._state.game[j][i + 1] == '*':
                        self._draw_matching_cell('BLUE')
                        self._match_sound.play()

                    elif self._state.game[j][i - 1] == '|' and self._state.game[j][i + 1] == '|':
                        self._draw_landing('BLUE')
                        self._land_sound.play()

                    else:
                        self._draw_cell('BLUE')

                elif self._state.game[j][i] == 'Z':

                    if self._state.game[j][i - 1] == '*' and self._state.game[j][i + 1] == '*':
                        self._draw_matching_cell('PINK')
                        self._match_sound.play()

                    elif self._state.game[j][i - 1] == '|' and self._state.game[j][i + 1] == '|':
                        self._draw_landing('PINK')
                        self._land_sound.play()

                    else:
                        self._draw_cell('PINK')

                self._x_counter += 1


    def _draw_cell(self, color: str) -> None:
        """Draws each cell in the gamestate."""
        
        red = (255, 0, 0)
        blue = (0, 0, 255)
        green = (0, 255, 0)
        yellow = (255, 255, 0)
        cyan = (0, 255, 255)
        pink = (255, 0, 255)
        orange = (255, 128, 0)
        empty = (0, 0, 0)

        w, h = pygame.display.get_surface().get_size() # 400, 35

        if self._x_counter < 6:
            self.x += int(w / 25) + 1
        else:
            self._x_counter = 0
            self._y_counter += 1
            self.y += int(h / 16.25) + 1
            self.x = int(w / 2.5)


        if self._y_counter == 13:
            self._y_counter = 0
            self.y = int(h / 18.571)

        if color == 'EMPTY':
            pygame.draw.rect(self._screen, empty, (self.x, self.y, int(w / 26), int(h / 17)))
            
        elif color == 'RED':
            pygame.draw.rect(self._screen, red, (self.x, self.y, int(w / 26), int(h / 17)))

        elif color == 'ORANGE':
            pygame.draw.rect(self._screen, orange, (self.x, self.y, int(w / 26), int(h / 17)))

        elif color == 'YELLOW':
            pygame.draw.rect(self._screen, yellow, (self.x, self.y, int(w / 26), int(h / 17)))

        elif color == 'GREEN':
            pygame.draw.rect(self._screen, green, (self.x, self.y, int(w / 26), int(h / 17)))

        elif color == 'CYAN':
            pygame.draw.rect(self._screen, cyan, (self.x, self.y, int(w / 26), int(h / 17)))

        elif color == 'BLUE':
            pygame.draw.rect(self._screen, blue, (self.x, self.y, int(w / 26), int(h / 17)))

        elif color == 'PINK':
            pygame.draw.rect(self._screen, pink, (self.x, self.y, int(w / 26), int(h / 17)))

    def _draw_matching_cell(self, color: str) -> None:
        """Makes the faller give a visual cue when matching."""
        
        red = (255, 153, 153)
        blue = (153, 153, 255)
        green = (153, 255, 153)
        yellow = (255, 255, 153)
        cyan = (153, 255, 255)
        pink = (255, 153, 204)
        orange = (255, 204, 153)
        empty = (0, 0, 0)

        w, h = pygame.display.get_surface().get_size() # 400, 35

        if self._x_counter < 6:
            self.x += int(w / 25) + 1
        else:
            self._x_counter = 0
            self._y_counter += 1
            self.y += int(h / 16.25) + 1
            self.x = int(w / 2.5)


        if self._y_counter == 13:
            self._y_counter = 0
            self.y = int(h / 18.571)

            
        if color == 'RED':
            pygame.draw.rect(self._screen, red, (self.x, self.y, int(w / 26), int(h / 17)))

        elif color == 'ORANGE':
            pygame.draw.rect(self._screen, orange, (self.x, self.y, int(w / 26), int(h / 17)))

        elif color == 'YELLOW':
            pygame.draw.rect(self._screen, yellow, (self.x, self.y, int(w / 26), int(h / 17)))

        elif color == 'GREEN':
            pygame.draw.rect(self._screen, green, (self.x, self.y, int(w / 26), int(h / 17)))

        elif color == 'CYAN':
            pygame.draw.rect(self._screen, cyan, (self.x, self.y, int(w / 26), int(h / 17)))

        elif color == 'BLUE':
            pygame.draw.rect(self._screen, blue, (self.x, self.y, int(w / 26), int(h / 17)))

        elif color == 'PINK':
            pygame.draw.rect(self._screen, pink, (self.x, self.y, int(w / 26), int(h / 17)))

    def _draw_landing(self, color: str) -> None:
        """Makes the faller have a visual cue when landing."""
        
        red = (255, 51, 51)
        blue = (51, 51, 255)
        green = (51, 255, 51)
        yellow = (255, 255, 51)
        cyan = (51, 255, 255)
        pink = (255, 51, 153)
        orange = (255, 153, 51)
        empty = (0, 0, 0)

        w, h = pygame.display.get_surface().get_size() 

        if self._x_counter < 6:
            self.x += int(w / 25) + 1
        else:
            self._x_counter = 0
            self._y_counter += 1
            self.y += int(h / 16.25) + 1
            self.x = int(w / 2.5)


        if self._y_counter == 13:
            self._y_counter = 0
            self.y = int(h / 18.571)

            
        if color == 'RED':
            pygame.draw.rect(self._screen, red, (self.x, self.y, int(w / 26), int(h / 17)))

        elif color == 'ORANGE':
            pygame.draw.rect(self._screen, orange, (self.x, self.y, int(w / 26), int(h / 17)))

        elif color == 'YELLOW':
            pygame.draw.rect(self._screen, yellow, (self.x, self.y, int(w / 26), int(h / 17)))

        elif color == 'GREEN':
            pygame.draw.rect(self._screen, green, (self.x, self.y, int(w / 26), int(h / 17)))

        elif color == 'CYAN':
            pygame.draw.rect(self._screen, cyan, (self.x, self.y, int(w / 26), int(h / 17)))

        elif color == 'BLUE':
            pygame.draw.rect(self._screen, blue, (self.x, self.y, int(w / 26), int(h / 17)))

        elif color == 'PINK':
            pygame.draw.rect(self._screen, pink, (self.x, self.y, int(w / 26), int(h / 17)))        
        

    def _draw_column_background(self) -> None:
        """Draws the background of the actual columns part which is the grey area."""
        
        grey = (64, 64, 64)
        w, h = pygame.display.get_surface().get_size()
        
        pygame.draw.rect(self._screen, grey, (int(w / 2.55), int(h / 26), int(w / 3.82), int(h / 1.2))) # x, y, width, height


class GameOver(Exception):
    """Creates game over error message if game ends."""
    pass

if __name__ == '__main__':
    ColumnsGame().run()