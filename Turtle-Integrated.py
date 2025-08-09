from tkinter import Tk,Frame,Canvas,Label,Button,NSEW,N,S,E,W
from turtle import TurtleScreen,RawTurtle
from random import randint
from time import time


#VARIABLES=================================
color1 = "red"
color2 = "blue"

areaColor = "black"
blockColor = "white"
blockSize = 5
targetColor = "red"
targetSize = 2
bonusColor = "blue"
bonusSize = 2

bonusDuration = 5
bonusScoreInterval = 50
bonusScoreIncrement = 20
bonusCurrentScore = 0
bonusStartingTime = 0.0
bonusOnGoing = False

pauseStartingTime = 0.0
gameStarted = False
pause = False
gameOver = False

score = 0
targetScoreIncrement = 10

rightBorder = None
leftBorder = None
topBorder = None
bottomBorder = None

speed = {"easy" : 7,"medium" : 12,"hard" : 17}
difficulty = "easy"
direction = "right"
dynamicSize = False
dynamicSpeed = False

defaultPos = [0,0]

blockPos = list(defaultPos)
targetPos = []
bonusPos = []

xCr = None
yCr = None

fingerDown = False
minSwipe = 5
swipeDuration = 5
iX = None
iY = None

cOrientation = None
aOrientation = ""

height = None
width = None


#FUNCTIONS================================
def checkOrientation(event = None):
    global cOrientation,height,width
    window.update_idletasks()
    height = window.winfo_height()
    width = window.winfo_width()
    if height > width:
        cOrientation = "portrait"
    else:
        cOrientation = "landscape"
    if cOrientation != aOrientation:
        changeLayout()

def traceFinger(event):
    global fingerDown,iX,iY,swipeStartTime
    if not fingerDown:
        iX = event.x
        iY = event.y
        swipeStartTime = time()
        fingerDown = True
    deltaX = event.x - iX
    deltaY = event.y - iY
    if (abs(deltaY) > minSwipe or abs(deltaX) > minSwipe) and (time() - swipeStartTime) <= swipeDuration:
        if abs(deltaY) >= abs(deltaX):
            if deltaY < 0:
                direct("up")
            else:
                direct("down")
        else:
            if deltaX > 0:
                direct("right")
            else:
                direct("left")
        iX = event.x
        iY = event.y
        swipeStartTime = 0.0

def findSwipe(event):
    global fingerDown
    fingerDown = False

def updateCorrection():
    global xCr,yCr,rightBorder,leftBorder,topBorder,bottomBorder
    if aOrientation == "portrait":
        xCr = 270
        yCr = -320
        rightBorder = 195 + xCr
        leftBorder = -760 + xCr
        topBorder = 1165 + yCr
        bottomBorder = -650 + yCr
    else:
        xCr = 80
        yCr = -80
        rightBorder = 760 + xCr
        leftBorder = -930 + xCr
        topBorder = 560 + yCr
        bottomBorder = -350 + yCr

def createScreen():
    global screen,block,target,bonus
    screen = TurtleScreen(turtleArea)
    block = RawTurtle(screen)
    block.up()
    target = RawTurtle(screen)
    target.hideturtle()
    target.up()
    bonus = RawTurtle(screen)
    bonus.hideturtle()
    bonus.up()
    setTurtles()

def setTurtles():
    screen.bgcolor(areaColor)
    block.color(blockColor)
    block.shapesize(blockSize)
    block.shape("turtle")
    block.speed(0)
    block.goto(blockPos[0]+xCr,blockPos[1]+yCr)
    target.color(targetColor)
    target.shapesize(targetSize)
    target.speed(0)
    target.shape("circle")
    bonus.color(bonusColor)
    bonus.shapesize(bonusSize)
    bonus.speed(0)
    bonus.shape("circle")

