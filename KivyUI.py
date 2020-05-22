#This programme can be found on https://github.com/NepoBigo/TuringGame/
#Please read the readme.md attached

from kivy.uix.spinner import Spinner
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.app import App
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.config import Config

#ensure window cannot be resized so all options will be shown
#Config.set('graphics', 'resizable', False)
#Config.write()

##Defines KivyUI
#sets up drop down menu (the "columns")
class DropMenu(Spinner):
  def __init__ (self, list, **kwargs):
    super().__init__(**kwargs)
    self.text_autoupdate = True
    self.values=(list)
    
    self.size_hint=(None, None)
    self.size=(100, 44)
    self.pos_hint={'center_x': .5, 'center_y': .5}

#sets up on state (the "rows")
class StateBox(BoxLayout):
  def __init__(self, state, states, **kwargs):
    super().__init__(**kwargs)
    self.orientation = "horizontal"
    self.state = state

    #label of state machine
    self.stateLabel = Label(text = "State " + self.state, size=(100, 44))
    self.add_widget(self.stateLabel)

    #possible vals and dirs of turing machine
    vals = ["X", "0", "1"]
    dirs = ["1", "0", "-1"]
    stateList = [str(i) for i in range(states)] + ["S"]
    self.dropMenuDict = {}

    #creates a row of dropdown to programme a state
    for val in vals:

      prop = [["val", vals], ["dir", dirs], ["sta", stateList]]

      for name, menuList in prop:
        varname = name + val
        self.dropMenuDict[varname] = DropMenu(menuList)
        self.add_widget(self.dropMenuDict[varname])

#defines the app
class ConfDictMaker(App):
  
  def __init__(self, states, **kwargs):
    #initialise values
    super().__init__(**kwargs)
    self.states = states
    self.outputDict = None
    Window.size = (1000, 44*states+100)
  
  def build(self):
    self.root = BoxLayout(orientation = "vertical") #box layout for whole window
    
    #label for instruction
    self.root.add_widget(Label(text = "The Turing Machine will start from state 0. Values in the drop down menu may be hidden. Scroll after selection to see more."))

    #labels for table
    self.labels = BoxLayout(orientation = "horizontal")
    self.root.add_widget(self.labels)
    self.labels.add_widget(Label(text = "State", size=(100, 44)))
    vals = ["X", "0", "1"]
    for val in vals:

      prop = ["Write if " + val, "Move if " + val, "State if " + val]

      for Name in prop:
        self.labels.add_widget(Label(text = Name, size=(100, 44)))

    #sets up row of dropdown menu :
    self.stateDict = {}
    for state in range(self.states):
      varname = "state" + str(state)
      self.stateDict[varname] = StateBox(str(state), self.states)
      self.root.add_widget(self.stateDict[varname])

    #button to close dictionary
    self.Btn = Button(text = "Submit Configuration", on_press = self.outputAndClose)
    self.root.add_widget(self.Btn)

  #closes kivy app
  def outputAndClose(self, instance):
    App.get_running_app().stop() #closes app
  
  #on close, returns dictionary. Prevents crashing if user accidentally closes window instead
  def on_stop(self):
    self.outputDict = {} #dictionary to compile different states
    for stateMenu in self.stateDict.values():
      update = stateMenu.dropMenuDict #imports dictionary from a stateBox
      confState = {stateMenu.state: {"X": {"output": {"val": update["valX"].text, "dir": int(update["dirX"].text)}, "nextstate": update["staX"].text}, 
      "0": {"output": {"val": update["val0"].text, "dir": int(update["dir0"].text)}, "nextstate": update["sta0"].text}, 
      "1": {"output": {"val": update["val1"].text, "dir": int(update["dir1"].text)}, "nextstate": update["sta1"].text}}}
      self.outputDict.update(confState) #updates dictionary

# test = ConfDictMaker(7)
# if __name__ == '__main__':
#   test.run()
# print(test.outputDict)
