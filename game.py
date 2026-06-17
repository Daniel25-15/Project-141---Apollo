# Glory to God the Father, God the Son, and God the Holy Spirit, the one and only True God, the Holy Trinity, for whom without I can do nothing.
# Romans 11:36

from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.shaders import lit_with_shadows_shader
import random, time

app = Ursina()

logo = """
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
 XX■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■XX 
   X■                                                       ■X   
    X■■                                                   ■■X    
     XX■                        ▄▓                       ■XX     
       X■■                      █▓                     ■■X       
        XX■                     █▓                    ■XX        
          X■                 ███████▓                ■X          
           X■■                  █▓                 ■■X           
            XX■                 █▓                ■XX            
              X■                █▓              ■■X              
               X■■              █▓             ■XX               
                XX■             █▓            ■X                 
                  X■■           █▓          ■■X                  
                   XX■          ▀          ■XX                   
                     X■    +---------+    ■X                     
                      X■■  |The Truth|  ■■X                      
                       XX■ +---------+ ■XX                       
                         X■■         ■■X                         
                          XX■       ■XX                          
                            X■     ■X                            
                             X■■ ■■X                             
                              XX■XX                              
                                X                                
"""

ascii_logo = """
   _■■_    
  (    )   
 (      )  
  \    /\  
  /\  /  \ 
 /  \/    \
/   / \   /
\  /   \ / 
 \/     \  
 (      )  
  (    )   
   -■■-    
"""

#the plane that everything is built on top of.
ground = Entity(
    model='plane',
    texture='grass',
    scale=(300, 1, 300),
    color=color.green,
    texture_scale=(100, 100),
    collider='box'
)

# configurations for the skycolor
sky = Sky()
sky.texture = "radial_gradient"
sky.color = color.red
# sky.color = color.hsv(26.3, 0.895, 0.710)
# sky.color = color.rgb(181, 90, 19)

# AmbientLight(color=color.rgba(0.3, 0.3, 0.3, 1))


#definition for the lootbox for the unlocking entity for the weapon 3
lootBox = Entity(
    model="cube",
    texture="brick",
    scale=1,
    color=color.gold,
    collider="box",
    position=(8, 4.5, 12)
)

# defining the UI elements
menu = Entity(
    parent=camera.ui,
    model="quad",
    color=color.white,
    scale=(0.6, 0.3),
    z=-0.1,
    enabled=False,
)
menu.collider = None
quit_button = Button(
    text="Escape",
    color=color.green,
    scale=(0.6, 0.2),
    y=0,
    parent=menu,
    z=-0.01
)
return_button = Button(
    text="return",
    color=color.green,
    scale=(0.6, 0.2),
    y=0.25,
    parent=menu,
    z=-0.01
)

# defining the credits menu UI
credits_button = Button(
    text="Credits",
    color=color.green,
    scale=(0.6, 0.2),
    y=-0.25,
    parent=menu,
    z=-0.01
)

CreditsMenu = Entity(
    parent=camera.ui,
    model="quad",
    color=color.white,
    world_scale = 15,
    z=-0.1,
    enabled=False,
)
CreditsLabel = Text(
    parent=CreditsMenu,
    y=0.0,
    scale=1.25,
    origin=(0, 0),
    color = color.black,
    text="Creator of the project: Daniel Glenn\nLead, and only, programmer: Daniel Glenn\nLead, and only, 3d modeler, Artist, and Animator: Jude Roberts",
    z=-0.2
)
CreditsMenuLeave = Button(
    text="Exit",
    color=color.green,
    scale=(0.5, 0.1),
    y=-0.375,
    parent=CreditsMenu,
    z=-0.01
)

UI_ADMIN_MENU = Entity(
    parent=camera.ui,
    model="quad",
    color=color.white,
    scale=(0.6, 0.3),
    z=-0.1,
    enabled=False,
)
UI_ADMIN_Exit = Button(
    text="Exit",
    color=color.gray,
    scale=(0.6, 0.2),
    y=0.25,
    parent=UI_ADMIN_MENU,
    z=-0.01
)
def ADMIN_MENU_EXIT():
    global admin_menu_toggle
    admin_menu_toggle = not admin_menu_toggle
    mouse.locked = not admin_menu_toggle
    player.enabled = not admin_menu_toggle
    UI_ADMIN_MENU.enabled = False

    UI_ADMIN_MENU.enabled = False

