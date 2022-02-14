# Derek Naing 70307889

BLOCK_WIDTH = 0.05
BLOCK_HEIGHT = 0.05
BLOCK_SPEED = 5
ROWS = 13
COLUMNS = 6

class GameState:
    def __init__(self):
        thelist = []
        for i in range(ROWS):
            thelist.append([''] * (COLUMNS * 3))
        self.game = thelist
        self.row = ROWS
        self.column = COLUMNS
        self.left = '['
        self.right = ']'
        self.frozen = False
        self.faller_exists = False
        self.matched = False
        self.game_ended = False
        self.ready = False


    def currentgamestate(self) -> None:
        """Prints out the gameboard list in viewable form to make it easier to check for bugs."""

        for thelist in self.game:
            print(thelist)

    def printboard(self) -> None:
        """Prints out the game board."""

        for nestedlist in self.game:

            print('|', end='')   

            for index in range(len(nestedlist) + 1):    
                    if index == self.column * 3:
                        print('|', end='')
                    elif nestedlist[index] != '':
                        print(nestedlist[index], end='')
                    elif nestedlist[index] == '':
                        print(' ', end='')

            print()
        print(' ', end='')  
        for i in range(self.column * 3):
            print('-', end='')
        print(' ')

    def _index_drop(self, column: int) -> int:
        """Converts the column dropped in the index dropped."""

        constant = column - 2
        index = (2 * column) + constant
        return index
     
    def create_faller(self, drop_column: int, first: str, second: str, third: str) -> None:
        """Creates one block of the faller in the column indicated by the player."""

        self.frozen = False
        self.faller_exists = True
        val = self._index_drop(drop_column)
        self.drop_index = val

        self.down_counter = 1
        self.turn_counter = 1

        if self.game[1][self.drop_index] != '':
            self.left = '|'
            self.right = '|'
        else:
            self.left = '['
            self.right = ']'
                        
        self.game[0][self.drop_index] = third
        self.game[0][self.drop_index - 1] = self.left
        self.game[0][self.drop_index + 1] = self.right


        self.printboard()

    def check_column_full(self, drop_column: int) -> bool:
        """Checks to see if the player is trying to drop into a column thats already full or not."""

        drop_index = self._index_drop(drop_column)
        if self.game[0][drop_index] == '':
            return True
        else:
            return False

    def change_all(self) -> None:
        """Helps change all brackets to | when needed."""
        for i in range(len(self.game)):
            for j in range(len(self.game[i])):
                if self.game[i][j] == '[' or self.game[i][j] == ']':
                    self.game[i][j] = '|'
                    
    def _check_frozen(self) -> None:
        """Checks to see if the faller is in a state of being frozen and changes the faller borders to | accordingly."""

        try:
            if self.turn_counter == self.row - 1:
                self.left = '|'
                self.right = '|'
                self.change_all()
                
            elif self.turn_counter == 1:
                if self.game[1][self.drop_index] == '':
                    if self.game[2][self.drop_index] != '':
                        self.left = '|'
                        self.right = '|'
                        self.change_all()
                    else:
                        self.left = '['
                        self.right = ']'             
                    
                else:
                    self.left = '|'
                    self.right = '|'
            elif self.turn_counter == 2:
                if self.game[3][self.drop_index] != '':
                    self.left = '|'
                    self.right = '|'
                    self.change_all()
                else:
                    self.left = '['
                    self.right = ']'
            elif self.turn_counter >= 3:
                if self.game[self.down_counter + 3][self.drop_index] != '':
                    self.left = '|'
                    self.right = '|'
                    self.change_all()
                else:
                    self.left = '['
                    self.right = ']'
            else:
                self.left = '['
                self.right = ']'

        except IndexError:
            self.left = '|'
            self.right = '|'
            self.change_all()

    def freeze_faller(self) -> None:
        """Freezes the faller and removes the | so that only the capital letters remain from the faller."""

        try:
            if self.turn_counter == 1 and self.game[0][self.drop_index - 1] == '|':
                self.game[0][self.drop_index - 1] = ''
                self.game[0][self.drop_index + 1] = ''
            elif self.turn_counter == 2 and self.game[0][self.drop_index - 1] == '|':
                self.game[0][self.drop_index - 1] = ''
                self.game[0][self.drop_index + 1] = ''
                self.game[1][self.drop_index - 1] = ''
                self.game[1][self.drop_index + 1] = ''
            elif self.turn_counter >= 3 and self.game[0 + self.down_counter][self.drop_index - 1] == '|':
                self.game[-1 + self.down_counter][self.drop_index - 1] = ''
                self.game[-1 + self.down_counter][self.drop_index + 1] = ''
                self.game[0 + self.down_counter][self.drop_index - 1] = ''
                self.game[0 + self.down_counter][self.drop_index + 1] = ''
                self.game[1 + self.down_counter][self.drop_index - 1] = ''
                self.game[1 + self.down_counter][self.drop_index + 1] = ''
        except IndexError:
            pass

    def drop(self, drop_column: int, first: str, second: str, third: str) -> None:
        """Drops the faller one block everytime this method is called and stops faller from continuing to drop if on edge of board or another faller."""

        self._check_frozen()


        try:
            self.check_game_over()
            
            if self.game[self.down_counter][self.drop_index] == '': # if row index 1 is empty then drop the second block

                self.game[0][self.drop_index] = second
                self.game[1][self.drop_index] = third 
                self.game[1][self.drop_index - 1] = self.left
                self.game[1][self.drop_index + 1] = self.right

                self.printboard()

                self.turn_counter += 1  

            elif self.game[self.down_counter + 1][self.drop_index] == '': # if row index 2 is empty then drop the third block

                self.game[0][self.drop_index] = first
                self.game[0][self.drop_index - 1] = self.left
                self.game[0][self.drop_index + 1] = self.right

                self.game[1][self.drop_index] = second
                self.game[1][self.drop_index - 1] = self.left
                self.game[1][self.drop_index + 1] = self.right

                self.game[2][self.drop_index] = third
                self.game[2][self.drop_index - 1] = self.left
                self.game[2][self.drop_index + 1] = self.right
                self.printboard()

                self.turn_counter += 1

            elif self.game[self.down_counter + 2][self.drop_index] == '': # if the row index below bottom most column block is empty then drop the whole column down

                self.game[0 + self.down_counter][self.drop_index] = first
                self.game[0 + self.down_counter][self.drop_index - 1] = self.left
                self.game[0 + self.down_counter][self.drop_index + 1] = self.right

                self.game[1 + self.down_counter][self.drop_index] = second
                self.game[1 + self.down_counter][self.drop_index - 1] = self.left
                self.game[1 + self.down_counter][self.drop_index + 1] = self.right

                self.game[2 + self.down_counter][self.drop_index] = third
                self.game[2 + self.down_counter][self.drop_index - 1] = self.left
                self.game[2 + self.down_counter][self.drop_index + 1] = self.right

                self.game[self.down_counter - 1][self.drop_index] = ''
                self.game[self.down_counter - 1][self.drop_index - 1] = ''
                self.game[self.down_counter - 1][self.drop_index + 1] = ''

                self.printboard()

                self.turn_counter += 1
                    
                self.down_counter += 1

            else:
                raise IndexError

        except IndexError:

            self.frozen = True

            self.freeze_faller()

            if self.matched == False:

                self.horizontal_matching()
                self.vertical_matching()
                self.diagonal_matching_right()
                self.diagonal_matching_left()
                self.printboard()

                if self.matched == False:
                    self.faller_exists = False

            elif self.matched == True:
                self.remove_matches()
                for i in range(self.row):
                    self.gravity()

                self.horizontal_matching()
                self.vertical_matching()
                self.diagonal_matching_right()
                self.diagonal_matching_left()

                self.printboard()

                if self.matched == False:
                    self.faller_exists = False
                    self.frozen = False


        except(GameOver):
            self.game_ended = True
            
    def move_right(self, drop_column: int, first: int, second: int, third: int) -> None:
        """Moves the faller right one block everytime this method is called and keeps it from moving right if touching edge of board or another faller."""

        self.drop_index += 3
        self._check_frozen()
        try:

            if self.turn_counter == 1 and self.game[-1 + self.down_counter][self.drop_index] == '':
                self.game[0][self.drop_index - 3] = ''
                self.game[0][self.drop_index - 4] = ''
                self.game[0][self.drop_index - 2] = ''

                self.game[0][self.drop_index - 1] = self.left  
                self.game[0][self.drop_index] = third  
                self.game[0][self.drop_index + 1] = self.right  
                self.printboard()

            elif self.turn_counter == 2 and self.game[-1 + self.down_counter][self.drop_index] == '' and self.game[0 + self.down_counter][self.drop_index] == '':
                self.game[1][self.drop_index - 3] = ''
                self.game[1][self.drop_index - 4] = ''
                self.game[1][self.drop_index - 2] = ''

                self.game[0][self.drop_index - 3] = ''
                self.game[0][self.drop_index - 4] = ''
                self.game[0][self.drop_index - 2] = ''                

                self.game[1][self.drop_index - 1] = self.left  
                self.game[1][self.drop_index] = third  
                self.game[1][self.drop_index + 1] = self.right  

                self.game[0][self.drop_index - 1] = self.left  
                self.game[0][self.drop_index] = second  
                self.game[0][self.drop_index + 1] = self.right  

                self.printboard()

            elif self.turn_counter >= 3 and self.game[-1 + self.down_counter][self.drop_index] == '' and self.game[0 + self.down_counter][self.drop_index] == '' and self.game[1 + self.down_counter][self.drop_index] == '':

                self.game[-1 + self.down_counter][self.drop_index - 3] = '' 
                self.game[-1 + self.down_counter][self.drop_index - 4] = ''
                self.game[-1 + self.down_counter][self.drop_index - 2] = ''

                self.game[0 + self.down_counter][self.drop_index - 3] = '' 
                self.game[0 + self.down_counter][self.drop_index - 4] = ''
                self.game[0 + self.down_counter][self.drop_index - 2] = ''

                self.game[1 + self.down_counter][self.drop_index - 3] = ''  
                self.game[1 + self.down_counter][self.drop_index - 4] = ''
                self.game[1 + self.down_counter][self.drop_index - 2] = ''


                self.game[-1 + self.down_counter][self.drop_index - 1] = self.left
                self.game[-1 + self.down_counter][self.drop_index] = first
                self.game[-1 + self.down_counter][self.drop_index + 1] = self.right

                self.game[0 + self.down_counter][self.drop_index - 1] = self.left
                self.game[0 + self.down_counter][self.drop_index] = second
                self.game[0 + self.down_counter][self.drop_index + 1] = self.right

                self.game[1 + self.down_counter][self.drop_index - 1] = self.left
                self.game[1 + self.down_counter][self.drop_index] = third
                self.game[1 + self.down_counter][self.drop_index + 1] = self.right
                self.printboard()

            else:
                self.drop_index -= 3
                self.printboard()
                print('Column cannot move any further to the right')

        except IndexError:
            self.drop_index -= 3
            self.printboard()
            print('Column cannot move any further to the right')
                
    def move_left(self, drop_column: int, first: int, second:int, third: int) -> None:
        """Moves the faller left one block everytime this method is called and keeps faller from moving left if touching edge of board or another faller."""

        self.drop_index -= 3
        self._check_frozen()
        self.check_game_over()
        try:

            if self.drop_index > 0:
                if self.turn_counter == 1 and self.game[-1 + self.down_counter][self.drop_index] == '':
                    self.game[0][self.drop_index + 2] = ''
                    self.game[0][self.drop_index + 3] = ''
                    self.game[0][self.drop_index + 4] = ''

                    self.game[0][self.drop_index - 1] = self.left  
                    self.game[0][self.drop_index] = third  
                    self.game[0][self.drop_index + 1] = self.right  
                    self.printboard()

                elif self.turn_counter == 2 and self.game[-1 + self.down_counter][self.drop_index] == '' and self.game[0 + self.down_counter][self.drop_index] == '':

                    self.game[0][self.drop_index + 2] = ''
                    self.game[0][self.drop_index + 3] = ''
                    self.game[0][self.drop_index + 4] = ''

                    self.game[1][self.drop_index + 2] = ''
                    self.game[1][self.drop_index + 3] = ''
                    self.game[1][self.drop_index + 4] = ''

                    self.game[0][self.drop_index - 1] = self.left  
                    self.game[0][self.drop_index] = third  
                    self.game[0][self.drop_index + 1] = self.right  

                    self.game[1][self.drop_index - 1] = self.left  
                    self.game[1][self.drop_index] = second  
                    self.game[1][self.drop_index + 1] = self.right  

                    self.printboard()

                elif self.turn_counter >= 3 and self.game[-1 + self.down_counter][self.drop_index] == '' and self.game[0 + self.down_counter][self.drop_index] == '' and self.game[1 + self.down_counter][self.drop_index] == '':

                    self.game[-1 + self.down_counter][self.drop_index + 2] = '' 
                    self.game[-1 + self.down_counter][self.drop_index + 3] = ''
                    self.game[-1 + self.down_counter][self.drop_index + 4] = ''

                    self.game[0 + self.down_counter][self.drop_index + 2] = '' 
                    self.game[0 + self.down_counter][self.drop_index + 3] = ''
                    self.game[0 + self.down_counter][self.drop_index + 4] = ''

                    self.game[1 + self.down_counter][self.drop_index + 2] = ''  
                    self.game[1 + self.down_counter][self.drop_index + 3] = ''
                    self.game[1 + self.down_counter][self.drop_index + 4] = ''


                    self.game[-1 + self.down_counter][self.drop_index - 1] = self.left
                    self.game[-1 + self.down_counter][self.drop_index] = first
                    self.game[-1 + self.down_counter][self.drop_index + 1] = self.right

                    self.game[0 + self.down_counter][self.drop_index - 1] = self.left
                    self.game[0 + self.down_counter][self.drop_index] = second
                    self.game[0 + self.down_counter][self.drop_index + 1] = self.right

                    self.game[1 + self.down_counter][self.drop_index - 1] = self.left
                    self.game[1 + self.down_counter][self.drop_index] = third
                    self.game[1 + self.down_counter][self.drop_index + 1] = self.right
                    self.printboard()

                else:
                    self.drop_index += 3
                    self.printboard()
                    print('Column cannot move any further to the left')

            else:
                self.drop_index += 3
                self.printboard()
                print('Column cannot move any further to the left')

        except IndexError:
            self.drop_index += 3
            self.printboard()
            print('Column cannot move any further to the left')

    def rotate(self, drop_column: int, one: int, two: int, three: int) -> tuple:
        """Rotates the faller properly."""

        thelist = [one, two, three]
        val = thelist[-1]
        del thelist[-1]
        thelist.insert(0, val)

        first = thelist[0]
        second = thelist[1]
        third = thelist[2]

        if self.turn_counter == 1:
            self.game[0][self.drop_index] = third
            self.printboard()

        elif self.turn_counter == 2:
            self.game[0][self.drop_index] = second
            self.game[1][self.drop_index] = third
            self.printboard()

        elif self.turn_counter >= 3:
            self.game[-1 + self.down_counter][self.drop_index] = first
            self.game[0 + self.down_counter][self.drop_index] = second
            self.game[1 + self.down_counter][self.drop_index] = third
            self.printboard()
                         
        return first, second, third


                    
    def horizontal_matching(self) -> None:
        """Matches gems if there are 3 or more horizontally aligned."""
        
        jewels = ['S', 'T', 'V', 'W', 'X', 'Y', 'Z']
        for i in range(self.row):  
            x = 4   # 7
            for j in range(self.column - 2):  
                if self.game[i][x - 3] == self.game[i][x] == self.game[i][x + 3]:
                    if self.game[i][x - 3] in jewels and self.game[i][x] in jewels and self.game[i][x + 3] in jewels:

                        

                        self.game[i][x - 1] = '*'
                        self.game[i][x + 1] = '*'

                        self.game[i][x + 2] = '*'
                        self.game[i][x + 4] = '*'
                            
                        self.game[i][x - 2] = '*'
                        self.game[i][x - 4] = '*'
                        
                

                        self.matched = True
                x += 3

    def vertical_matching(self) -> None:
        """Matches gems if there are 3 or more vertically aligned."""

        jewels = ['S', 'T', 'V', 'W', 'X', 'Y', 'Z']
        loop = self.row - 2

        for i in range(loop): 
            for j in range(self.column * 3): 
                if self.game[i][j] == self.game[i + 1][j] == self.game[i + 2][j]:
                    if self.game[i][j] in jewels and self.game[i + 1][j] in jewels and self.game[i + 2][j] in jewels:

                        self.game[i][j - 1] = '*'
                        self.game[i][j + 1] = '*'

                        self.game[i + 1][j - 1] = '*'
                        self.game[i + 1][j + 1] = '*'

                        self.game[i + 2][j - 1] = '*'
                        self.game[i + 2][j + 1] = '*'

                        self.matched = True

    def diagonal_matching_left(self) -> None:
        """Matches gems if three match diagonally."""

        jewels = ['S', 'T', 'V', 'W', 'X', 'Y', 'Z']
        for i in range(self.row - 2): 
            x = 1
            for j in range(self.column - 2):  
                if self.game[i][x] == self.game[i + 1][x + 3] == self.game[i + 2][x + 6]:
                    if self.game[i][x] in jewels and self.game[i + 1][x + 3] in jewels and self.game[i + 2][x + 6] in jewels:
                        self.game[i][x - 1] = '*'
                        self.game[i][x + 1] = '*'

                        self.game[i + 1][x + 2] = '*'
                        self.game[i + 1][x + 4] = '*'
                            
                        self.game[i + 2][x + 5] = '*'
                        self.game[i + 2][x + 7] = '*'
                        
                        

                        self.matched = True
                x += 3

    def diagonal_matching_right(self) -> None:
        """Matches gems if three match diagonally."""

        jewels = ['S', 'T', 'V', 'W', 'X', 'Y', 'Z']
        for i in range(-1, -self.row + 1, -1):
            x = 1
            for j in range(self.column - 2):
                if self.game[i][x] == self.game[i - 1][x + 3] == self.game[i - 2][x + 6]:
                    if self.game[i][x] in jewels and self.game[i - 1][x + 3] in jewels and self.game[i - 2][x + 6] in jewels:
                         
                        self.game[i][x - 1] = '*'
                        self.game[i][x + 1] = '*'

                        self.game[i - 1][x + 2] = '*'
                        self.game[i - 1][x + 4] = '*'
                            
                        self.game[i - 2][x + 5] = '*'
                        self.game[i - 2][x + 7] = '*'
                        
                        

                        self.matched = True
        
                x += 3
                
    def remove_matches(self) -> None:
        """Removes all gems that are matched."""

        jewels = ['S', 'T', 'V', 'W', 'X', 'Y', 'Z']

        for i in range(len(self.game)):  

            for j in range(1, len(self.game[i]) - 1):
                if self.game[i][j] in jewels and self.game[i][j - 1] == '*' and self.game[i][j + 1] == '*':

                    self.game[i][j] = ''
                    self.game[i][j + 1] = ''
                    self.game[i][j - 1] = ''

        self.matched = False

    def gravity(self) -> None:
        """Creates gravity on the field by dropping any floating pieces."""
        for i in range(self.row - 1): 
            x = 1
            for j in range(self.column):
                if self.game[i][x] != '' and self.game[i + 1][x] == '' or self.game[i + 1][x] == ' ':

                    self.game[i + 1][x] = self.game[i][x]
                    self.game[i + 1][x - 1] = self.game[i][x - 1]
                    self.game[i + 1][x + 1] = self.game[i][x + 1]

                    self.game[i][x] = ''
                    self.game[i][x - 1] = ''
                    self.game[i][x + 1] = ''

                x += 3

    def check_game_over(self) -> 'Error':
        """Raises game over error if faller doesn't fit."""

        if self.turn_counter == 1:
            if self.game[1][self.drop_index] != '':
                raise GameOver
        elif self.turn_counter == 2:
            if self.game[2][self.drop_index] != '':
                raise GameOver

    def contents_insert(self, line_list: list) -> None:
        """Given a list of contents, they are inserted into the board and matching is done."""
    
        for i in range(self.row): 
            x = 1
            for j in range(self.column): 
                self.game[i][x] = line_list[i][j]
                x += 3
        for i in range(self.row):
            self.gravity()

        self.horizontal_matching()
        self.vertical_matching()
        self.diagonal_matching_right()
        self.diagonal_matching_left()
        

        self.printboard()

    def content_drop(self) -> None:
        """Drops content items."""

        if self.matched == True:
            self.remove_matches()
            for i in range(self.row):
                self.gravity()
            self.printboard()

            self.matched = False

            self.horizontal_matching()
            self.vertical_matching()
            self.diagonal_matching_right()
            self.diagonal_matching_left()

            if self.matched == False:
                self.ready = True


class GameOver(Exception):
    """Creates game over error message if game ends."""
    pass