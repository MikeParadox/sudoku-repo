# Sudoku Solver
"""
Difficulty levels have limited amount of clues:
    easiest - no limit
    easy - 20
    medium - 10
    hard - 5
    hardest - no


"""
import random
import csv


def identify_player():
    """Authorise a player and return player's name.
    
    Authorises player's account by name and password or creates new account.
    :return: player's name
    :rtype: str
    """

    try:
        with open("users.csv", 'r') as users_file:
            pass
    except:
        with open("users.csv", 'a+') as users_file:
            writer = csv.writer(users_file, delimiter=',')
            writer.writerow(["username", "password"])

    user_password_dict = {}
    with open("users.csv", 'r') as users_file:
        reader = csv.DictReader(users_file)
        for line in reader:
            user_password_dict[line["username"]] = line["password"]
    
    is_authorisation_done = False
    player_name = ''
    while not is_authorisation_done:
        choice = input("Do you want to l)og in, c)reate new account or q)uit?  ")
        while choice != 'c' and choice != 'l':
            choice = input("Invalid input. Try again: ")
        if choice == 'c':
            player_name = input("Enter a name: ")
            while player_name in user_password_dict.keys():
                player_name = input("Sorry, but this username is already taken."
                                    " Please, choose another one: ")
            password = input("Create a password: ")
            user_password_dict[player_name] = password
            is_authorisation_done = True
            with open("users.csv", 'w') as user_file:
                user_file.write("username,password" + '\n')
                for item in user_password_dict.items():
                    user_file.write(f"{item[0]},{item[1]}" + '\n')
        else:
            player_name = input("Enter a name: ")
            if player_name in user_password_dict.keys():
                password = input("Enter your password: ")
                while (password != user_password_dict[player_name]):
                    password = input("Incorrect password. Please try again"
                                     " or hit enter to go back: ")
                    if password == '':
                        break
                if password != '':
                    is_authorisation_done = True
            else:
                print(f"There is no {player_name} in the list.")
                continue

    return player_name


def generate_inputs():
    """ Generate data for the field.
    
    :return: dictionary with data coordinates (tuples) of cells and space for data
    :rtype: dict
    """
    inputs = {}
    count = 0
    for i in range(1, 10):
        for j in range(1, 10):
            count += 1
            inputs[(i, j)] = f" "
    return inputs


def generate_uniques(inputs):
    """ Generate list of lists of all combinations which must contain unique
        numbers.
    
    :param inputs: takes all user inputs
    :type inputs: dict
    :return: list of lists of all unique combinations
    :rtype: list
    """
    cells = []
    for i in range(9):
        cells.append([])
    
    for i in range(1, 10):
        for j in range(1, 10):
            if 1 <= i < 4:
                if 1 <= j < 4:
                    cells[0].append(inputs[(i, j)])
                elif 4 <= j < 7:
                    cells[1].append(inputs[(i, j)])
                elif 7 <= j <= 9:
                    cells[2].append(inputs[(i, j)])
            elif 4 <= i < 7:
                if 1 <= j < 4:
                    cells[3].append(inputs[(i, j)])
                elif 4 <= j < 7:
                    cells[4].append(inputs[(i, j)])
                elif 7 <= j <= 9:
                    cells[5].append(inputs[(i, j)])
            elif 7 <= i <= 9:
                if 1 <= j < 4:
                    cells[6].append(inputs[(i, j)])
                elif 4 <= j < 7:
                    cells[7].append(inputs[(i, j)])
                elif 7 <= j <= 9:
                    cells[8].append(inputs[(i, j)])
    uniques = []
    for i in range(1, 10):
        horizontal_line = []
        vertical_line = []
        for j in range(1, 10):
            horizontal_line.append(inputs[(i, j)])
            vertical_line.append(inputs[(j, i)])
        uniques.append(horizontal_line)
        uniques.append(vertical_line)
    [uniques.append(i) for i in cells]
    return uniques


