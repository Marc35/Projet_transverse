import pygame
import math
import pymunk
import pymunk.pygame_util
import random






def clicking():#Send True if the mouse is pressed
    return pygame.mouse.get_pressed()[0]

def mouse_event(mouse_B4): #Give info about the state of the mouse's buttons
    """
    Return 1 at THE exact frame the mouse button is pressed
    Return -1 at THE exact frame the mouse button is unpressed
    Return 0 otherwise
    """
    #________________Check when mouse button is clicked/realeased________________
    if mouse_B4 == False and clicking() == True: 
        return 1
    elif mouse_B4 == True and clicking() == False:
        return -1
    return 0

def scalar(v1, v2):#Return the scalar of 2 vector
    """
    Return the scalar of 2 vector
    """
    if len(v1) != len(v2):
        raise ValueError("2 vec différents lors d'un scalire est impossible")
    summ =0
    for i in range(len(v1)):
        summ+=v1[i]*v2[i]
    return summ

def norm(vector):#Return the norm of a vector
    
    summ = 0
    for val in vector:
        summ +=val*val
    return math.sqrt(summ)

def draw(screen, space, draw_options, background_image): #Draw everything for the game to render correctly
    """
    This function draw everything needed for the game
    
    """
    screen.blit(background_image, (0, 0)) #Place the background image
    space.debug_draw(draw_options)        #Debug options to allow pymunk to show 
    """if bird:
        if ball:#If there is already a ball on screen (a rigid body so the bird azs been launched)
                #We reotate the bird acording to the body rotation,       convert radian in degre \/
            blitRotate(screen, bird, (bird_pos.x, bird_pos.y), (w/2, h/2), -1*ball.body.angle*180/math.pi)
        else:
            #Is there is no ball we show the bird without azny roation
            blitRotate(screen, bird, (bird_pos.x, bird_pos.y), (w/2, h/2), 0)
        if ball2 and ball3:
            blitRotate(screen, bird, (ball2.body.position[0], ball2.body.position[1]), (w/2, h/2), -1*ball2.body.angle*180/math.pi)
            blitRotate(screen, bird, (ball3.body.position[0], ball3.body.position[1]), (w/2, h/2), -1*ball3.body.angle*180/math.pi)
        pygame.draw.line(screen, "black", (0,0), (50, 50), 4)#Draw a line 
        pygame.draw.line(screen, "red", (50,0), (100, 50), 4)#Draw a line
        #Command use: pygame.draw.line(screen, "color", (x1,y1), (x2, y2), size)
        text = font.render("Score : "+str(score), True, (255,255,255))

        # create a rectangular object for the
        # text surface object
        textRect = text.get_rect()# GET REKT

        # set the center of the rectangular object.
        textRect.center = (1300, 20)
        screen.blit(text, textRect)
        for oink in d_pig["shape"]:
            blitRotate(screen, pig, (oink.body.position[0], oink.body.position[1]), (pig.get_size()[0]/2, pig.get_size()[1]/2), -1*oink.body.angle*180/math.pi)
        #Show the diffenrent bird on top for the user to choose from
        screen.blit(red, (150,0))
        screen.blit(chuck, (200,0))
        screen.blit(bomb, (300,-10))
        screen.blit(terence_for_show, (400,0))
        screen.blit(blues, (525,15))
        screen.blit(matilda, (600,0))
        screen.blit(hammer, (725,0))
        #Command use: screen.blit(image, (x,y)) the x and y of the image needs to be it's top left corner's coordinates
        
        #Draw lines to show the separation between the birds 
        pygame.draw.line(screen, "black", (50,0), (50, 50), 4)
        for i in range(1, 9):
            pygame.draw.line(screen, "black", (100*i,0), (100*i, 50), 4)
    elif building:
        if placing:
            pygame.draw.circle(screen, "black", pygame.mouse.get_pos(), 5)
        #Draw forward and backward arrow
        pygame.draw.line(screen, "black", (0,25), (50, 50), 4)
        pygame.draw.line(screen, "black", (0,25), (50, 0), 4) 
        pygame.draw.line(screen, "black", (450,0), (450, 50), 4)
        pygame.draw.line(screen, "black", (550,0), (550, 50), 4)

        pygame.draw.line(screen, "red", (50,0), (100, 25), 4)
        pygame.draw.line(screen, "red", (50,50), (100, 25), 4)
        
        pygame.draw.line(screen, "green", (125,50), (100, 0), 4)
        pygame.draw.line(screen, "green", (125,50), (200, 0), 4)
        pygame.draw.line(screen, "black", (50,0), (50, 50), 4)

        pygame.draw.line(screen, "black", (200,0), (300, 50), 4)
        pygame.draw.line(screen, "black", (200,50), (300, 0), 4)

        pygame.draw.line(screen, "brown", (300,25), (400, 25), 4)

        pygame.draw.line(screen, "yellow", (410,25), (440, 25), 4)
        pygame.draw.line(screen, "yellow", (425,10), (425, 40), 4)

        pygame.draw.line(screen, "green", (465,25), (485, 25), 4)
        pygame.draw.line(screen, "green", (475,15), (475, 35), 4)

        pygame.draw.line(screen, "orange", (515,25), (535, 25), 4)
        
        pygame.draw.line(screen, "red", (560,25), (590, 25), 4)

        pygame.draw.line(screen, "white", (600,0), (700, 50), 4)

        pygame.draw.line(screen, "blue", (740,10), (740, 40), 4)
        pygame.draw.line(screen, "blue", (760,10), (760, 40), 4)
        text = font.render("Weight : "+str(building_weight), True, (255,255,255))

        # create a rectangular object for the
        # text surface object
        textRect = text.get_rect()# GET REKT

        # set the center of the rectangular object.
        textRect.center = (1300, 20)
        screen.blit(text, textRect)
        for i in range(1, 11):
            pygame.draw.line(screen, "black", (100*i,0), (100*i, 50), 4)"""

