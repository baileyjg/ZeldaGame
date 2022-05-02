import pygame
import time

from pygame.locals import *
from time import sleep


class Sprite:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 0
        self.height = 0

    # Abstract methods
    def draw(self, g):
        pass

    def update(self):
        pass

    def marshal(self):
        pass

    # IsInstanceOf Methods
    def isBrick(self):
        return False

    def isLink(self):
        return False

    def isPot(self):
        return False

    def isBoomerang(self):
        return False

    # Getters
    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getWidth(self):
        return self.width

    def getHeight(self):
        return self.height

    # Setters
    def setX(self, x):
        self.x = x

    def setY(self, y):
        self.y = y


class Link(Sprite):
    def __init__(self, x, y, d, m):
        super(Link, self).__init__(x, y)
        self.pX = 0
        self.pY = 0
        self.width = 68
        self.height = 75
        self.speed = 10.0
        self.direction = d
        self.model = m
        self.images = [None]
        self.rect = None

    def draw(self, g):
        if self.images[0] is None:  # If link's images have not been loaded, load them in
            self.images.clear()
            for i in range(40):
                self.images.append(self.model.getView().loadImage("images/link" + str(i) + ".png"))

        self.rect = self.images[self.direction].get_rect()
        self.rect.x = self.x + self.model.getScrollPosX()
        self.rect.y = self.y + self.model.getScrollPosY()
        g.blit(self.images[self.direction], self.rect)

        # Handle link's animation loop
        if self.direction == 9 or (
                self.direction % 10) == 9:  # If direction is 9, 19, 29, or 39 then reset link to idle
            self.direction -= 9
        elif self.model.getView().getController().getKeyRight() or self.model.getView().getController().getKeyLeft() or self.model.getView().getController().getKeyUp() or self.model.getView().getController().getKeyDown():  # Increment direction image if keys are down
            self.direction += 1
        else:
            # Reset to idle positions if no keys are down
            self.direction -= self.direction % 10

    def update(self):
        # Handle link's movement
        # Images 0 - 9 are down, 10 - 19 are left, 20 - 29 are up, 30 - 39 are right

        if self.model.getView().getController().getKeyRight():
            if self.direction < 30:
                self.direction = 30
            self.x = self.x + self.speed
        elif self.model.getView().getController().getKeyLeft():
            if self.direction < 10 or self.direction > 19:
                self.direction = 10
            self.x = self.x - self.speed
        elif self.model.getView().getController().getKeyUp():
            if self.direction < 20 or self.direction > 29:
                self.direction = 20
            self.y = self.y - self.speed
        elif self.model.getView().getController().getKeyDown():
            if self.direction > 9:
                self.direction = 0
            self.y = self.y + self.speed

        if self.rect is not None:
            self.rect.x = self.x + self.model.getScrollPosX()
            self.rect.y = self.y + self.model.getScrollPosY()

        if not (self.model.getScrolling()):  # Debounce to ensure scrolling doesn't glitch back and forth
            if self.x + self.width >= 700 and self.model.getScrollDestX() != -700:  # Scroll right
                self.model.getView().getController().scrollRight()
            elif self.x + self.width < 700 and self.model.getScrollDestX() != 0:  # Scroll left
                self.model.getView().getController().scrollLeft()
            elif self.y + self.height >= 500 and self.model.getScrollDestY() != -500:  # Scroll down
                self.model.getView().getController().scrollDown()
            elif self.y + self.height < 500 and self.model.getScrollDestY() != 0:  # Scroll up
                self.model.getView().getController().scrollUp()

        for i in range(len(self.model.getSprites())):  # Iterate over the sprites checking for collisions
            if self.model.getSprites()[i].isLink():  # Do not allow link to collide with himself
                continue
            if self.model.doesCollide(self, self.model.getSprites()[i]):
                p = None
                if self.model.getSprites()[i].isBrick():
                    self.brickCollisionDetected(self.model.getSprites()[i])
                elif self.model.getSprites()[i].isPot():
                    p = self.model.getSprites()[i]
                    p.linkCollisionDetected(self)
        return True

    def brickCollisionDetected(self, b):  # Fix link's position if he is colliding with a brick sprite
        if self.y + self.height >= b.getY() >= self.pY and self.direction <= 9:  # Toe collision
            self.setY(b.getY() - self.height - 1)
        if self.x <= b.getX() + b.getWidth() <= self.pX and 19 >= self.direction > 9:  # Left collision
            self.setX(b.getX() + b.getWidth() + 1)
        if self.y <= b.getY() + b.getHeight() <= self.pY and 29 >= self.direction > 19:  # Head collision
            self.setY(b.getY() + b.getHeight() + 1)
        if self.x + self.width >= b.getX() >= self.pX and 39 >= self.direction > 29:  # Right collision
            self.setX(b.getX() - self.width - 1)

    def savePreviousLocation(self):
        self.pX = self.x
        self.pY = self.y

    def toString(self):
        return "Link (x, y, width, height) = (" + str(self.x) + ", " + str(self.y) + ", " + str(
            self.width) + ", " + str(self.height) + ")"

    def isLink(self):
        return True

    # Getters
    def getDirection(self):
        return self.direction

    def getPX(self):
        return self.pX

    def getPY(self):
        return self.pY

    # Setters
    def set_direction(self, d):
        self.direction = d