UI_ADMIN_Exit.on_click = ADMIN_MENU_EXIT

# class (or a builder) for all of the walls, to make them eisier to replicate more of them
class Wall():
    def __init__(self,Name, model_type, texture_type, scale_def, color_def, texture_scale_def, collider_type, position_all):
        self.entity = Entity(
            model=model_type,
            texture=texture_type,
            scale=scale_def,
            color=color_def,
            texture_scale=texture_scale_def,
            collider=collider_type,
            position=position_all,
        )

# (x, y, z)
# using the walls and actually building them
def buildWalls():
    wall1 = Wall("Wall1", 'cube', 'white_cube', (1, 9, 9), color.gray,  (1, 1), 'box', (5.5, 4.5, 10.5))
    wall2 = Wall("Wall2", 'cube', 'white_cube', (9, 9, 1), color.gray,  (1, 1), 'box', (9.5, 4.5, 14.5))
    wall3 = Wall("Wall3", 'cube', 'white_cube', (1, 9, 9), color.gray,  (1, 1), 'box', (14.5, 4.5, 10.5))
    wall4 = Wall("Wall4", 'cube', 'white_cube', (2, 1, 2), color.gray,  (1, 1), 'box', (13, 0.5, 11))
    wall5 = Wall("Wall5", 'cube', 'white_cube', (2, 1, 2), color.gray,  (1, 1), 'box', (13, 1.5, 13))
    wall6 = Wall("Wall6", 'cube', 'white_cube', (2, 3, 2), color.gray,  (1, 1), 'box', (11, 1.5, 13))
    wall7 = Wall("Wall7", 'cube', 'white_cube', (4, 4, 4), color.gray,  (1, 1), 'box', (8, 2, 12))

buildWalls()

# pre defining elements for later use, some of them are empty because they will have things added into them later

bullets_1 = []
bullets_2 = []
bullets_3 = []

mag_1 = 10
mag_2 = 15
mag_3 = 35

ammo_amount_1 = 120
ammo_amount_2 = 100
ammo_amount_3 = 500

global_score = 0
global_health = 100

fireRate3 = 0.05
cooldown_timer = 0.0

dummies = []
followers = []

inventory = []

#defining the 3 weapon types ( NOTE THESE WILL BE REPLACED EVENTUALLY WITH A CLASS or BUILDER for the weapons to make implementing different ones eisier)

gun_NoModel = Entity(parent=camera, model='pistolModel', color=color.dark_gray, origin_y=-0.5, scale= (0.5, 0.5, 0.5), position= (1.5, -1.5, 2.5), rotation=(0, -90, 0), overlay=True, add_to_scene_entities=False, render_queue=1)
gun_NoModel_2 = Entity(parent=camera, model='cube', color=color.green, origin_y=-0.5, scale= (0.5, 0.5, 2), position= (2, -1, 2.5), overlay=True,)
gun_NoModel_3 = Entity(parent=camera, model='Assault Rifle.glb', color=color.red, origin_y=-0.5, scale= (0.5, 0.5, 2), position= (2, -1, 2.5), rotation=(0, -110, 0), overlay=True,)
gun_NoModel_2.enabled = False
gun_NoModel_3.enabled = False

gun_NoModel.collider = None
gun_NoModel_2.collider = None
gun_NoModel_3.collider = None

gun_NoModel.intersects = False
enable_gun_3 = False

globalUIelementsColor = color.black

# defining the player, and giving it the pre built basic movement capabilites
player = FirstPersonController(
    speed = 15,
    # model='sphere',
    model = None,
    y=0,
    # scale=(0.5, 1, 0.5),
    # collider = "box"
    # position=(10, 0, 10)
)

player.collider = 'sphere'
# player.scale = (0.5, 0.5, 0.5)
# player.height = 8
# camera.y = 2

