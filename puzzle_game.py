"""
    CS5001 Final Project
    Puzzle Slider Game
    Wan-Ting Yun
    NUID 002745697
"""
    
import math
import turtle
import random
import re
import time
import os
import unittest

# get the directory of file
path = os.getcwd()

# screen set up
screen = turtle.Screen()
screen.setup(850, 900)
screen.title("CS5001 Sliding Puzzle Game")

# declare global variables
puzzle, ori, location, instance, file_list, error_msg = {}, [], [], [], [], ""
file_count, count, flag, player_name, move = 0, 0, False, "", 0

# set up different turtles
_pen = turtle.Turtle() # for adding puzzles
_pen.hideturtle()

_player = turtle.Turtle() # for showing player moves
_player.ht()

_error = turtle.Turtle() # for error message
_error.hideturtle()


# for adding splash screen and buttons
def add_pic(x, y, image):
    _pic = turtle.Turtle()
    screen.addshape(image)
    _pic.speed(0)
    _pic.penup()
    _pic.goto(x, y)
    _pic.shape(image)


# for drawing the rectangles on the screen
def draw_rectangle(x, y, width, length, color):
    _line = turtle.Turtle()
    _line.hideturtle()
    _line.pensize(5)
    _line.speed(0)
    _line.penup()
    _line.goto(x, y)
    _line.color(color)
    _line.pendown()
    for i in range(2):
        _line.fd(width); _line.right(90); _line.fd(length); _line.right(90)

# declare class for each piece of puzzles
class Puzzle:

    blank_info = [] # keep track of the blank piece
    
    def __init__(self, x, y, image, pos):
        self.image = image # the directory of the puzzle image
        self.x = x # x coordinate
        self.y = y # x coordinate
        self.pos = pos # the position of the puzzle (starts from 0)
        image_name = self.image.split("/")[::-1]
        image_name[0] = image_name[0].split(".")
        if image_name[0][0] == "blank":
            Puzzle.blank_info.append([self.pos, self.x, self.y])

    def change_blank(self): # change the information of the blank
        image_name = self.image.split("/")[::-1]
        image_name[0] = image_name[0].split(".")
        if image_name[0][0] == "blank":
            Puzzle.blank_info[0] = [self.pos, self.x, self.y]
            
    def reset(self): # reset the image to its original order
        self.image = ori[self.pos]
        
    def swap(self, other): # swap the images between two positions
        self.image, other.image =  other.image, self.image
            
    def clicked_in_region(self, x, y): # check if the mouse click on the puzzle
        if math.sqrt((x - self.x)**2) < 50:
            if math.sqrt((y -self.y)**2) < 50:
                return True

    def is_adjacent(self): # check if the mouse click on the piece adjacent to the blank
        if math.sqrt((Puzzle.blank_info[0][1] - self.x)**2 + (Puzzle.blank_info[0][2] -self.y)**2) <= 100:
            return True