class Brick(Sprite):
    def __init__(self, x, y, m):
        super(Brick, self).__init__(x, y)
        self.image = None
        self.model = m
        self.width = 50
        self.height = 50
        self.rect = None

    def existingBrick(self, x, y):  # Checks if the brick exists
        if self.x == x and self.y == y:
            return True
        return False

    def update(self):
        if self.rect is not None:
            self.rect.x = self.x + self.model.getScrollPosX()
            self.rect.y = self.y + self.model.getScrollPosY()
        return True

    def draw(self, g):  # Draws the brick
        if self.image is None:
            self.image = self.model.getView().loadImage("images/brick.jpg")
            self.rect = self.image.get_rect()
        # g.drawImage(self.image, self.x + self.model.getScrollPosX(), self.y + self.model.getScrollPosY(), self.width,
        #             self.height)

        g.blit(self.image, self.rect)

    def toString(self):
        return "Brick (x, y, width, height) = (" + str(self.x) + ", " + str(self.y) + ", " + str(
            self.width) + ", " + str(self.height) + ")"

    def isBrick(self):
        return True


class Pot(Sprite):
    def __init__(self, x, y, m):  # Default constructor
        super(Pot, self).__init__(x, y)
        self.width = 40
        self.height = 40
        self.images = [None]
        self.model = m
        self.direction = 0
        self.broken = False
        self.removeDelay = 30
        self.collisionOffset = 12
        self.speed = 15
        self.rect = None  # Holds the rectangle for the non-broken image
        self.broken_rect = None  # Holds the rectangle for the broken image

    def update(self):  # Communicates to model when to remove the pot
        for i in range(len(self.model.getSprites())):
            b = None
            if self.model.getSprites()[i].isBrick() and self.model.doesCollide(self, self.model.getSprites()[i]):
                b = self.model.getSprites()[i]
                if self.direction == 0:  # Do nothing
                    pass
                elif self.direction == 1:
                    self.x = b.getX() + b.getWidth() + self.collisionOffset
                elif self.direction == 2:
                    self.x = b.getX() - self.width - self.collisionOffset
                elif self.direction == 3:
                    self.y = b.getY() + b.getHeight() + self.collisionOffset
                elif self.direction == 4:
                    self.y = b.getY() - self.height - self.collisionOffset
                elif self.model.getController().debug:
                    print("Invalid brick/pot collision!")
                self.broken = True
                break
        # Update the current image rectangle position
        if self.rect is not None:
            self.rect.x = self.x + self.model.getScrollPosX()
            self.rect.y = self.y + self.model.getScrollPosY()
            self.broken_rect.x = self.x + self.model.getScrollPosX()
            self.broken_rect.y = self.y + self.model.getScrollPosY()

        if self.broken:
            self.removeDelay -= 1
            if self.removeDelay <= 0:
                return False
        if self.direction != 0:
            if self.direction == 1:
                self.x -= self.speed
            elif self.direction == 2:
                self.x += self.speed
            elif self.direction == 3:
                self.y -= self.speed
            elif self.direction == 4:
                self.y += self.speed
            elif self.model.getController().debug:
                print("Invalid pot direction!")
        return True

    def draw(self, g):
        if self.images[0] is None:
            self.images.clear()
            self.images.append(self.model.getView().loadImage("images/pot.png"))
            self.rect = self.images[0].get_rect()
            self.images.append(self.model.getView().loadImage("images/pot_broken.png"))
            self.broken_rect = self.images[1].get_rect()

        if self.broken:  # Draw the pot depending on broken status
            # self.rect = self.images[1].get_rect()
            self.broken_rect.x = self.x + self.model.getScrollPosX()
            self.broken_rect.y = self.y + self.model.getScrollPosY()
            g.blit(self.images[1], self.broken_rect)
            # g.drawImage(self.images[1], self.x + self.model.getScrollPosX(), self.y + self.model.getScrollPosY(),
            #             self.width, self.height)
        else:
            # self.rect = self.images[0].get_rect()
            self.rect.x = self.x + self.model.getScrollPosX()
            self.rect.y = self.y + self.model.getScrollPosY()
            g.blit(self.images[0], self.rect)
            # g.drawImage(self.images[0], self.x + self.model.getScrollPosX(), self.y + self.model.getScrollPosY(),
            #             self.width, self.height)

    def linkCollisionDetected(self, l):  # Determine where the pot should slide based on link collision
        if self.direction == 0 and not self.broken:  # Check if the pot has already been collided with
            if l.getDirection() <= 9:  # Toe collision
                self.direction = 4
            elif l.getDirection() >= 10 and l.getDirection() <= 19:  # Left collision
                self.direction = 1
            elif l.getDirection() >= 20 and l.getDirection() <= 29:  # Head collision
                self.direction = 3
            elif l.getDirection() >= 30:  # Right collision
                self.direction = 2

    def existingPot(self, x, y):  # Checks if a pot exists
        if self.x == x and self.y == y:
            return True
        return False

    def toString(self):
        return "Pot (x, y, width, height) = (" + str(self.x) + ", " + str(self.y) + ", " + str(self.width) + ", " + str(
            self.height) + ")"

    def isPot(self):
        return True

    # Setters
    def setBroken(self, b):
        self.broken = b