# player.collider = BoxCollider(player, center=(0,1,0), size=(1.5, 2, 1.5))
# player.slope_smoothing = 2 

# Adding the weapon models to the player to show they are being held
player.gun_1 = gun_NoModel
player.gun_2 = gun_NoModel_2
player.gun_3 = gun_NoModel_3

player.ignore_list.append(gun_NoModel)

# x, y, z = 5, 5, 6
#defines the UI elements for each of the ammo counters that update when a bullet is shot
UI_Bullet_Counter_1 = Text(
    text=f"Ammo: {mag_1}\nReserve: {ammo_amount_1}",
    scale=1.25,
    position=(0.37, -0.388),
    parent=camera.ui,
    color=globalUIelementsColor
)
UI_weapon_1_2d = Sprite(
    scale=0.025,
    position=(0.3, -0.415),
    parent=camera.ui,
    texture="pistolPNG"
)
UI_Bullet_Counter_2 = Text(
    text=f"Ammo: {mag_2}\nReserve: {ammo_amount_2}",
    scale=1.25,
    # position=(-0.8, 0.40),
    position=(0.37, -0.388),
    parent=camera.ui,
    color=globalUIelementsColor
)
UI_weapon_2_2d = Sprite(
    scale=0.025,
    position=(0.3, -0.415),
    parent=camera.ui,
    texture="bulletsPNG"
)
UI_Bullet_Counter_3 = Text(
    text=f"Ammo: {mag_3}\nReserve: {ammo_amount_3}",
    scale=1.25,
    # position=(-0.8, 0.35),
    position=(0.37, -0.388),
    parent=camera.ui,
    color=globalUIelementsColor
)
UI_weapon_3_2d = Sprite(
    scale=0.025,
    position=(0.3, -0.415),
    parent=camera.ui,
    texture="pistolPNG"
)

UI_Score_Counter = Text(
    text=f"Score: {global_score}",
    scale=1,
    position=(0.0, 0.45),
    parent=camera.ui,
    color=globalUIelementsColor
)
UI_score_2d = Sprite(
    scale=0.01,
    position=(-0.05, 0.44),
    parent=camera.ui,
    texture="scorePNG"
)

# defines the UI elements for the health of the player that gets updated later
UI_Health_Counter = Text(
    text=f"Health: {global_health}",
    scale=1.5,
    position=(-0.8, -0.4),
    parent=camera.ui,
    color=globalUIelementsColor
)
UI_health_2d = Sprite(
    scale=0.01,
    position=(-0.825, -0.415),
    parent=camera.ui,
    texture="healthPNG"
)

lootBox_2 = Entity(
    model="cube",
    texture="scorePNG",
    scale=1,
    color=color.gold,
    collider="box",
    position=(12, 4.5, 12)
)

# handles the death function by reseting health, reseting score, and reseting player position
def handleDeath():
    global global_score, global_health
    global_score = 0
    UI_Score_Counter.text = f"Score: {global_score}"
    player.x = 0
    player.y= 0
    player.z= 0
    global_health = 100
    UI_Health_Counter.text = f"Health: {global_health}"

def showCredits():
    menu.enabled = False
    CreditsMenu.enabled = True

def ExitCredits():
    CreditsMenu.enabled = False
    mouse.locked = True
    player.enabled = True

# was used to create randomly generated target dummies NOTE is not used anymore, but MIGHT come back later in an update.
def generate_dummies():
    for i in range(9):
        x = random.choice([3, 4, 5, 6, 9])
        y = random.choice([3, 4, 5, 6, 9])
        z = random.choice([3, 4, 5, 6, 9])

        dummy = Entity(model='cube', color=color.white,texture='target.png',scale=(1,1,0.1),dx=0.05, position=(x,y,z), collider='box')
        dummies.append(dummy)
# generate_dummies()
escape_menu_toggle = False
admin_menu_toggle = False
generateNewFollowerToggle = False


# generateFollowerEntity(3, 0, 0, 1)
scale_var = 1

