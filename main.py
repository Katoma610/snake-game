from tkinter import *
import random
import time

SEGMENT_SIZE = 20
WIDTH = 800
HEIGHT = 600
IS_IN_GAME = False
IS_IN_MENU = True


class Segment:
    def __init__(self, x, y):
        self.x1 = x
        self.y1 = y
        self.x2 = x + SEGMENT_SIZE
        self.y2 = y + SEGMENT_SIZE
        self.id = canvas.create_rectangle(self.x1, self.y1, self.x2, self.y2, fill='green', outline='black')


class Snake:
    def __init__(self, segments):
        self.segments = segments
        self.vector = {'Right': (1, 0),
                       'Left': (-1, 0),
                       'Up': (0, -1),
                       'Down': (0, 1)}
        self.allowedDirections = {'Right': ('Up', 'Down'),
                                  'Left': ('Up', 'Down'),
                                  'Up': ('Right', 'Left'),
                                  'Down': ('Right', 'Left')}
        self.direction = 'Right'

    def move(self):
        lastCoords = canvas.coords(self.segments[-1].id)
        canvas.move(self.segments[-1].id, SEGMENT_SIZE * self.vector[self.direction][0],
                    SEGMENT_SIZE * self.vector[self.direction][1])

        # Check if snake is out of the screen and, if it is, move it to the other side
        if canvas.coords(self.segments[-1].id)[2] > WIDTH or canvas.coords(self.segments[-1].id)[0] > WIDTH:
            canvas.coords(self.segments[-1].id, 0, canvas.coords(self.segments[-1].id)[1], SEGMENT_SIZE,
                          canvas.coords(self.segments[-1].id)[3])
        elif canvas.coords(self.segments[-1].id)[2] < 0 or canvas.coords(self.segments[-1].id)[0] < 0:
            canvas.coords(self.segments[-1].id, WIDTH - SEGMENT_SIZE, canvas.coords(self.segments[-1].id)[1], WIDTH,
                          canvas.coords(self.segments[-1].id)[3])
        elif canvas.coords(self.segments[-1].id)[3] < 0 or canvas.coords(self.segments[-1].id)[1] < 0:
            canvas.coords(self.segments[-1].id, canvas.coords(self.segments[-1].id)[0], HEIGHT - SEGMENT_SIZE,
                          canvas.coords(self.segments[-1].id)[2],
                          HEIGHT)
        elif canvas.coords(self.segments[-1].id)[3] > HEIGHT or canvas.coords(self.segments[-1].id)[1] > HEIGHT:
            canvas.coords(self.segments[-1].id, canvas.coords(self.segments[-1].id)[0], 0,
                          canvas.coords(self.segments[-1].id)[2],
                          SEGMENT_SIZE)

        for i in range(len(self.segments) - 2, -1, -1):
            segment = self.segments[i].id
            newLastCoords = canvas.coords(segment)
            canvas.coords(segment, lastCoords[0], lastCoords[1], lastCoords[2],
                          lastCoords[3])
            lastCoords = newLastCoords
        self.collisionCheck()

    def changeDirection(self, event):
        if event.keysym in self.allowedDirections[self.direction] and event.keysym in self.vector.keys():
            self.direction = event.keysym

    def collisionCheck(self):
        headCoords = canvas.coords(self.segments[-1].id)
        for i in range(len(apples)):
            apple = apples[i]
            if apple.x1 == headCoords[0] and apple.y1 == headCoords[1] and apple.x2 == headCoords[2] and apple.y2 == \
                    headCoords[3]:
                canvas.delete(apple.id)
                apples.pop(i)
                snakeSegments.insert(0, Segment(canvas.coords(self.segments[0].id)[0], canvas.coords(self.segments[0].id)[1]))
                scoreLabel.value += 1
                scoreLabel.update()
                addApple()

        for j in range(len(self.segments) - 1):
            segment = self.segments[j]

            if canvas.coords(segment.id) == headCoords:
                global IS_IN_GAME, IS_IN_MENU
                IS_IN_GAME = False
                IS_IN_MENU = True
                if scoreLabel.value > highScoreLabel.value:
                    highScoreLabel.value = scoreLabel.value
                    highScoreLabel.update()
                createGameOverScreen()


class Apple:
    def __init__(self, x, y):
        self.x1 = x
        self.y1 = y
        self.x2 = x + SEGMENT_SIZE
        self.y2 = y + SEGMENT_SIZE
        self.id = canvas.create_rectangle(self.x1, self.y1, self.x2, self.y2, fill='red', outline='black')


class Score:
    def __init__(self, x, y, text, value):
        self.x = x
        self.y = y
        self.text = text
        self.value = value
        self.id = canvas.create_text(x, y, fill='white', font='Arial 15', text=text + str(value))

    def update(self):
        canvas.itemconfigure(self.id, text=self.text + str(self.value))


