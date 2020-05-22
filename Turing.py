#This programme can be found on https://github.com/NepoBigo/TuringGame/
#Please read the readme.md attached

from libdw import sm

#Turing class: state machine at the heart of the game
class Turing(sm.SM):

  def __init__(self, confDict, state = "0", cursorNow = 0, count = 0, tape = None):
    #Starts SM with confDict
    #structure of confdict:
    #state: in it is dict for all states from 0
    #in state: in it is dict for all inputs
    #in inputs: dict for nextstate and output
    self.__confDict = confDict
    self.start_state = 0

    #initialise values
    self.__tape = tape #string of 0, 1, X and S
    self.__state = state
    if tape != None:
      self.__len = len(self.__tape)
    self.__cursorNow = cursorNow
    self.__cursorThen = 0
    self.__count = count

  def get_next_values(self, state, inp):
    #returns stop command if input or state is S:
    if inp == "S" or state == "S":

      return "S", {"val": "S", "dir": 0}

    #possible states of inp: X, 1, 0
    #reads next values, output from confDict
    nextstate = self.__confDict[state][inp]["nextstate"]

    #output is a dictionary of ["val"] and ["dir"] (direction)
    #val: 1, 0, X or S (for stop)
    #dir: -1, 0, 1
    output = self.__confDict[state][inp]["output"]

    return nextstate, output

  def step(self):
    #updates values for state, cursorNow, cursorThen and Tape during a step
    #function to get the next cursor
    def nextCursor(cursor, output):
      cursor += output["dir"]

      #ensure tape is within bounds, if not it will just repeat itself
      if cursor < 0:

        cursor = 0

      elif cursor >= self.__len:

        cursor = self.__len - 1
        
      return cursor

    #get next counter
    newState, output = self.get_next_values(self.__state, self.__tape[self.__cursorNow])

    #updates tape with corrected values
    self.__tape = self.__tape[:self.__cursorNow] + output["val"] + self.__tape[self.__cursorNow + 1:]

    #updates cursor and state values
    self.__cursorThen = self.__cursorNow
    self.__cursorNow = nextCursor(self.__cursorNow, output)
    self.__state = newState

    #adds 1 to count
    self.__count += 1

    #halts if timeout or output value or state is S (for Stop)
    if self.__count > self.__len*10 or output["val"] == "S" or self.__state == "S":

      return False

    #returns true to keep game alive
    return True

  def __str__(self):
    #output a nicely formatted string
    #see: https://ozzmaker.com/add-colour-to-text-in-python/
    #count: white text black bw \033[0;37;40m 
    #normal: black text white bw \033[0;30;47m
    #write head: white text yellow bw \033[0;30;43m
    #read head: red text white bw \033[0;31;47m
    #other comments: white text black bw \033[0;37;40m
    cursorWrite = self.__cursorThen
    cursorRead = self.__cursorNow

    count = "\033[0;37;40m#{:<4}".format(str(self.__count))
    write = self.__tape[cursorWrite]
    read = self.__tape[cursorRead]
    if self.__count == 0:
      etc = "\033[0;30;46mWrite Cursor:{} Writing: {}\033[0;37;40m State:{} \033[0;31;40mRead Cursor:{} Reading:{}\033[0;37;40m".format(
        "-", "-", self.__state, str(cursorRead), read)
    elif self.__state == "S":
      etc = "\033[0;30;46mWrite Cursor:{} Writing: {}\033[0;37;40m State:{} \033[0;31;40mRead Cursor:{} Reading:{}\033[0;37;40m".format(
        str(cursorWrite), write, self.__state, "-", "-")
    else:
      etc = "\033[0;30;46mWrite Cursor:{} Writing: {}\033[0;37;40m State:{} \033[0;31;40mRead Cursor:{} Reading:{}\033[0;37;40m".format(
        str(cursorWrite), write, self.__state, str(cursorRead), read)

    if cursorWrite == cursorRead:
      if self.__count == 0:
        T1 = "\033[0;30;47m" + self.__tape[:cursorWrite]
        T2 = "\033[0;31;47m" + write
        T3 = "\033[0;30;47m" + self.__tape[cursorWrite + 1:]
      elif self.__state == "S":
        T1 = "\033[0;30;47m" + self.__tape[:cursorWrite]
        T2 = "\033[0;30;46m" + write
        T3 = "\033[0;30;47m" + self.__tape[cursorWrite + 1:]
      else:
        T1 = "\033[0;30;47m" + self.__tape[:cursorWrite]
        T2 = "\033[0;31;46m" + write
        T3 = "\033[0;30;47m" + self.__tape[cursorWrite + 1:]
    elif cursorWrite > cursorRead:
      T1 = "\033[0;30;47m" + self.__tape[:cursorRead]
      T2 = "\033[0;31;47m" + read + "\033[0;30;46m" + write
      T3 = "\033[0;30;47m" + self.__tape[cursorWrite + 1:]
    elif cursorWrite < cursorRead:
      T1 = "\033[0;30;47m" + self.__tape[:cursorWrite]
      T2 = "\033[0;30;46m" + write + "\033[0;31;47m" + read
      T3 = "\033[0;30;47m" + self.__tape[cursorRead + 1:]

    output = "{} {}{}{}\033[0;37;40m\n      {}\033[0;37;40m".format(count, T1, T2, T3, etc)
    return output

  #to process tape and print out each step
  def run(self):
    running = True
    print(self)
    while running == True:
      running = self.step()
      print(self)

  #to process tape without printing out each step
  def quietRun(self):
    running = True
    while running == True:
      running = self.step()

  #dict to get status of Turing for testing
  def getDict(self):
    dict = {"tape": self.__tape, 
    "state": self.__state, 
    "cursorNow": self.__cursorNow, 
    "cursorThen": self.__cursorThen, #remove??
    "count" : self.__count, 
    "len": self.__len}
    
    return dict
  
  #to test if input dictionary is legitimate
  def test(self):
    try:
      for state in self.__confDict.keys():
        for inp in ["X", "0", "1"]:
          self.get_next_values(state, inp)
      return True
    except:
      return False

  @property
  def tape(self):
    return self.__tape