def bindKeys():
    window.bind("<space>",f_option)
    window.bind("w",lambda event: direct("up")) 
    window.bind("<Up>",lambda event: direct("up"))
    window.bind("s",lambda event: direct("down"))
    window.bind("<Down>",lambda event: direct("down"))
    window.bind("a",lambda event: direct("left"))
    window.bind("<Left>",lambda event: direct("left"))
    window.bind("d",lambda event: direct("right"))
    window.bind("<Right>",lambda event: direct("right"))

def direct(newDirection):
    global direction
    direction = newDirection

def animate():
    global blockPos,gameOver,score,blockSize,speed
    if not pause and not gameOver and gameStarted:
        x = blockPos[0]
        y = blockPos[1]
        if direction == "right":
            block.setheading(0)
            x += speed[difficulty]
        elif direction == "left":
            block.setheading(180)
            x -= speed[difficulty]
        elif direction == "up":
            block.setheading(90)
            y += speed[difficulty]
        else:
            block.setheading(270)
            y -= speed[difficulty]
        if y < bottomBorder or y > topBorder or x < leftBorder or x > rightBorder:
            game_over()
        else:
            if abs(blockPos[0] - targetPos[0]) < blockSize*5 and abs(blockPos[1] - targetPos[1]) < blockSize*5:
                if dynamicSize:
                    blockSize -= blockSize/10
                    block.shapesize(blockSize)
                if dynamicSpeed:
                    speed[difficulty] += speed[difficulty]/2
                score += targetScoreIncrement
                scoreMsg.config(text = f"Score: {score}")
                target.hideturtle()
                spawn_target()
        blockPos = [x,y]
        block.goto(blockPos[0]+xCr,blockPos[1]+yCr)
        window.after(17,animate)

def spawn_target():
    global targetPos
    while True:
        x = randint(leftBorder,rightBorder)
        y = randint(bottomBorder,topBorder)
        if x != blockPos[0] or y != blockPos[1]:
            targetPos = [x,y]
            break
    target.goto(targetPos[0]+xCr,targetPos[1]+yCr)
    target.showturtle()

def spawn_bonus():
    pass

