import pygame
import time

from pygame.locals import *
from time import sleep


class Sprite:
    def __init__(self, x, y):
        self.x = x;
        self.y = y;
        self.width = 0;
        self.height = 0;

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
        return false

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
        self.x = x;

    def setY(self, y):
        self.y = y


class Link(Sprite):
    def __init__(self, x, y, d, m):
        super(x, y)
        self.pX = 0
        self.pY = 0
        self.width = 68;
        self.height = 75;
        self.speed = 10.0
        self.direction = d;
        self.model = m;
        self.images = []

    def draw(self, g):
        if self.images[0] is None:  # If link's images have not been loaded, load them in
            for i in range(40):
                self.images.append(self.model.getView().loadImage("images/link" + i + ".png"))

        g.drawImage(self.images[self.direction], self.x + self.model.getScrollPosX(), self.y + self.model.getScrollPosY())

        # Handle link's animation loop
        if self.direction == 9 or (self.direction % 10) == 9: # If direction is 9, 19, 29, or 39 then reset link back to first direction stance else increment the animation
            self.direction -= 9
        elif self.model.getView().getController().getKeyRight() or self.model.getView().getController().getKeyLeft() or self.model.getView().getController().getKeyUp() or self.model.getView().getController().getKeyDown(): # Increment direction image if keys are down
            self.direction += 1
        else:
            # Reset to idle positions if no keys are down
            self.direction -= self.direction % 10;

    def update(self):
    # Handle link's movement
    # Images 0 - 9 are down, 10 - 19 are left, 20 - 29 are up, 30 - 39 are right
    # console.log(self.model.getView().getController().getKeyRight())
    if (self.model.getView().getController().getKeyRight()) {
    if (self.direction < 30) {
    self.direction = 30;
    }
    self.x = self.x + self.speed
    } else if (self.model.getView().getController().getKeyLeft()) {
    if (self.direction < 10 | | self.direction > 19) {
    self.direction = 10;
    }
    self.x = self.x - self.speed
    } else if (self.model.getView().getController().getKeyUp()) {
    if (self.direction < 20 | | self.direction > 29) {
    self.direction = 20;
    }
    self.y = self.y - self.speed
    } else if (self.model.getView().getController().getKeyDown()) {
    if (self.direction > 9) {
    self.direction = 0;
    }
    self.y = self.y + self.speed
    }

    if (!self.model.getScrolling()) {// Debounce to ensure scrolling doesn't glitch back and forth
    if (self.x + self.width >= 700 & & self.model.getScrollDestX() != -700) {// Scroll right
    self.model.getView().getController().scrollRight();
    } else if (self.x + self.width < 700 & & self.model.getScrollDestX() != 0) {// Scroll left
    self.model.getView().getController().scrollLeft();
    } else if (self.y + self.height >= 500 & & self.model.getScrollDestY() != -500) {// Scroll down
    self.model.getView().getController().scrollDown();
    } else if (self.y + self.height < 500 & & self.model.getScrollDestY() != 0) {// Scroll up
    self.model.getView().getController().scrollUp();
    }
    }

    for (let i = 0; i < self.model.getSprites().length; i++) {// Iterate over the sprites checking for collisions
    if (self.model.getSprites()[i].isLink()) // Do not allow link to collide with himself
    continue;
    if (self.model.doesCollide(self, self.model.getSprites()[i])) {
    let p = undefined
    if (self.model.getSprites()[i].isBrick())
    self.brickCollisionDetected(self.model.getSprites()[i]);
    else if (self.model.getSprites()[i].isPot()) {
    p = self.model.getSprites()[i];
    p.linkCollisionDetected(self);
    }
    }
    }
    return true;
    }