class Boomerang(Sprite):
    def __init__(self, x, y, d, m):
        super(Boomerang, self).__init__(x, y)
        self.width = 16
        self.height = 24
        self.direction = d
        self.speed = 15
        self.model = m
        self.image = 0  # Which image is the boomerang currently drawing
        self.rect = None
        self.images = [None]

    def draw(self, g):
        if self.images[0] is None:  # Lazy load the boomerang images
            self.images.clear()
            for i in range(4):
                self.images.append(self.model.getView().loadImage("images/boomerang" + str(i) + ".png"))
            self.rect = self.images[0].get_rect()

        if self.rect is not None:
            self.rect.x = self.x + self.model.getScrollPosX()
            self.rect.y = self.y + self.model.getScrollPosY()
            self.rect.width = self.width
            self.rect.height = self.height
            g.blit(self.images[self.image], self.rect)

    def update(self):
        if self.image != 3:  # Increment the direction each update to animate the boomerang
            self.image += 1
        else:
            self.image = 0
        if self.rect is not None:
            self.rect = self.images[self.image].get_rect()  # Set the rectangle to the current image
            self.rect.x = self.x + self.model.getScrollPosX()
            self.rect.y = self.y + self.model.getScrollPosY()
            self.rect.width = self.width
            self.rect.height = self.height

        if self.direction == 0:  # Control how the boomerangs coordinates change depending on direction
            self.x -= self.speed
        elif self.direction == 1:
            self.x += self.speed
        elif self.direction == 2:
            self.y -= self.speed
        elif self.direction == 3:
            self.y += self.speed

        for i in range(len(self.model.getSprites())):  # Check for a boomerang / pot collision
            p = None
            if self.model.getSprites()[i].isPot() and self.model.doesCollide(self, self.model.getSprites()[i]):
                p = self.model.getSprites()[i]
                p.setBroken(True)
                return False
            elif self.model.getSprites()[i].isBrick() and self.model.doesCollide(self, self.model.getSprites()[i]):
                return False

        return True

    def isBoomerang(self):
        return True

    def toString(self):
        return "Boomerang (x, y, width, height) = (" + str(self.x) + ", " + str(self.y) + ", " + str(
            self.width) + ", " + str(self.height) + ")"

    # Setters
    def setDirection(self, d):
        self.direction = d