def game_over():
    global gameOver
    gameOver = True
    resultScoreMsg.config(text = f"Score: {score}")
    resultPanel.grid(column = 0,row = 0,sticky = NSEW,padx = width//15,pady = height//4)
    resultPanel.lift()
    window.bind("<Return>",f_reset)



#BUTTON FUNCTIONS=========================
def f_difficulty():
    difficultyPanel.grid(column = 0,row = 1,sticky = N+W+E)

def f_easy():
    global difficulty
    difficulty = "easy"
    bn_difficulty.config(text = f"Difficulty: {difficulty}")
    difficultyPanel.grid_forget()

def f_medium():
    global difficulty
    difficulty = "medium"
    bn_difficulty.config(text = f"Difficulty: {difficulty}")
    difficultyPanel.grid_forget()

def f_hard():
    global difficulty
    difficulty = "hard"
    bn_difficulty.config(text = f"Difficulty: {difficulty}")
    difficultyPanel.grid_forget()

def f_play(event = None):
    global gameStarted
    if not gameStarted:
        gameStarted = True
        window.bind("<Return>",f_resume)
        startPanel.destroy()
        screenFrame.pack(fill = "both",expand = True)
        spawn_target()
        bindKeys()
        animate()

def f_option(event = None):
    global pause,pauseStartingTime
    if not gameOver and not pause:
        if bonusOnGoing:
            pauseStartingTime = time()
        pause = True
        optionPanel.grid(column = 0,row = 0,sticky = NSEW,padx = 200,pady = 50)
        optionPanel.lift()
        window.bind("<Right>",f_fd)
        window.bind("<Left>",f_bk)
        window.bind("<Return>",f_resume)

def f_resume(event = None):
    global pause,bonusStartingTime
    if pause:
        optionPanel.grid_forget()
        pause = False
        if bonusOnGoing:
            current_time = time()
            pause_duration = current_time - pauseStartingTime
            bonusStartingTime += pause_duration
        bindKeys()
        animate()

def f_reset(event = None):
    global pause,gameOver,score,bonusOnGoing,bonusCurrentScore,blockPos,direction
    if pause or gameOver:
        optionPanel.grid_forget()
        resultPanel.grid_forget()
        score = 0
        bonusCurrentScore = 0
        bonusOnGoing = False
        blockPos = list(defaultPos)
        direction = "right"
        block.goto(blockPos)
        spawn_target()
        pause = gameOver = False
        animate()

def f_fd(event = None):
    global difficulty
    if difficulty == "medium":
        difficulty = "hard"
    else:
        difficulty = "medium"
    optionDifficultyMsg.config(text = difficulty)

def f_bk(event = None):
    global difficulty
    if difficulty == "medium":
        difficulty = "easy"
    else:
        difficulty = "medium"
    optionDifficultyMsg.config(text = difficulty)




#===========GUI=============
def createWindow():
    global window
    window = Tk()
    window.config(bg = "black")
    window.focus_set()

def changeLayout():
    global aOrientation,gameStarted
    if gameStarted:
        f_reset()
        gameStarted = False
    for widget in window.winfo_children():
        widget.destroy()
    #FRAMES====================
    global startPanel,difficultyPanel,screenFrame,turtleFrame,sidePanel,infoPanel,buttonPanel,optionPanel,optionDifficultyPanel,resultPanel
    startPanel = Frame(window)
    startPanel.columnconfigure(0,weight = 1)
    startPanel.rowconfigure(0,weight = 1)
    startPanel.rowconfigure(1,weight = 1)

    difficultyPanel = Frame(startPanel)
    difficultyPanel.columnconfigure(0,weight = 1)

    screenFrame = Frame(window)
    
    turtleFrame = Frame(screenFrame,bg = areaColor)
    turtleFrame.columnconfigure(0,weight = 1)
    turtleFrame.rowconfigure(0,weight = 1)

    sidePanel = Frame(screenFrame,bg = "black")
    
    infoPanel = Frame(sidePanel,bg = "white")
    infoPanel.columnconfigure(0,weight = 3)
    infoPanel.rowconfigure(0,weight = 1)
    infoPanel.rowconfigure(1,weight = 1)
    infoPanel.rowconfigure(2,weight = 1)

    buttonPanel = Frame(sidePanel,bg = "white")
    buttonPanel.columnconfigure(0,weight = 1)
    buttonPanel.columnconfigure(1,weight = 1)
    buttonPanel.columnconfigure(2,weight = 1)
    buttonPanel.rowconfigure(0,weight = 1)
    buttonPanel.rowconfigure(1,weight = 1)
    buttonPanel.rowconfigure(2,weight = 1)

    optionPanel = Frame(turtleFrame,bg = "black")
    optionPanel.columnconfigure(0,weight = 1)
    optionPanel.columnconfigure(1,weight = 1)
    optionPanel.columnconfigure(2,weight = 1)
    optionPanel.columnconfigure(3,weight = 1)
    optionPanel.rowconfigure(0,weight = 1)
    optionPanel.rowconfigure(1,weight = 2)
    optionPanel.rowconfigure(2,weight = 1)
    optionPanel.rowconfigure(3,weight = 2)
    optionPanel.rowconfigure(4,weight = 1)
    optionPanel.rowconfigure(5,weight = 2)
    optionPanel.rowconfigure(6,weight = 1)
    optionPanel.rowconfigure(7,weight = 2)
    optionPanel.rowconfigure(8,weight = 1)

    optionDifficultyPanel = Frame(optionPanel,bg = "black")
    optionDifficultyPanel.columnconfigure(0,weight = 1)
    optionDifficultyPanel.columnconfigure(1,weight = 3)
    optionDifficultyPanel.columnconfigure(2,weight = 1)
    optionDifficultyPanel.rowconfigure(0,weight = 1)

    resultPanel = Frame(turtleFrame,bg = "black",border = 0)
    resultPanel.columnconfigure(0,weight = 1)
    resultPanel.columnconfigure(1,weight = 1)
    resultPanel.columnconfigure(2,weight = 1)
    resultPanel.columnconfigure(3,weight = 1)
    resultPanel.rowconfigure(0,weight = 1)
    resultPanel.rowconfigure(1,weight = 1)
    resultPanel.rowconfigure(2,weight = 1)
    resultPanel.rowconfigure(3,weight = 1)

    #CANVAS
    global turtleArea
    turtleArea = Canvas(turtleFrame)
        
    #MsgS=====================
    global scoreMsg,difficultyMsg,optionDifficultyMsg,resultMsg,resultScoreMsg
    scoreMsg = Label(infoPanel,text = f"Score: {score}",font = ("times new roman",10),fg = "white",bg = "black")
    difficultyMsg = Label(infoPanel,text = difficulty,font = ("times new roman",10),fg = "white",bg = "black")

    optionDifficultyMsg = Label(optionDifficultyPanel,text = difficulty,font = ("times new roman",15),fg = "black",bg = "white")

    resultMsg = Label(resultPanel,text = "GAME OVER!",font = ("times new roman",15,"bold"),fg = "red",bg = "black")
    resultScoreMsg = Label(resultPanel,text = f"Score: {score}",font = ("times new roman",10,"bold"),fg = "white",bg = "black")


    #BUTONS=======================
    global bn_difficulty,bn_easy,bn_medium,bn_hard,PlayBtn,optionsBtn,resumeBtn,resetBtn,quitBtn,bkBtn,fdBtn,resultResetBtn,resultQuitBtn,upBtn,downBtn,leftBtn,rightBtn
    bn_difficulty = Button(startPanel,text  = f"Difficulty: {difficulty}",fg = "green",bg = "white",command = f_difficulty)

    bn_easy = Button(difficultyPanel,text  = "easy",fg = "white",bg = "green",command = f_easy)
    bn_medium = Button(difficultyPanel,text  = "medium",fg = "white",bg = "orange",command = f_medium)
    bn_hard = Button(difficultyPanel,text  = "hard",fg = "white",bg = "red",command = f_hard)

    PlayBtn = Button(startPanel,text  = "PLAY",font = ("times new roman",20,"bold"),fg = "black",bg = "white",command = f_play)

    optionsBtn = Button(infoPanel,text  = "l l",font = ("arial",10),fg = "white",bg = "black",command = f_option)

    resumeBtn = Button(optionPanel,text = "RESUME",font = ("times new roman",15),fg = "black",bg = "white",command = f_resume)
    resetBtn = Button(optionPanel,text = "RESET",font = ("times new roman",15),fg = "black",bg = "white",command = f_reset)
    quitBtn = Button(optionPanel,text = "QUIT",font = ("times new roman",15),fg = "black",bg = "white",command = window.destroy)

    bkBtn = Button(optionDifficultyPanel,text  = "<",font = ("arial",15),fg = "black",bg = "white",command = f_bk)
    fdBtn = Button(optionDifficultyPanel,text  = ">",font = ("arial",15),fg = "black",bg = "white",command = f_fd)

    resultResetBtn = Button(resultPanel,text  = "RESET",font = ("times new roman",15),fg = "black",bg = "white",command = f_reset)
    resultQuitBtn = Button(resultPanel,text = "QUIT",font = ("times new roman",15),fg = "black",bg = "white",command = window.destroy)

    upBtn = Button(buttonPanel,text = "↑",font = ("arial",10),fg = "white",bg = "black",command = lambda: direct("up"))
    downBtn = Button(buttonPanel,text = "↓",font = ("arial",10),fg = "white",bg = "black",command = lambda: direct("down"))
    leftBtn = Button(buttonPanel,text = "←",font = ("arial",10),fg = "white",bg = "black",command = lambda: direct("left"))
    rightBtn = Button(buttonPanel,text = "→",font = ("arial",10),fg = "white",bg = "black",command = lambda: direct("right"))

    #================PLACEMENT===============
    turtleArea.grid(column = 0,row = 0,sticky = NSEW)
    #Msgs
    scoreMsg.grid(column = 0,row = 0,columnspan = 3,sticky = NSEW)
    difficultyMsg.grid(column = 0,row = 1,columnspan = 3,sticky = NSEW)

    optionDifficultyMsg.grid(column = 1,row = 0,sticky = NSEW)

    resultMsg.grid(column = 0,row = 0,columnspan = 4,rowspan = 2,sticky = NSEW)
    resultScoreMsg.grid(column = 1,row = 2,columnspan = 2,sticky = NSEW)

    #Buttons
    bn_difficulty.grid(column = 0,row = 0,sticky = N+E+W)

    bn_easy.grid(column = 0,row = 0,sticky = NSEW)
    bn_medium.grid(column = 0,row = 1,sticky = NSEW)
    bn_hard.grid(column = 0,row = 2,sticky = NSEW)

    PlayBtn.grid(column = 0,row = 1)
    optionsBtn.grid(column = 0,row = 2,sticky = NSEW)

    resumeBtn.grid(column = 1,row = 1,columnspan = 2,sticky = NSEW)
    resetBtn.grid(column = 1,row = 3,columnspan = 2,sticky = NSEW)
    quitBtn.grid(column = 1,row = 7,columnspan = 2,sticky = NSEW)

    bkBtn.grid(column = 0,row = 0,sticky = NSEW)
    fdBtn.grid(column = 2,row = 0,sticky = NSEW)

    resultResetBtn.grid(column = 0,row = 3,columnspan = 2,sticky = NSEW,padx = 20,pady = 20)
    resultQuitBtn.grid(column = 2,row = 3,columnspan = 2,sticky = NSEW,padx = 20,pady = 20)

    upBtn.grid(column = 1,row = 0,sticky = NSEW)
    downBtn.grid(column = 1,row = 2,sticky = NSEW)
    leftBtn.grid(column = 0,row = 1,sticky = NSEW)
    rightBtn.grid(column = 2,row = 1,sticky = NSEW)
    
    
    startPanel.pack(fill = "both",expand = True)
    optionDifficultyPanel.grid(column = 1,row = 5,columnspan = 2,sticky = NSEW)
    turtleFrame.grid(column = 0,row = 0,sticky = NSEW)
    infoPanel.grid(column = 0,row = 0,sticky = NSEW)
    
    if cOrientation == "portrait":
        screenFrame.columnconfigure(0,weight = 1)
        screenFrame.rowconfigure(0,weight = 200)
        screenFrame.rowconfigure(1,weight = 1)
        sidePanel.columnconfigure(0,weight = 2)
        sidePanel.columnconfigure(1,weight = 1)
        sidePanel.rowconfigure(0,weight = 1)
        sidePanel.grid(column = 0,row = 1,sticky = NSEW)
        buttonPanel.grid(column = 1,row = 0,sticky = NSEW)
    else:
        screenFrame.columnconfigure(0,weight = 100)
        screenFrame.columnconfigure(1,weight = 1)
        screenFrame.rowconfigure(0,weight = 1)
        sidePanel.columnconfigure(0,weight = 1)
        sidePanel.rowconfigure(0,weight = 2)
        sidePanel.rowconfigure(1,weight = 1)
        sidePanel.grid(column = 1,row = 0,sticky = NSEW)
        buttonPanel.grid(column = 0,row = 1,sticky = NSEW)
    aOrientation = cOrientation
    updateCorrection()
    createScreen()

createWindow()
checkOrientation()
window.bind("<Return>",f_play)
window.bind("<Configure>",checkOrientation)
turtleArea.focus_set()
turtleArea.bind("<B1-Motion>",traceFinger)
turtleArea.bind("<ButtonRelease-1>",findSwipe)
window.mainloop()