# load a file from the file system
def load_file(file_name):
    global ori
    global location
    global puzzle
    global instance
    global square_root
    global error_msg

    try:
        with open(file_name, "r") as file:
            for line in file:
                line = re.sub(r'[:]', '', line)
                line = line.split()
                puzzle[line[0]] = line[1] # store the information in .puz file into a dictionary called "puzzle"

            number = int(puzzle["number"]) # the number of puzzle pieces
            square_root = int(math.sqrt(number))
        
            for i in range(1, number + 1):
                ori.append(path + "/" + puzzle[str(i)]) # store the original order of the puzzle in a list called "ori"
            location = ori.copy()
            random.shuffle(location) # scramble the puzzle and store the order in a list called "location"

            if number not in [4, 9, 16]: # check if the puzzle file is malformed
                error_image(path + "/" + "Resources/file_error.gif", 0, 0)
                error_msg = "Unable to process the puzzle file (invalid # of puzzles) LOCATION: load_file()"
                error_file()
                return False
            
            add_image(path + "/" + puzzle["thumbnail"], 300, 300)
            
            if number == 4:
                pos0 = Puzzle(-300, 240, location[0], 0)
                pos1 = Puzzle(-200, 240, location[1], 1)
                pos2 = Puzzle(-300, 140, location[2], 2)
                pos3 = Puzzle(-200, 140, location[3], 3)
                instance = [pos0, pos1, pos2, pos3] # store the instances of the class Puzzle into a list called "instance"
                return True

            elif number == 9:
                pos0 = Puzzle(-300, 240, location[0], 0)
                pos1 = Puzzle(-200, 240, location[1], 1)
                pos2 = Puzzle(-100, 240, location[2], 2)
                pos3 = Puzzle(-300, 140, location[3], 3)
                pos4 = Puzzle(-200, 140, location[4], 4)
                pos5 = Puzzle(-100, 140, location[5], 5)
                pos6 = Puzzle(-300, 40, location[6], 6)
                pos7 = Puzzle(-200, 40, location[7], 7)
                pos8 = Puzzle(-100, 40, location[8], 8)
                instance = [pos0, pos1, pos2, pos3, pos4, pos5, pos6, pos7, pos8]
                return True
      
            elif number == 16:
                pos0 = Puzzle(-300, 240, location[0], 0)
                pos1 = Puzzle(-200, 240, location[1], 1)
                pos2 = Puzzle(-100, 240, location[2], 2)
                pos3 = Puzzle(0, 240, location[3], 3)
                pos4 = Puzzle(-300, 140, location[4], 4)
                pos5 = Puzzle(-200, 140, location[5], 5)
                pos6 = Puzzle(-100, 140, location[6], 6)
                pos7 = Puzzle(0, 140, location[7], 7)
                pos8 = Puzzle(-300, 40, location[8], 8)
                pos9 = Puzzle(-200, 40, location[9], 9)
                pos10 = Puzzle(-100, 40, location[10], 10)
                pos11 = Puzzle(0, 40, location[11], 11)
                pos12 = Puzzle(-300, -60, location[12], 12)
                pos13 = Puzzle(-200, -60, location[13], 13)
                pos14 = Puzzle(-100, -60, location[14], 14)
                pos15 = Puzzle(0, -60, location[15], 15)
                instance = [pos0, pos1, pos2, pos3, pos4, pos5, pos6, pos7, pos8, pos9, pos10, pos11, pos12, pos13, pos14, pos15]
                return True
            
    except:
        error_image(path + "/" + "Resources/file_error.gif", 0, 0)
        error_msg = "Unable to process the puzzle file LOCATION: load_file()"
        error_file()
        screen.exitonclick()
        return False
           

# add all the puzzles and the thumbnail image to the screen
def add_puzzle():
    for i in range(len(instance)):
        screen.addshape(instance[i].image)
        _pen.speed(0)
        _pen.penup()
        _pen.goto(instance[i].x, instance[i].y)
        _pen.shape(instance[i].image)
        _pen.stamp()

   
# for adding the thumbnail image
def add_image(image, x, y):
    screen.addshape(image)
    _pen.speed(0)
    _pen.penup()
    _pen.goto(x, y)
    _pen.shape(image)
    _pen.stamp()

# activated after clicking
def clicker(x, y):
    global flag
    flag = False
    _player.clear() # clear the previous staqtus of the player moves
    _error.clear() # clear the error image showing on the screen
    click_on_puzzle(x, y)
    player_move()
    click_on_button(x, y)
    if flag == False: # if the puzzle is not reset, then activates win and lose
        win()
        lose()

# activated if the puzzle piece is clicked
def click_on_puzzle(x, y):
    global count
    for i in range(len(instance)):
        if instance[i].clicked_in_region(x, y): # check which of the puzzles got clicked
            if instance[i].is_adjacent() and instance[i].pos != Puzzle.blank_info[0][0]: # check if clicked on the piece adjacent to the blank
                count += 1 # keep track of the number of successful swaps
                add_image(instance[i].image, Puzzle.blank_info[0][1], Puzzle.blank_info[0][2])
                instance[i].swap(instance[Puzzle.blank_info[0][0]])
                add_image(instance[i].image, instance[i].x, instance[i].y)
                Puzzle.blank_info[0][0], Puzzle.blank_info[0][1], Puzzle.blank_info[0][2]= i, instance[i].x, instance[i].y

