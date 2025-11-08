import importlib
import random
import tkinter
import tkinter.ttk
from PIL import Image, ImageTk

import game_statistics
from game_statistics import statistics_list
from wordle_list import wordle_list
from allowed_words import allowed_words


def game_loop():
    """Procedure that runs the main game loop"""

    # initialise game window
    root = tkinter.Tk()
    root.title("Wordle")
    root.resizable(False, False)
    frame = tkinter.ttk.Frame(root, style="white.TFrame")
    frame.grid()

    # initialise globally-used styles
    tkinter_style = tkinter.ttk.Style()
    title_font = ("nyt-karnakcondensed", 37, "bold")
    statistics_title_font = ("nyt-karnakcondensed", 15, "bold")
    statistics_font = ("nyt-karnakcondensed", 12)

    # initialise statistics window
    statistics_root = tkinter.Toplevel()
    statistics_frame = tkinter.ttk.Frame(statistics_root, style="white.TFrame")
    statistics_root.withdraw()
    initialise_statistics(statistics_root, statistics_frame)
    update_statistics(statistics_frame)

    # add statistics component to main game window
    stats_icon = (Image.open("Icons/statistics.png"))
    stats_icon = stats_icon.resize((20, 20))
    stats_icon = ImageTk.PhotoImage(stats_icon)
    left_title_fill = tkinter.ttk.Button(frame, image=stats_icon, style="big.TButton",
                                         command=lambda: display_statistics(statistics_root))
    left_title_fill.grid(column=0, row=0, columnspan=2, padx=10, pady=10)

    # add game title to main game window
    title = tkinter.ttk.Label(frame, text="Wordle", font=title_font, style="white.TLabel")
    title.grid(column=2, row=0, sticky="n", padx=50, pady=10, columnspan=10)

    # add light/dark mode component to main game window
    dark_mode_icon = (Image.open("Icons/dark_mode_icon.png"))
    dark_mode_icon = dark_mode_icon.resize((20, 20))
    dark_mode_icon = ImageTk.PhotoImage(dark_mode_icon)
    light_mode_icon = (Image.open("Icons/light_mode_icon.png"))
    light_mode_icon = light_mode_icon.resize((20, 20))
    light_mode_icon = ImageTk.PhotoImage(light_mode_icon)
    mode_button = tkinter.ttk.Button(frame, image=dark_mode_icon, style="big.TButton")
    mode_button.grid(column=12, row=0, columnspan=2, padx=10, pady=10)
    change_mode(mode_button, light_mode_icon, dark_mode_icon, tkinter_style, statistics_font, statistics_title_font)
    mode_button["command"] = lambda: change_mode(
        mode_button, light_mode_icon, dark_mode_icon, tkinter_style, statistics_font, statistics_title_font)

    # add title seperator and gap to main game window
    title_seperator = tkinter.ttk.Separator(frame, orient="horizontal")
    title_seperator.grid(column=0, row=1, sticky="we", columnspan=14)
    title_gap = tkinter.ttk.Label(frame, style="invisible.TLabel")
    title_gap.grid(column=0, row=2, columnspan=14)

    # initialise empty boxes for the six rows of user-inputted guesses
    boxes = create_boxes(frame)

    # initialise the user guess variable as appropriate Tkinter type
    guess = tkinter.StringVar()

    # select a random word from the word list as the target word
    word = random.choice(wordle_list)

    # keep track of what letters make up the target word
    alphabet = {"A": [0], "B": [0], "C": [0], "D": [0], "E": [0], "F": [0], "G": [0], "H": [0], "I": [0], "J": [0],
                "K": [0], "L": [0], "M": [0], "N": [0], "O": [0], "P": [0], "Q": [0], "R": [0], "S": [0], "T": [0],
                "U": [0], "V": [0], "W": [0], "X": [0], "Y": [0], "Z": [0]}
    for letter in word:
        alphabet[letter][0] = word.count(letter)

    # initialise the main game loop, responding to user-inputted guesses
    message = tkinter.ttk.Label(frame, style="white.TLabel", anchor="center", text="Take a guess!")

    # initialise box for user input
    guess_entry = tkinter.ttk.Entry(frame, textvariable=guess, width=7)
    guess_entry.grid(column=5, row=9, padx=12, pady=3, columnspan=6, sticky="w")
    guess_entry.focus()

    # create the entry button for the main game window
    guess_button = tkinter.ttk.Button(frame, text="Enter", width=4, style="small.TButton",
                                      command=lambda: check_guess(guess, message, word, boxes, alphabet, guess_entry,
                                                                  guess_button, statistics_frame))
    guess_button.grid(column=9, row=9, pady=3, columnspan=6, sticky="w")

    # bind the <return> key to the entry button protocol
    guess_entry.bind("<Return>", lambda event: check_guess(guess, message, word, boxes, alphabet, guess_entry,
                                                           guess_button, statistics_frame))

    # initialise space for output for commenting on user-inputted guess
    message.grid(column=0, row=10, columnspan=14, pady=5, sticky="n")

    root.mainloop()