# defines the follower generation, and adds each follower to a list. 
def generateFollower():
    for i in range(random.randint(5, 15)): # generates a random integer of followers
        # spaces each spawn for each follower out by taking a set integer, and then multiplying the number of followers by 3 to distance them
        spawn_x = 5 + (i * 3)
        follower = Entity(
            model="character",
            scale=1, #(scale_var, scale_var, scale_var)
            position=(spawn_x, 0, 0),
            collider="box",
            # shader=lit_with_shadows_shader,
            # color=color.black,
            # texture="newmodel.png"
        )
        follower.speed = random.randint(2, 5)
        # adds each follower to a list that is used later
        followers.append(follower)
        generateNewFollowerToggle = False

# generateFollower()



def return_to_game():
    global escape_menu_toggle
    escape_menu_toggle = not escape_menu_toggle
    mouse.locked = not escape_menu_toggle
    player.enabled = not escape_menu_toggle
    menu.enabled = False

quit_button.on_click = application.quit
return_button.on_click = return_to_game

credits_button.on_click = showCredits
CreditsMenuLeave.on_click = ExitCredits
# quit_button.enabled = escape_menu_toggle

# OLD CODE, UN USED
def final_menu():
    global escape_menu_toggle
    escape_menu_toggle = True

    escape_menu_toggle = not escape_menu_toggle
    mouse.locked = not escape_menu_toggle
    player.enabled = not escape_menu_toggle

    if 'win_message' in globals():
        # destroy(win_message)
        pass
# takes the distance given, and the amount the player is to be taken off of the ground, and then uses a raycast to check to position for any entities in the way
# if there are entities it stops, if there arent, then the position where the player ends up is calculated by adding player position to the player moving forward for the distance, to get an integer
# with that integer, the player is animated its movement so that it isnt a teleport, and moves to that position
def dash(MoveDistance, raise_y):
    MoveDistance
    dashHitInfo = raycast(player.position + Vec3(0, 1, 0), player.forward, distance=MoveDistance, ignore=(player,))
    if dashHitInfo.hit:
        finalMoveDistance = dashHitInfo.distance - 0.5
    else:
        finalMoveDistance = MoveDistance
        if raise_y == 1:
            player.y += 3

    targetPosition = player.position + (player.forward * finalMoveDistance)
    player.animate_position(targetPosition, duration=0.3, curve=curve.linear)

weapon = 1

# class or builder for the bullet entity that is used by every weapon. takes arguments to change the apperance of the bullet
class Bullet(Entity):
    def __init__(self, color_def, **kwargs):
        super().__init__(
            parent=scene,
            model='9mmbullet_model_final.glb',
            scale=1,
            color=color_def,
            collider='box',
            # texture="BulletTexture"
            **kwargs
        )
        self.speed = 400
        self.lifetime = 2.5
    # has its own update function, because it needs to calculate the movement and path it needs to take
    def update(self):
        global global_score
        self.lifetime -= time.dt
        if self.lifetime <= 0:
            destroy(self)
            return
        # checks for any collisions with the bullet, and then checks if those collisions are 'worth' triggering something else 
        distThisFrame = self.speed * time.dt
        hit_info = raycast(self.world_position, self.forward, distance=distThisFrame, ignore=(self, player))

        if hit_info.hit:
            if hit_info.entity in dummies:
                dummies.remove(hit_info.entity)
                destroy(hit_info.entity)
                global_score += 1
                UI_Score_Counter.text = f"Score: {global_score}"
            elif hit_info.entity in followers: 
                followers.remove(hit_info.entity)
                destroy(hit_info.entity)
                global_score += 1
                UI_Score_Counter.text = f"Score: {global_score}"
                print(len(followers))
            destroy(self)
        else:
            self.position += self.forward * distThisFrame

# takes the duration of the shake and the intesity, and for the duration, it moves the camera position in random directions with the intesity being the areas it can vary
def cameraShake(duration=0.2, intensity=0.1):
    originalPosition = camera.position
    def executeShake(durationRemaining):
        if durationRemaining > 0:
            camera.x = originalPosition.x + random.uniform(-intensity, intensity)
            camera.y = originalPosition.y + random.uniform(-intensity, intensity)
            invoke(executeShake, durationRemaining - 0.02, delay=0.02)
        else:
            camera.position = originalPosition
    executeShake(duration)