# gameTest = Turing(
# tape = "11110111000000S",
# confDict = {"0": {"1": {"nextstate": "0", "output": {"dir": 1, "val": "1"}}, 
# "0": {"nextstate": "1", "output": {"dir": 1, "val": "1"}}}, 
# "1": {"1": {"nextstate": "1", "output": {"dir": 1, "val": "1"}}, 
# "0": {"nextstate": "S", "output": {"dir": -1, "val": "0"}}}}
# )
# print(gameTest.getDict())
# gameTest.run()
# print(gameTest.tape)
# print(gameTest.test())

# print("XXXXXXXXXX")

# gameTest2 = Turing(
# tape = "0111111XXXXXXXXXXXX",
# confDict = {'0': {'X': {'output': {'val': '0', 'dir': 1}, 'nextstate': '0'}, '0': {'output': {'val': '0', 'dir': 1}, 'nextstate': '0'}, '1': {'output': {'val': '1', 'dir': 1}, 'nextstate': '1'}}, '1': {'X': {'output': {'val': '0', 'dir': -1}, 'nextstate': '2'}, '0': {'output': {'val': '0', 'dir': -1}, 'nextstate': '2'}, '1': {'output': {'val': '1', 'dir': 1}, 'nextstate': '1'}}, '2': {'X': {'output': {'val': 'X', 'dir': -1}, 'nextstate': '2'}, '0': {'output': {'val': '0', 'dir': 1}, 'nextstate': '6'}, '1': {'output': {'val': 'X', 'dir': 1}, 'nextstate': '3'}}, '3': {'X': {'output': {'val': 'X', 'dir': 1}, 'nextstate': '3'}, '0': {'output': {'val': '0', 'dir': 0}, 'nextstate': '4'}, '1': {'output': {'val': '1', 'dir': 1}, 'nextstate': '3'}}, '4': {'X': {'output': {'val': '1', 'dir': 0}, 'nextstate': '5'}, '0': {'output': {'val': '0', 'dir': 1}, 'nextstate': '4'}, '1': {'output': {'val': '1', 'dir': 1}, 'nextstate': '4'}}, '5': {'X': {'output': {'val': 'X', 'dir': 0}, 'nextstate': '5'}, '0': {'output': {'val': '0', 'dir': -1}, 'nextstate': '2'}, '1': {'output': {'val': '1', 'dir': -1}, 'nextstate': '5'}}, '6': {'X': {'output': {'val': '1', 'dir': 1}, 'nextstate': '6'}, '0': {'output': {'val': '0', 'dir': 0}, 'nextstate': 'S'}, '1': {'output': {'val': '1', 'dir': 1}, 'nextstate': '5'}}}
# )
# # print(gameTest2.getDict())
# gameTest2.run()
# # print(gameTest2.tape)
# # print(gameTest2.test())