brickCollisionDetected(b)
{ // Fix
link
's position if he is colliding with a brick sprite
if (self.y + self.height >= b.getY() & & self.pY <= b.getY() & & self.direction <= 9) // Toe collision
self.setY(b.getY() - self.height - 1);
if (
        self.x <= b.getX() + b.getWidth() & & self.pX >= b.getX() + b.getWidth() & & self.direction <= 19 & & self.direction > 9) // Left collision
self.setX(b.getX() + b.getWidth() + 1);
if (
        self.y <= b.getY() + b.getHeight() & & self.pY >= b.getY() + b.getHeight() & & self.direction <= 29 & & self.direction > 19) // Head collision
self.setY(b.getY() + b.getHeight() + 1);
if (
        self.x + self.width >= b.getX() & & self.pX <= b.getX() & & self.direction <= 39 & & self.direction > 29) // Right collision
self.setX(b.getX() - self.width - 1);
}

savePreviousLocation()
{
self.pX = self.x;
self.pY = self.y;
}

toString()
{
return "Link (x, y, width, height) = (" + self.x + ", " + self.y + ", " + self.width + ", " + self.height + ")";
}

isLink()
{
return true;
}

// Getters
getDirection()
{
return self.direction;
}

getPX()
{
return self.pX;
}

getPY()
{
return self.pY;
}

// Setters
setDirection(d)
{
self.direction = d;
}
}

class Brick extends Sprite{

constructor(x, y, m){
super(x, y)
self.image
self.model = m;
self.width = 50;
self.height = 50;
}

< !-- Brick(Json ob, Model m){// Unmarshal constructor -->
< !-- model = m; -->
< !-- x = (int)ob.getLong("brickX"); -->
< !-- y = (int)ob.getLong("brickY"); -->
< !-- width = 50; -->
< !-- height = 50; -->
< !--} -->

existingBrick(x, y){// Checks if the brick exists
if (self.x == x & & self.y == y)


return true;
return false;
}

< !-- Json
marshal()
{ // Marshals
a
single
brick -->
< !-- Json
ob = Json.newObject();
-->
< !-- ob.add("brickX", x);
-->
< !-- ob.add("brickY", y);
-->
< !--
return ob;
-->
< !--} -->

update()
{
// Do
nothing
return true;
}

draw(g)
{ // Draws
the
brick
if (self.image == undefined) {
self.image = self.model.getView().loadImage("images/brick.jpg");
}
g.drawImage(self.image, self.x + self.model.getScrollPosX(), self.y + self.model.getScrollPosY(), self.width,
            self.height);
}

toString()
{
return "Brick (x, y, width, height) = (" + self.x + ", " + self.y + ", " + self.width + ", " + self.height + ")";
}

isBrick()
{
return true;
}
}

