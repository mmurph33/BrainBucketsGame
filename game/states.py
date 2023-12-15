import logging
from cmu_graphics import *
from PIL import Image as PILImage
from tools import Button
from collections import deque
import random as rnd
import time


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

        def getCellDetails(self):
            # Ensure that mazeState is correctly used here
            cellWidth = self.mazeState.mazeWidth // self.mazeState.cols
            cellHeight = self.mazeState.mazeHeight // self.mazeState.rows
            cellLeft = self.mazeState.mazeLeft + self.col * cellWidth
            cellTop = self.mazeState.mazeTop + self.row * cellHeight
            return cellWidth, cellHeight, cellLeft, cellTop

        def draw(self):
            cellWidth, cellHeight, cellLeft, cellTop = self.getCellDetails()
            if self.isStart:
                drawRect(
                    cellLeft + 2,
                    cellTop + 2,
                    cellWidth - 2,
                    cellHeight - 2,
                    fill=gradient(
                        "lightBlue", "powderBlue", "paleTurquoise", start="center"
                    ),
                    opacity=50,
                )
            if self.isExit:
                drawStar(
                    cellLeft + cellWidth / 2,
                    cellTop + cellHeight / 2,
                    min(cellWidth, cellHeight) / 4,
                    5,
                    fill="yellow",
                    border="whiteSmoke",
                    borderWidth=1,
                    align="center",
                )
                
            wall_positions = {
                "top": (cellLeft, cellTop, cellLeft + cellWidth, cellTop),
                "bottom": (
                    cellLeft,
                    cellTop + cellHeight,
                    cellLeft + cellWidth,
                    cellTop + cellHeight,
                ),
                "left": (cellLeft, cellTop, cellLeft, cellTop + cellHeight),
                "right": (
                    cellLeft + cellWidth,
                    cellTop,
                    cellLeft + cellWidth,
                    cellTop + cellHeight,
                ),
            }
            for wall, positions in wall_positions.items():
                if self.walls[wall]:
                    drawLine(*positions, fill="whiteSmoke", lineWidth=5)

    def __init__(self, app):
        super().__init__(app)
        self.rows = 6
        self.cols = 6
        self.mazeWidth, self.mazeHeight, self.mazreLeft, self.mazeTop = (
            self.gameApp.width // 3,
        ) * 4
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
        self.dotLocation = None

    def generateMaze(self, rows, cols):
        self.maze = [[self.Cell(r, c, self) for c in range(cols)] for r in range(rows)]
        startY, startX = rnd.randint(0, rows - 1), rnd.randint(0, cols - 1)
        self.startCell = self.maze[startY][startX]
        self.dotLocation = self.dotLocation
        self.startCell.isStart = True
        self.mazeBacktracking(self.startCell)
        self.exitCell = self.findFurthestCell(self.startCell)
        self.exitCell.isExit = True
        return self.maze

    def mazeBacktracking(self, cell):
        cell.visited = True
        while neighbors := self.getUnvisitedNeighbors(cell):
            nextCell = rnd.choice(neighbors)
            self.removeWalls(cell, nextCell)
            self.mazeBacktracking(nextCell)

    def getUnvisitedNeighbors(self, cell):
        neighbors = []
        for dr, dc in self.directionMap:
            newR, newC = cell.row + dr, cell.col + dc
            if (
                0 <= newR < self.rows
                and 0 <= newC < self.cols
                and not self.maze[newR][newC].visited
            ):
                neighbors.append(self.maze[newR][newC])
        return neighbors

    def removeWalls(self, currentCell, nextCell):
        delta = (nextCell.col - currentCell.col, nextCell.row - currentCell.row)
        wallInfo = self.directionMap[delta]
        currentCell.walls[wallInfo["currentWall"]] = False
        nextCell.walls[wallInfo["nextWall"]] = False

    def getCellDetails(self, row, col):
        cellWidth = self.mazeWidth // self.cols
        cellHeight = self.mazeHeight // self.rows
        cellLeft = self.mazeLeft + col * cellWidth
        cellTop = self.mazeTop + row * cellHeight
        return cellWidth, cellHeight, cellLeft, cellTop

    def getUnvisitedNeighbors(self, cell):
        neighbors = []
        for dr, dc in self.directionMap:
            newR, newC = cell.row + dr, cell.col + dc
            if (
                0 <= newR < self.rows
                and 0 <= newC < self.cols
                and not self.maze[newR][newC].visited
            ):
                neighbors.append(self.maze[newR][newC])
        return neighbors

    def findExit(self, start):
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

    def mazeBacktrack(self, currentCell):
        currentCell.visited = True
        neighbors = self.getUnvisitedNeighbors(currentCell)

        while neighbors:
            nextCell = neighbors.pop()
            if not nextCell.visited:
                self.removeWalls(currentCell, nextCell)
                self.mazeBacktrack(nextCell)

    def findFurthestCell(self, startCell):
        queue = [(startCell, 0)]
        visited = [[False for _ in range(self.cols)] for _ in range(self.rows)]
        visited[startCell.row][startCell.col] = True

        furthestCell = startCell
        maxDistance = 0

        while queue:
            currentCell, distance = queue.pop(0)

            if distance > maxDistance:
                furthestCell = currentCell
                maxDistance = distance

            for neighbor in self.getValidNeighbors(currentCell):
                if not visited[neighbor.row][neighbor.col]:
                    queue.append((neighbor, distance + 1))
                    visited[neighbor.row][neighbor.col] = True

        return furthestCell

    def findFastestPath(self, startCell, exitCell):
        queue = deque([(startCell, [startCell])])
        visited = {startCell}

        while queue:
            cell, path = queue.popleft()
            for neighbor in self.getValidNeighbors(cell):
                if neighbor not in visited:
                    visited.add(neighbor)
                    newPath = path + [neighbor]
                    if neighbor == exitCell:
                        return newPath
                    queue.append((neighbor, newPath))

        return None

    def getValidNeighbors(self, cell):
        neighbors = []
        for direction in self.directionMap:
            dr, dc = direction
            newR, newC = cell.row + dr, cell.col + dc
            if (
                0 <= newR < self.rows
                and 0 <= newC < self.cols
                and self.isMovePossible(cell, self.maze[newR][newC])
            ):
                neighbors.append(self.maze[newR][newC])
        return neighbors

    def isMovePossible(self, fromCell, toCell):
        # This method should be updated to check if there is no wall between cells
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

    def draw(self):
        for row in range(self.rows):
            for col in range(self.cols):
                self.maze[row][col].draw()
                if (row, col) == self.dotLocation:
                    self.maze[row][col].drawDot()