def check_files():
    """Procedure for checking that the user has all necessary file in the directory - error handling"""

    files = ["Icons/dark_mode_icon.png", "Icons/light_mode_icon.png", "Icons/statistics.png", "allowed_words.py",
             "game_statistics.py"]

    try:
        for file in files:
            open(file)

    except FileNotFoundError:
        print(f"'{file}' not found in directory.\nPlease make sure that all game files are present.")
        exit(1)


def initialise_statistics(statistics_root, statistics_frame):
    """Procedure that initialises the statistics pop-up window"""

    statistics_root.title("Statistics")
    statistics_root.resizable(False, False)
    statistics_frame.grid()
    statistics_title = tkinter.ttk.Label(statistics_frame, style="statistics_title.TLabel", text="Statistics")
    statistics_title.grid(column=0, row=0, sticky="n", pady=5)


def update_statistics(statistics_frame):
    """Procedure that populates the statistics window with the relevant saved data"""

    # reloads game statistics to check if a new game has been completed
    importlib.reload(game_statistics)

    labels = [
        "Total games completed",
        "1st attempt completions",
        "2nd attempt completions",
        "3rd attempt completions",
        "4th attempt completions",
        "5th attempt completions",
        "6th attempt completions",
    ]

    for i, (label_text, s) in enumerate(zip(labels, statistics_list), start=1):
        lbl = tkinter.ttk.Label(statistics_frame, style="statistics.TLabel", text=f"{label_text}: {s}")
        lbl.grid(column=0, row=i, padx=10, pady=3 if i == 1 else 0)

    # bottom filler
    tkinter.ttk.Label(statistics_frame, style="statistics.TLabel", text="").grid(column=0, row=len(labels) + 1, pady=1)


def display_statistics(statistics_root):
    """Procedure that either hides or displays the statistics pop-up window"""

    global statistics_open

    if statistics_open:
        statistics_root.withdraw()
    else:
        statistics_root.deiconify()

    statistics_open = not statistics_open


def change_mode(mode_button, light_mode_icon, dark_mode_icon, tkinter_style, statistics_font, statistics_title_font):
    """Procedure that changes all game window themes from light to dark or vice versa"""

    global light_mode

    if light_mode:
        mode_button["image"] = dark_mode_icon
        tkinter_style.theme_use("clam")
        tkinter_style.configure("white.TLabel", background="white", foreground="black")
        tkinter_style.configure("invisible.TLabel", background="white", foreground="white")
        tkinter_style.configure("unfilled.TLabel", background="white", bordercolor="#d4d6db", foreground="white")
        tkinter_style.configure("correctly_filled.TLabel", background="#6aaa64", bordercolor="#888a8c",
                                foreground="white")
        tkinter_style.configure("partially_filled.TLabel", background="#c9b458", bordercolor="#888a8c",
                                foreground="white")
        tkinter_style.configure("incorrectly_filled.TLabel", background="#787c7e", bordercolor="#888a8c",
                                foreground="white")
        tkinter_style.configure("big.TButton", background="white", font=("nyt-karnakcondensed", 10))
        tkinter_style.configure("white.TFrame", background="white")
        tkinter_style.configure("statistics.TLabel", background="white", foreground="black", font=statistics_font)
        tkinter_style.configure("statistics_title.TLabel", background="white", foreground="black",
                                font=statistics_title_font)

    else:
        mode_button["image"] = light_mode_icon
        tkinter_style.theme_use("clam")
        tkinter_style.configure("white.TLabel", background="#121213", foreground="white")
        tkinter_style.configure("invisible.TLabel", background="#121213", foreground="#121213")
        tkinter_style.configure("unfilled.TLabel", background="#121213", bordercolor="#3a3a3c", foreground="white")
        tkinter_style.configure("correctly_filled.TLabel", background="#548e4e", bordercolor="#565758",
                                foreground="white")
        tkinter_style.configure("partially_filled.TLabel", background="#b49f3b", bordercolor="#565758",
                                foreground="white")
        tkinter_style.configure("incorrectly_filled.TLabel", background="#3a3a3c", bordercolor="#565758",
                                foreground="white")
        tkinter_style.configure("big.TButton", background="white", font=("nyt-karnakcondensed", 10))
        tkinter_style.configure("white.TFrame", background="#121213")
        tkinter_style.configure("statistics.TLabel", background="#121213", foreground="white", font=statistics_font)
        tkinter_style.configure("statistics_title.TLabel", background="#121213", foreground="white",
                                font=statistics_title_font)

    light_mode = not light_mode