def print_field(inputs):
    """ Print field for a game with guessed numbers.
    
    :param inputs: takes all user inputs
    :type inputs: dict
    """
    for i in range (1, 10):
        if i == 1:
            print(46 * '-', end='')
            print ('')
        for j in range (1,10):
            print (f'| {inputs[i, j]:2} ', end='')
        print('|', end='')
        print('')
        for j in range(46):
            if i != 9:
                if j % 5 == 0:
                    print ('+', end='')
                else:
                    print ('-', end='')
                    print ('', end='')
        if i != 9:
            print ('')
    print(46 * '-')


def fill_inputs(inputs):
    """ Fill the inputs with random combination to form solved sudoku.
    
    :param inputs: takes all use inputs
    :type inputs: dict
    :return: inputs, modified to combination that is solution to game
    :rtype: dict
    """
    def fill_current_square(inputs, row, column):
        current_square = []
        while row != 1 and row != 4 and row != 7:
            row -= 1
        while column != 1 and column != 4 and column != 7:
            column -= 1
        current_square = [inputs[(i, j)] for i in range(row, row + 3)
                          for j in range(column, column + 3)]
        return current_square

    field_done = False
    filled_inputs = {}
    while(not field_done):
        figures = [i for i in range(1, 10)]
        filled_inputs = inputs.copy()
        
        temp = figures[:]
        for i in range(1, 10):
            figure = random.choice(temp)
            filled_inputs[(1, i)] = figure
            temp.remove(figure)
            
        row = 2
        
        while(row < 10):
            line_done = True
            count = 0
            temp = figures[:]
            for column in range(1, 10):
                figure = random.choice(temp)
                current_row = [filled_inputs[(row, x)] for x in range(1, column)]
                current_column = [filled_inputs[(y, column)] for y in range(1, row)]
                current_square = fill_current_square(filled_inputs, row, column)
                while(figure in current_row or figure in current_column or figure in current_square):
                    figure = random.choice(temp)
                    count += 1
                    if count == 100:
                        line_done = False
                        break
                if line_done:
                    filled_inputs[(row, column)] = figure
                    temp.remove(figure)
                else:
                    break
            if line_done:
                row += 1
            else:
                break

            if row == 9:
                field_done = True
    return filled_inputs

    #TODO function has been done and tested, just needed to provide documentation


def choose_difficulty_level():
    """ Take difficulty level from user and return number of initial figures.

    :return: number of initially given figures on the field, number of clues
             and difficulty level
    :rtype: tuple
    """
    difficulty_level = input("Choose difficulty level (1 - 5):"
                             "Remember, there is no clues in level 5: ")
    while (difficulty_level != '1' and difficulty_level != '2' and
           difficulty_level != '3' and difficulty_level != '4'
           and difficulty_level != '5'):
        difficulty_level = input("Invalid input. Please, enter again: ")
    
    num_initial_figures = 0
    num_clues = 0
    
    if difficulty_level == '1':
        num_initial_figures = 40
        num_clues = 81
    elif difficulty_level == '2':
        num_initial_figures = 35
        num_clues = 20
    elif difficulty_level == '3':
        num_initial_figures = 30
        num_clues = 10
    elif difficulty_level == '4':
        num_initial_figures = 25
        num_clues = 5
    elif difficulty_level == '5':
        num_initial_figures = 20
        num_clues = 0

    return num_initial_figures, num_clues, difficulty_level


def is_move_checking():
    """ Ask player to use auto move checking and indicate the decision.
    
    :return: indicator whether auto check is enabled
    :rtype: bool
    """
    
    choice = input("Do you need immediate wrong move indication(y/n): ")
    while(choice != 'y' and choice != 'n'):
        choice = input("Invalid input, please, try again: ")
    
    return choice