# activated if the button is clicked
def click_on_button(x, y):
    global error_msg
    if math.sqrt((x - 300)**2) < 50:
        if math.sqrt((y -(-280))**2) < 50:
            quit_game()

    if math.sqrt((x - 210)**2) < 50:
        if math.sqrt((y -(-280))**2) < 50:
            if file_count > 10: # if there are more than 10 puzzles, an error message will pop up
                error_image(path + "/" + "Resources/file_warning.gif", 0, 0)
                error_msg = "More than 10 puzzle files (showing first 10) LOCATION: check_puzzle_file()"
                error_file()
                load()
            else:
                load()
                
            
    if math.sqrt((x - 120)**2) < 50:
        if math.sqrt((y -(-280))**2) < 50:
            reset()

# check if the player wins the game
def win():
    w = 0
    for i in range(len(instance)): # check if the images are in original order
        if instance[i].image == ori[i]:
            w += 1
        
    if w == int(puzzle["number"]):
        add_image(path + "/" + "Resources/winner.gif", 0, 0)
        add_image(path + "/" + "Resources/credits.gif", 0, 0)
        time.sleep(3)
        leader_board("a")
        screen.exitonclick()
        
# check if the player loses the game    
def lose():
    if count >= move: # if the player moves the puzzle more than the max moves
        add_image(path + "/" + "Resources/Lose.gif", 0, 0)
        add_image(path + "/" + "Resources/credits.gif", 0, 0)
        time.sleep(3)
        screen.exitonclick()

# activated when the reset button is clicked       
def reset():
    global flag
    flag = True # check if the puzzle is reset
    for i in range(len(instance)):
        instance[i].reset()
        instance[i].change_blank()
    
    add_puzzle()
    
# store the lists of .puz files and the number of files
def check_puzzle_file():
    global file_count
    global file_list
    all_list = os.listdir(path)
    for i in range(len(all_list)):
        all_list[i] = all_list[i].split(".")
    for j in all_list:
        if j[-1] == "puz":
            file_list.append(f"{j[0]}.{j[1]}")
            file_count += 1

# activated when the load button is clicked
def load():
    global instance
    global location
    global count
    global puzzle
    global ori
    global error_msg
    global flag

    text = [x +"\n" for x in file_list]
    choice = ''.join(text[:10]) # merge the strings in the file list into a single line of string
    file = screen.textinput("Load Puzzle", f"Enter the name of the puzzle you wish to load. Choices are:\n{choice}")

    if file in file_list:
        # clear the previous screen
        _error.clear()
        instance.clear()
        location.clear()
        puzzle.clear()
        ori.clear()
        count = 0
        _pen.clear()
        if load_file(f"{path}/{file}"):
            add_puzzle()
            print(is_solvable(location)) # print "True" if the puzzle is solvable
        else:
            load()
        for i in range(len(instance)):
            instance[i].change_blank()
    else:
        error_image(path + "/" + "Resources/file_error.gif", 0, 0)
        error_msg = f"File {file} does not exist LOCATION: load_file()"
        error_file()
        return False

# activated when the quit button is clicked    
def quit_game():
    add_image(path + "/" + "Resources/quitmsg.gif", 0, 0)
    add_image(path + "/" + "Resources/credits.gif", 0, 0)
    time.sleep(3)
    screen.exitonclick()
           
# show the updated player moves on the screen
def player_move():
    _player.up()
    _player.goto(-300, -300)
    _player.write(f"Player Moves: {count}", font=('Cambria', 25, 'bold'))


# for adding error message on the screen
def error_image(image, x, y):
    screen.addshape(image)
    _error.speed(0)
    _error.penup()
    _error.goto(x, y)
    _error.shape(image)
    _error.stamp()

# log errors to the designated .err file
def error_file():
    with open(path + "/" + "5001_puzzle.err", "a+") as error_file:
        error_file.write(f"{time.ctime(time.time())} Error: {error_msg}\n")
        
# show the leader board on the right side of the screen
def leader_board(mode):
    global error_msg
    leader = []
    n = 0
    _leader = turtle.Turtle()
    _leader.ht()
    _leader.up()
    _leader.color("blue3")
    if mode == "r": # read and show the stored data of leaders
        try:
            with open(path + "/" + "leader_board.txt", "r") as read_board:
                _leader.goto(150, 230)
                _leader.write("Leaders:\n", font=('Cambria', 22, 'normal'))
                for line in read_board:
                    leader.append(line)
                leader.sort() # show the completion moves in an ascending order
                for element in leader:
                    _leader.goto(150, 190 - n)
                    n = n + 40
                    _leader.write(element, font=('Cambria', 22, 'normal'))
        except:
            error_msg = "Cound not open leaderboard.txt LOCATION: leader_board()"
            error_file()
                
    if mode == "a": # append the new leaders in the designated file
        with open(path + "/" + "leader_board.txt", "a+") as append_board:
            append_board.write(f"{count}: {player_name}\n")


               