class Pot extends Sprite {

constructor(x, y, m){// Default constructor
super(x, y)
self.width = 40;
self.height = 40;
self.images =[]
self.model = m;
self.direction = 0
self.broken = false
self.removeDelay = 30
self.collisionOffset = 12
self.speed = 15
}

< !-- Pot(Json ob, Model m){// Unmarshal constructor -->
< !-- setX((int)ob.getLong("potX")); -->
< !-- setY((int)ob.getLong("potY")); -->
< !-- width = 40; -->
< !-- height = 40; -->
< !-- direction = (int)ob.getLong("potDirection"); -->
< !-- broken = ob.getBool("potBroken"); -->
< !-- model = m; -->
< !--} -->

< !-- Json marshal() {-->
< !-- Json ob = Json.newObject(); -->
< !-- ob.add("potX", x); -->
< !-- ob.add("potY", y); -->
< !-- ob.add("potDirection", direction); -->
< !-- ob.add("potBroken", broken); -->
< !--


return ob;
-->
< !--} -->

update()
{ // Communicates
to
model
when
to
remove
the
pot
for (let i = 0; i < self.model.getSprites().length; i++) {
let b = undefined;
if (self.model.getSprites()[i].isBrick() & & self.model.doesCollide(self, self.model.getSprites()[i])) {
b = self.model.getSprites()[i];
switch(self.direction) {
case 0: //
Do
nothing
break;
case
1:
self.x = b.getX() + b.getWidth() + self.collisionOffset;
break;
case
2:
self.x = b.getX() - self.width - self.collisionOffset;
break;
case
3:
self.y = b.getY() + b.getHeight() + self.collisionOffset;
break;
case
4:
self.y = b.getY() - self.height - self.collisionOffset;
break;
default:
if (self.model.getController().debug) console.log("Invalid brick/pot collision!");
break;
}
self.broken = true;
break;
}
}
if (self.broken) {
self.removeDelay--;
if (self.removeDelay <= 0) {
return false;
}
}
if (self.direction != 0) {
switch(self.direction) {
case
1: self.x -= self.speed;
break;
case
2: self.x += self.speed;
break;
case
3: self.y -= self.speed;
break;
case
4: self.y += self.speed;
break;
case
0: // Do
nothing
break;
default:
if (self.model.getController().debug) console.log("Invalid pot direction!");
break;
}
}
return true;
}

draw(g)
{
if (self.images[0] == undefined) {
self.images[0] = self.model.getView().loadImage("images/pot.png");
self.images[1] = self.model.getView().loadImage("images/pot_broken.png");
}

if (self.broken) {// Draw the pot depending on broken status
g.drawImage(self.images[1], self.x + self.model.getScrollPosX(), self.y + self.model.getScrollPosY(), self.width, self.height);
} else {
g.drawImage(self.images[0], self.x + self.model.getScrollPosX(), self.y + self.model.getScrollPosY(), self.width, self.height);
}

}

linkCollisionDetected(l)
{ // Determine
where
the
pot
should
slide
based
on
link
collision
if (self.direction == 0 & & !self.broken) {// Check if the pot has already been collided with or broken by a boomerang
if (l.getDirection() <= 9) // Toe collision
self.direction = 4;
else if (l.getDirection() >= 10 & & l.getDirection() <= 19) // Left collision
self.direction = 1;
else if (l.getDirection() >= 20 & & l.getDirection() <= 29) // Head collision
self.direction = 3;
else if (l.getDirection() >= 30) // Right collision
self.direction = 2;
}
}

existingPot(x, y)
{ // Checks if the
pot
exists
if (self.x == x & & self.y == y) return true;
return false;
}

toString()
{
return "Pot (x, y, width, height) = (" + x + ", " + y + ", " + width + ", " + height + ")";
}

isPot()
{
return true;
}

// Setters
setBroken(b)
{
self.broken = b;
}
}

class Boomerang extends Sprite{
static images =[]

constructor(x, y, d, m){
super(x, y)
self.width = 16;
self.height = 24;
self.direction = d;
self.speed = 15
self.model = m;
self.image = 0 // Which image is the boomerang currently drawing
}

draw(g) {
if (self.constructor.images[0] == = undefined) {// Lazy load the boomerang images
for (let i = 0; i < 4; i++) {
self.constructor.images[i] = self.model.getView().loadImage("images/boomerang" + i + ".png");
}
}

g.drawImage(self.constructor.images[self.image], self.x + self.model.getScrollPosX(), self.y + self.model.getScrollPosY(), self.width, self.height);
}

update() {
if (self.image != 3) // Increment the direction each update to animate the boomerang
self.image++;
else
self.image = 0;

if (self.direction == 0) // Control how the boomerangs coordinates change depending on direction
self.x -= self.speed;
else if (self.direction == 1)
self.x += self.speed;
else if (self.direction == 2)
self.y -= self.speed;
else if (self.direction == 3)
self.y += self.speed;

for (let i = 0; i < self.model.getSprites().length; i++) {// Check for a boomerang / pot collision
let p = undefined;
if (self.model.getSprites()[i].isPot() & & self.model.doesCollide(self, self.model.getSprites()[i])) {
p = self.model.getSprites()[i];
p.setBroken(true);


return false;
} else if (self.model.getSprites()[i].isBrick() & & self.model.doesCollide(self, self.model.getSprites()[
    i])) {// Brick / boomerang collision
return false;
}
}
return true;
}

< !-- @ Override -->
< !-- Json
marshal()
{-->
< !-- // Do
nothing, no
need
to
marshal
boomerangs -->
< !--
return null;
-->
< !--} -->

isBoomerang()
{
return true;
}

toString()
{
return "Boomerang (x, y, width, height) = (" + x + ", " + y + ", " + width + ", " + height + ")";
}

// Setters
setDirection(d)
{
self.direction = d;
}
}