# handles the reloads for each weapon. each weapon takes the ammount of ammo its supposed to have, and subtracts that amount of ammo from the ammo reserve, and then resets the ammo it can. if you dont have enough for a full mag, then you get whatever you have left
# takes the minimum between the max size minus the ammount currently in the mag, and the size in the reserve 
def reload_1():
    global mag_1, ammo_amount_1
    ammoNeededToAdd = min(10 - mag_1, ammo_amount_1)
    mag_1 += ammoNeededToAdd
    ammo_amount_1 -= ammoNeededToAdd
    UI_Bullet_Counter_1.text = f"Ammo: {mag_1}\nReserve: {ammo_amount_1}"
def reload_2():
    global mag_2, ammo_amount_2
    ammoNeededToAdd = min(15 - mag_2, ammo_amount_2)
    mag_2 += ammoNeededToAdd
    ammo_amount_2 -= ammoNeededToAdd
    UI_Bullet_Counter_2.text = f"Ammo: {mag_2}\nReserve: {ammo_amount_2}"
def reload_3():
    global mag_3, ammo_amount_3
    ammoNeededToAdd = min(35 - mag_3, ammo_amount_3)
    mag_3 += ammoNeededToAdd
    ammo_amount_3 -= ammoNeededToAdd
    UI_Bullet_Counter_3.text = f"Ammo: {mag_3}\nReserve: {ammo_amount_3}"

weaponToggle = False
#BROKEN
def disableWeapon():
    global weaponToggle,weapon 
    print(f"DISABLED WEAPON: {weapon}")
    weaponToggle = not weaponToggle
    if weaponToggle == False:
        if weapon == 1:
            gun_NoModel.enabled = False

#handles all of the keyboard inputs that trigger other things (keybinds that trigger things)
def input(key):
    # print(key)
    global escape_menu_toggle, weapon, mag_1, mag_2, mag_3, admin_menu_toggle, enable_gun_3, ammo_amount_1, ammo_amount_2, ammo_amount_3, global_score
    if key == 'escape':
        escape_menu_toggle = not escape_menu_toggle
        mouse.locked = not escape_menu_toggle
        player.enabled = not escape_menu_toggle
        if CreditsMenu.enabled:
            CreditsMenu.enabled = False
        # quit_button.enabled = not escape_menu_toggle
        menu.enabled = escape_menu_toggle


    if key == 'left mouse down' and not menu.enabled:
       # once the shoot button is clicked, the weapon is checked, and then the ammo count is checked. if both are in valid states, then the bullet fires. Otherwise the check breaks and nothing happens
        if weapon == 1 and mag_1 > 0:
            Bullet(color.black, position=camera.world_position + gun_NoModel.forward, rotation=camera.world_rotation)
            gun_NoModel.blink(color.white)
            mag_1 -= 1
            UI_Bullet_Counter_1.text = f"Ammo: {mag_1}\nReserve: {ammo_amount_1}"
            print(mag_1)
        elif weapon == 2 and mag_2 > 0:
            Bullet(color.green, position=camera.world_position + gun_NoModel_2.forward, rotation=camera.world_rotation)
            gun_NoModel_2.blink(color.white)
            mag_2 -= 1
            UI_Bullet_Counter_2.text = f"Ammo: {mag_2}\nReserve: {ammo_amount_2}"
            print(mag_2)
        elif weapon == 3:
            pass
