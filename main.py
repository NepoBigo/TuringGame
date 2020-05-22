#This programme was written by Ng Ri Chi (1004143, CC06) for the DW Final Assignment.
#Please read the readme.md attached

from Turing import Turing
from KivyUI import ConfDictMaker
import os
import ast
import pprint

#ensure working directory is the same as where the files are
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

#helps Kivy to reset so window can be opened again after its closed
def reset():
  import kivy.core.window as window
  from kivy.base import EventLoop
  if not EventLoop.event_listeners:
    from kivy.cache import Cache
  window.Window = window.core_select_lib('window', window.window_impl, True)
  Cache.print_usage()
  for cat in Cache._categories:
    Cache._objects[cat] = {}


#handles the run of each game
class Game():

  def __init__(self, kwargs):
    self.__Description = kwargs["Description"] #description of game
    #The following 3 inputs also accept None
    self.__ModelDict = kwargs["ModelDict"] #to calculate model answer to check if user has correct input
    self.__States = kwargs["States"] #set number of states in Turing Machine
    self.__Tape = kwargs["Tape"] #Allows for model tape
    self.__UserDict = None

  #function to get tape from user
  def getTape(self, tapeInput = None):
    #function to get input from user
    def getInput(text):
      return input(text)
    #sorts out if tape is already given as input
    if tapeInput == None:
      prompt = "Please enter your tape with the following symbols:\nX for blank, 0 and 1 only\nIf you want the turing machine to terminate at the end of the tape write S as the last character\nIf not it will loop at the last cell: "
      tape = ""
      status = "Check"
    else:
      tape = tapeInput
      status = "MainCheck"
    #checks if things are correct
    while status != "Pass":
      #prompts user to enter tape
      if status == "Check":
        tape = getInput(prompt)
        status = "MainCheck"
      #check if tape is correctly entered
      if status == "MainCheck":
        tape = tape.upper()
        sCheck = False
        for letter in tape:
          #if S is not the last character
          if sCheck == True:
            status = "Check"
            prompt = "Please ensure S only appears as the last character:"
            break
          #ensures only permitted letters exists
          elif letter == "0" or letter == "1" or letter == "X":
            pass
          #if S is detected, the status will be flaged
          elif letter == "S":
            sCheck = True
          #rejects other inputs
          else:
            status = "Check"
            prompt = "Please only enter X, 0 or 1. \nIf you want the turing machine to terminate at the end of the tape write S as the last character\nIf not it will loop at the last cell:"
            pass
        #if status remains as MainCheck it means that it has passed all checks
        if status == "MainCheck":
          status = "Pass"
      #ensures tape is not empty
      if tape == "":
        status = "Check"
        prompt = "Please type something in the input: "
    return tape

  #function to get confDict from user
  def getDict(self, status):
    global winOpened
    winOpened = False #to state if Kivy UI is used
    #launches kivy GUI
    def gui():
      global winOpened
      winOpened = True #states that window was opened
      print("Opening GUI template")
      window = ConfDictMaker(self.__States)
      if __name__ == '__main__':
        window.run()
      return window.outputDict
    #if user just press enter, GUI is launched
    if status == "":
      #opens up ConfDictMaker to allow user to enter dictionary
      output = gui()
    #if user inputs any other text, launcher will get dict from textfile
    else:
      f = open("confDict.txt", "r")
      StrUserInput = f.read().strip("\n")
      f.close()
      print("We found the file!\n" + StrUserInput)
      output = ast.literal_eval(StrUserInput)
      #ensures input is correct, if not GUI launcher is launched
      dictTest = Turing(output).test()
      if dictTest == False:
        print("The input is incompatible. Please use the GUI template")
        output = gui()
    return output

  def run(self):
    print("Let's start! Here is the challenge:\n\n" + self.__Description + "\n")
    
    #displays tape, and seeks user input to enter/overwrite tape
    if self.__Tape == None:
      self.__Tape = self.getTape()
    else:
      print("Here is the tape that is provided for this challenge:")
      print(self.__Tape)
      userInput = input("Press ENTER to accept the given tape, or enter your own tape to overwrite it: ")
      if userInput == "":
        pass
      else:
        self.__Tape = self.getTape(userInput)

    #visually confirms tape to user and prompts input of dictionary
    print("Alright, the following tape will be used:\n\n\033[0;30;47m" + self.__Tape + "\033[0;37;40m\n\n")
    print("Here is a reminder of your challenge:\n\n" + self.__Description + "\n\n")

    #Allows user to input States if it is not given
    if self.__States == None:
      display = "Please input the number of states for the Turing Machine:"
      correct = False
      while correct == False:
        userInput = input(display)
        try: 
          self.__States = int(userInput)
          correct = True
        except:
          display = "Please only input numbers:"
      print("The Turing machine will have " + str(self.__States) + " inputs\n\n")

    #prompt to get tape from dictionary
    print("You can enter the turing machine configuration dictionary into the file confDict.txt or use the GUI template\n\nTips for configuring: \n1) Structure of the dictionary is as follows:\n    State that is being defined\n     'output'\n      'val': Value to be written\n      'dir': Direction of movement. -1 moves head left left, 0 is no movement, 1 is to the right\n     'nextstate' gives us the next state\n2) It is recommended to modify a dictionary made by the GUI template\n")
    UserInput = input("Press ENTER to use the GUI helper or enter some characters to use the confDict.txt: ")
    
    #gets dictionary
    self.__UserDict = self.getDict(UserInput)

    #confirms dictionary
    print("\nThe following dictionary was entered\n")
    pprint.pprint(self.__UserDict)

    #asks if user wants to save dictionary for later use
    userInput = input("Enter SAVE to save this into confDict.txt to modify it on a text editor for the next run, or ENTER to go to the next step: ")
    if userInput.upper() == "SAVE":
      try:
        f = open("confDict.txt", "w")
        f.write(pprint.pformat(self.__UserDict))
        f.close()
        print("Save complete")
      except:
        print("Sorry there was an error")

    #turing machine finally starts
    input("\n\nPress ENTER to start the Turing Machine!")

    User = Turing(
    tape = self.__Tape,
    confDict = self.__UserDict
    )
    User.run()
    print("\nFinal output is:\n\033[0;30;47m" + User.tape + "\033[0;37;40m\n\nInitial input is\n\033[0;30;47m" + self.__Tape + "\033[0;37;40m\n") #prints out final and initial results

    #if a model confDict is available, check if its correct. If it is, congrajulates the user, else encourage the user to try again
    if self.__ModelDict != None:
      Model = Turing(
      tape = self.__Tape,
      confDict = self.__ModelDict
      )
      Model.quietRun()
      print("Model output is:" + "\n\033[0;30;47m" + Model.tape + "\033[0;37;40m\n")

      if Model.tape == User.tape:
        print("Congratulations! Your machine is correct!")
      else:
        print("The output is incorrect. But no problem, you can try again :)")
    
    #returns to main menu. Also allows the user to see result before Kivy reset spams the screen
    input("\nPress ENTER to return to main menu\n")

