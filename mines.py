#Mines Game
#Edwin Yu

#Imports
import simplegui
import math
import random

#Initialize global constants and variables
#Colors corresponding to each number
COLORS = {
    "_": "Gray", 
    "*": "Black", 
    "1": "Blue", 
    "2": "Green", 
    "3": "Red", 
    "4": "Purple", 
    "5": "Maroon", 
    "6": "Teal", 
    "7": "Black", 
    "8": "Gray"
}

#Height and width of each square, font size
ROW_HEIGHT = 24
COLUMN_WIDTH = 24
FONT_SIZE = ROW_HEIGHT * 0.75

#Size of canvas
width = 0
height = 0

#Number of rows and columns
rows = 0
columns = 0

#Number of squares, mines, and squares needed to clear
squares_number = 0
mines_number = 0
squares_needed = 0

#Arrays corresponding to information about board
mine_locations = [] #Array of mine placement
game_board = [] #Two-dimensional array of mine placement
neighbor_mines_board = [] #Two-dimensional array of number of neighboring mines
checked_board = [] #Two-dimensional array indicating which squares are checked
display_board = [] #Two-dimensional array displayed on canvas

#Flagging mode off
flagging = False

end_message = ""

#Get input from user and convert to int
def user_input(prompt, lower_limit, upper_limit):
    try:
        int_input = int(input(prompt)) #Convert user input to integer
        if lower_limit <= int_input <= upper_limit: #Is input within boundaries?
            return int_input
        else:
            return user_input(prompt, lower_limit, upper_limit) #Ask user again if not within bounds
    except:
            return user_input(prompt, lower_limit, upper_limit) #Ask user again if cannot convert to int

#Use user inputs to generate mine locations, counts of neighboring mines, and squares marked as checked
def generate_board():
    global squares_needed, mine_locations, game_board, neighbor_mines_board, checked_board, display_board
    
    squares_needed = squares_number - mines_number #Calculate number of squares needed to clear.
    
    mine_locations.extend(mines_number * [1] + (squares_number - mines_number) * [0]) #Create an array of mines and safe squares
    random.shuffle(mine_locations) #Shuffle the array.
    
    game_board.append([0] * (columns + 2)) #Append invisible top border to game board for edge cases of check_square
    for row in range(rows):
        game_board.append([0] + mine_locations[row * columns: (row + 1) * columns] + [0]) #Use mine_locations to generate board, borders
    game_board.append([0] * (columns + 2)) #Append invisible bottom border to game board for edge cases of check_square
    
    for row in range(rows + 2):
            neighbor_mines_board.append([0] * (columns + 2)) #Create board of number of neighboring mines
    for row in range(rows + 2):
        for column in range(columns + 2):
            if game_board[row][column] == 1: #If square is a mine
                #Add 1 to the number of neighboring mines for all neighboring squares
                for neighbor_row in [row - 1, row + 1]:
                    for neighbor_column in [column - 1, column, column + 1]:
                        neighbor_mines_board[neighbor_row][neighbor_column] += 1
                for neighbor_column in [column - 1, column + 1]:
                    neighbor_mines_board[row][neighbor_column] += 1
    
    checked_board.append([1] * (columns + 2)) #Mark invisible borders as already checked so check_square will not expand beyond
    for row in range(rows):
        checked_board.append([1] + [0] * (columns) + [1]) #Mark visible squares as unchecked, invisible as checked
    checked_board.append([1] * (columns + 2)) #Mark invisible borders as already checked
    
    for row in range(rows + 2): 
        display_board.append([""] * (columns + 2)) #Display nothing on board at the start
    
    frame.set_draw_handler(draw_board) #Set draw handler
    frame.set_mouseclick_handler(mine_click) #Set mouse click handler to allow interaction with board
    frame.set_keydown_handler(toggle_flag) #Set keydown handler for toggling flagging mode

#Check indicated square to determine if each square is safe, expand to neighboring squares if applicable
def check_square(square_row, square_column):
    if game_board[square_row][square_column] == 1: #If square is a mine,
        mine_square(square_row, square_column)
        
    if checked_board[square_row][square_column] == 0 and game_board[square_row][square_column] == 0: #If square is previously unchecked and safe,
        safe_square(square_row, square_column)

#User clicks a mine, loses
def mine_square(square_row, square_column):
    global display_board, end_message
    #Display all mines
    for row in range(1, rows + 1):
        for column in range(1, columns + 1):
            if game_board[row][column] == 1:
                display_board[row][column] = "*" #Display mines as star
    display_board[square_row][square_column] = "+" #Display losing mine as plus
    end_message = "You lose!"
    frame.set_mouseclick_handler(dead_mouse)

#User clicks a safe square
def safe_square(square_row, square_column):
    global checked_board, squares_needed, display_board, end_message
    checked_board[square_row][square_column] = 1 #Mark square as checked
    squares_needed -=  1 #Reduce number of squares needed to win
    
    if neighbor_mines_board[square_row][square_column] == 0: #If there are no neighboring mines,
        display_board[square_row][square_column] = "_" #Display square with indicator
        #Expand to check all neighboring squares
        for row in [square_row - 1, square_row + 1]:
            for column in [square_column - 1, square_column, square_column + 1]:
                check_square(row, column)
        for column in [square_column - 1, square_column + 1]:
            check_square(square_row, column)
        
    elif neighbor_mines_board[square_row][square_column] >= 1: #If there are neighboring mines,
        display_board[square_row][square_column] = str(neighbor_mines_board[square_row][square_column]) #Display only that square
    
    if squares_needed == 0: #If user has cleared all safe squares,
        end_message = "You win!"
        frame.set_mouseclick_handler(dead_mouse)

