from PIL import Image as PILImage
from cmu_graphics import *
from states import GameStateManager, MainMenuState, GameState
from tools import Button


def gameConfiguration(app):
    app.stepsPerSecond = 100
    app.gameStateManager = GameStateManager()
    app.gameStateManager.addState("MainMenu", MainMenuState(app))


def appMedia(app):
    app.courtIMG = PILImage.open(
        "content/court_img.png"
    )  # https://www.midjourney.com/jobs/0eb2e5ce-8c84-4f7f-b669-3edfe68f05d3?index=0
    app.courtIMG = CMUImage(app.courtIMG)
    app.bgIMG = PILImage.open(
        "content/main_menu.png"
    )  # https://www.midjourney.com/jobs/7e2bb4f1-96c3-4ce6-bb99-ae0232a18993?index=1
    app.bgIMG = CMUImage(app.bgIMG)


def onAppStart(app):
    gameConfiguration(app)
    appMedia(app)
    app.gameStateManager.changeState("MainMenu")


def onStep(app):
    app.gameStateManager.onStep()


def onMousePress(app, mouseX, mouseY):
    app.gameStateManager.onMousePress(mouseX, mouseY)


def onKeyPress(app, key):
    app.gameStateManager.onKeyPress(key)


def redrawAll(app):
    app.gameStateManager.draw()


def main():
    runApp(width=880, height=880)


main()