class Model:
    def __init__(self):  # Default constructor
        self.sprites = []
        self.link = None
        self.brick = None
        self.pot = None
        self.createObjects()  # Creates all hardcoded objects

        self.scrolling = False  # Boolean to indicate whether the map is still scrolling to its destination
        self.scrollSpeed = 60
        self.scrollPosX = 0
        self.scrollPosY = 0
        self.scrollDestX = 0
        self.scrollDestY = 0
        self.roomSizeX = 700
        self.roomSizeY = 500
        self.controller = None

    def createObjects(self):
        # Create Hardcoded Link
        self.link = Link(70, 70, 0, self)
        self.sprites.append(self.link)

        # Create Hardcoded Bricks
        self.brick = Brick(0, 0, self)
        self.sprites.append(self.brick)
        self.brick = Brick(0, 50, self)
        self.sprites.append(self.brick)
        self.brick = Brick(0, 100, self)
        self.sprites.append(self.brick)
        self.brick = Brick(0, 150, self)
        self.sprites.append(self.brick)
        self.brick = Brick(0, 200, self)
        self.sprites.append(self.brick)
        self.brick = Brick(0, 250, self)
        self.sprites.append(self.brick)
        self.brick = Brick(0, 300, self)
        self.sprites.append(self.brick)
        self.brick = Brick(0, 350, self)
        self.sprites.append(self.brick)
        self.brick = Brick(50, 0, self)
        self.sprites.append(self.brick)
        self.brick = Brick(100, 0, self)
        self.sprites.append(self.brick)
        self.brick = Brick(150, 0, self)
        self.sprites.append(self.brick)
        self.brick = Brick(200, 0, self)
        self.sprites.append(self.brick)
        self.brick = Brick(250, 0, self)
        self.sprites.append(self.brick)
        self.brick = Brick(300, 0, self)
        self.sprites.append(self.brick)
        self.brick = Brick(350, 0, self)
        self.sprites.append(self.brick)
        self.brick = Brick(400, 0, self)
        self.sprites.append(self.brick)
        self.brick = Brick(450, 0, self)
        self.sprites.append(self.brick)
        self.brick = Brick(500, 0, self)
        self.sprites.append(self.brick)
        self.brick = Brick(550, 0, self)
        self.sprites.append(self.brick)
        self.brick = Brick(600, 0, self)
        self.sprites.append(self.brick)
        self.brick = Brick(650, 0, self)
        self.sprites.append(self.brick)
        self.brick = Brick(650, 150, self)
        self.sprites.append(self.brick)
        self.brick = Brick(650, 200, self)
        self.sprites.append(self.brick)
        self.brick = Brick(650, 250, self)
        self.sprites.append(self.brick)
        self.brick = Brick(650, 300, self)
        self.sprites.append(self.brick)
        self.brick = Brick(650, 350, self)
        self.sprites.append(self.brick)
        self.brick = Brick(650, 400, self)
        self.sprites.append(self.brick)
        self.brick = Brick(650, 450, self)
        self.sprites.append(self.brick)
        self.brick = Brick(600, 450, self)
        self.sprites.append(self.brick)
        self.brick = Brick(550, 450, self)
        self.sprites.append(self.brick)
        self.brick = Brick(400, 450, self)
        self.sprites.append(self.brick)
        self.brick = Brick(350, 450, self)
        self.sprites.append(self.brick)
        self.brick = Brick(300, 450, self)
        self.sprites.append(self.brick)
        self.brick = Brick(150, 450, self)
        self.sprites.append(self.brick)
        self.brick = Brick(100, 450, self)
        self.sprites.append(self.brick)
        self.brick = Brick(50, 450, self)
        self.sprites.append(self.brick)
        self.brick = Brick(0, 450, self)
        self.sprites.append(self.brick)
        self.brick = Brick(250, 50, self)
        self.sprites.append(self.brick)
        self.brick = Brick(250, 100, self)
        self.sprites.append(self.brick)
        self.brick = Brick(250, 150, self)
        self.sprites.append(self.brick)
        self.brick = Brick(250, 200, self)
        self.sprites.append(self.brick)
        self.brick = Brick(250, 250, self)
        self.sprites.append(self.brick)
        self.brick = Brick(600, 300, self)
        self.sprites.append(self.brick)
        self.brick = Brick(550, 300, self)
        self.sprites.append(self.brick)
        self.brick = Brick(500, 300, self)
        self.sprites.append(self.brick)
        self.brick = Brick(450, 300, self)
        self.sprites.append(self.brick)
        self.brick = Brick(400, 300, self)
        self.sprites.append(self.brick)
        self.brick = Brick(250, 300, self)
        self.sprites.append(self.brick)
        self.brick = Brick(700, 0, self)
        self.sprites.append(self.brick)
        self.brick = Brick(700, 150, self)
        self.sprites.append(self.brick)
        self.brick = Brick(700, 200, self)
        self.sprites.append(self.brick)
        self.brick = Brick(700, 300, self)
        self.sprites.append(self.brick)
        self.brick = Brick(700, 350, self)
        self.sprites.append(self.brick)
        self.brick = Brick(700, 400, self)
        self.sprites.append(self.brick)
        self.brick = Brick(700, 450, self)
        self.sprites.append(self.brick)
        self.brick = Brick(750, 0, self)
        self.sprites.append(self.brick)
        self.brick = Brick(800, 0, self)
        self.sprites.append(self.brick)
        self.brick = Brick(850, 0, self)
        self.sprites.append(self.brick)
        self.brick = Brick(900, 0, self)
        self.sprites.append(self.brick)
        self.brick = Brick(950, 0, self)
        self.sprites.append(self.brick)
        self.brick = Brick(1000, 0, self)
        self.sprites.append(self.brick)
        self.brick = Brick(1050, 0, self)
        self.sprites.append(self.brick)
        self.brick = Brick(1100, 0, self)
        self.sprites.append(self.brick)
        self.brick = Brick(1150, 0, self)
        self.sprites.append(self.brick)
        self.brick = Brick(1200, 0, self)
        self.sprites.append(self.brick)
        self.brick = Brick(1250, 0, self)
        self.sprites.append(self.brick)
        self.brick = Brick(1300, 0, self)
        self.sprites.append(self.brick)
        self.brick = Brick(1350, 0, self)
        self.sprites.append(self.brick)
        self.brick = Brick(1350, 50, self)
        self.sprites.append(self.brick)
        self.brick = Brick(1350, 100, self)
        self.sprites.append(self.brick)
        self.brick = Brick(1350, 150, self)
        self.sprites.append(self.brick)
        self.brick = Brick(1350, 200, self)
        self.sprites.append(self.brick)
        self.brick = Brick(1350, 250, self)
        self.sprites.append(self.brick)
        self.brick = Brick(1350, 300, self)
        self.sprites.append(self.brick)
        self.brick = Brick(1350, 350, self)
        self.sprites.append(self.brick)
        self.brick = Brick(1350, 400, self)
        self.sprites.append(self.brick)
        self.brick = Brick(1350, 450, self)
        self.sprites.append(self.brick)
        self.brick = Brick(1300, 450, self)
        self.sprites.append(self.brick)
        self.brick = Brick(1250, 450, self)
        self.sprites.append(self.brick)
        self.brick = Brick(1200, 450, self)
        self.sprites.append(self.brick)
        self.brick = Brick(1150, 450, self)
        self.sprites.append(self.brick)
        self.brick = Brick(1100, 450, self)
        self.sprites.append(self.brick)
        self.brick = Brick(750, 450, self)
        self.sprites.append(self.brick)
        self.brick = Brick(900, 450, self)
        self.sprites.append(self.brick)
        self.brick = Brick(950, 450, self)
        self.sprites.append(self.brick)
        self.brick = Brick(1000, 450, self)
        self.sprites.append(self.brick)
        self.brick = Brick(1050, 450, self)
        self.sprites.append(self.brick)
        self.brick = Brick(700, 250, self)
        self.sprites.append(self.brick)
        self.brick = Brick(750, 250, self)
        self.sprites.append(self.brick)
        self.brick = Brick(800, 250, self)
        self.sprites.append(self.brick)
        self.brick = Brick(850, 250, self)
        self.sprites.append(self.brick)
        self.brick = Brick(900, 250, self)
        self.sprites.append(self.brick)
        self.brick = Brick(950, 250, self)
        self.sprites.append(self.brick)
        self.brick = Brick(950, 300, self)
        self.sprites.append(self.brick)
        self.brick = Brick(950, 200, self)
        self.sprites.append(self.brick)
        self.brick = Brick(900, 500, self)
        self.sprites.append(self.brick)
        self.brick = Brick(750, 500, self)
        self.sprites.append(self.brick)
        self.brick = Brick(950, 500, self)
        self.sprites.append(self.brick)
        self.brick = Brick(1000, 500, self)
        self.sprites.append(self.brick)
        self.brick = Brick(1050, 500, self)
        self.sprites.append(self.brick)
        self.brick = Brick(1100, 500, self)
        self.sprites.append(self.brick)
        self.brick = Brick(1150, 500, self)
        self.sprites.append(self.brick)
        self.brick = Brick(1200, 500, self)
        self.sprites.append(self.brick)
        self.brick = Brick(1250, 500, self)
        self.sprites.append(self.brick)
        self.brick = Brick(1300, 500, self)
        self.sprites.append(self.brick)
        self.brick = Brick(1350, 500, self)
        self.sprites.append(self.brick)
        self.brick = Brick(1350, 550, self)
        self.sprites.append(self.brick)
        self.brick = Brick(1350, 600, self)
        self.sprites.append(self.brick)
        self.brick = Brick(1350, 650, self)
        self.sprites.append(self.brick)
        self.brick = Brick(1350, 700, self)
        self.sprites.append(self.brick)
        self.brick = Brick(1350, 750, self)
        self.sprites.append(self.brick)
        self.brick = Brick(1350, 800, self)
        self.sprites.append(self.brick)
        self.brick = Brick(1350, 850, self)
        self.sprites.append(self.brick)
        self.brick = Brick(1350, 900, self)
        self.sprites.append(self.brick)
        self.brick = Brick(1350, 950, self)
        self.sprites.append(self.brick)
        self.brick = Brick(700, 500, self)
        self.sprites.append(self.brick)
        self.brick = Brick(700, 550, self)
        self.sprites.append(self.brick)
        self.brick = Brick(700, 600, self)
        self.sprites.append(self.brick)
        self.brick = Brick(700, 700, self)
        self.sprites.append(self.brick)
        self.brick = Brick(700, 850, self)
        self.sprites.append(self.brick)
        self.brick = Brick(700, 900, self)
        self.sprites.append(self.brick)
        self.brick = Brick(700, 950, self)
        self.sprites.append(self.brick)
        self.brick = Brick(750, 950, self)
        self.sprites.append(self.brick)
        self.brick = Brick(800, 950, self)
        self.sprites.append(self.brick)
        self.brick = Brick(850, 950, self)
        self.sprites.append(self.brick)
        self.brick = Brick(900, 950, self)
        self.sprites.append(self.brick)
        self.brick = Brick(950, 950, self)
        self.sprites.append(self.brick)
        self.brick = Brick(1000, 950, self)
        self.sprites.append(self.brick)
        self.brick = Brick(1050, 950, self)
        self.sprites.append(self.brick)
        self.brick = Brick(1100, 950, self)
        self.sprites.append(self.brick)
        self.brick = Brick(1150, 950, self)
        self.sprites.append(self.brick)
        self.brick = Brick(1200, 950, self)
        self.sprites.append(self.brick)
        self.brick = Brick(1250, 950, self)
        self.sprites.append(self.brick)
        self.brick = Brick(1300, 950, self)
        self.sprites.append(self.brick)
        self.brick = Brick(850, 700, self)
        self.sprites.append(self.brick)
        self.brick = Brick(850, 750, self)
        self.sprites.append(self.brick)
        self.brick = Brick(850, 800, self)
        self.sprites.append(self.brick)
        self.brick = Brick(900, 800, self)
        self.sprites.append(self.brick)
        self.brick = Brick(1100, 800, self)
        self.sprites.append(self.brick)
        self.brick = Brick(1050, 800, self)
        self.sprites.append(self.brick)
        self.brick = Brick(1100, 650, self)
        self.sprites.append(self.brick)
        self.brick = Brick(1100, 600, self)
        self.sprites.append(self.brick)
        self.brick = Brick(1100, 550, self)
        self.sprites.append(self.brick)
        self.brick = Brick(1150, 800, self)
        self.sprites.append(self.brick)
        self.brick = Brick(1200, 800, self)
        self.sprites.append(self.brick)
        self.brick = Brick(650, 600, self)
        self.sprites.append(self.brick)
        self.brick = Brick(650, 700, self)
        self.sprites.append(self.brick)
        self.brick = Brick(650, 550, self)
        self.sprites.append(self.brick)
        self.brick = Brick(650, 500, self)
        self.sprites.append(self.brick)
        self.brick = Brick(650, 850, self)
        self.sprites.append(self.brick)
        self.brick = Brick(650, 900, self)
        self.sprites.append(self.brick)
        self.brick = Brick(650, 950, self)
        self.sprites.append(self.brick)
        self.brick = Brick(600, 950, self)
        self.sprites.append(self.brick)
        self.brick = Brick(550, 950, self)
        self.sprites.append(self.brick)
        self.brick = Brick(0, 400, self)
        self.sprites.append(self.brick)
        self.brick = Brick(0, 500, self)
        self.sprites.append(self.brick)
        self.brick = Brick(0, 550, self)
        self.sprites.append(self.brick)
        self.brick = Brick(0, 600, self)
        self.sprites.append(self.brick)
        self.brick = Brick(150, 500, self)
        self.sprites.append(self.brick)
        self.brick = Brick(300, 500, self)
        self.sprites.append(self.brick)
        self.brick = Brick(400, 500, self)
        self.sprites.append(self.brick)
        self.brick = Brick(350, 500, self)
        self.sprites.append(self.brick)
        self.brick = Brick(550, 500, self)
        self.sprites.append(self.brick)
        self.brick = Brick(600, 500, self)
        self.sprites.append(self.brick)
        self.brick = Brick(100, 500, self)
        self.sprites.append(self.brick)
        self.brick = Brick(50, 500, self)
        self.sprites.append(self.brick)
        self.brick = Brick(0, 650, self)
        self.sprites.append(self.brick)
        self.brick = Brick(0, 700, self)
        self.sprites.append(self.brick)
        self.brick = Brick(0, 750, self)
        self.sprites.append(self.brick)
        self.brick = Brick(0, 800, self)
        self.sprites.append(self.brick)
        self.brick = Brick(0, 850, self)
        self.sprites.append(self.brick)
        self.brick = Brick(0, 900, self)
        self.sprites.append(self.brick)
        self.brick = Brick(0, 950, self)
        self.sprites.append(self.brick)
        self.brick = Brick(50, 950, self)
        self.sprites.append(self.brick)
        self.brick = Brick(100, 950, self)
        self.sprites.append(self.brick)
        self.brick = Brick(150, 950, self)
        self.sprites.append(self.brick)
        self.brick = Brick(200, 950, self)
        self.sprites.append(self.brick)
        self.brick = Brick(250, 950, self)
        self.sprites.append(self.brick)
        self.brick = Brick(300, 950, self)
        self.sprites.append(self.brick)
        self.brick = Brick(350, 950, self)
        self.sprites.append(self.brick)
        self.brick = Brick(400, 950, self)
        self.sprites.append(self.brick)
        self.brick = Brick(450, 950, self)
        self.sprites.append(self.brick)
        self.brick = Brick(500, 950, self)
        self.sprites.append(self.brick)
        self.brick = Brick(300, 550, self)
        self.sprites.append(self.brick)
        self.brick = Brick(300, 600, self)
        self.sprites.append(self.brick)
        self.brick = Brick(300, 650, self)
        self.sprites.append(self.brick)
        self.brick = Brick(300, 700, self)
        self.sprites.append(self.brick)
        self.brick = Brick(300, 750, self)
        self.sprites.append(self.brick)
        self.brick = Brick(300, 800, self)
        self.sprites.append(self.brick)
        self.brick = Brick(650, 650, self)
        self.sprites.append(self.brick)
        self.brick = Brick(700, 650, self)
        self.sprites.append(self.brick)
        self.brick = Brick(1300, 650, self)
        self.sprites.append(self.brick)
        self.brick = Brick(1250, 650, self)
        self.sprites.append(self.brick)
        self.brick = Brick(1250, 800, self)
        self.sprites.append(self.brick)
        self.brick = Brick(1300, 800, self)
        self.sprites.append(self.brick)
        self.brick = Brick(1100, 150, self)
        self.sprites.append(self.brick)
        self.brick = Brick(1150, 150, self)
        self.sprites.append(self.brick)
        self.brick = Brick(1200, 150, self)
        self.sprites.append(self.brick)
        self.brick = Brick(1100, 300, self)
        self.sprites.append(self.brick)
        self.brick = Brick(1150, 300, self)
        self.sprites.append(self.brick)
        self.brick = Brick(1200, 300, self)
        self.sprites.append(self.brick)
        self.brick = Brick(1100, 200, self)
        self.sprites.append(self.brick)
        self.brick = Brick(1200, 200, self)
        self.sprites.append(self.brick)
        self.brick = Brick(1150, 200, self)
        self.sprites.append(self.brick)
        self.brick = Brick(1100, 250, self)
        self.sprites.append(self.brick)
        self.brick = Brick(1150, 250, self)
        self.sprites.append(self.brick)
        self.brick = Brick(1200, 250, self)
        self.sprites.append(self.brick)
        self.brick = Brick(400, 150, self)
        self.sprites.append(self.brick)
        self.brick = Brick(450, 150, self)
        self.sprites.append(self.brick)
        self.brick = Brick(500, 150, self)
        self.sprites.append(self.brick)
        self.brick = Brick(600, 700, self)
        self.sprites.append(self.brick)
        self.brick = Brick(550, 700, self)
        self.sprites.append(self.brick)
        self.brick = Brick(500, 700, self)
        self.sprites.append(self.brick)
        self.brick = Brick(450, 700, self)
        self.sprites.append(self.brick)
        self.brick = Brick(400, 700, self)
        self.sprites.append(self.brick)
        self.brick = Brick(350, 700, self)
        self.sprites.append(self.brick)
        self.brick = Brick(250, 800, self)
        self.sprites.append(self.brick)
        self.brick = Brick(200, 800, self)
        self.sprites.append(self.brick)
        self.brick = Brick(150, 800, self)
        self.sprites.append(self.brick)
        self.brick = Brick(750, 700, self)
        self.sprites.append(self.brick)
        self.brick = Brick(800, 700, self)
        self.sprites.append(self.brick)
        self.brick = Brick(950, 150, self)
        self.sprites.append(self.brick)

        # Create Hardcoded Pots
        self.pot = Pot(302, 305, self)
        self.sprites.append(self.pot)
        self.pot = Pot(356, 303, self)
        self.sprites.append(self.pot)
        self.pot = Pot(300, 349, self)
        self.sprites.append(self.pot)
        self.pot = Pot(298, 396, self)
        self.sprites.append(self.pot)
        self.pot = Pot(447, 75, self)
        self.sprites.append(self.pot)
        self.pot = Pot(453, 224, self)
        self.sprites.append(self.pot)
        self.pot = Pot(426, 604, self)
        self.sprites.append(self.pot)
        self.pot = Pot(471, 605, self)
        self.sprites.append(self.pot)
        self.pot = Pot(521, 603, self)
        self.sprites.append(self.pot)
        self.pot = Pot(121, 626, self)
        self.sprites.append(self.pot)
        self.pot = Pot(166, 625, self)
        self.sprites.append(self.pot)
        self.pot = Pot(119, 676, self)
        self.sprites.append(self.pot)
        self.pot = Pot(167, 676, self)
        self.sprites.append(self.pot)
        self.pot = Pot(232, 853, self)
        self.sprites.append(self.pot)
        self.pot = Pot(231, 900, self)
        self.sprites.append(self.pot)
        self.pot = Pot(651, 756, self)
        self.sprites.append(self.pot)
        self.pot = Pot(651, 800, self)
        self.sprites.append(self.pot)
        self.pot = Pot(944, 588, self)
        self.sprites.append(self.pot)
        self.pot = Pot(991, 589, self)
        self.sprites.append(self.pot)
        self.pot = Pot(943, 632, self)
        self.sprites.append(self.pot)
        self.pot = Pot(996, 635, self)
        self.sprites.append(self.pot)
        self.pot = Pot(1180, 656, self)
        self.sprites.append(self.pot)
        self.pot = Pot(779, 783, self)
        self.sprites.append(self.pot)
        self.pot = Pot(958, 807, self)
        self.sprites.append(self.pot)
        self.pot = Pot(1005, 808, self)
        self.sprites.append(self.pot)
        self.pot = Pot(953, 101, self)
        self.sprites.append(self.pot)
        self.pot = Pot(950, 54, self)
        self.sprites.append(self.pot)
        self.pot = Pot(813, 153, self)
        self.sprites.append(self.pot)
        self.pot = Pot(856, 154, self)
        self.sprites.append(self.pot)
        self.pot = Pot(1003, 208, self)
        self.sprites.append(self.pot)
        self.pot = Pot(1051, 208, self)
        self.sprites.append(self.pot)
        self.pot = Pot(1002, 264, self)
        self.sprites.append(self.pot)
        self.pot = Pot(1054, 265, self)
        self.sprites.append(self.pot)
        self.pot = Pot(827, 430, self)
        self.sprites.append(self.pot)

    def update(self):  # Update the model
        for i in self.sprites.copy():  # Update all sprites
            if i.isLink():  # Save Link's previous location
                self.link.savePreviousLocation()
            if not (i.update()):
                self.sprites.remove(i)  # Remove sprites when they return a false update

        if self.scrollPosX == self.scrollDestX and self.scrollPosY == self.scrollDestY:  # Checks for scrolling
            self.scrolling = False
        else:
            self.scrolling = True
            # Handle scrolling animation
            if self.scrollPosX < self.scrollDestX:
                self.scrollPosX += min(self.scrollSpeed, self.scrollDestX - self.scrollPosX)
            else:
                self.scrollPosX -= min(self.scrollSpeed, self.scrollPosX - self.scrollDestX)

            if self.scrollPosY < self.scrollDestY:
                self.scrollPosY += min(self.scrollSpeed, self.scrollDestY - self.scrollPosY)
            else:
                self.scrollPosY -= min(self.scrollSpeed, self.scrollPosY - self.scrollDestY)

    def doesCollide(self, sprite_one, sprite_two):  # Check for a collision between two sprites
        # Check if link is not colliding
        if sprite_one.getX() + sprite_one.getWidth() <= sprite_two.getX():
            return False
        if sprite_one.getX() >= sprite_two.getX() + sprite_two.getWidth():
            return False
        if sprite_one.getY() >= sprite_two.getY() + sprite_two.getHeight():
            return False
        if sprite_one.getY() + sprite_one.getHeight() <= sprite_two.getY():
            return False

        # Otherwise the sprites are colliding
        if self.controller.debug:
            print("Sprite collision detected!")
            print(sprite_one)
            print(sprite_two)
        return True

    def addSprite(self, s):  # Add a sprite to the above array
        self.sprites.append(s)
        if self.controller.debug:
            print("Added " + s.toString())

    def removeSprite(self, i):  # Remove a sprite from the above array
        self.sprites.pop(i)

    # Getters
    def getSprites(self):
        return self.sprites

    def getLink(self):
        return self.link

    def getScrollPosX(self):
        return self.scrollPosX

    def getScrollPosY(self):
        return self.scrollPosY

    def getScrollDestX(self):
        return self.scrollDestX

    def getScrollDestY(self):
        return self.scrollDestY

    def getScrolling(self):
        return self.scrolling

    def getView(self):
        return self.view

    def getController(self):
        return self.controller

    def getRoomSizeX(self):
        return self.roomSizeX

    def getRoomSizeY(self):
        return self.roomSizeY

    # Setters
    def setView(self, v):
        self.view = v

    def setController(self, c):
        self.controller = c

    def setScrollPos(self, x, y):
        self.scrollPosX = x
        self.scrollPosY = y

    def setScrollDest(self, x, y):
        self.scrollDestX = x
        self.scrollDestY = y