def check_guess(guess, message, word, boxes, alphabet, guess_entry, guess_button, statistics_frame):
    """Procedure for dealing with a user-inputted guess, updating the grid appropriately"""

    global guesses, won

    # get user input from textbox
    guess_str = str(guess.get()).upper()

    if len(guess_str) == 5 and not won and guesses < 6:
        if guess_str in allowed_words:
            guesses += 1
            # evaluate the user's guess and fill in the grid
            evaluate_word(word, alphabet, guess_str, boxes)
            # delete the user's most recent guess to leave the textbook empty for a next guess
            guess_entry.delete(0, 5)
            message["text"] = "Take a guess!"

        else:
            message["text"] = "Invalid word"
            # select the input in the textbox so that it can be replaced immediately without manual deleting
            guess_entry.select_range(0, 'end')

    # incorrect guess length
    elif len(guess_str) > 5:
        message["text"] = "Word too long"
    else:
        message["text"] = "Word too short"

    # game over procedure
    if won:
        message["text"] = f"You won! The answer was {word}."
        won_protocol(statistics_frame)
    elif guesses == 6:
        message["text"] = f"You lost! The answer was {word}."
        won = False

    if won is not None:
        # disable input to prevent further submissions
        guess_entry.config(state="disabled")
        guess_button.config(state="disabled")
        guess_entry.unbind("<Return>")
    else:
        # refocus the textbox for more user input
        guess_entry.focus()


def evaluate_word(word, alphabet, guess_str, boxes):
    """Procedure for evaluating a user-inputted word, updating the grid appropriately, assuming it is a valid word"""

    global won

    for letter in range(5):
        # flag a non-duplicate in the target word
        if len(alphabet[guess_str[letter]]) == 1:
            alphabet[guess_str[letter]].append(False)
        # flag a duplicate in the target word
        if guess_str.count(guess_str[letter]) > 1:
            # repeated character
            repeated = True
            for repeated_letter in range(5):
                # remove the status as duplicate if the duplicate has been correctly identified in the correct place
                if guess_str[repeated_letter] == word[repeated_letter] == guess_str[letter]:
                    alphabet[guess_str[letter]][0] -= 1
            alphabet[guess_str[letter]][1] = True
        else:
            # no repeated character
            repeated = False

        # green for correct letter in correct place
        if guess_str[letter] == word[letter]:
            boxes[guesses - 1][letter]["style"] = "correctly_filled.TLabel"
        # yellow for correct letter in incorrect place
        elif guess_str[letter] in word and alphabet[guess_str[letter]][0] > 0:
            boxes[guesses - 1][letter]["style"] = "partially_filled.TLabel"
            # reduce duplicate count if one duplicate has been guessed by the user (albeit in the wrong place)
            if repeated:
                alphabet[guess_str[letter]][0] -= 1
        # grey for incorrect letter altogether
        else:
            boxes[guesses - 1][letter]["style"] = "incorrectly_filled.TLabel"

        # change box style for filled in guess
        boxes[guesses - 1][letter]["relief"] = "raised"
        boxes[guesses - 1][letter]["text"] = guess_str[letter]

    # reformat the alphabet list to get rid of the flags created above (for evaluation)
    for letter in range(5):
        if len(alphabet[guess_str[letter]]) == 2:
            # get rid of the second element - the boolean flag
            alphabet[guess_str[letter]].pop(1)

    if guess_str == word:
        won = True


def won_protocol(statistics_frame):
    """Procedure for dealing with when the user has won a game"""

    # update statistics file
    with open("game_statistics.py", "w") as file:
        statistics_list[0] += 1
        statistics_list[guesses] += 1
        file.write(f"statistics_list = {statistics_list}\n")

    # update statistics window
    update_statistics(statistics_frame)


def create_boxes(frame):
    """Procedure that creates the boxes for the user input and returns a 2x2 list of references to these boxes"""

    # initialise ranges
    start_column = 2
    column_step = 2
    rows = range(3, 9)
    cols = range(5)

    boxes = []

    # populate boxes matrix, referencing the grid
    for r_index, row in enumerate(rows):
        row_boxes = []

        for c_index in cols:
            box = tkinter.ttk.Label(
                frame, borderwidth=10, relief="sunken", style="unfilled.TLabel", width=2, anchor="center")
            box.grid(column=start_column + c_index * column_step, row=row, columnspan=2, pady=3)

            row_boxes.append(box)
        boxes.append(row_boxes)

    return boxes


if __name__ == '__main__':
    # initialise global variables
    light_mode = True
    statistics_open = False
    won = None
    guesses = 0

    # check that no game files are missing
    check_files()

    # commence game loop
    game_loop()