""" BONUS """

# compare each element in a list to calculate the inversions
def compare_value(list_a):
    count = 0
    indexing_length = range(0, len(list_a) - 1)

    for i in indexing_length:
        current_value = list_a[i]

        for j in range(i+1, len(list_a)):
            if current_value < list_a[j]:
                count = count + 1
    return count


# for odd-sized puzzle: solvable iff when its number of inversions is even
# for even-sized puzzle: solvable iff the number of inversions + the row of the blank square is odd

def is_solvable(list_b):
    order = []
    matrix = {}
    inversion = 0
    for index, value in enumerate(list_b):
        value = value.split("/")[::-1]
        value[0] = value[0].split(".")
        order.append(value[0][0])
    even_order = order.copy()
    even_order.remove("blank") # store the order of puzzles
    for element in range(len(even_order)):
        even_order[element] = int(even_order[element])

    matrix = [order[i : i + int(math.sqrt(len(list_b)))] for i in range(0, len(order), int(math.sqrt(len(list_b))))] # create a matrix of the list

    if type(list_b) != list:
        raise TypeError

    if len(list_b) == 4:
        if compare_value(even_order) % 2 != 0 and "blank" in matrix[0]:
            return True
        elif compare_value(even_order) % 2 == 0 and "blank" in matrix[1]:
            return True
        else:
            return False

    if len(list_b) == 9:
        if compare_value(even_order) % 2 == 0:
            return True
        elif compare_value(even_order) % 2 != 0:
            return False
            
    if len(list_b) == 16:
        if compare_value(even_order) % 2 != 0 and ("blank" in matrix[0] or "blank" in matrix[2]):
            return True
        elif compare_value(even_order) % 2 == 0 and ("blank" in matrix[1] or "blank" in matrix[3]):
            return True
        else:
            return False

# PyUnit test to validate the algorithm        
class TestSolvableness(unittest.TestCase):
    def test_is_solvable(self):
        result_1 = is_solvable(ori)
        self.assertEqual(result_1, True)
        lst = ['blank.gif', '3.gif', '2.gif', '4.gif']
        result_2 = is_solvable(lst)
        self.assertEqual(result_2, False)

    # negative test
    def test_bad_init(self):
        with self.assertRaises(TypeError):
            is_solvable(10)


def main():
    global player_name
    global move
    add_pic(0, 0, path + "/" + "Resources/splash_screen.gif")
    time.sleep(3)
    screen.clear()
    try: # test if the starter .puz file exists
        f = open(path + "/" + "leader_board.txt", "r")
        f.close()
    except FileNotFoundError: # show error message if the leaderboard file does not exist
        add_pic(0, 0, path + "/" + "Resources/leaderboard_error.gif")
        time.sleep(2)
        screen.clear()
    player_name = screen.textinput("CS5001 Puzzle Slide", "Your Name")
    move = screen.numinput("CS5001 Puzzle Slide - Moves", "Enter the number of moves (chances) you want (5-200)?", 50, minval=5, maxval=200.)
    file_name = path + "/" + "mario.puz"
    draw_rectangle(-370, 320, 470, 510, "black")
    draw_rectangle(-370, -230, 730, 100, "black")
    draw_rectangle(130, 320, 230, 510, "blue3")
    
    if load_file(file_name): # check if the file exists
        add_puzzle()
        screen.onclick(clicker)
        check_puzzle_file()
        add_pic(300, -280, path + "/" + "Resources/quitbutton.gif")
        add_pic(210, -280, path + "/" + "Resources/loadbutton.gif")
        add_pic(120, -280, path + "/" + "Resources/resetbutton.gif")
        leader_board("r")
        print(is_solvable(location))
        unittest.main(verbosity=3)
        
   
if __name__ == "__main__":
    main()