class Model
    {

        constructor(c) // Default
    constructor
    {
        self.sprites = [];
    self.createObjects() // Creates
    all
    hardcoded
    objects

    self.scrolling = false // Boolean
    to
    indicate
    whether
    the
    map is still
    scrolling
    to
    its
    destination
    self.scrollSpeed = 60
    self.scrollPosX = 0
    self.scrollPosY = 0
    self.scrollDestX = 0
    self.scrollDestY = 0
    self.roomSizeX = 700
    self.roomSizeY = 500
    }

    createObjects()
    {
    // Create
    Hardcoded
    Link
    self.link = new
    Link(70, 70, 0, self)
    self.sprites.push(self.link)

    // Create
    Hardcoded
    Bricks
    self.brick = new
    Brick(0, 0, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(0, 50, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(0, 100, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(0, 150, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(0, 200, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(0, 250, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(0, 300, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(0, 350, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(50, 0, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(100, 0, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(150, 0, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(200, 0, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(250, 0, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(300, 0, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(350, 0, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(400, 0, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(450, 0, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(500, 0, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(550, 0, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(600, 0, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(650, 0, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(650, 150, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(650, 200, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(650, 250, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(650, 300, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(650, 350, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(650, 400, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(650, 450, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(600, 450, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(550, 450, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(400, 450, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(350, 450, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(300, 450, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(150, 450, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(100, 450, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(50, 450, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(0, 450, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(250, 50, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(250, 100, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(250, 150, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(250, 200, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(250, 250, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(600, 300, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(550, 300, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(500, 300, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(450, 300, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(400, 300, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(250, 300, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(700, 0, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(700, 150, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(700, 200, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(700, 300, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(700, 350, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(700, 400, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(700, 450, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(750, 0, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(800, 0, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(850, 0, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(900, 0, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(950, 0, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(1000, 0, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(1050, 0, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(1100, 0, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(1150, 0, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(1200, 0, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(1250, 0, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(1300, 0, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(1350, 0, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(1350, 50, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(1350, 100, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(1350, 150, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(1350, 200, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(1350, 250, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(1350, 300, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(1350, 350, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(1350, 400, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(1350, 450, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(1300, 450, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(1250, 450, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(1200, 450, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(1150, 450, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(1100, 450, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(750, 450, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(900, 450, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(950, 450, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(1000, 450, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(1050, 450, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(700, 250, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(750, 250, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(800, 250, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(850, 250, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(900, 250, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(950, 250, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(950, 300, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(950, 200, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(900, 500, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(750, 500, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(950, 500, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(1000, 500, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(1050, 500, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(1100, 500, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(1150, 500, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(1200, 500, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(1250, 500, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(1300, 500, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(1350, 500, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(1350, 550, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(1350, 600, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(1350, 650, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(1350, 700, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(1350, 750, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(1350, 800, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(1350, 850, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(1350, 900, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(1350, 950, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(700, 500, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(700, 550, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(700, 600, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(700, 700, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(700, 850, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(700, 900, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(700, 950, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(750, 950, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(800, 950, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(850, 950, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(900, 950, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(950, 950, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(1000, 950, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(1050, 950, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(1100, 950, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(1150, 950, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(1200, 950, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(1250, 950, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(1300, 950, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(850, 700, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(850, 750, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(850, 800, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(900, 800, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(1100, 800, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(1050, 800, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(1100, 650, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(1100, 600, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(1100, 550, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(1150, 800, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(1200, 800, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(650, 600, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(650, 700, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(650, 550, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(650, 500, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(650, 850, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(650, 900, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(650, 950, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(600, 950, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(550, 950, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(0, 400, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(0, 500, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(0, 550, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(0, 600, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(150, 500, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(300, 500, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(400, 500, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(350, 500, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(550, 500, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(600, 500, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(100, 500, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(50, 500, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(0, 650, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(0, 700, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(0, 750, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(0, 800, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(0, 850, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(0, 900, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(0, 950, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(50, 950, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(100, 950, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(150, 950, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(200, 950, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(250, 950, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(300, 950, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(350, 950, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(400, 950, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(450, 950, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(500, 950, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(300, 550, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(300, 600, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(300, 650, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(300, 700, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(300, 750, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(300, 800, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(650, 650, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(700, 650, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(1300, 650, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(1250, 650, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(1250, 800, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(1300, 800, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(1100, 150, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(1150, 150, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(1200, 150, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(1100, 300, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(1150, 300, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(1200, 300, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(1100, 200, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(1200, 200, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(1150, 200, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(1100, 250, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(1150, 250, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(1200, 250, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(400, 150, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(450, 150, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(500, 150, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(600, 700, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(550, 700, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(500, 700, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(450, 700, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(400, 700, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(350, 700, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(250, 800, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(200, 800, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(150, 800, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(750, 700, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(800, 700, self)
    self.sprites.push(self.brick)
    self.brick = new
    Brick(950, 150, self)
    self.sprites.push(self.brick)

    // Create
    Hardcoded
    Pots
    self.pot = new
    Pot(302, 305, self)
    self.sprites.push(self.pot)
    self.pot = new
    Pot(356, 303, self)
    self.sprites.push(self.pot)
    self.pot = new
    Pot(300, 349, self)
    self.sprites.push(self.pot)
    self.pot = new
    Pot(298, 396, self)
    self.sprites.push(self.pot)
    self.pot = new
    Pot(447, 75, self)
    self.sprites.push(self.pot)
    self.pot = new
    Pot(453, 224, self)
    self.sprites.push(self.pot)
    self.pot = new
    Pot(426, 604, self)
    self.sprites.push(self.pot)
    self.pot = new
    Pot(471, 605, self)
    self.sprites.push(self.pot)
    self.pot = new
    Pot(521, 603, self)
    self.sprites.push(self.pot)
    self.pot = new
    Pot(121, 626, self)
    self.sprites.push(self.pot)
    self.pot = new
    Pot(166, 625, self)
    self.sprites.push(self.pot)
    self.pot = new
    Pot(119, 676, self)
    self.sprites.push(self.pot)
    self.pot = new
    Pot(167, 676, self)
    self.sprites.push(self.pot)
    self.pot = new
    Pot(232, 853, self)
    self.sprites.push(self.pot)
    self.pot = new
    Pot(231, 900, self)
    self.sprites.push(self.pot)
    self.pot = new
    Pot(651, 756, self)
    self.sprites.push(self.pot)
    self.pot = new
    Pot(651, 800, self)
    self.sprites.push(self.pot)
    self.pot = new
    Pot(944, 588, self)
    self.sprites.push(self.pot)
    self.pot = new
    Pot(991, 589, self)
    self.sprites.push(self.pot)
    self.pot = new
    Pot(943, 632, self)
    self.sprites.push(self.pot)
    self.pot = new
    Pot(996, 635, self)
    self.sprites.push(self.pot)
    self.pot = new
    Pot(1180, 656, self)
    self.sprites.push(self.pot)
    self.pot = new
    Pot(779, 783, self)
    self.sprites.push(self.pot)
    self.pot = new
    Pot(958, 807, self)
    self.sprites.push(self.pot)
    self.pot = new
    Pot(1005, 808, self)
    self.sprites.push(self.pot)
    self.pot = new
    Pot(953, 101, self)
    self.sprites.push(self.pot)
    self.pot = new
    Pot(950, 54, self)
    self.sprites.push(self.pot)
    self.pot = new
    Pot(813, 153, self)
    self.sprites.push(self.pot)
    self.pot = new
    Pot(856, 154, self)
    self.sprites.push(self.pot)
    self.pot = new
    Pot(1003, 208, self)
    self.sprites.push(self.pot)
    self.pot = new
    Pot(1051, 208, self)
    self.sprites.push(self.pot)
    self.pot = new
    Pot(1002, 264, self)
    self.sprites.push(self.pot)
    self.pot = new
    Pot(1054, 265, self)
    self.sprites.push(self.pot)
    self.pot = new
    Pot(827, 430, self)
    self.sprites.push(self.pot)
    }

    update() // Update
    the
    model
    {
    for (let i = 0; i < self.sprites.length; i++) { // Update all sprites
    if (self.sprites[i].isLink()) // If the sprite is a link save his previous location for collision calculations
    self.link.savePreviousLocation();
    if (!self.sprites[i].update()) self.sprites.splice(i, 1); // Remove sprites when they


return a
false
update
}

if (self.scrollPosX == self.scrollDestX & & self.scrollPosY == self.scrollDestY){// Checks if the map is still scrolling
self.scrolling = false;
} else {
self.scrolling = true;
// Handle
scrolling
animation
if (self.scrollPosX < self.scrollDestX){
self.scrollPosX += Math.min(self.scrollSpeed, self.scrollDestX - self.scrollPosX);
} else {
self.scrollPosX -= Math.min(self.scrollSpeed, self.scrollPosX - self.scrollDestX);
}

if (self.scrollPosY < self.scrollDestY){
self.scrollPosY += Math.min(self.scrollSpeed, self.scrollDestY - self.scrollPosY);
} else {
self.scrollPosY -= Math.min(self.scrollSpeed, self.scrollPosY - self.scrollDestY);
}
}
}

doesCollide(spriteOne, spriteTwo)
{ // Check
for a collision between two sprites
// Check if link is not colliding
if (spriteOne.getX() + spriteOne.getWidth() <= spriteTwo.getX())
return false;
if (spriteOne.getX() >= spriteTwo.getX() + spriteTwo.getWidth())
    return false;
if (spriteOne.getY() >= spriteTwo.getY() + spriteTwo.getHeight())
    return false;
if (spriteOne.getY() + spriteOne.getHeight() <= spriteTwo.getY())
    return false;

// Otherwise
the
sprites
are
colliding
if (self.controller.debug) {
console.log("Sprite collision detected!");
console.log(spriteOne);
console.log(spriteTwo);
}
return true;
}

addSprite(s)
{ // Add
a
sprite
to
the
above
array
self.sprites.push(s)
if (self.controller.debug)
    console.log("Added " + s.toString());
}

removeSprite(i)
{ // Remove
a
sprite
from the above

array
sprites.remove(i);
}

// Getters
getSprites()
{
return self.sprites;
}

getLink()
{
return self.link;
}

getScrollPosX()
{
return self.scrollPosX;
}

getScrollPosY()
{
return self.scrollPosY;
}

getScrollDestX()
{
return self.scrollDestX;
}

getScrollDestY()
{
return self.scrollDestY;
}

getScrolling()
{
return self.scrolling;
}

getView()
{
return self.view;
}

getController()
{
return self.controller
}

getRoomSizeX()
{
return self.roomSizeX;
}

getRoomSizeY()
{
return self.roomSizeY;
}

// Setters
setView(v)
{
self.view = v;
}

setController(c)
{
self.controller = c
}

setScrollPos(x, y)
{
self.scrollPosX = x;
self.scrollPosY = y;
}

setScrollDest(x, y)
{
self.scrollDestX = x;
self.scrollDestY = y;
}
}

class View
    {

        constructor(c, m)
    {
        self.controller = c;
    self.model = m;
    self.canvas = document.getElementById("myCanvas");
    // c.loadFile(); // Load
    the
    objects
    on
    startup
    }

    loadImage(fileName)
    { // Loads
    various
    images


try {
let image = new Image()
image.src = fileName
if (self.controller.debug) {
console.log("Loaded " + fileName);
}
return image;
} catch(e)
{
console.log("Error loading " + fileName + "!");
console.trace()
}
return undefined;
}

paintComponent()
{
// Minipulate
the
700
x500
canvas
let
ctx = self.canvas.getContext("2d");
ctx.fillStyle = "aqua"
ctx.fillRect(0, 0, 700, 500);

let
sprites = self.model.getSprites() // Utilizing
an
iterator
instead
of
an
index
method
sprites.forEach(draw)

function
draw(value, index, array)
{
if (sprites[index].isLink())
return
value.draw(ctx)
}
self.model.getLink().draw(ctx); // Draw
link
last
so
that
he is over
everything
}

// Getters
getController()
{
return self.controller;
}
}

class Controller
    {
    // private
    String
    saveFile = "map.json";

    constructor(m)
    {
        self.model = m;
    self.keyLeft = false
    self.keyRight = false
    self.keyUp = false
    self.keyDown = false
    self.brickSnapIncrement = 50
    self.debug = false
    let
    self = self
    document.onkeydown = function(event)
    {self.keyPressed(event)} // When
    a
    key is pressed
    document.onkeyup = function(event)
    {self.keyReleased(event)} // When
    a
    key is released
    }

    // Keyboard
    control
    keyPressed(event)
    {
        let
    c = event.key;
    let
    code = event.keyCode

    switch(code)
    {
        case
    39: self.keyRight = true;
    break;


case
37: self.keyLeft = true;
break;
case
38: self.keyUp = true;
break;
case
40: self.keyDown = true;
break;
}

if (!(self.model.getScrolling())){// Check to make sure view is stationary first
if (event.key == "Escape" | | event.key == "Q" | | event.key == "q"){// Quits the application
close()

} else if (c == 'V' | | c == 'v') {// Toggles debug console messages
self.debug = !self.debug;
console.log("Toggled debug.");
}
}
}

keyReleased(event)
{
    let
code = event.keyCode

switch(code)
{
case
39: self.keyRight = false;
break;
case
37: self.keyLeft = false;
break;
case
38: self.keyUp = false;
break;
case
40: self.keyDown = false;
break;
}

if (!self.model.getScrolling()) {// Make sure the model is not scrolling
if (event.code === "ControlLeft") {
let b = undefined;
let l = self.model.getLink();
if (self.model.getLink().getDirection() <= 9) {// Link is facing forward
b = new Boomerang(l.getX() + l.getWidth() / 2, l.getY() + l.getHeight() / 2, 3, self.model);
} else if (self.model.getLink().getDirection() >= 10 & & self.model.getLink().getDirection() <= 19) {// Link is facing left
b = new Boomerang(l.getX() + l.getWidth() / 2, l.getY() + l.getHeight() / 2, 0, self.model);
} else if (self.model.getLink().getDirection() >= 20 & & self.model.getLink().getDirection() <= 29) {// Link is facing backwards
b = new Boomerang(l.getX() + l.getWidth() / 2, l.getY() + l.getHeight() / 2, 2, self.model);
} else {// Link is facing right
b = new Boomerang(l.getX() + l.getWidth() / 2, l.getY() + l.getHeight() / 2, 1, self.model);
}
self.model.addSprite(b);
}
}
}

< !-- update() -->
< !-- {-->
< !-- console.log(self.keyRight) -->
< !--} -->

< !-- loadFile()
{ // Load
objects
from save file

-->
< !--
try {-->
< !-- Json loadObject = Json.load(saveFile); -->
< !-- model.unmarshal(loadObject); -->
< !-- if (debug) -->
< !-- System.out.println(saveFile + " loaded."); -->
< !--} -->
< !-- catch(Exception
e){-->
< !-- System.out.println("Error loading " + saveFile + "!");
-->
< !-- e.printStackTrace(System.err);
-->
< !-- System.exit(1);
-->
< !--} -->
< !--} -->

scrollLeft()
{
self.model.setScrollDest(self.model.getScrollDestX() + self.model.getRoomSizeX(), self.model.getScrollDestY());
}

scrollRight()
{
self.model.setScrollDest(self.model.getScrollDestX() - self.model.getRoomSizeX(), self.model.getScrollDestY());
}

scrollUp()
{
self.model.setScrollDest(self.model.getScrollDestX(), self.model.getScrollDestY() + self.model.getRoomSizeY());
}

scrollDown()
{
self.model.setScrollDest(self.model.getScrollDestX(), self.model.getScrollDestY() - self.model.getRoomSizeY());
}

// Getters
getKeyRight()
{
return self.keyRight;
}

getKeyLeft()
{
return self.keyLeft;
}

getKeyUp()
{
return self.keyUp;
}

getKeyDown()
{
return self.keyDown;
}
}

class Game
    {

        constructor()
    {
    // Prepares
    the
    viewing
    window and assigns
    controller
    tasks
    self.model = new
    Model();
    self.controller = new
    Controller(self.model);
    self.view = new
    View(self.controller, self.model);
    self.model.setView(self.view);
    self.model.setController(self.controller)
    }

    // Runs
    a
    loop
    for the turtle animation
    onTimer()
    {
    // controller.update();
    self.model.update(); // Updates the model, sprites, and scroll view
    self.view.paintComponent()
    }
    }


let
game = new
Game();
let
timer = setInterval(function()
{game.onTimer();}, 40);

##########################################################################################
##########################################################################################


class Model():
    def __init__(self):
        self.dest_x = 0
        self.dest_y = 0

    def update(self):
        if self.rect.left < self.dest_x:
            self.rect.left += 1
        if self.rect.left > self.dest_x:
            self.rect.left -= 1
        if self.rect.top < self.dest_y:
            self.rect.top += 1
        if self.rect.top > self.dest_y:
            self.rect.top -= 1

    def set_dest(self, pos):
        self.dest_x = pos[0]
        self.dest_y = pos[1]


class View():
    def __init__(self, model):
        screen_size = (800, 600)
        self.screen = pygame.display.set_mode(screen_size, 32)
        self.turtle_image = pygame.image.load("turtle.png")
        self.model = model
        self.model.rect = self.turtle_image.get_rect()

    def update(self):
        self.screen.fill([0, 200, 100])
        self.screen.blit(self.turtle_image, self.model.rect)
        pygame.display.flip()


class Controller():
    def __init__(self, model):
        self.model = model
        self.keep_going = True

    def update(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.keep_going = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.keep_going = False
            elif event.type == pygame.MOUSEBUTTONUP:
                self.model.set_dest(pygame.mouse.get_pos())
        keys = pygame.key.get_pressed()
        if keys[K_LEFT]:
            self.model.dest_x -= 1
        if keys[K_RIGHT]:
            self.model.dest_x += 1
        if keys[K_UP]:
            self.model.dest_y -= 1
        if keys[K_DOWN]:
            self.model.dest_y += 1


print("Use the arrow keys to move. Press Esc to quit.")
pygame.init()
m = Model()
v = View(m)
c = Controller(m)
while c.keep_going:
    c.update()
    m.update()
    v.update()
    sleep(0.04)
print("Goodbye")
