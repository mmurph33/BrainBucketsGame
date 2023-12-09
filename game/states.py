from cmu_graphics import *
from PIL import Image as PILImage
from tools import Button


class GameState:
    def __init__(self, app):
        self.gameApp = app

    def onStep(self):
        pass

    def draw(self):
        pass

    def onMousePress(self, mx, my):
        pass

    def onKeyPress(self, key):
        pass


class GameStateManager:
    def __init__(self):
        self.states = {}
        self.currentState = None

    def addState(self, name, state):
        self.states[name] = state

    def changeState(self, name):
        self.currentState = self.states[name]

    def startRandomPuzzle(self):
        puzzleName = random.choice["Maze", "Memory", "Logic"]

    def onStep(self):
        if self.currentState:
            self.currentState.onStep()

    def onMousePress(self, mx, my):
        if self.currentState:
            self.currentState.onMousePress(mx, my)

    def onKeyPress(self, key):
        if self.currentState:
            self.currentState.onKeyPress(key)

    def draw(self):
        if self.currentState:
            self.currentState.draw()


class MainMenuState(GameState):
    def __init__(self, app):
        super().__init__(app)
        self.title = "BrainBucket Challenge"
        self.description = "Train your Brain and your Game"

        self.buttons = [
            Button(
                app.width / 2 - 100,
                400,
                200,
                90,
                "Play",
                self.startGame,
                color="lightblue",
            ),
            Button(
                app.width / 2 - 100,
                500,
                200,
                90,
                "LeaderBoard",
                self.enterLeaderboard,
                color="lightblue",
            ),
            Button(
                app.width / 2 - 100,
                600,
                200,
                90,
                "Tutorial",
                self.enterTutorial,
                color="lightblue",
            ),
        ]

    def draw(self):
        drawImage(
            self.gameApp.bgIMG,
            0,
            0,
            width=self.gameApp.width,
            height=self.gameApp.height,
        )
        drawLabel(
            self.title,
            app.width / 2,
            100,
            size=50,
            fill=gradient("mediumSlateBlue", "mediumPurple", "blueViolet"),
            font="Super Legend Boy",
        )
        drawLabel(
            self.description,
            app.width / 2,
            150,
            size=20,
            fill=gradient("mediumSlateBlue", "mediumPurple", "blueViolet"),
            font="Super Legend Boy",
        )
        for button in self.buttons:
            button.draw()

    def onMousePress(self, mx, my):
        for button in self.buttons:
            button.onMousePress(mx, my)

    def startGame(self):
        self.gameApp.gameStateManager.changeState("StartGame")

    def enterLeaderboard(self):
        self.gameApp.gameStateManager.changeState("Leaderboard")

    def enterTutorial(self):
        self.gameApp.gameStateManager.changeState("Tutorial")


class StartGameState(GameState):
    def __init__(self, app):
        super().__init__(app)

        self.messages = [
            "Welcome to 'BrainBasket!",
            "In this game, it's not just about your skills on the court or your smarts",
            "it's about balancing both to achieve greatness!",
            "Here's how it works:",
            "Each round, you'll face a brain-teasing challenge.",
            "Solve it as quickly and accurately as you can.",
            "Your score for this task is crucial, but there's more to it.",
            "After solving the puzzle, you'll step onto the court with a basketball in hand.",
            "Your accumulated points will determine your shot accuracy.",
            "Sink the shot to keep your score!",
            "But remember, the clock is ticking!",
            "You have 2 minutes to complete as many rounds as possible and rack up the highest score you can.",
            "Are you ready to train your brain and your game?",
            "Let's hit the court and show what you're made of!",
        ]

        self.instructions = "Press 'Enter' to begin your first puzzle!"

    def draw(self):
        for i in range(self.messages):
            drawLabel(
                self.messages[i],
                440,
                50 + (65 * i),
                size=20,
                font="Super Legend Boy",
                fill="black",
            )

        drawLabel(self.instructions, 440, 850, size=20, fill="grey")

    def onKeyPress(self, key):
        if key == "Space":
            self.gameApp.gameStateManager.startRandomPuzzle()