class View:
    def __init__(self, c, m):
        self.controller = c
        self.model = m
        screen_size = (700, 500)
        self.screen = pygame.display.set_mode(screen_size, 32)

    def loadImage(self, fileName):  # Loads various images
        try:
            image = pygame.image.load(fileName)
            if self.controller.debug:
                print("Loaded " + fileName)
            return image
        except:
            print("Error loading " + fileName + "!")
            return None

    def update(self):
        sprites = self.model.getSprites()
        self.screen.fill([0, 200, 100])
        for sprite in sprites:
            sprite.draw(self.screen)
        pygame.display.flip()

    # Getters
    def getController(self):
        return self.controller


class Controller:
    def __init__(self, m):
        self.model = m
        self.keyLeft = False
        self.keyRight = False
        self.keyUp = False
        self.keyDown = False
        self.brickSnapIncrement = 50
        self.debug = False
        self.keep_going = True

    def throw_boomerang(self):
        if not (self.model.getScrolling()):  # Make sure the model is not scrolling
            b = None
            l = self.model.getLink()
            if self.model.getLink().getDirection() <= 9:  # Link is facing forward
                b = Boomerang(l.getX() + l.getWidth() / 2, l.getY() + l.getHeight() / 2, 3, self.model)
            elif 10 <= self.model.getLink().getDirection() <= 19:
                b = Boomerang(l.getX() + l.getWidth() / 2, l.getY() + l.getHeight() / 2, 0, self.model)
            elif 20 <= self.model.getLink().getDirection() <= 29:
                b = Boomerang(l.getX() + l.getWidth() / 2, l.getY() + l.getHeight() / 2, 2, self.model)
            else:  # Link is facing right
                b = Boomerang(l.getX() + l.getWidth() / 2, l.getY() + l.getHeight() / 2, 1, self.model)
            self.model.addSprite(b)

    def update(self):  # Handle key presses and releases
        for event in pygame.event.get():
            if event.type == QUIT:
                self.keep_going = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.keep_going = False
                elif event.key == K_LEFT:
                    self.keyLeft = True
                elif event.key == K_RIGHT:
                    self.keyRight = True
                elif event.key == K_UP:
                    self.keyUp = True
                elif event.key == K_DOWN:
                    self.keyDown = True
                elif event.key == K_LCTRL:
                    self.throw_boomerang()
                elif event.key == K_v:
                    self.debug = not self.debug
                    print("Toggled debug")
            elif event.type == KEYUP:
                if event.key == K_LEFT:
                    self.keyLeft = False
                elif event.key == K_RIGHT:
                    self.keyRight = False
                elif event.key == K_UP:
                    self.keyUp = False
                elif event.key == K_DOWN:
                    self.keyDown = False

    def scrollLeft(self):
        self.model.setScrollDest(self.model.getScrollDestX() + self.model.getRoomSizeX(), self.model.getScrollDestY())

    def scrollRight(self):
        self.model.setScrollDest(self.model.getScrollDestX() - self.model.getRoomSizeX(), self.model.getScrollDestY())

    def scrollUp(self):
        self.model.setScrollDest(self.model.getScrollDestX(), self.model.getScrollDestY() + self.model.getRoomSizeY())

    def scrollDown(self):
        self.model.setScrollDest(self.model.getScrollDestX(), self.model.getScrollDestY() - self.model.getRoomSizeY())

    # Getters
    def getKeyRight(self):
        return self.keyRight

    def getKeyLeft(self):
        return self.keyLeft

    def getKeyUp(self):
        return self.keyUp

    def getKeyDown(self):
        return self.keyDown


print("Use the arrow keys to move. Press Esc to quit.")
pygame.init()
m = Model()
c = Controller(m)
m.setController(c)
v = View(c, m)
m.setView(v)

while c.keep_going:
    c.update()
    m.update()
    v.update()
    sleep(0.04)
print("Goodbye")
