from cmu_graphics import *


class Button:
    def __init__(
        self,
        x,
        y,
        width,
        height,
        text,
        action,
        size=16,
        color="black",
        font="Super Legend Boy",
        border="black",
        borderWidth=2,
    ):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.action = action  # action is now a callback function
        self.size = size
        self.color = color
        self.font = font
        self.border = border
        self.borderWidth = borderWidth

    def pointInBounds(self, px, py):
        return self.x <= px <= (self.x + self.width) and self.y <= py <= (
            self.y + self.height
        )

    def onMousePress(self, mx, my):
        if self.pointInBounds(mx, my) and self.action:
            self.action()

    def draw(self):
        cx = self.x + self.width / 2
        cy = self.y + self.height / 2
        drawRect(self.x, self.y, self.width, self.height, fill=self.color)
        drawLabel(
            self.text,
            cx,
            cy,
            align="center",
            size=16,
            fill="navy",
            font="Super Legend Boy"
        )