def set_up_game(inputs, filled_inputs, num_initial_figures):
    """ Fill a field with random initial numbers accordingly difficulty level.

    :param inputs: takes all user inputs
    :type inputs: dict
    :param filled_inputs: inputs with the completely solved game
    :type filled_inputs: dict
    :param num_initial_figures: num of figures initially given to a player
    :type num_initial_figures: int
    :return: modified inputs with initial play set
    :rtype: dict
    """
    
    initial_inputs = inputs.copy()
    list_of_initial_keys = list(filled_inputs.items())
    list_of_initial_keys = random.sample(list_of_initial_keys,
                                         num_initial_figures)
    
    for item in list_of_initial_keys:
        initial_inputs[item[0]] = item[1]
    
    return initial_inputs


def play_on_paper(initial_inputs, filled_inputs):
    """Make a file with the field filled with initial inputs.
    
    Makes a file with game for printing and optionally, a file with solution.
    :param initial_inputs: set of figures given by machine to start the game
    :type initial_inputs: dict
    :param filled_inputs: set of figures of solved game
    :type filled_inputs: dict
    
    """
    # TODO ask user where to save a file(cwd by default, and if it is show it)
    pass


def give_a_clue(inputs, filled_inputs):
    """ Give a random figure that has not been guessed.
    
    :param inputs: takes all user inputs
    :type inputs: dict
    :param filled_inputs: inputs with the completely solved game
    :type filled_inputs: dict
    :return: inputs with one additional figure tipped to user by machine
    :rtype: dict
    """

    while True:
        clue_key = random.choice(list(inputs.keys()))
        if inputs[clue_key] == ' ':
            inputs[clue_key] = filled_inputs[clue_key]
            return inputs


def display_solution(filled_inputs):
    """ Display filled field to player and stop the game.
    
    :param filled_inputs: inputs with the completely solved game
    :type filled_inputs: dict
    :return: indicator whether game should be stopped
    :rtype: bool
    """
    
    inp = input("Do you want to see the solution and stop the game (y, n): ")
    
    while (inp != 'y' and inp != 'n'):
        inp = input("Invalid input. Please, try again (y, n): ")
        
    if inp == 'y':
        print_field(filled_inputs)
        return True
    else:
        print("Good choice. You may use a clue instead.")
        return False


def clear_field(initial_inputs):
    """ Return the field to the initial state.
    
    :param ititial_inputs: set of figures given by machine to start the game
    :type initial_inputs: dict
    :return: initial inputs
    :rtype: dict
    """

    print("The field is cleared. Good luck that time!")
    
    return initial_inputs


def check_move(move, filled_inputs):
    """ Check if move is correct.
    
    :param move: coordinates and token for a move
    :type move: tuple
    :param filled_inputs: inputs with the completely solved game
    :type filled_inputs: dict
    :return: indicator of move correctness
    :rtype: bool
    """
    if filled_inputs[(move[0], move[1])] == move[2]:
        return True
    else:
        return False


def refresh_statistics(player_name, is_game_won):
    """ Refresh or make a record containing wins and loses of the player.

    Does nothing if a player did not enter the name
    :param player_name: name of the player
    :type player_name: str
    :param is_game_won: indicator showing whether the game is won or lost
    :type is_game_won: bool
    """
    
    if player_name == '':
        return
    
    head = ''
    stats_lines = []
    is_in_stats = False
    
    with open("statistics.csv", 'a+') as stats_file:
        pass
    
    with open("statistics.csv", 'r') as stats_file:
        stats = csv.reader(stats_file)
        try:
            head = next(stats)
            for line in stats:
                stats_lines.append(line)
        except:
            with open("statistics.csv", 'w') as stats_file:
                stats_file.write('player_name,wins,losses\n')
    
    for line in stats_lines:
        if line[0] == player_name:
            is_in_stats = True
            if is_game_won:
                line[1] = str(int(line[1]) + 1)
            else:
                line[2] = str(int(line[2]) + 1)
            break
            
    if not is_in_stats:
        if is_game_won:
            stats_lines.append([f"{player_name}", '1', '0'])
        else:
            stats_lines.append([f"{player_name}", '0', '1'])
    
    for i in range(len(stats_lines)):
        stats_lines[i] = ','.join(stats_lines[i])
    
    with open("statistics.csv", 'w') as stats_file:
        stats_file.write(','.join(head) + '\n')
        for line in stats_lines:
            stats_file.write(line + '\n')