# if you ADS (Aim Down Sights) then the camera zooms in (NOTE THIS WILL BE REWORKED LATER) and then the gun model position shifts over to make it look more defined
    if key == 'right mouse down' and player.gun_3 and not menu.enabled:
        camera.z = 5
        if weapon == 1:
            gun_NoModel.position = (0.25, -1.5, 2.5)
        if weapon == 2:
            gun_NoModel_2.position = (0.25, -1.5, 2.5)
        if weapon == 3:
            gun_NoModel_3.position = (0.15, -1, 2.5)
            gun_NoModel_3.rotation =(0, -87, 0)
    if key == 'right mouse up' and player.gun_3:
        camera.z = 0
        if weapon == 1:
            gun_NoModel.position = (1.5, -1.5, 2.5)
        if weapon == 2:
            gun_NoModel_2.position = (2, -1, 2.5)
        if weapon == 3:
            gun_NoModel_3.position = (2, -1, 2.5)
            gun_NoModel_3.rotation =(0, -90, 0)
    # was an early form of weapon swapping
    if key == '1':
        weapon = 1
    if key == '2':
        weapon = 2  
    if key == '3':
        weapon = 3
    if key == 'control' or key == 'left control':
        camera.y = -0.5
    if key == 'control up' or key == 'left control up':
        camera.y = 0
    # if key == 'c':
    #     camera.y = 14
    # if key == 'c up':
    #     camera.y = 0
    if key == 'z' and not menu.enabled:
        dash(15, 1)
    if key == 'v' and not menu.enabled:
        dash(15, 0)
    if key == 'r' and not menu.enabled:
        if weapon == 1:invoke(reload_1, delay=0.45)
        if weapon == 2:invoke(reload_2, delay=0.6)
        if weapon == 3:invoke(reload_3, delay=0.8)
    if key == 'x':
        weapon += 1
    if key == "scroll down":
        weapon += 1
    if key == "scroll up":
        weapon -= 1
    if key == 'f':
        disableWeapon()
    if key == "mouse5":
        admin_menu_toggle = not admin_menu_toggle
        mouse.locked = not admin_menu_toggle
        player.enabled = not admin_menu_toggle
        UI_ADMIN_MENU.enabled = True
    # if the player hits e, then a raycast (bassically, incredibly simplified, it is an invisible line coming from the players camera in this instance, and checks for any collisoins in a distance of 10) is used to find collisions
    # if there is a collision, then check what that collision was. if it is something worth executing other code, it continues the code, and as of right now, if the score is greater than or equal to 30, it enables weapon 3, or checks the score variable, and if the score is greater than 15 it executes the next code section, and gives more ammo
    if key == 'e':
        lootBoxRaycast = raycast(camera.world_position, camera.forward, distance=10, ignore=(player,))
        if lootBoxRaycast.hit:
            if lootBoxRaycast.entity == lootBox:
                if global_score >= 30:
                    lootBox.enabled = False
                    enable_gun_3 = True
        ammoBoxRefillRaycast = raycast(camera.world_position, camera.forward, distance=10, ignore=(player,))
        if ammoBoxRefillRaycast.hit:
            if ammoBoxRefillRaycast.entity == lootBox_2:
                if global_score >= 15:
                    global_score -= 15
                    print("CONNECTED")
                    ammo_amount_1 = 120
                    ammo_amount_2 = 100
                    ammo_amount_3 = 500
                    UI_Bullet_Counter_1.text = f"Ammo: {mag_1}\nReserve: {ammo_amount_1}"
                    UI_Bullet_Counter_2.text = f"Ammo: {mag_2}\nReserve: {ammo_amount_2}"
                    UI_Bullet_Counter_3.text = f"Ammo: {mag_3}\nReserve: {ammo_amount_3}"




print(f"CAMERA INT {camera.y}")
print(f"PLAYER HEIGHT: {player.height}")
print(f"PLAYER XT: {player.x}")

followerSpeed = 3

