import sys
from PyQt6.QtWidgets import (QLabel, QGridLayout, QLineEdit, QSizePolicy, QGraphicsDropShadowEffect,
                             QWidget, QPushButton, QApplication, QMainWindow)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QIcon, QColor
import pandas as pd
import numpy as np

class Dashboard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("YAHTZEE")
        self.setGeometry(600,50,450,850)
        self.setWindowIcon(QIcon("yahtzee_logo.jpg"))
        self.rng = np.random.default_rng()
        self.keep = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0}
        self.turn = 0
        self.rolls = 0
        self.is_checked = False
        self.score = 0
        self.turn_score = 0
        initial = {"Turn": [], "Rolls": [], "Choice": [], "Score": []}
        self.dice_roll = self.rng.integers(1,7,5)
        self.data = pd.DataFrame(initial)
        self.init_ui()

    def init_ui(self):
        #Central Widget & Layout Object
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QGridLayout(central_widget)

        # Labels and Buttons
        self.yahtzee_label = QLabel("YAHTZEE", self)
        self.dice1_label = QLabel("1️⃣", self)
        self.dice2_label = QLabel("2️⃣", self)
        self.dice3_label = QLabel("3️⃣", self)
        self.dice4_label = QLabel("4️⃣", self)
        self.dice5_label = QLabel("5️⃣", self)
        self.tempYahtzee_label = QLabel("YAHTZEE!", self)
        self.invalidChoice_label = QLabel("Invalid Choice", self)

            #Left Column
        self.aces_button = QPushButton("Aces\n", self)
        self.twos_button = QPushButton("Twos\n", self)
        self.threes_button = QPushButton("Threes\n", self)
        self.fours_button = QPushButton("Fours\n", self)
        self.fives_button = QPushButton("Fives\n", self)
        self.sixes_button = QPushButton("Sixes\n", self)
        self.roll_button = QPushButton("Roll", self)

            #Center Column
        self.keep_dice_button = QPushButton("Keep\nDice", self)
        self.keep_dice_choice = QLineEdit(self)
        self.keep_dice_choice.setPlaceholderText("Enter Dice # (1-5)")
        self.submitDice_button = QPushButton("Submit Dice #", self)
        self.yahtzee_button = QPushButton("Yahtzee\n", self)
        self.roll_label = QLabel(self)

            #Right Column
        self.three_of_a_kind_button = QPushButton("Three of\na Kind", self)
        self.four_of_a_kind_button = QPushButton("Four of\na Kind", self)
        self.full_house_button = QPushButton("Full\nHouse", self)
        self.small_straight_button = QPushButton("Small\nStraight", self)
        self.large_straight_button = QPushButton("Large\nStraight", self)
        self.chance_button = QPushButton("Chance\n", self)
        self.scratch_button = QPushButton("Scratch", self)
        self.scratch_choice = QLineEdit(self)

            #Temp Bottom Center Column
        self.scratch_choice.setPlaceholderText("Enter Scratch Choice")
        self.submitScratch_button = QPushButton("Submit Scratch Choice", self)
        self.play_again_button = QPushButton("Play Again", self)

        #Hide Temp Labels
        self.tempYahtzee_label.hide()
        self.invalidChoice_label.hide()
        self.keep_dice_choice.hide()
        self.submitDice_button.hide()
        self.roll_label.hide()
        self.scratch_choice.hide()
        self.submitScratch_button.hide()
        self.play_again_button.hide()

        #Layout
            #Top 
        main_layout.addWidget(self.yahtzee_label, 0, 0, 1, 3)
        main_layout.addWidget(self.dice1_label, 1, 0)
        main_layout.addWidget(self.dice2_label, 1, 1)
        main_layout.addWidget(self.dice3_label, 1, 2)
        main_layout.addWidget(self.dice4_label, 2, 0)
        main_layout.addWidget(self.dice5_label, 2, 2)
        main_layout.addWidget(self.tempYahtzee_label, 2, 1)
        main_layout.addWidget(self.invalidChoice_label, 3, 0, 1, 3)

            #Bottom Left Column
        main_layout.addWidget(self.aces_button, 4, 0)
        main_layout.addWidget(self.twos_button, 5, 0)
        main_layout.addWidget(self.threes_button, 6, 0)
        main_layout.addWidget(self.fours_button, 7, 0)
        main_layout.addWidget(self.fives_button, 8, 0)
        main_layout.addWidget(self.sixes_button, 9, 0)
        main_layout.addWidget(self.roll_button, 10, 0)

            #Bottom Center Column
        main_layout.addWidget(self.keep_dice_button, 4, 1)
        main_layout.addWidget(self.keep_dice_choice, 5, 1)
        main_layout.addWidget(self.submitDice_button, 6, 1)
        main_layout.addWidget(self.yahtzee_button, 9, 1)
        main_layout.addWidget(self.roll_label, 10, 1)
        main_layout.addWidget(self.play_again_button, 10, 1)

            #Bottom Right Column
        main_layout.addWidget(self.three_of_a_kind_button, 4, 2)
        main_layout.addWidget(self.four_of_a_kind_button, 5, 2)
        main_layout.addWidget(self.full_house_button, 6, 2)
        main_layout.addWidget(self.small_straight_button, 7, 2)
        main_layout.addWidget(self.large_straight_button, 8, 2)
        main_layout.addWidget(self.chance_button, 9, 2)
        main_layout.addWidget(self.scratch_button, 10, 2)

            #Bottom Misc
        main_layout.addWidget(self.scratch_choice, 10, 1)
        main_layout.addWidget(self.submitScratch_button, 11, 1)

        #Alignment/Object Making
            #Top 
        self.yahtzee_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Maximum)
        self.yahtzee_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.dice1_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Maximum)
        self.dice1_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.dice2_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Maximum)
        self.dice2_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.dice3_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Maximum)
        self.dice3_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.dice4_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Maximum)
        self.dice4_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.dice5_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Maximum)
        self.dice5_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.tempYahtzee_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Maximum)
        self.tempYahtzee_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.invalidChoice_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Maximum)
        self.invalidChoice_label.setAlignment(Qt.AlignmentFlag.AlignCenter)     

                #Object
        self.yahtzee_label.setObjectName("yahtzee_label")
        self.dice1_label.setObjectName("dice1_label")
        self.dice2_label.setObjectName("dice2_label")
        self.dice3_label.setObjectName("dice3_label")
        self.dice4_label.setObjectName("dice4_label")
        self.dice5_label.setObjectName("dice5_label")
        self.tempYahtzee_label.setObjectName("tempYahtzee_label")
        self.invalidChoice_label.setObjectName("invalidChoice_label")

            #Bottom Left Column
        self.aces_button.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        self.aces_button.setObjectName("aces_button")
        self.twos_button.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        self.twos_button.setObjectName("twos_button")
        self.threes_button.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        self.threes_button.setObjectName("threes_button")
        self.fours_button.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        self.fours_button.setObjectName("fours_button")
        self.fives_button.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        self.fives_button.setObjectName("fives_button")
        self.sixes_button.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        self.sixes_button.setObjectName("sixes_button")
        self.roll_button.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        self.roll_button.setObjectName("roll_button")

            #Bottom Center Column
        self.keep_dice_button.setObjectName("keep_dice_button")
        self.keep_dice_choice.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Maximum)
        self.keep_dice_choice.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.keep_dice_choice.setObjectName("keep_dice_choice")
        self.submitDice_button.setObjectName("submitDice_button")
        self.yahtzee_button.setObjectName("yahtzee_button")
        self.roll_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Maximum)
        self.roll_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.roll_label.setObjectName("roll_label")

            #Bottom Right Column
        self.three_of_a_kind_button.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        self.three_of_a_kind_button.setObjectName("three_of_a_kind_button")
        self.four_of_a_kind_button.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        self.four_of_a_kind_button.setObjectName("four_of_a_kind_button")
        self.full_house_button.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        self.full_house_button.setObjectName("full_house_button")
        self.small_straight_button.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        self.small_straight_button.setObjectName("small_straight_button")
        self.large_straight_button.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        self.large_straight_button.setObjectName("large_straight_button")
        self.chance_button.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        self.chance_button.setObjectName("chance_button")
        self.scratch_button.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        self.scratch_button.setObjectName("scratch_button")

            #Bottom Misc
        self.scratch_choice.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Maximum)
        self.scratch_choice.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.scratch_choice.setObjectName("scratch_choice")
        self.submitScratch_button.setObjectName("submitScratch_button")
        self.play_again_button.setObjectName("play_again_button")

        #Style Sheet
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0,0,0,0)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)            # Softness of the shadow
        shadow.setXOffset(5)                # Horizontal position
        shadow.setYOffset(5)                # Vertical position
        shadow.setColor(QColor(0, 0, 0, 150))

        self.yahtzee_label.setGraphicsEffect(shadow)

        self.setStyleSheet("""
            QLabel, QPushButton, QLineEdit{
                font-family: calibri;
                font-weight: bold;  
                           }
            QLabel#yahtzee_label{
                font-size: 75px;
                background-color: hsl(0, 100%, 50%);
                color: white;
                border-radius: 15px;          
                font-weight: bold;
                           }
            QLabel#dice1_label, #dice2_label, #dice3_label, #dice4_label, #dice5_label{
                font-size: 100px;
                border-radius: 15px;          
                font-family: Segoe UI emoji; 
                border: none;     
                           }
            QLabel#tempYahtzee_label, #roll_label{
                font-size: 30px;
                border-radius: 15px;          
                background: transparent;
                border: none;
                color: hsl(0, 100%, 50%);
                font-weight: bold;
                           }
            QLabel#roll_label{
                font-style: italic;           
                           }
            QLabel#invalidChoice_label{
                font-size: 20px;
                background: transparent;
                border: none;
                font-weight: bold;
                padding: 2px;
                color: black;
                           }
            QPushButton{
                font-size: 25px;
                background-color: hsl(0, 0%, 100%);
                color: black;
                border-radius: 15px;
                padding: 0px;
                           }
            QPushButton:hover{
                background-color: hsl(0 , 0%, 90%);           
                           }
            QLineEdit{
                font-size: 15px;
                color: black;           
                           }
            QMainWindow{
                background-color: hsl(45, 80%, 90%);
                           }
                           """)
        
        #Button Connections
            #Left Column
        self.aces_button.clicked.connect(self.aces)
        self.twos_button.clicked.connect(self.twos)
        self.threes_button.clicked.connect(self.threes)
        self.fours_button.clicked.connect(self.fours)
        self.fives_button.clicked.connect(self.fives)
        self.sixes_button.clicked.connect(self.sixes)
        self.roll_button.clicked.connect(self.roll)

            #Center Column
        self.keep_dice_button.clicked.connect(self.keep_dice)
        self.submitDice_button.clicked.connect(self.submitDice)
        self.submitScratch_button.clicked.connect(self.submitScratch)
        self.yahtzee_button.clicked.connect(self.yahtzee)
        self.play_again_button.clicked.connect(self.play_again)

            #Right Column
        self.three_of_a_kind_button.clicked.connect(self.three_kind)
        self.four_of_a_kind_button.clicked.connect(self.four_kind)
        self.full_house_button.clicked.connect(self.full_house)
        self.small_straight_button.clicked.connect(self.small_straight)
        self.large_straight_button.clicked.connect(self.large_straight)
        self.chance_button.clicked.connect(self.chance)
        self.scratch_button.clicked.connect(self.scratch)

    def play_again(self):
        self.new_game = Dashboard()
        self.new_game.show()
        self.close()

    def end_game(self):
        top = ["aces", "twos", "threes", "fours", "fives", "sixes"]
        bonus_check = self.data.set_index("Choice")
        bonus = 35
        bot_total = 0
        top_total = 0
        for i in top:
            top_total+=int(bonus_check.loc[i,"Score"])
        if top_total >= 63:
            top_total +=bonus
        bot_total = self.score-top_total
        update = pd.DataFrame([{"Turn": np.nan, "Rolls": np.nan, "Choice": "total", "Score": self.score}])
        self.data = pd.concat([self.data, update], ignore_index=True)
        self.data.to_pickle("yahtzee_data.pkl")
        self.tempYahtzee_label.setText(f"Top: {top_total}\nBottom: {bot_total}\nScore: {self.score}")
        self.tempYahtzee_label.show()
        self.invalidChoice_label.setText("GAME OVER")
        self.invalidChoice_label.show()
        self.roll_label.hide()
        self.keep_dice_button.hide()
        self.roll_button.hide()
        self.scratch_button.hide()

        self.dice1_label.setText("6️⃣")
        self.dice2_label.setText("6️⃣")
        self.dice3_label.setText("6️⃣")
        self.dice4_label.setText("6️⃣")
        self.dice5_label.setText("6️⃣")

        self.play_again_button.show()

    def roll(self):
        if self.turn == 0:
            self.turn = 1
        if self.rolls <=2:
            self.turn_score = 0
            self.is_clicked = False
            self.rolls +=1
            self.dice_roll = self.rng.integers(1,7,5)
            if sum(self.keep.values()) > 0:
                for key, value in self.keep.items():
                    if value > 0:
                        self.dice_roll[key] = value
                self.keep = {key: 0 for key in self.keep}
            self.dice_display(self.dice_roll)
        else:
            self.invalidChoice_label.show()
            QTimer.singleShot(1250, self.invalidChoice_label.hide)

    def scratch(self):
        if self.turn >0:
            self.scratch_choice.show()
            self.submitScratch_button.show()
            self.roll_label.hide()
        else:
            self.invalidChoice_label.show()
            QTimer.singleShot(1250, self.invalidChoice_label.hide)
    
    def submitScratch(self):
        if self.turn > 0 and not self.is_clicked:
            input = str(self.scratch_choice.text().lower())
            if not (input == "roll" or input == "scratch"):
                try:
                    input = input.replace(" ", "_")
                    input += "_button"
                    button = getattr(self, input)
                    button.hide()
                    self.scratch_choice.hide()
                    self.scratch_choice.clear()
                    self.submitScratch_button.hide()
                    update = pd.DataFrame([{"Turn": self.turn, "Rolls": self.rolls, "Choice": "scratch", "Score": np.nan}])
                    self.data = pd.concat([self.data, update], ignore_index=True)
                    self.roll_label.show()
                    self.turn +=1
                    self.rolls = 0
                    self.is_clicked = True
                    if self.turn >13:
                        self.end_game()
                except:
                    self.invalidChoice_label.show()
                    QTimer.singleShot(1250, self.invalidChoice_label.hide)
            elif input == "":
                self.scratch_choice.hide()
                self.scratch_choice.clear()
                self.submitScratch_button.hide()
            else:
                self.invalidChoice_label.show()
                QTimer.singleShot(1250, self.invalidChoice_label.hide)
        else:
            self.invalidChoice_label.show()
            self.scratch_choice.hide()
            self.scratch_choice.clear()
            self.submitScratch_button.hide()
            QTimer.singleShot(1250, self.invalidChoice_label.hide)

    def aces(self):
        if self.turn > 0 and not self.is_clicked:
            self.turn_score=np.count_nonzero(self.dice_roll == 1)
            self.score += self.turn_score
            self.aces_button.hide()
            update = pd.DataFrame([{"Turn": self.turn, "Rolls": self.rolls, "Choice": "aces", "Score": self.turn_score}])
            self.data = pd.concat([self.data, update], ignore_index=True)
            self.turn +=1
            self.rolls = 0
            self.is_clicked = True
            if self.turn >13:
                self.end_game()
        else:
            self.invalidChoice_label.show()
            QTimer.singleShot(1250, self.invalidChoice_label.hide)

    def twos(self):
        if self.turn > 0 and not self.is_clicked:
            self.turn_score=2*np.count_nonzero(self.dice_roll == 2)
            self.score += self.turn_score
            self.twos_button.hide()
            update = pd.DataFrame([{"Turn": self.turn, "Rolls": self.rolls, "Choice": "twos", "Score": self.turn_score}])
            self.data = pd.concat([self.data, update], ignore_index=True)
            self.turn +=1
            self.rolls = 0
            self.is_clicked = True
            if self.turn >13:
                self.end_game()
        else:
            self.invalidChoice_label.show()
            QTimer.singleShot(1250, self.invalidChoice_label.hide)
            
    def threes(self):
        if self.turn > 0 and not self.is_clicked:
            self.turn_score=3*np.count_nonzero(self.dice_roll == 3)
            self.score += self.turn_score
            self.threes_button.hide()
            update = pd.DataFrame([{"Turn": self.turn, "Rolls": self.rolls, "Choice": "threes", "Score": self.turn_score}])
            self.data = pd.concat([self.data, update], ignore_index=True)
            self.turn +=1
            self.rolls = 0
            self.is_clicked = True
            if self.turn >13:
                self.end_game()
        else:
            self.invalidChoice_label.show()
            QTimer.singleShot(1250, self.invalidChoice_label.hide)
    
    def fours(self):
        if self.turn > 0 and not self.is_clicked:
            self.turn_score=4*np.count_nonzero(self.dice_roll == 4)
            self.score += self.turn_score
            self.fours_button.hide()
            update = pd.DataFrame([{"Turn": self.turn, "Rolls": self.rolls, "Choice": "fours", "Score": self.turn_score}])
            self.data = pd.concat([self.data, update], ignore_index=True)
            self.turn +=1
            self.rolls = 0
            self.is_clicked = True
            if self.turn >13:
                self.end_game()
        else:
            self.invalidChoice_label.show()
            QTimer.singleShot(1250, self.invalidChoice_label.hide)

    def fives(self):
        if self.turn > 0 and not self.is_clicked:
            self.turn_score=5*np.count_nonzero(self.dice_roll == 5)
            self.score += self.turn_score
            self.fives_button.hide()
            update = pd.DataFrame([{"Turn": self.turn, "Rolls": self.rolls, "Choice": "fives", "Score": self.turn_score}])
            self.data = pd.concat([self.data, update], ignore_index=True)
            self.turn +=1
            self.rolls = 0
            self.is_clicked = True
            if self.turn >13:
                self.end_game()
        else:
            self.invalidChoice_label.show()
            QTimer.singleShot(1250, self.invalidChoice_label.hide)

    def sixes(self):
        if self.turn > 0 and not self.is_clicked:
            self.turn_score=6*np.count_nonzero(self.dice_roll == 6)
            self.score += self.turn_score
            self.sixes_button.hide()
            update = pd.DataFrame([{"Turn": self.turn, "Rolls": self.rolls, "Choice": "sixes", "Score": self.turn_score}])
            self.data = pd.concat([self.data, update], ignore_index=True)
            self.turn +=1
            self.rolls = 0
            self.is_clicked = True
            if self.turn >13:
                self.end_game()
        else:
            self.invalidChoice_label.show()
            QTimer.singleShot(1250, self.invalidChoice_label.hide)

    def yahtzee(self):
        if self.turn > 0 and not self.is_clicked:
            if len(np.unique(self.dice_roll)) == 1:
                self.turn_score = 50
                self.score += self.turn_score
                self.yahtzee_button.hide()
                update = pd.DataFrame([{"Turn": self.turn, "Rolls": self.rolls, "Choice": "yahtzee", "Score": self.turn_score}])
                self.data = pd.concat([self.data, update], ignore_index=True)
                self.turn +=1
                self.rolls = 0
                self.is_clicked = True
                if self.turn >13:
                    self.end_game()
            else: 
                self.invalidChoice_label.show()
                QTimer.singleShot(1250, self.invalidChoice_label.hide)
        else:
            self.invalidChoice_label.show()
            QTimer.singleShot(1250, self.invalidChoice_label.hide)

    def three_kind(self):
        if self.turn > 0 and not self.is_clicked:
            check = np.unique(self.dice_roll)
            is_valid = False
            for num in check:
                is_valid = {num,num,num}.issubset(self.dice_roll)
                if is_valid:
                    break
            if is_valid:
                self.turn_score = sum(self.dice_roll)
                self.score +=self.turn_score
                self.three_of_a_kind_button.hide()
                update = pd.DataFrame([{"Turn": self.turn, "Rolls": self.rolls, "Choice": "three_of_a_kind", "Score": self.turn_score}])
                self.data = pd.concat([self.data, update], ignore_index=True)
                self.turn +=1
                self.rolls = 0
                self.is_clicked = True
                if self.turn >13:
                    self.end_game()
            else:
                self.invalidChoice_label.show()
                QTimer.singleShot(1250, self.invalidChoice_label.hide)
        else:
            self.invalidChoice_label.show()
            QTimer.singleShot(1250, self.invalidChoice_label.hide)
    
    def four_kind(self):
        if self.turn > 0 and not self.is_clicked:
            check = np.unique(self.dice_roll)
            is_valid = False
            for num in check:
                is_valid = {num,num,num,num}.issubset(self.dice_roll)
                if is_valid:
                    break
            if is_valid:
                self.turn_score = sum(self.dice_roll)
                self.score += self.turn_score
                self.four_of_a_kind_button.hide()
                update = pd.DataFrame([{"Turn": self.turn, "Rolls": self.rolls, "Choice": "four_of_a_kind", "Score": self.turn_score}])
                self.data = pd.concat([self.data, update], ignore_index=True)
                self.turn +=1
                self.rolls = 0
                self.is_clicked = True
                if self.turn >13:
                    self.end_game()
            else:
                self.invalidChoice_label.show()
                QTimer.singleShot(1250, self.invalidChoice_label.hide)
        else:
            self.invalidChoice_label.show()
            QTimer.singleShot(1250, self.invalidChoice_label.hide)

    def full_house(self):
        if self.turn > 0 and not self.is_clicked:
            value1 = self.dice_roll[0]
            count1 = np.count_nonzero(self.dice_roll == value1)
            if count1 == 2 or count1 == 3:
                value2 = 0
                count2 = 0
                for i in range(0,5):
                    if self.dice_roll[i] != value1:
                        value2 = self.dice_roll[i]
                        break
                count2 = np.count_nonzero(self.dice_roll == value2)
                if count1 + count2 == 5:
                    self.turn_score = 25
                    self.score +=self.turn_score
                    self.full_house_button.hide()
                    update = pd.DataFrame([{"Turn": self.turn, "Rolls": self.rolls, "Choice": "full_house", "Score": self.turn_score}])
                    self.data = pd.concat([self.data, update], ignore_index=True)
                    self.turn +=1
                    self.rolls = 0
                    self.is_clicked = True
                    if self.turn >13:
                        self.end_game()
            else:
                self.invalidChoice_label.show()
                QTimer.singleShot(1250, self.invalidChoice_label.hide)
        else:
            self.invalidChoice_label.show()
            QTimer.singleShot(1250, self.invalidChoice_label.hide)

    def small_straight(self):
        if self.turn > 0 and not self.is_clicked:
            check = np.unique(self.dice_roll)
            if ({1,2,3,4}.issubset(check) or {2,3,4,5}.issubset(check) or {3,4,5,6}.issubset(check)):
                self.turn_score = 30
                self.score += self.turn_score
                self.small_straight_button.hide()
                update = pd.DataFrame([{"Turn": self.turn, "Rolls": self.rolls, "Choice": "small_straight", "Score": self.turn_score}])
                self.data = pd.concat([self.data, update], ignore_index=True)
                self.turn += 1
                self.rolls = 0
                self.is_clicked = True
                if self.turn >13:
                    self.end_game()
            else:
                self.invalidChoice_label.show()
                QTimer.singleShot(1250, self.invalidChoice_label.hide)
        else:
            self.invalidChoice_label.show()
            QTimer.singleShot(1250, self.invalidChoice_label.hide)
    
    def large_straight(self):
        if self.turn > 0 and not self.is_clicked:
            check = np.sort(self.dice_roll)
            if ({1,2,3,4,5}.issubset(check) or {2,3,4,5,6}.issubset(check)):
                self.turn_score = 40
                self.score += self.turn_score
                self.large_straight_button.hide()
                update = pd.DataFrame([{"Turn": self.turn, "Rolls": self.rolls, "Choice": "large_straight", "Score": self.turn_score}])
                self.data = pd.concat([self.data, update], ignore_index=True)
                self.turn += 1
                self.rolls = 0
                self.is_clicked = True
                if self.turn >13:
                    self.end_game()
            else:
                self.invalidChoice_label.show()
                QTimer.singleShot(1250, self.invalidChoice_label.hide)
        else:
            self.invalidChoice_label.show()
            QTimer.singleShot(1250, self.invalidChoice_label.hide)

    def chance(self):
        if self.turn > 0 and not self.is_clicked:
            self.turn_score = sum(self.dice_roll)
            self.score += self.turn_score
            self.chance_button.hide()
            update = pd.DataFrame([{"Turn": self.turn, "Rolls": self.rolls, "Choice": "chance", "Score": self.turn_score}])
            self.data = pd.concat([self.data, update], ignore_index=True)
            self.turn +=1
            self.rolls = 0
            self.is_clicked = True
            if self.turn >13:
                self.end_game()
        else:
            self.invalidChoice_label.show()
            QTimer.singleShot(1250, self.invalidChoice_label.hide)

    def keep_dice(self):
        if self.turn >0 and self.rolls<3:
            self.keep_dice_choice.show()
            self.submitDice_button.show()
        else:
            self.invalidChoice_label.show()
            QTimer.singleShot(1250, self.invalidChoice_label.hide)

    def submitDice(self):
        index = self.keep_dice_choice.text().strip()
        if index.isdigit():
            index = int(index)-1
            try:
                self.keep.update({index: self.dice_roll[index]})
                self.keep_dice_choice.hide()
                self.keep_dice_choice.clear()
                self.submitDice_button.hide()
            except:
                self.invalidChoice_label.show()
                QTimer.singleShot(1250, self.invalidChoice_label.hide)
        elif index == "":
            self.keep_dice_choice.hide()
            self.keep_dice_choice.clear()
            self.submitDice_button.hide()
        else:
            self.invalidChoice_label.show()
            QTimer.singleShot(1250, self.invalidChoice_label.hide)

    def dice_display(self, array):
        dice_faces = {0: "", 1: "1️⃣", 2: "2️⃣", 3: "3️⃣", 4: "4️⃣", 5: "5️⃣", 6: "6️⃣"}
        for i in range(0,5):
            label = getattr(self, f"dice{i+1}_label")
            label.setText(dice_faces[array[i]])
        if len(np.unique(array)) == 1:
            self.tempYahtzee_label.show()
            QTimer.singleShot(1250, self.tempYahtzee_label.hide)
        self.roll_label.setText(f"Roll: {self.rolls}")
        self.roll_label.show()
        self.keep = {key: 0 for key in self.keep}

class main():
    app = QApplication(sys.argv)
    yahtzee_app = Dashboard()
    yahtzee_app.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