def save_game(player_name, inputs, filled_inputs, num_clues_remained,
              difficulty_level):
    # TODO TESTS
    """ Use user's name to make a file (named after user) to resume game later.

    :param player_name: name of the player
    :type player_name: str
    :param inputs: takes all user inputs
    :type inputs: dict
    :param filled_inputs: inputs with the completely solved game
    :type filled_inputs: dict
    :param num_clues_remained: clues remained to save game moment
    :type num_clues_remained: int
    :param difficulty_level: chosen difficulty level of game
    :type difficulty_level: str
    """

    keys = list(inputs.keys())
    values = list(inputs.values())
    list_with_lines_to_save = []

    for i in range(len(inputs)):
        list_with_lines_to_save.append(f"{keys[i][0]}{keys[i][1]}{values[i]}")

    with open(f"{player_name}_initial_inputs.csv", 'w') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerow(["row", "column", "value"])
        for i in list_with_lines_to_save:
            writer.writerow(i)

    keys = list(filled_inputs.keys())
    values = list(filled_inputs.values())
    list_with_lines_to_save = []

    for i in range(len(inputs)):
        list_with_lines_to_save.append(f"{keys[i][0]}{keys[i][1]}{values[i]}")

    with open(f"{player_name}_filled_inputs.csv", 'w') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerow(["row", "column", "value"])
        for i in list_with_lines_to_save:
            writer.writerow(i)

    with open(f"{player_name}_difficulty_num_clues.txt") as file:
        file.write(f"{str(num_clues_remained)} {difficulty_level}" )


def is_game_saved(player_name):
    # TODO TESTS
    """ Check if there is a game saved by the player.
    
    :param player_name: name, the user used to save previous game
    :type player_name: str
    :return: indicator about presence of the saved game
    :rtype: bool
    """
    try:
        with open(f"{player_name}.csv", 'r') as file:
            pass
        with open(f"{player_name}_filled_inputs.csv", 'r') as file:
            pass
        with open(f"{player_name}_difficulty_num_clues.csv", 'r') as file:
            pass
        return True
    except OSError:
        return False


def continue_saved_game(player_name):
    # TODO TESTS
    """ Read file with provided name to continue the game.

    If there is no such file name, offers to enter another name or play
    new game.
    :param player_name: Name, the user used to save previous game
    :type player_name: str
    :return: tuple with inputs and filled inputs of the saved game
    :rtype: tuple
    """
    dict_inputs = {}

    with open(f"{player_name}.csv", 'r') as file:
        reader = csv.DictReader(file)
        for line in reader:
            try:
                dict_inputs[(int(line["row"]), int(line["column"]))] = int(
                    line["value"])
            except ValueError:
                dict_inputs[(int(line["row"]), int(line["column"]))] = ' '

    dict_solution = {}

    with open(f"{player_name}_filled_inputs.csv", 'r') as file:
        reader = csv.DictReader(file)
        for line in reader:
            try:
                dict_solution[(int(line["row"]), int(line["column"]))] = int(
                    line["value"])
            except ValueError:
                dict_solution[(int(line["row"]), int(line["column"]))] = ' '

    with open(f"{player_name}_difficulty_num_clues.csv", 'r') as file:
        num_clues_remained, difficulty_level = file.readline().split()
        return dict_inputs, dict_solution, num_clues_remained, difficulty_level


def undo_move(moves, inputs):
    """ Undo the last move of the player.

    :param moves: list of dicts represents all moves done by a player
    :type moves: list
    :param inputs: takes all user inputs
    :type inputs: dict
    :return: tuple with moves and inputs updated
    :rtype: tuple
    """
    inputs[moves[-1].key()] = ' '
    moves.pop()

    return (moves, inputs)