# the update functin runs 60 times per second. 
def update():
    global mag_3, cooldown_timer, fireRate3, weapon, global_health, followerSpeed, generateNewFollowerToggle, enable_gun_3, globalUIelementsColor
    if held_keys["shift"]:
        player.speed = 20
    else:
        player.speed = 15

    if cooldown_timer > 0:
        cooldown_timer -= time.dt
        
    move_input = Vec3(held_keys['d'] - held_keys['a'], 0, held_keys['w'] - held_keys['s'])
    origin = player.position + Vec3(0, 1, 0)
    if move_input.length() > 0:
        flat_forward = Vec3(camera.forward.x, 0, camera.forward.z)
        if flat_forward.length() == 0:
            flat_forward = Vec3(0, 0, 1)
        flat_forward = flat_forward.normalized()
        flat_right = Vec3(camera.right.x, 0, camera.right.z).normalized()

        desired_dir = (flat_forward * move_input.z + flat_right * move_input.x)
        if desired_dir.length() > 0:
            desired_dir = desired_dir.normalized()
            move_distance = max(0.05, player.speed * time.dt)
            hit = raycast(origin, desired_dir, distance=move_distance + 0.2, ignore=(player,))

            if hit.hit:
                neededclearance = 0.48
                if hasattr(hit, 'distance') and hit.distance < neededclearance:
                    player.position += hit.world_normal * (neededclearance - hit.distance + 0.01)
                slide = desired_dir - hit.world_normal * desired_dir.dot(hit.world_normal)
                if slide.length() > 0.001:
                    player.direction = slide.normalized()
                else:
                    player.direction = Vec3(0, 0, 0)
            else:
                player.direction = desired_dir
    else:
        pass
    flat_forward = Vec3(camera.forward.x, 0, camera.forward.z)
    if flat_forward.length() == 0:
        flat_forward = Vec3(0, 0, 1)
    flat_forward = flat_forward.normalized()
    flat_right = Vec3(camera.right.x, 0, camera.right.z)
    if flat_right.length() == 0:
        flat_right = Vec3(1, 0, 0)
    flat_right = flat_right.normalized()

    clearance = 0.48
    dir_candidates = []
    if 'desired_dir' in locals() and isinstance(desired_dir, Vec3) and desired_dir.length() > 0:
        dir_candidates.append(desired_dir)
    dir_candidates.extend([flat_forward, -flat_forward, flat_right, -flat_right])
    for check_dir in dir_candidates:
        hit2 = raycast(origin, check_dir, distance=clearance, ignore=(player,))
        if hit2.hit and hasattr(hit2, 'distance') and hit2.distance < clearance:
            player.position += hit2.world_normal * (clearance - hit2.distance + 0.01)

    if weapon == 1:
        gun_NoModel.enabled = True
        gun_NoModel_2.enabled = False
        gun_NoModel_3.enabled = False
        UI_Bullet_Counter_3.color = color.white
        UI_Bullet_Counter_2.color = color.white
        UI_Bullet_Counter_1.color = globalUIelementsColor
        UI_Bullet_Counter_1.enabled = True
        UI_Bullet_Counter_2.enabled = False
        UI_Bullet_Counter_3.enabled = False
        UI_weapon_1_2d.enabled = True
        UI_weapon_2_2d.enabled = False
        UI_weapon_3_2d.enabled = False

    elif weapon == 2:
        gun_NoModel.enabled = False
        gun_NoModel_2.enabled = True
        gun_NoModel_3.enabled = False
        UI_Bullet_Counter_2.color = globalUIelementsColor
        UI_Bullet_Counter_1.color = color.white
        UI_Bullet_Counter_3.color = color.white
        UI_Bullet_Counter_1.enabled = False
        UI_Bullet_Counter_2.enabled = True
        UI_Bullet_Counter_3.enabled = False
        UI_weapon_1_2d.enabled = False
        UI_weapon_2_2d.enabled = True
        UI_weapon_3_2d.enabled = False
    elif weapon == 3 and enable_gun_3:
        gun_NoModel.enabled = False
        gun_NoModel_2.enabled = False
        gun_NoModel_3.enabled = True
        UI_Bullet_Counter_3.color = globalUIelementsColor
        UI_Bullet_Counter_2.color = color.white
        UI_Bullet_Counter_1.color = color.white
        UI_Bullet_Counter_1.enabled = False
        UI_Bullet_Counter_2.enabled = False
        UI_Bullet_Counter_3.enabled = True
        UI_weapon_1_2d.enabled = False
        UI_weapon_2_2d.enabled = False
        UI_weapon_3_2d.enabled = True

    if weapon > 3:
        weapon = 1
    if weapon < 1:
        weapon = 3

    if global_health <= 0:
        handleDeath()

    if held_keys["left mouse"] and weapon == 3  and mag_3 > 0 and enable_gun_3:
        if cooldown_timer <=0:
            Bullet(color.red, position=camera.world_position + camera.forward * 2, rotation=camera.world_rotation)
            gun_NoModel_3.blink(color.white)
            mag_3 -= 1
            UI_Bullet_Counter_3.text = f"Ammo: {mag_3}\nReserve: {ammo_amount_3}"
            print(mag_3)
            cooldown_timer = fireRate3
    if not enable_gun_3 and weapon == 3:
        weapon = 2
    for dummy in dummies:
            # targetDummyPos = Vec3(player.x, dummy.y, player.z)
            # dummy.look_at(targetDummyPos)
            # dummy.look_at(player)
            pass
    
    for f in followers:
        playerDirection = player.position - f.position
        if playerDirection.length() > 1.5:
            playerDirection = playerDirection.normalized()

            moveVector = playerDirection

            for otherF in followers:
                if otherF == f:
                    continue
                
                distToSame = distance(f, otherF)
                if distToSame < 1.0:
                    pushBack = f.position - otherF.position
                    if pushBack.length() > 0:
                        moveVector += pushBack.normalized() * 0.8
            moveVector = moveVector.normalized()

            move_x = playerDirection.x * time.dt * followerSpeed
            move_z = playerDirection.z * time.dt * followerSpeed

            wallHitCheck = raycast(
                origin=f.position + Vec3(0, 1, 0),
                direction=Vec3(playerDirection.x, 0, playerDirection.z),
                distance=1.2,
                ignore=(f, player)
            )

            centerRaycastCheck = raycast(f.position + Vec3(0, 1, 0), direction=moveVector, distance=1.5, ignore=(f, player))
            if centerRaycastCheck.hit:
                wallNormal =  centerRaycastCheck.world_normal
                wallNormal.y = 0
                wallNormal = wallNormal.normalized()

                dotProduct = moveVector.x * wallNormal.x + moveVector.z * wallNormal.z
                slideVector = moveVector - (wallNormal * dotProduct)

                if slideVector.length() > 0.1:
                    moveVector = slideVector.normalized()
                else:
                    moveVector = Vec3(-wallNormal.z, 0, wallNormal.x)

                left_direction = Vec3(moveVector.x - moveVector.z, 0, moveVector.z + moveVector.x).normalized()
                right_direction = Vec3(moveVector.x + moveVector.z, 0, moveVector.z - moveVector.x).normalized()

                leftHitCheck = raycast(f.position + Vec3(0, 1, 0), direction=left_direction, distance=1.5, ignore=(f, player))
                rightHitCheck = raycast(f.position + Vec3(0, 1, 0), direction=right_direction, distance=1.5, ignore=(f, player))

                if not leftHitCheck.hit:
                    moveVector = left_direction
                elif not rightHitCheck.hit:
                    moveVector = right_direction
                else:
                    moveVector = Vec3(0, 0, 0)
                
            f.x += moveVector.x * time.dt * followerSpeed
            f.z += moveVector.z * time.dt * followerSpeed

            # if not wallHitCheck.hit:
            #     f.x += move_x
            #     f.z += move_z

            f.look_at(player)
            f.rotation_x = 0
            f.rotation_z = 0
            f.rotation_y += 90
            if distance(f, player) < 1.5:
                global_health -= 10
                print(f"DAMAGED HEALTH: {global_health}")
                UI_Health_Counter.text = f"Health: {global_health}"
                cameraShake(0.05, 0.2)
                knockbackCheck = raycast(player.position + Vec3(0, 1, 0), player.back, distance=3.25, ignore=(player,))
                if knockbackCheck.hit:
                    finalKnockbackDistance = knockbackCheck.distance - 0.5
                else:
                    finalKnockbackDistance = 3
                    knockbackLandPosition = player.position + (player.back * finalKnockbackDistance)
                    player.animate_position(knockbackLandPosition, duration=0.275, curver=curve.linear)
                # player.position += playerDirection * -2
        if f.y <= -25:
            print("FELL OFF")
            f.y = 0
    if player.y <= -25:
        print("TERRAIN TERRAIN")
        handleDeath()

    if len(followers) <= 0 and not generateNewFollowerToggle:
        pass

    if len(dummies) == 0:
        # generate_dummies()
        pass


print(logo)

scene.colliders_visible = True
app.run()