#Mouse click handler determines square
def mine_click(position):
    global display_board
    if position[0] <= width:
        square_row = math.ceil(position[1] / (ROW_HEIGHT))
        square_column = math.ceil(position[0] / (COLUMN_WIDTH))
        if not flagging: #If flagging mode is off,
            check_square(square_row, square_column) #Check the clicked square
        elif checked_board[square_row][square_column] == 0 and display_board[square_row][square_column] == "": #If flagging is on and square is unchecked and not flagged,
            display_board[square_row][square_column] = "F"
        elif checked_board[square_row][square_column] == 0 and display_board[square_row][square_column] == "F": #If flagging is on and square is unchecked and flagged,
            display_board[square_row][square_column] = ""

#Mouse click handler disables mouse
def dead_mouse(position):
    pass

#Toggle flagging mode
def toggle_flag(key):
    global flagging
    if key == simplegui.KEY_MAP["f"]:
        flagging = not flagging

#Game board draw handler
def draw_board(canvas):
    frame.set_canvas_background("Silver")
    #Draw grid lines
    for column in range(columns):
        canvas.draw_line([column * COLUMN_WIDTH, 0], [column * COLUMN_WIDTH, height], 2, "White")
        canvas.draw_line([(column + 1) * COLUMN_WIDTH - 2, 0], [(column + 1) * COLUMN_WIDTH - 2, height], 2, "Gray")
    for row in range(rows):
        canvas.draw_line([0, row * ROW_HEIGHT], [width, row * ROW_HEIGHT], 2, "White")
        canvas.draw_line([0, (row + 1) * ROW_HEIGHT - 2], [width, (row + 1) * ROW_HEIGHT - 2], 2, "Gray")
    
    #Draw numbers and other displayed infomation with appropriate colors
    for row in range(1, rows + 1):
        for column in range(1, columns + 1):
            if display_board[row][column] != "" and display_board[row][column] != "+" and display_board[row][column] != "F": #If square is not blank and not losing mine and not flag,
                #Color square gray and display contents
                canvas.draw_polygon([[(column - 1)* COLUMN_WIDTH, (row - 1) * ROW_HEIGHT], [column * COLUMN_WIDTH, (row - 1) * ROW_HEIGHT], [column * COLUMN_WIDTH, row * ROW_HEIGHT], [(column - 1) * COLUMN_WIDTH, row * ROW_HEIGHT]], 0.5, "Black", "Gray")
                canvas.draw_text(display_board[row][column], [column * COLUMN_WIDTH - 0.5 * (COLUMN_WIDTH + frame.get_canvas_textwidth(display_board[row][column], FONT_SIZE)), row * ROW_HEIGHT - 0.75 * (ROW_HEIGHT - FONT_SIZE)], FONT_SIZE, COLORS[display_board[row][column]])
            elif display_board[row][column] == "+": #If square is losing mine,
                #Color square red and display contents
                canvas.draw_polygon([[(column - 1)* COLUMN_WIDTH, (row - 1) * ROW_HEIGHT], [column * COLUMN_WIDTH, (row - 1) * ROW_HEIGHT], [column * COLUMN_WIDTH, row * ROW_HEIGHT], [(column - 1) * COLUMN_WIDTH, row * ROW_HEIGHT]], 0.5, "Black", "Red")
                canvas.draw_text(display_board[row][column], [column * COLUMN_WIDTH - 0.5 * (COLUMN_WIDTH + frame.get_canvas_textwidth(display_board[row][column], FONT_SIZE)), row * ROW_HEIGHT - 0.75 * (ROW_HEIGHT - FONT_SIZE)], FONT_SIZE, "Black")
            elif display_board[row][column] == "F": #If square is flag,
                #Display contents
                canvas.draw_text(display_board[row][column], [column * COLUMN_WIDTH - 0.5 * (COLUMN_WIDTH + frame.get_canvas_textwidth(display_board[row][column], FONT_SIZE)), row * ROW_HEIGHT - 0.75 * (ROW_HEIGHT - FONT_SIZE)], FONT_SIZE, "Red")
    
    canvas.draw_text("Squares remaining: " + str(squares_needed), [width + 10, 20], 16, "Navy")
    canvas.draw_text("Flagging: " + str(flagging), [width + 10, 40], 16, "Maroon")
    canvas.draw_text(end_message, [width + 10, 60], 16, "Black")

#Give game instructions
input("Your goal is to clear all safe regions while avoiding mines. To clear a region, click on it. Numbers show how many neighboring regions have mines. You can toggle flagging of potential mine regions by pressing 'F' and clicking on the regions. Continue by entering anything:")

#Get number of rows, columns, and mines from user
rows = user_input("Enter valid number of rows:", 3, 30)
columns = user_input("Enter valid number of columns:", 3, 30)
squares_number = rows * columns
mines_number = user_input("Enter valid number of mines:", 1, squares_number - 1)

#Set canvas width and height
width = COLUMN_WIDTH * columns
height = ROW_HEIGHT * rows

#Create frame
frame = simplegui.create_frame("Mines", width + 180, height)

#Start game
frame.start()
generate_board()