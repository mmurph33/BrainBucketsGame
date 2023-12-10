from cmu_graphics import *
from PIL import Image as PILImage
from tools import Button
from collections import deque
import random as rnd


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
        puzzleName = rnd.choice(["Maze"])
        self.changeState(puzzleName)

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

        self.instructions = "Press 'Space' to begin your first puzzle!"

    def draw(self):
        for i in range(len(self.messages)):
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
        if key == "space":
            self.gameApp.gameStateManager.startRandomPuzzle()


class LeaderboardState(GameState):
    def __init__(self, app):
        super().__init__(app)
        self.title = "Leaderboard"
        self.description = "Top 10 Players"

    def draw(self):
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


class TutorialState(GameState):
    def __init__(self, app):
        super().__init__(app)
        self.title = "Tutorial"
        self.description = "How to Play"

    def draw(self):
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


class MazeState(GameState):
    class Cell:
        def __init__(self, row, col, mazeState):
            self.mazeState = mazeState
            self.row = row
            self.col = col
            self.isStart = False
            self.isExit = False
            self.visited = False
            self.walls = {"top": True, "right": True, "bottom": True, "left": True}

        def __eq__(self, other):
            return (
                isinstance(other, MazeState.Cell)
                and self.row == other.row
                and self.col == other.col
            )

        def __repr__(self):
            return f"Cell({self.row}, {self.col})"

        def __hash__(self):
            return hash((self.row, self.col))

        def getCellDetails(self, row, col):
            cWidth = self.mazeState.mazeWidth // self.mazeState.cols
            cHeight = self.mazeState.mazeWidth // self.mazeState.rows
            cLeft = self.mazeState.mazeLeft + row * cWidth
            cTop = self.mazeState.mazeTop + col * cHeight
            return (cWidth, cHeight, cLeft, cTop)

        def draw(self, row, col):
            cWidth, cHeight, cLeft, cTop = self.getCellDetails(row, col)
            if self.isStart:
                drawRect(
                    cLeft + 2,
                    cTop + 2,
                    cWidth - 2,
                    cHeight - 2,
                    fill=gradient(
                        "lightBlue", "powderBlue", "paleTurquoise", start="center"
                    ),
                    opacity=50,
                )
            if self.isExit:
                drawStar(
                    cLeft + cWidth / 2,
                    cTop + cHeight / 2,
                    min(cWidth, cHeight) / 4,
                    5,
                    fill="yellow",
                    border="whiteSmoke",
                    borderWidth=1,
                    align="center",
                )
            if self.walls["top"]:
                drawLine(
                    cLeft,
                    cTop,
                    cLeft + cWidth,
                    cTop,
                    fill="whiteSmoke",
                    lineWidth=5,
                )
            if self.walls["bottom"]:
                drawLine(
                    cLeft,
                    cTop + cHeight,
                    cLeft + cWidth,
                    cTop + cHeight,
                    fill="whiteSmoke",
                    lineWidth=5,
                )
            if self.walls["left"]:
                drawLine(
                    cLeft,
                    cTop,
                    cLeft,
                    cTop + cHeight,
                    fill="whiteSmoke",
                    lineWidth=5,
                )
            if self.walls["right"]:
                drawLine(
                    cLeft + cWidth,
                    cTop,
                    cLeft + cWidth,
                    cTop + cHeight,
                    fill="whiteSmoke",
                    lineWidth=5,
                )

    def __init__(self, app):
        super().__init__(app)
        self.rows = 6
        self.cols = 6
        self.mazeWidth = self.gameApp.width // 3
        self.mazeHeight = self.gameApp.height // 3
        self.mazeLeft = self.gameApp.width // 3
        self.mazeTop = self.gameApp.height // 3
        self.directionMap = {
            (0, -1): {"delta": "top", "currentWall": "top", "nextWall": "bottom"},
            (0, 1): {"delta": "bottom", "currentWall": "bottom", "nextWall": "top"},
            (-1, 0): {"delta": "left", "currentWall": "left", "nextWall": "right"},
            (1, 0): {"delta": "right", "currentWall": "right", "nextWall": "left"},
        }
        self.maze = self.generateMaze(self.rows, self.cols)
        self.gameApp.background = gradient(
            "steelBlue", "navy", "midnightBlue", start="top"
        )

    def generateMaze(self, rows, cols):
        print("Generating maze...")
        self.maze = [[self.Cell(r, c, self) for r in range(rows)] for c in range(cols)]

        startRow, startCol = rnd.randint(0, rows - 1), rnd.randint(0, cols - 1)
        self.start = self.maze[startRow][startCol]
        self.start.isStart = True
        self.mazeBacktrack(self.start)
        self.findExit(self.start)
        print("Maze generated with start at:", startRow, startCol)
        return self.maze

    def removeWalls(self, currentCell, nextCell):
        delta = (nextCell.col - currentCell.col, nextCell.row - currentCell.row)
        if wallInfo := self.directionMap.get(delta):
            currentCell.walls[wallInfo["currentWall"]] = False
            nextCell.walls[wallInfo["nextWall"]] = False

    def getUnvisitedNeighbors(self, cell):
        neighbors = []
        for (dr, dc), _ in self.directionMap.items():
            newR = cell.row + dr
            newC = cell.col + dc
            # Check boundaries and visited status
            if (
                0 <= newR < self.rows
                and 0 <= newC < self.cols
                and not self.maze[newR][newC].visited
            ):
                neighbors.append(self.maze[newR][newC])
        return neighbors

    def findExit(self, start):
        print(f"Finding exit from start {start}")
        queue = [(start, 0)]
        visited = [[False for _ in range(self.cols)] for _ in range(self.rows)]
        visited[start.col][start.row] = True

        furthestExit = start
        furthestDistance = 0

        while queue:
            cell, distance = queue.pop(0)

            if distance > furthestDistance:
                furthestDistance = distance
                furthestExit = cell

            for neighbor in self.getValidNeighbors(cell):
                if not visited[neighbor.col][neighbor.row]:
                    visited[neighbor.col][neighbor.row] = True
                    queue.append((neighbor, distance + 1))
        furthestExit.isExit = True
        print(f"Exit found at {furthestExit} with distance {furthestDistance}")

    def mazeBacktrack(self, currentCell):
        currentCell.visited = True
        neighbors = self.getUnvisitedNeighbors(currentCell)
        rnd.shuffle(
            neighbors
        )  # Shuffle the neighbors to ensure random order of traversal

        for nextCell in neighbors:
            if not nextCell.visited:  # If the neighbor hasn't been visited
                self.removeWalls(currentCell, nextCell)
                self.mazeBacktrack(nextCell)  # Recursively visit the next cell

    def isMovePossible(self, fromCell, toCell):
        delta = (toCell.col - fromCell.col, toCell.row - fromCell.row)
        wallInfo = self.directionMap.get(delta)
        return not fromCell.walls[wallInfo["currentWall"]] if wallInfo else False

    def getValidNeighbors(self, cell):
        neighbors = []
        for direction in self.directionMap:
            dc, dr = direction
            if (
                0 <= cell.col + dc < self.cols
                and 0 <= cell.row + dr < self.rows
                and self.isMovePossible(cell, self.maze[cell.col + dc][cell.row + dr])
            ):
                neighbors.append(self.maze[cell.col + dc][cell.row + dr])
        return neighbors

    def findFastestPath(self, start, exit):
        queue = deque([(start, [start])])
        visited = {start}

        while queue:
            (cell, path) = queue.popleft()
            for neighbor in self.getValidNeighbors(cell):
                if neighbor not in visited:
                    visited.add(neighbor)
                    newPath = path + [neighbor]
                    if neighbor == exit:
                        return newPath
                    queue.append((neighbor, newPath))

    def draw(self):
        for row in range(self.rows):
            for col in range(self.cols):
                self.maze[row][col].draw(row, col)
