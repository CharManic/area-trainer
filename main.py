# Summer work completed. 🎉🎉

# Imports
import tkinter as tk
import math
import random
from ctypes import windll

# -------------------------------------

# Makes text and other widgets look less ugly.
windll.shcore.SetProcessDpiAwareness(1)


# -------------------------------------

# Trainer Class
class Trainer(tk.Tk):
    def __init__(self):
        """Sets up the initial window, widgets, and attributes for the Trainer."""

        super().__init__()

        self.title("Area Trainer")

        # Attributes
        self.attempts = 0
        self.score = 0
        self.chosenShape = 0

        self.username = ""
        self.password = ""

        self.radioButtons = []

        self.mainFrame = tk.Frame()
        self.mainFrame.pack(fill='both', expand=True)

        self.titleLabel = tk.Label(self.mainFrame)

        self.errorLabel = tk.Label(self.mainFrame,
                                   font=("Helvetica", 11, "bold"))

        self.usernameEntry = tk.Entry(self.mainFrame,
                                      fg="grey",
                                      width=50,
                                      font=("Helvetica", 11))
        self.passwordEntry = tk.Entry(self.mainFrame,
                                      fg="grey",
                                      width=50,
                                      font=("Helvetica", 11))

        self.submitButton = tk.Button(self.mainFrame,
                                      text="Submit",
                                      font=("Helvetica", 10, "bold"))

        self.quitButton = tk.Button(self.mainFrame,
                                    font=("Helvetica", 10, "bold"))

        self.centreWindow()
        self.resizable(False, False)

    def loginMenu(self):
        """Sets up login menu, allows user to input a username and password of existing account, or create a new one."""

        # Title
        self.titleLabel.pack(pady=55)
        self.titleLabel.config(text="Area Trainer",
                               font=("Arial", 22, "bold"))

        # Divider
        dividerCanvas = tk.Canvas(self.mainFrame,
                                  height=5,
                                  width=self.winfo_width())
        dividerCanvas.create_line(50, 2, 450, 2, width=2)

        dividerCanvas.pack(pady=(0, 50))

        # Username Entry
        self.usernameEntry.insert(0, "Username")
        self.usernameEntry.bind("<FocusIn>", lambda event: self.focusIn(event, True))
        self.usernameEntry.bind("<FocusOut>", lambda event: self.focusOut(event, True))
        self.bind_all("<Button-1>", lambda event: event.widget.focus_set())

        self.usernameEntry.pack(padx=100, pady=(0, 10))

        # Password Entry
        self.passwordEntry.insert(0, "Password")
        self.passwordEntry.bind("<FocusIn>", lambda event: self.focusIn(event, False))
        self.passwordEntry.bind("<FocusOut>", lambda event: self.focusOut(event, False))

        self.passwordEntry.pack(padx=100, pady=(0, 35))

        # Error Message Label
        self.errorLabel.pack()

        # Login Button
        loginButton = tk.Button(self.mainFrame,
                                text="Login",
                                command=self.login,
                                font=("Helvetica", 10, "bold"))

        loginButton.pack(pady=(10, 25))

        # Setup Button
        setupButton = tk.Button(self.mainFrame,
                                text="Create new account",
                                command=lambda: [loginButton.destroy(), setupButton.destroy(), self.setup()],
                                font=("Helvetica", 10, "bold"))

        setupButton.pack()

    def centreWindow(self):
        """Centres Trainer window."""

        # Finds screen dimensions.
        screenHeight = self.winfo_screenheight()
        screenWidth = self.winfo_screenwidth()

        # Repositions window.
        self.geometry(f"500x500+{(screenWidth - 500) // 2}+{(screenHeight - 500) // 2}")
        self.update_idletasks()

    def focusIn(self, _, isUsername):
        """Allows for default text to be removed when entry is selected. Will not change if the entry holds an input."""

        # Checks whether the entry is usernameEntry or passwordEntry.
        if isUsername:
            entry = self.usernameEntry
        else:
            entry = self.passwordEntry

        # Checks to see whether the user has inputted anything.
        if entry["fg"] == "grey":
            entry.delete(0, tk.END)
            entry.config(fg="black")

    def focusOut(self, _, isUsername):
        """Allows for default text to be displayed when entry is not selected. Will not change if the entry holds an
        input."""

        # Checks whether the entry is usernameEntry or passwordEntry.
        if isUsername:
            entry = self.usernameEntry
            text = "Username"
        else:
            entry = self.passwordEntry
            text = "Password"

        # Checks to see whether the user has inputted anything.
        if not entry.get():
            entry.delete(0, tk.END)
            entry.config(fg="grey")
            entry.insert(0, text)

    def setup(self):
        """Sets up account creation window."""

        # Setup Label
        setupLabel = tk.Label(self.mainFrame,
                              font=("Helvetica", 11, "bold"),
                              text="Please enter a username and a strong password.")

        setupLabel.pack(pady=(0, 10))

        # Create Account Button
        createAccButton = tk.Button(self.mainFrame,
                                    text="Create",
                                    command=self.createAccount,
                                    font=("Helvetica", 10, "bold"))

        createAccButton.pack()

    def createAccount(self):
        """Creates a new account if inputs fit the checked criteria."""

        self.username = self.usernameEntry.get()
        self.password = self.passwordEntry.get()

        # Check inputs.
        inputFlags = self.inputChecker()

        if all(inputFlags):
            fileEmpty = False
            # Check if file is empty or not (to ensure correct formatting).
            with open("accounts.txt", "r") as file:
                if file.readline() == "":
                    fileEmpty = True

            # Write username and password to file.
            file = open("accounts.txt", "a")
            if not fileEmpty:
                file.write("\n")
            file.write(self.username + "," + self.password + ",")
            file.close()
            self.areaTrainer()

        else:
            # Nothing has been inputted.
            if not inputFlags[0]:
                self.errorLabel.config(text="Please enter a valid username and password.")

            # Password is not of a suitable length.
            if not inputFlags[1]:
                self.errorLabel.config(text="Password must be longer than 5 characters.")

            # Password does not have any digits or symbols.
            if not inputFlags[2] or not inputFlags[3]:
                self.errorLabel.config(text="Password must contain numbers and symbols.")

            # Username has been taken.
            if not inputFlags[4]:
                self.errorLabel.config(text="Username has been taken.")

    def inputChecker(self):
        """Checks to see if the user has inputted anything, if the password is strong enough, and if the username is
        available."""

        # Flags
        isInputted = False
        passwordLong = False
        hasNumbers = False
        hasSymbols = False

        # Check if username and password have been inputted.
        if ((self.username and self.password) and
                (self.usernameEntry["fg"] != "grey" and self.passwordEntry["fg"] != "grey")):
            isInputted = False

        # Check if password is of suitable length.
        if len(self.password) >= 6:
            passwordLong = True

        # Check if password has numbers AND symbols - implemented separately to ensure both character types are present.
        if not self.password.isalpha():
            hasNumbers = True
        if not self.password.isalnum():
            hasSymbols = True

        # Check if username has been taken.
        userAvailable = True
        try:
            file = open("accounts.txt", "r")
            for line in file:
                takenUsername = line[0:line.index(",")]
                if self.username == takenUsername:
                    userAvailable = False
            file.close()

        except FileNotFoundError:
            # No other usernames exist, thus nothing needs to happen.
            pass

        return isInputted, passwordLong, hasNumbers, hasSymbols, userAvailable

    def areaTrainer(self):
        """Sets up a window with options to practise area calculations, see session history, or to close the window."""

        self.score = 0

        # Unpack everything from previous interface
        for widget in self.mainFrame.winfo_children():
            widget.pack_forget()

        # Set up label to welcome the user.
        welcomeLabel = tk.Label(self.mainFrame,
                                height=3,
                                text=f"Welcome, {self.username}!",
                                font=("Arial", 17, "bold"))
        welcomeLabel.pack()

        # Set up label.
        shapesLabel = tk.Label(self.mainFrame,
                               text=f"Choose the shape you wish to practise:",
                               font=("Arial", 16, "bold"))
        shapesLabel.pack(pady=(0, 20))

        # Set up buttons corresponding to each shape (triangle, rectangle, trapezium, circle).
        triangleButton = tk.Button(self.mainFrame,
                                   text="Triangle",
                                   width=20,
                                   borderwidth=5,
                                   command=lambda: self.shapesPractice(0),
                                   font=("Helvetica", 14, "bold"))

        rectangleButton = tk.Button(self.mainFrame,
                                    text="Rectangle",
                                    width=20,
                                    borderwidth=5,
                                    command=lambda: self.shapesPractice(1),
                                    font=("Helvetica", 14, "bold"))

        trapeziumButton = tk.Button(self.mainFrame,
                                    text="Trapezium",
                                    width=20,
                                    borderwidth=5,
                                    command=lambda: self.shapesPractice(2),
                                    font=("Helvetica", 14, "bold"))

        circleButton = tk.Button(self.mainFrame,
                                 text="Circle",
                                 width=20,
                                 borderwidth=5,
                                 command=lambda: self.shapesPractice(3),
                                 font=("Helvetica", 14, "bold"))

        triangleButton.pack(pady=10)
        rectangleButton.pack(pady=10)
        trapeziumButton.pack(pady=10)
        circleButton.pack(pady=10)

        # Set up button linked to session history.
        historyButton = tk.Button(self.mainFrame,
                                  text="Session History",
                                  font=("Helvetica", 10, "bold"),
                                  command=self.history)
        historyButton.pack()

        # Set up quit button.
        self.quitButton.pack(pady=10)
        self.quitButton.config(text="Quit Trainer",
                               command=root.destroy)

    def shapesPractice(self, num):
        """Sets up a window that presents the user with initial side values and asks for their area (integer
        answers)."""

        # 0 is triangle, 1 is rectangle, etc.
        self.chosenShape = num

        for widget in self.mainFrame.winfo_children():
            widget.pack_forget()

        # Calculation variables
        area = 0
        height = 0
        base2 = 0

        # Radius / Base Value
        base = random.randint(1, 20)

        # Height Value (for triangle, rectangle, and trapezium)
        if self.chosenShape == 0 or self.chosenShape == 1 or self.chosenShape == 2:
            height = random.randint(1, 20)

        # Second Base Value (for trapezium)
        if self.chosenShape == 2:
            base2 = random.randint(1, 20)

        # Initialise labels.
        dimensionsLabel = tk.Label(self.mainFrame,
                                   font=("Arial", 16, "bold"))
        calculateLabel = tk.Label(self.mainFrame,
                                  font=("Arial", 16, "bold"))

        dimensionsLabel.pack(pady=(20, 0))
        calculateLabel.pack()

        # Area Calculations / Label

        match self.chosenShape:
            # Triangle: A = 0.5 * b * h
            case 0:
                area = int(round(0.5 * base * height, 0))
                dimensionsLabel.config(text=f"b = {base}; h = {height}.")
                calculateLabel.config(text="Calculate the area of the triangle!")

            # Rectangle: A = b * h
            case 1:
                area = base * height
                dimensionsLabel.config(text=f"b = {base}; h = {height}.")
                calculateLabel.config(text="Calculate the area of the rectangle!")

            # Trapezium: A = (a + b) / 2 * h
            case 2:
                area = int(round(0.5 * (base + base2) * height, 0))
                dimensionsLabel.config(text=f"a = {base}; b = {base2}; h = {height}.")
                calculateLabel.config(text="Calculate the area of the trapezium!")

            # Circle: A = pi * r^2
            case 3:
                area = int(round(math.pi * (base ** 2), 0))
                dimensionsLabel.config(text=f"r = {base}")
                calculateLabel.config(text="Calculate the area of the circle!")

        # Generate random area values relatively close to actual value.
        areaAnswers = [area]
        for i in range(0, 3):
            randArea = area
            # Loop is only broken when the random area is not already in the list.
            while randArea in areaAnswers:
                randArea = random.randint(int(area * 0.5), int(area * 1.5))
            areaAnswers.append(randArea)

        random.shuffle(areaAnswers)
        chosenAnswer = tk.IntVar(self.mainFrame, 10000)

        self.radioButtons.clear()

        # Generate radio buttons with area values.
        for i in range(0, len(areaAnswers)):
            radio = tk.Radiobutton(self.mainFrame,
                                   text=areaAnswers[i],
                                   value=areaAnswers[i],
                                   variable=chosenAnswer,
                                   padx=20,
                                   font=("Arial", 12),
                                   justify=tk.LEFT,
                                   tristatevalue=i)
            self.radioButtons.append(radio)
            radio.pack(pady=(20, 0))

        # Set up feedback label that displays whether the user got the answer correct or not after submitted.
        feedbackLabel = tk.Label(self.mainFrame,
                                 font=("Helvetica", 12))
        feedbackLabel.pack(pady=10)

        # Set up submit button.
        self.submitButton.pack(pady=(20, 0))
        self.submitButton.config(command=lambda: self.checkAnswer(feedbackLabel,
                                                                  chosenAnswer.get(),
                                                                  area))

    def checkAnswer(self, label, userAnswer, answer):
        """Checks to see if inputted answer is correct, awarding score depending on the number of attempts."""

        questionDone = False

        # Check if a radio has been selected. If not, raise the issue.
        if userAnswer == 10000:
            label.config(text="Please select one of the provided answers.")

        # Chosen answer is incorrect.
        elif answer != userAnswer:
            self.attempts += 1

            if self.attempts < 2:
                label.config(text="Not quite. Try again!")

            # User has run out of tries.
            else:
                label.config(text=f"The answer was {answer}. Better luck next time! Score: {self.score}")
                questionDone = True

        # Chosen answer is correct.
        else:
            # +2 score if done in 1 attempt.
            if self.attempts == 0:
                self.score += 2

            # +1 score if done in 2 attempts.
            else:
                self.score += 1
            label.config(text=f"Correct! The answer was {answer}. Score: {self.score}")

            questionDone = True

        # Show buttons to let the user try another question, or quit the trainer and return to the main menu.
        if questionDone:
            self.attempts = 0
            self.submitButton.config(text="Next Question", command=lambda: self.shapesPractice(self.chosenShape))

            # Set up quit session button.
            self.quitButton.pack(pady=15)
            self.quitButton.config(text="Quit Session",
                                   command=self.saveScore)

            # Disable radio buttons.
            for radio in self.radioButtons:
                radio.configure(state=tk.DISABLED)

    def login(self):
        """Checks inputted information against that in the accounts.txt file to determine if the user can access
        their account."""

        # Retrieve username and password
        self.username = self.usernameEntry.get()
        self.password = self.passwordEntry.get()
        try:
            file = open("accounts.txt", "r")
            loggedIn = False
            for line in file:
                # Lines in accounts.txt are formatted as "username,password,score1,score2,score3 [and so on]".
                # Retrieves username from line.

                retrievedUsername = line[0:line.index(",")]
                # Retrieve password by first removing the username section, and then removing the scores.
                retrievedPassword = line[line.index(",") + 1:][:line[line.index(",") + 1:].index(",")]
                # Authenticate user.
                if self.username == retrievedUsername:
                    if self.password == retrievedPassword:
                        loggedIn = True
                        break

            if loggedIn:
                self.areaTrainer()
            else:
                self.errorLabel.config(text="User not found.")

        # If the accounts.txt file does not exist, the account cannot be retrieved and so the user must make one.
        except FileNotFoundError:
            self.errorLabel.config(text="No accounts exist. Please create a new account.")

    def saveScore(self):
        """Adds score values to accounts.txt file besides the user's account information."""

        # Retrieve lines from accounts.txt.
        with open("accounts.txt", "r") as file:
            lines = file.readlines()

        # Look for the current user in the file.
        for i in range(len(lines)):
            takenLine = lines[i]

            # Slice the line as to only obtain the username.
            takenUsername = takenLine[0:takenLine.index(",")]

            # Remove the new line from the end of the line and add the session score to it, before updating the file.
            if self.username == takenUsername:
                takenLine = takenLine[:-1]
                takenLine += f"{self.score},\n"
                lines[i] = takenLine
                break

        # Update the file.
        with open("accounts.txt", "w") as file:
            file.writelines(lines)
        self.areaTrainer()

    def history(self):
        """Displays session history with previous scores."""

        for widget in self.mainFrame.winfo_children():
            widget.pack_forget()

        # Set up title label.
        self.titleLabel.pack()
        self.titleLabel.config(text="Session History",
                               font=("Arial", 16, "bold"))

        historyText = tk.Text(self.mainFrame)

        sessionHistory = []

        # Find scores of the current user's sessions.
        with open("accounts.txt", "r") as file:
            for line in file:
                takenUsername = line[0:line.index(",")]
                if self.username == takenUsername:
                    # Slice after the password and before the new line character at the end of the line.
                    sessionHistory = line[len(self.username) + len(self.password) + 1:-1].split(",")

        # Remove empty strings from the start and end of the list.
        sessionHistory.pop(0)
        sessionHistory.pop(-1)

        # Add session numbers and scores to list.
        for i in range(len(sessionHistory)):
            sessionHistory[i] = f"Session {i + 1}: {sessionHistory[i]}"

        # Add list to the text widget.
        historyString = "\n".join(sessionHistory)
        historyText.insert("1.0", historyString)

        historyText.pack(pady=10, padx=10, fill="both", expand=True)

        # Add scrollbar to account for a large number of sessions
        scrollbar = tk.Scrollbar(historyText)
        scrollbar.pack(side=tk.RIGHT,
                       fill=tk.Y)
        
        # Add back button.
        self.quitButton.pack(pady=10)
        self.quitButton.config(text="Back",
                               command=self.areaTrainer)


# -------------------------------------

# Main Program

# Initialises object and starts trainer.
ROOT = Trainer()
ROOT.loginMenu()
ROOT.mainloop()
