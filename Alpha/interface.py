from tkinter import *
import StatisticalMachineTranslation

titleRow = 0
titleColumn = 0
titleRowSpan = 2
titleColumnSpan = 3

translationDirectionRow = 2
translationDirectionColumn = 0
translationDirectionRowSpan = 2
translationDirectionColumnSpan = 3

inputRow = 4
inputColumn = 0
inputRowSpan = 4
inputColumnSpan = 2

translateButtonRow = 5
translateButtonColumn = 2
translateButtonRowSpan = 2
translateButtonColumnSpan = 1

outputRow = 8
outputColumn = 0
outputRowSpan = 2
outputColumnSpan = 3

quitRow = 10
quitColumn = 0
quitRowSpan = 1
quitColumnSpan = 3

xpadding = 3
ypadding = 3

ALL=N+S+E+W

TranslationAppTitle = "Statistical Translation"
TranslationAppWidgets = {}

def Translate():
    translation = (StatisticalMachineTranslation.Translate(TranslationAppWidgets["Input"].get(1.0,END)))
    TranslationAppWidgets["Output"].insert(END,translation)
    print(translation)

'''
    All widgets are created like this:
    1. What type of widget it is.
    2. What text does the widget display.
    3. What does the widget do.
    4. Where will the widget be displayed.
'''

''' Widget Creation '''
def CreateWidgets(root):
    CreateTitleLabel(root)
    CreateTranslationDirectionLabel(root)
    CreateTranslationInputBox(root)
    CreateTranslateButton(root)
    CreateOutputBox(root)
    CreateQuitButton(root)

def CreateTitleLabel(root):
    TITLE = Label(root)
    TITLE["text"] = "Statistical Machine Translator"
    # This widget does not have a command attached
    TITLE.grid(row = titleRow, column = titleColumn, rowspan =  titleRowSpan, columnspan = titleColumnSpan, sticky = ALL, padx = xpadding, pady = ypadding)
    TranslationAppWidgets["Title"] = TITLE

def CreateTranslationDirectionLabel(root):
    DIRECTION = Label(root)
    DIRECTION["text"] = "English to Romanian"
    # This widget does not have a command attached
    DIRECTION.grid(row = translationDirectionRow, column = translationDirectionColumn, rowspan =  translationDirectionRowSpan, columnspan = translationDirectionColumnSpan, sticky = ALL, padx = xpadding, pady = ypadding)
    TranslationAppWidgets["Direction"] = DIRECTION

def CreateTranslationInputBox(root):
    INPUT = Text(root)
    INPUT.insert(END,"Input English sentence.")
    INPUT["width"] = 30
    INPUT["height"] = 10
    INPUT.focus_set() # This is not a command per se. This line ensures the input box is selected by default
    INPUT.grid(row = inputRow, column = inputColumn, rowspan = inputRowSpan, columnspan = inputColumnSpan, sticky = ALL, padx = xpadding, pady = ypadding)
    TranslationAppWidgets["Input"] = INPUT

def CreateTranslateButton(root):
    TRANSLATE = Button(root)
    TRANSLATE["text"] = "Translate"
    TRANSLATE["command"] = Translate
    TRANSLATE.grid(row = translateButtonRow, column = translateButtonColumn, rowspan =  translateButtonRowSpan, columnspan = translateButtonColumnSpan, sticky = ALL, padx = xpadding, pady = ypadding)
    TranslationAppWidgets["TranslateButton"] = TRANSLATE

def CreateOutputBox(root):
    OUTPUT = Text(root)
    OUTPUT["width"] = 30
    OUTPUT["height"] = 10
    OUTPUT["state"] = DISABLED
    OUTPUT.grid(row = outputRow, column = outputColumn, rowspan = outputRowSpan, columnspan = outputColumnSpan, sticky = ALL, padx = xpadding, pady = ypadding)
    TranslationAppWidgets["Output"] = OUTPUT

def CreateQuitButton(root):
    QUIT = Button(root)
    QUIT["text"] = "QUIT"
    QUIT["command"] = root.quit
    QUIT.grid(row = quitRow, column = quitColumn, rowspan =  quitRowSpan, columnspan = quitColumnSpan, sticky = ALL, padx = xpadding, pady = ypadding)
    TranslationAppWidgets["Quit"] = QUIT

''' Main '''
def main():
    root = Tk()
    CreateWidgets(root)
    root.title(TranslationAppTitle)
    root.mainloop()

if __name__ == "__main__":
    main()