def create_structure(space, rects):
    """
    Create all the diffenrents structure of the game
    """
    l_prop = []
    clr = [(128,128,128,100), (139, 69, 19, 100)]
    # For each props, gets it position, size, color and mass
    for pos, size, color, mass in rects:
        body = pymunk.Body() #Create a new body (by default is a dynamic body)
        body.position = pos  #Sets the position of the body to it's assigned position
        shape = pymunk.Poly.create_box(body, size, radius=5)    #Create a rectangle shape with the previoulsy created body
                                                                #the size given and a radius to round up the edges
        shape.color = clr[color] #Set up it's color
        shape.mass = mass   #Set up it's mass
        shape.elasticity = 0.4  #Give it an arbitrary elasticity
        shape.friction = 0.3    #Give it an arbitrary frition
        l_prop.append(shape) #Add the shape to a list of all props
        space.add(body, shape)  #Add the newly created props to the game
    return l_prop

def map_limit(space, w=1600, h=1000):
    #A list of rectangle that will be used to act as map limit
    rec=[
        [(w/2, h-20), (w, 40)],
        [(w/2, 25), (w, 50)],
        [(0, h/2), (40, h)],
        [(w, h/2), (40, h)]
    ]
    #Similar to the previous function "create_structure", refer to it if you have question about this code
    for r in rec:
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        body.position = r[0]
        shape = pymunk.Poly.create_box(body, r[1])
        shape.elasticity = 0.4
        shape.friction = 0.2
        space.add(body, shape)

def add_object(space, x, y,radius, mass):
    """
    Adds an ball to the space with:
        Some coordinates
        A radius
        A mass
    """
    body = pymunk.Body(1,1) #Create the body
    body.position = (x, y) #Setup it's position according to given coordinates
    shape = pymunk.Circle(body, radius) #Creating a circle shape with the body and radius
    shape.mass = mass #We give it the given mass
    shape.color = (0,0,0,0)
    shape.elasticity = 2/3 #Give an elasticity
    shape.friction = 3/4 #And a friction
    space.add(body, shape) #Then adds it to the pymnuk space
    return shape

def blitRotate(screen, bird, pos, originPos, angle):

    # offset from pivot to center
    bird_rect = bird.get_rect(topleft = (pos[0] - originPos[0], pos[1]-originPos[1]))#Create a rectangle
    offset_center_to_pivot = pygame.math.Vector2(pos) - bird_rect.center
    
    # roatated offset from pivot to center
    rotated_offset = offset_center_to_pivot.rotate(-angle)

    # roatetd bird center
    rotated_bird_center = (pos[0] - rotated_offset.x, pos[1] - rotated_offset.y)

    # get a rotated bird
    rotated_bird = pygame.transform.rotate(bird, angle)
    rotated_bird_rect = rotated_bird.get_rect(center = rotated_bird_center)

    screen.blit(rotated_bird, rotated_bird_rect) #Show the rotated bird to the screen
 