def print_num_clues(num_clues):
    """ Print number of clues left.

    :param num_clues: number of available clues
    :type num_clues: int
    """

    if num_clues:
        print(f"You have {num_clues} clues")
    else:
        print("You have no clues, good luck!")


def get_input():
    """ Take and validate input from the user.

    :return: move or command for an action
    :rtype: tuple
    """
    while (True):
        move = input("\nEnter your move by selecting row, column "
                     "and figure without whitespaces or\n"
                     "'t' for tip\n"
                     "'q' to quit\n"
                     "'r' to restart game\n"
                     "'u' to undo move\n"
                     "'a' to get a solution\n"
                     "'s' to save game to play later: ")
        if (len(move) == 1):
            if move in ('t', 'q', 'r', 'u', 'c', 'g', 's'):
                move = (move,)
                break
            else:
                print("Invalid input. Try again")
                continue
        elif len(move) == 3:
            try:
                move = (int(move[0]), int(move[1]), int(move[2]))
                if ((1 <= move[0] <= 9) and (1 <= move[1] <= 9) and
                        (1 <= move[2] <= 9)):
                    break
                else:
                    print("Please, choose a row, column and token between"
                          " 1 and 9")
                    continue
            except ValueError as v_err:
                print("Please, choose a row, column and token between"
                      " 1 and 9")
                continue
        else:
            print(
                "Please choose a square between 1 and 9 or another option")
            continue

    return move


def operate_move(move):
    """ Take the move and make changes to inputs.

    :param move: user's move
    :type move: tuple
    """
    pass


def operate_command(command):
    """ Take a command and make needed action.

    :param command: user's command
    :type command: str
    """
    pass


def play_game():
    # TODO FINISH REVISING PSEUDOCODE
    """ Provide gameplay to user and refresh the statistics.

    """

    print("Hello and welcome to our Sudoku game!")
    choose_game_mode = input("Do you want to play on paper or via computer(p/c)"
                             ": ")
    while input != 'p' and input != 'c':
        choose_game_mode = input("Invalid input, choose 'p' to play on paper, "
                                 "or 'c' to play via computer")

    if choose_game_mode == 'c':
        # player_name = identify_player() # TODO uncomment after debugging
        player_name = "Mike" # TODO delete after debugging
        if is_game_saved(player_name):
            do_continue_game = input("Do you want to continue saved game(y/n):"
                                     " ")
            while do_continue_game != 'y' and do_continue_game != 'n':
                do_continue_game = input("Invalid input, please, try again: ")
            if do_continue_game == 'n':
                do_give_up = input("Are you sure to give up?"
                                   "Game will be count as lost(y/n): ")
                while do_give_up != 'y' and do_give_up != 'n':
                    do_give_up = input("Invalid input, please, try again:"
                                       " ")
            if do_continue_game == 'y' or do_give_up == 'n':
                inputs, filled_inputs, num_clues, difficulty_level = \
                    continue_saved_game(player_name)
            else:
                # TODO count this game to statistics as lost and DELETE FILES
                inputs = generate_inputs()
                uniques = generate_uniques(inputs)
                filled_inputs = fill_inputs(inputs)
                # num_initial_figures, num_clues = choose_difficulty_level()
                # TODO uncomment after debugging
                num_initial_figures, num_clues = (20, 2)
                if num_clues != 0:
                    is_auto_checking = is_move_checking()
                initial_inputs = set_up_game(inputs, filled_inputs,
                                             num_initial_figures)
                print_field(initial_inputs)
                inputs = initial_inputs.copy()


    
    
    
    
    game_done = False #TODO think about the way to indicate that game was finished

        
# play_game()


def play_again(inputs, uniques, modified_inputs):
    """ Restart game with generating new initial figures."""
    
    pass


# TODO give different points for wins and losses in different difficulty levels