# ! Maze Dynamics
# ? ------------------------------------------------------------





"""class MazeGame:
    def __init__(self, stateManager):
        app.rows = 6
        app.cols = 6
        app.mazeLeft = 250
        app.mazeTop = 250
        app.mazeWidth = 300
        app.mazeHeight = 300
        app.start = Cell(0, 0)
        app.exit = Cell(5, 5)
        app.maze = generateMaze(app.rows, app.cols)
        app.fastestPath = findFastestPath(app.maze, app.start, app.exit)
        app.dotRow = app.start.r
        app.dotCol = app.start.c
        app.startTime = None
        app.elapsedTime = None
        app.mazeCompleted = False
        app.startedMaze = False
        app.endTime = None
        app.moves = 0
        app.visitedPositions = []
        app.dotVisited = []
        app.wrongMoves = 0
        app.fewestSteps = len(app.fastestPath)
        app.background = gradient("steelBlue", "navy", "midnightBlue", start="top")


def onStep(self):
    if app.startedMaze:
        app.elapsedTime = (
            app.endTime if app.mazeCompleted else rounded(time.time() - app.startTime)
        )


def onKeyPress(self, key):
    if not app.startedMaze:
        app.startedMaze = True
        app.startTime = time.time()
    if key == "up":
        moveDot(app, -1, 0)
    elif key == "down":
        moveDot(app, 1, 0)
    elif key == "left":
        moveDot(app, 0, -1)
    elif key == "right":
        moveDot(app, 0, 1)


def moveDot(app, dRow, dCol):
    newRow = app.dotRow + dRow
    newCol = app.dotCol + dCol
    if isValidMove(app, newRow, newCol, dRow, dCol):
        app.dotVisited.append((app.dotRow, app.dotCol))
        app.dotRow, app.dotCol = newRow, newCol
        app.maze[app.dotRow][app.dotCol].visited = True
        app.visitedPositions.append((app.dotRow, app.dotCol))
        checkMazeCompletion(app)
        app.moves += 1


def isValidMove(app, newRow, newCol, dRow, dCol):
    if 0 <= newRow < app.rows and 0 <= newCol < app.cols:
        currentCell = app.maze[app.dotRow][app.dotCol]
        return not currentCell.walls[getWallDirection(dRow, dCol)]
    app.wrongMoves += 1
    return False


def getWallDirection(dRow, dCol):
    if dRow == -1:
        return "top"
    elif dRow == 1:
        return "bottom"
    elif dCol == -1:
        return "left"
    elif dCol == 1:
        return "right"


#
def checkMazeCompletion(app):
    if (app.dotRow, app.dotCol) == (app.exit.r, app.exit.c):
        app.mazeCompleted = True
        app.endTime = app.elapsedTime


def redrawAll(app):
    drawMaze(app)
    timeAdjustmentRate = 0.75
    expectedTime = app.fewestSteps * timeAdjustmentRate
    if not app.mazeCompleted:
        drawLabel(
            f"Moves: {app.moves}",
            400,
            675,
            size=25,
            fill="hotPink",
            align="center",
            font="Super Legend Boy",
        )
        drawLabel(
            f"Time: {app.elapsedTime or 0}s",
            400,
            725,
            size=25,
            fill="hotPink",
            align="center",
            font="Super Legend Boy",
        )
        drawLabel(
            f"Score: {calculateScore(app)}",
            400,
            775,
            size=25,
            fill="hotPink",
            align="center",
            font="Super Legend Boy",
        )
    else:
        drawLabel(
            f"Maze completed in {app.moves} steps and {app.elapsedTime} seconds.",
            app.width / 2,
            700,
            size=25,
            fill="hotPink",
            align="center",
            font="Super Legend Boy",
        )
        drawLabel(
            f"Score: {calculateScore(app)}",
            app.width / 2,
            750,
            size=25,
            fill="deepPink",
            align="center",
            font="Super Legend Boy",
        )
    drawLabel(
        f"Shortest Steps: {app.fewestSteps}",
        400,
        50,
        size=25,
        fill="hotPink",
        align="center",
        font="Super Legend Boy",
    )
    drawLabel(
        f"Expected Time: {expectedTime}s",
        400,
        120,
        size=25,
        fill="hotPink",
        align="center",
        font="Super Legend Boy",
    )


def drawMaze(app):
    for row in range(app.rows):
        for col in range(app.cols):
            app.maze[row][col].draw(row, col)
    drawDot(app)


def drawDot(app):
    cellLeft, cellTop = getCellLeftTop(app, app.dotRow, app.dotCol)
    cellWidth, cellHeight = getCellSize(app)
    drawCircle(
        cellLeft + cellWidth / 2,
        cellTop + cellHeight / 2,
        min(cellWidth, cellHeight) / 4,
        fill="darkViolet",
        border="darkMagenta",
        borderWidth=1,
        align="center",
    )


def calculateScore(app):
    baseScore = 800
    stepPenalty = 50
    invalidMovePenalty = 50
    timeAdjustmentRate = 0.75

    playerTime = app.elapsedTime if app.elapsedTime is not None else 0
    playerSteps = app.moves
    invalidMoves = app.wrongMoves

    expectedTime = app.fewestSteps * timeAdjustmentRate
    timeDifference = playerTime - expectedTime
    extraSteps = max(playerSteps - app.fewestSteps, 0)

    if timeDifference > 0:
        timePenalty = 25
        score = (
            baseScore
            - (timePenalty * timeDifference)
            - (stepPenalty * extraSteps)
            - (invalidMovePenalty * invalidMoves)
        )
    else:
        timeBonus = 50
        score = (
            baseScore
            + (timeBonus * abs(timeDifference))
            - (stepPenalty * extraSteps)
            - (invalidMovePenalty * invalidMoves)
        )

    return max(score, 0)


def main():
    runApp(width=800, height=800)


main()
"""