def rectRect(r1x, r1y, r1w, r1h, r2x, r2y, r2w, r2h): #Say if 2 rectangles are touching each other
    """
    Input:
        r1x, r1y, = coordinates of the 1st rectangle
        r1w, r1h, = width and length of the 1st rectangle
        
        r2x, r2y, = coordinates of the 2nd rectangle
        r2w, r2h  = width and length of the 2nd rectangle
    Output:
        Bool: True => They are touching
              False =>They ain't touching 
    
    """
    return r1x + r1w >= r2x and r1x <= r2x + r2w and r1y + r1h >= r2y and r1y <= r2y + r2h

def gravity_formula(body, dt):
    #shorten lines that uses this formula
    return [100*dt*9.81*body.mass*math.sin(body.angle) , 100*dt*9.81*body.mass*math.sin(body.angle+math.pi/2)]

def remove_ball(space, ball, ball2, ball3, egg, origin_bird_pos, bird_pos, launching):
    if ball: #If there is currently a ball
        space.remove(ball, ball.body) #We remove it
        ball = None #We set it back to being None
        launching = False #If there is no ball then nothing is being launched

        #We reset the birds Position
        bird_pos.x = origin_bird_pos[0] 
        bird_pos.y = origin_bird_pos[1]

        #If we have a 2 other balls or if we have an egg, we remove them too
        if ball2 and ball3: 
            space.remove(ball2, ball2.body)
            space.remove(ball3, ball3.body)
            ball2, ball3 = None, None
        elif egg:
            space.remove(egg, egg.body)
            egg = None
    return (ball, bird_pos, launching, ball2, ball3, egg)

def rects_files(file_name, line_number):
    l_rec = []
    with open(file_name, "r") as f:
        file = f.readlines()
        for val in file[line_number%len(file)].split(";"):
            l_rec.append(val)
        f.close()
    return l_rec