#import game config from file
f = open("confGame.txt", "r")
confGame = f.readlines()
f.close()

#loads menu from file
menuItems = {}
for game in confGame:
  if game[0] == "#":
    pass
  else:
    dictIN = ast.literal_eval(game)
    num = str(len(menuItems))
    title = dictIN.pop("Title")
    menuItems.update({num: {"Title": title, "Game": dictIN}})

#exit option
exitNum = str(len(menuItems))
menuItems.update({exitNum: {"Title": "Exit", "Game": None}})

#Prints title sequence
turingTitle = "\n___________           .__                   ________                       \n\__    ___/_ _________|__| ____    ____    /  _____/_____    _____   ____  \n  |    | |  |  \_  __ \  |/    \  / ___\  /   \  ___\__  \  /     \_/ __ \ \n  |    | |  |  /|  | \/  |   |  \/ /_/  > \    \_\  \/ __ \|  Y Y  \  ___/ \n  |____| |____/ |__|  |__|___|  /\___  /   \______  (____  /__|_|  /\___  >\n                              \//_____/           \/     \/      \/     \/ \n"
wikipedia = "\n\na mathematical model of computation that defines an abstract machine, which manipulates symbols on a strip of tape according to a table of rules. Despite the model's simplicity, given any computer algorithm, a Turing machine capable of simulating that algorithm's logic can be constructed"
print("\n\nWelcome to the" + turingTitle + "Here we will explore the turing machine, described by Wikipedia as" + wikipedia)

#sets up menu in the game
status = "Menu"
while status != "Exit":
  if status == "Menu":
  #prints out menu according to menuItems
    print("\nTHE TURING GAME\n\n  Main Menu:\n")
    for game in menuItems:
      print("\033[0;37;40m  {:<4}  {}".format(game, menuItems[game]["Title"]))
    
    gameChoice = None
    userInput = input("\nPlease enter your option: ") #gets user choice of game
    while gameChoice == None: #ensures input is correct and sets gameChoice and status accordingly
      if userInput in menuItems.keys():
        gameChoice = userInput
        status = "Game"
        if userInput == exitNum:
          status = "Exit"
        else:
          status = "Game"
      else:
        userInput = input("\nSorry your input is invalid. Please only input the numbers in the main menu: ")
  
  #runs game and resets kivy after each run
  if status == "Game": #enters game mode
    print("\nYou have chosen option " + str(gameChoice))
    play = Game(menuItems[gameChoice]["Game"])
    play.run()
    del play
    if winOpened == True:
      reset()
      winOpened == False
    status = "Menu"

#allows player to exit game
print("\n\nHope you have had fun. See you soon!\n\n")
exit()