def addApple():
    while True:
        appleFlag = True
        segmentFlag = True
        x = random.randint(0, (WIDTH - SEGMENT_SIZE) // SEGMENT_SIZE)
        y = random.randint(0, (HEIGHT - SEGMENT_SIZE) // SEGMENT_SIZE)

        for apple in apples:
            if canvas.coords(apple.id) == [x * 20, y * 20, x * 20 + SEGMENT_SIZE, y * 20 + SEGMENT_SIZE]:
                appleFlag = False
                break

        for segment in snakeSegments:
            if canvas.coords(segment.id) == [x * 20, y * 20, x * 20 + SEGMENT_SIZE, y * 20 + SEGMENT_SIZE]:
                segmentFlag = False
                break

        if appleFlag and segmentFlag:
            apples.append(Apple(x * 20, y * 20))
            return


def startGame(event=None):
    initGame()
    global IS_IN_GAME, IS_IN_MENU
    IS_IN_GAME = True
    IS_IN_MENU = False

    addApple()


def initGame():
    for apple in apples:
        canvas.delete(apple.id)
    apples.clear()

    for segment in snakeSegments:
        canvas.delete(segment.id)
    snakeSegments.clear()

    gameOverLabel.place_forget()
    menuLabel.place_forget()
    playAgainLabel.place_forget()
    closeText.place_forget()
    playText.place_forget()
    snakeLabel.place_forget()

    scoreLabel.value = 0
    scoreLabel.update()

    snakeSegments.extend([Segment(SEGMENT_SIZE, SEGMENT_SIZE),
                          Segment(SEGMENT_SIZE * 2, SEGMENT_SIZE),
                          Segment(SEGMENT_SIZE * 3, SEGMENT_SIZE),
                          Segment(SEGMENT_SIZE * 4, SEGMENT_SIZE),
                          Segment(SEGMENT_SIZE * 5, SEGMENT_SIZE)])

    snake.direction = 'Right'

    canvas.bind_all('<KeyPress>', snake.changeDirection)


def createMenu(event=None):
    global IS_IN_MENU
    IS_IN_MENU = True

    closeText.place(relx=0.5, rely=0.6, anchor=CENTER)
    playText.place(relx=0.5, rely=0.5, anchor=CENTER)
    snakeLabel.place(relx=0.5, rely=0.3, anchor=CENTER)

    gameOverLabel.place_forget()
    menuLabel.place_forget()
    playAgainLabel.place_forget()


def createGameOverScreen():
    gameOverLabel.place(relx=0.5, rely=0.3, anchor=CENTER)
    menuLabel.place(relx=0.5, rely=0.6, anchor=CENTER)
    playAgainLabel.place(relx=0.5, rely=0.5, anchor=CENTER)
    closeText.place(relx=0.5, rely=0.7, anchor=CENTER)


def close(event=None):
    global IS_IN_GAME, IS_IN_MENU
    IS_IN_GAME = False
    IS_IN_MENU = False


root = Tk()
root.title("Snake")
root.resizable(False, False)

canvas = Canvas(root, width=WIDTH, height=HEIGHT, bg="black")
canvas.pack()

apples = []
snakeSegments = [Segment(SEGMENT_SIZE, SEGMENT_SIZE),
                 Segment(SEGMENT_SIZE * 2, SEGMENT_SIZE),
                 Segment(SEGMENT_SIZE * 3, SEGMENT_SIZE),
                 Segment(SEGMENT_SIZE * 4, SEGMENT_SIZE),
                 Segment(SEGMENT_SIZE * 5, SEGMENT_SIZE)]

snake = Snake(snakeSegments)

closeText = Button(root, font=('Arial', 20), foreground='red', text='Close', bg='black', command=close, borderwidth=0)
playText = Button(root, font=('Arial', 20), foreground='red', text='Play', bg='black', command=startGame, borderwidth=0)
snakeLabel = Label(root, font=('Arial', 40), foreground='white', text='Snake Game', bg='black')

gameOverLabel = Label(root, font=('Arial', 40), foreground='white', text='Game Over', bg='black')
menuLabel = Button(root, font=('Arial', 20), foreground='red', text='Menu', bg='black', command=createMenu,
                   borderwidth=0)
playAgainLabel = Button(root, font=('Arial', 20), foreground='red', text='Play Again', bg='black', command=startGame,
                        borderwidth=0)

scoreLabel = Score(690, 20, 'Score: ', 0)
highScoreLabel = Score(690, 50, 'High Score: ', 0)

createMenu()


def main():
    while IS_IN_GAME or IS_IN_MENU:
        root.update()
        root.update_idletasks()

        if IS_IN_GAME and not IS_IN_MENU:
            time.sleep(0.1)
            snake.move()


if __name__ == '__main__':
    main()