class DummyV1:
    def __init__(self, space, pos):
        self.default_friction = 0.99
        self.space = space
        self.head_radius = 15

        # Part offsets, relative to the center of the body (which is the upper torso)
        self.head_relOffset = (0, -self.head_radius * 3)
        self.upperTorso_relOffset = (0, 0)
        self.lowerTorso_relOffset = (0, 25)

        self.leftArm_relOffset = (-55, -20)
        self.rightArm_relOffset = (55, -20)

        self.leftLeg_relOffset = (-12, 72)
        self.rightLeg_relOffset = (12, 72)

        # Constraint Offsets
        # Neck
        self.head_neckOffset = (0, 10)
        self.upperTorso_neckOffset = (0, -30)

        # Shoulders
        self.leftArm_leftShoulderOffset = (30, 0)
        self.rightArm_rightShoulderOffset = (-30, 0)
        self.upperTorso_leftShoulderOffset = (-25, -20)
        self.upperTorso_rightShoulderOffset = (25, -20)

        # Hips
        self.upperTorso_leftLowerTorsoOffset = (0, 16)
        self.upperTorso_rightLowerTorsoOffset = (0, 16)

        # Legs
        self.lowerTorso_leftLegOffset = (-11, 12)
        self.lowerTorso_rightLegOffset = (11, 12)


        # Head - Physical Object Information
        self.head_mass = 5
        self.head_moment = 150
        self.head_body = pymunk.Body(self.head_mass, self.head_moment, body_type=pymunk.Body.DYNAMIC)
        self.head_body.position = (pos[0] + self.head_relOffset[0], pos[1] + self.head_relOffset[1])  # Set position to given position + box_offset
        self.head_shape = pymunk.Circle(self.head_body, self.head_radius)
        self.head_shape.friction = self.default_friction

        # Upper Torso - Physical Object Information
        self.upperTorso_mass = 10
        self.upperTorso_moment = 300
        self.upperTorsoWidth, self.upperTorsoHeight = 40, 60
        self.upperTorsoVertices = [(-self.upperTorsoWidth / 2, -self.upperTorsoHeight / 2), (self.upperTorsoWidth / 2, -self.upperTorsoHeight / 2),
                                   (self.upperTorsoWidth / 3, self.upperTorsoHeight / 4), (-self.upperTorsoWidth / 3, self.upperTorsoHeight / 4)]
        self.upperTorso_body = pymunk.Body(self.upperTorso_mass, self.upperTorso_moment, body_type=pymunk.Body.DYNAMIC)
        self.upperTorso_body.position = (pos[0] + self.upperTorso_relOffset[0], pos[1] + self.upperTorso_relOffset[1])
        self.upperTorso_shape = pymunk.Poly(self.upperTorso_body, self.upperTorsoVertices)
        self.upperTorso_shape.friction = self.default_friction

        # Lower Torso - Physical Object Information
        self.lowerTorso_mass = 10
        self.lowerTorso_moment = 300
        self.lowerTorsoWidth, self.lowerTorsoHeight = 60, 25
        self.lowerTorsoVertices = [(-self.lowerTorsoWidth / 4, -self.lowerTorsoHeight / 4),
                                   (self.lowerTorsoWidth / 4, -self.lowerTorsoHeight / 4),
                                   (self.lowerTorsoWidth / 3, self.lowerTorsoHeight / 2),
                                   (-self.lowerTorsoWidth / 3, self.lowerTorsoHeight / 2)]
        self.lowerTorso_body = pymunk.Body(self.lowerTorso_mass, self.lowerTorso_moment, body_type=pymunk.Body.DYNAMIC)
        self.lowerTorso_body.position = (pos[0] + self.lowerTorso_relOffset[0], pos[1] + self.lowerTorso_relOffset[1])
        self.lowerTorso_shape = pymunk.Poly(self.lowerTorso_body, self.lowerTorsoVertices)
        self.lowerTorso_shape.friction = self.default_friction

        # Left Arm - Physical Object Information
        self.leftArm_mass = 10
        self.leftArm_moment = 150
        self.leftArmWidth, self.leftArmHeight = 65, 15
        self.leftArmVertices = [(-self.leftArmWidth / 2, -self.leftArmHeight / 2),
                                   (self.leftArmWidth / 2, -self.leftArmHeight / 2),
                                   (self.leftArmWidth / 2, self.leftArmHeight / 2),
                                   (-self.leftArmWidth / 2, self.leftArmHeight / 2)]
        self.leftArm_body = pymunk.Body(self.leftArm_mass, self.leftArm_moment, body_type=pymunk.Body.DYNAMIC)
        self.leftArm_body.position = (pos[0] + self.leftArm_relOffset[0], pos[1] + self.leftArm_relOffset[1])
        self.leftArm_shape = pymunk.Poly(self.leftArm_body, self.leftArmVertices)
        self.leftArm_shape.friction = self.default_friction

        # Right Arm - Physical Object Information
        self.rightArm_mass = 10
        self.rightArm_moment = 150
        self.rightArmWidth, self.rightArmHeight = 65, 15
        self.rightArmVertices = [(-self.rightArmWidth / 2, -self.rightArmHeight / 2),
                                (self.rightArmWidth / 2, -self.rightArmHeight / 2),
                                (self.rightArmWidth / 2, self.rightArmHeight / 2),
                                (-self.rightArmWidth / 2, self.rightArmHeight / 2)]
        self.rightArm_body = pymunk.Body(self.rightArm_mass, self.rightArm_moment, body_type=pymunk.Body.DYNAMIC)
        self.rightArm_body.position = (pos[0] + self.rightArm_relOffset[0], pos[1] + self.rightArm_relOffset[1])
        self.rightArm_shape = pymunk.Poly(self.rightArm_body, self.rightArmVertices)
        self.rightArm_shape.friction = self.default_friction

        # Left Leg - Physical Object Information
        self.leftLeg_mass = 10
        self.leftLeg_moment = 200
        self.leftLegWidth, self.leftLegHeight = 15, 65
        self.leftLegVertices = [(-self.leftLegWidth / 2, -self.leftLegHeight / 2),
                                 (self.leftLegWidth / 2, -self.leftLegHeight / 2),
                                 (self.leftLegWidth / 2, self.leftLegHeight / 2),
                                 (-self.leftLegWidth / 2, self.leftLegHeight / 2)]
        self.leftLeg_body = pymunk.Body(self.leftLeg_mass, self.leftLeg_moment, body_type=pymunk.Body.DYNAMIC)
        self.leftLeg_body.position = (pos[0] + self.leftLeg_relOffset[0], pos[1] + self.leftLeg_relOffset[1])
        self.leftLeg_shape = pymunk.Poly(self.leftLeg_body, self.leftLegVertices)
        self.leftLeg_shape.friction = self.default_friction

        # Right Leg - Physical Object Information
        self.rightLeg_mass = 10
        self.rightLeg_moment = 200
        self.rightLegWidth, self.rightLegHeight = 15, 65
        self.rightLegVertices = [(-self.rightLegWidth / 2, -self.rightLegHeight / 2),
                                (self.rightLegWidth / 2, -self.rightLegHeight / 2),
                                (self.rightLegWidth / 2, self.rightLegHeight / 2),
                                (-self.rightLegWidth / 2, self.rightLegHeight / 2)]
        self.rightLeg_body = pymunk.Body(self.rightLeg_mass, self.rightLeg_moment, body_type=pymunk.Body.DYNAMIC)
        self.rightLeg_body.position = (pos[0] + self.rightLeg_relOffset[0], pos[1] + self.rightLeg_relOffset[1])
        self.rightLeg_shape = pymunk.Poly(self.rightLeg_body, self.rightLegVertices)
        self.rightLeg_shape.friction = self.default_friction

        self.list_body = [
            self.head_body,

            self.upperTorso_body,
            self.lowerTorso_body,

            self.leftArm_body,
            self.rightArm_body,

            self.leftLeg_body,
            self.rightLeg_body
        ]
        self.list_shape = [
            self.head_shape,

            self.upperTorso_shape,
            self.lowerTorso_shape,

            self.leftArm_shape,
            self.rightArm_shape,

            self.leftLeg_shape,
            self.rightLeg_shape
        ]
    def addToSpace(self):
        # Add Head
        self.space.add(self.head_body, self.head_shape)

        # Torso
        self.space.add(self.upperTorso_body, self.upperTorso_shape)
        self.space.add(self.lowerTorso_body, self.lowerTorso_shape)

        # Arms
        self.space.add(self.leftArm_body, self.leftArm_shape)
        self.space.add(self.rightArm_body, self.rightArm_shape)

        # Legs
        self.space.add(self.leftLeg_body, self.leftLeg_shape)
        self.space.add(self.rightLeg_body, self.rightLeg_shape)

        # Joints
        # Neck
        self.neckConstraint = pymunk.PivotJoint(self.head_body, self.upperTorso_body, (
        (self.upperTorso_body.position.x + self.upperTorso_neckOffset[0]),
        (self.upperTorso_body.position[1] + self.upperTorso_neckOffset[1])))
        self.space.add(self.neckConstraint)

        # Arms
        self.leftArmConstraint = pymunk.PivotJoint(self.leftArm_body, self.upperTorso_body, (
        (self.upperTorso_body.position.x + self.upperTorso_leftShoulderOffset[0]),
        (self.upperTorso_body.position[1] + self.upperTorso_leftShoulderOffset[1])))
        self.rightArmConstraint = pymunk.PivotJoint(self.rightArm_body, self.upperTorso_body, (
        (self.upperTorso_body.position.x + self.upperTorso_rightShoulderOffset[0]),
        (self.upperTorso_body.position[1] + self.upperTorso_rightShoulderOffset[1])))
        # self.leftArmConstraint.max_force = 50000 ** 50
        # self.leftArmConstraint.max_bias = 20 ** 60
        # self.leftArmConstraint.error_bias = 0
        self.space.add(self.leftArmConstraint, self.rightArmConstraint)

        # Hips
        self.leftHipConstraint = pymunk.PivotJoint(self.lowerTorso_body, self.upperTorso_body, (
        (self.upperTorso_body.position.x + self.upperTorso_leftLowerTorsoOffset[0]),
        (self.upperTorso_body.position[1] + self.upperTorso_leftLowerTorsoOffset[1])))
        self.RightHipConstraint = pymunk.PivotJoint(self.lowerTorso_body, self.upperTorso_body, (
        (self.upperTorso_body.position.x + self.upperTorso_rightLowerTorsoOffset[0]),
        (self.upperTorso_body.position[1] + self.upperTorso_rightLowerTorsoOffset[1])))
        self.space.add(self.leftHipConstraint, self.RightHipConstraint)

        # Legs
        self.leftLegConstraint = pymunk.PivotJoint(self.leftLeg_body, self.lowerTorso_body, (
        (self.lowerTorso_body.position.x + self.lowerTorso_leftLegOffset[0]),
        (self.lowerTorso_body.position[1] + self.lowerTorso_leftLegOffset[1])))
        self.rightLegConstraint = pymunk.PivotJoint(self.rightLeg_body, self.lowerTorso_body, (
        (self.lowerTorso_body.position.x + self.lowerTorso_rightLegOffset[0]),
        (self.lowerTorso_body.position[1] + self.lowerTorso_rightLegOffset[1])))
        self.space.add(self.leftLegConstraint, self.rightLegConstraint)

    def apply_gravity(self, dt):
        for body in self.list_body:
            g = gravity_formula(body, dt)
            body.apply_impulse_at_local_point((g[0],g[1]),(0,0))
            body.position.y
    