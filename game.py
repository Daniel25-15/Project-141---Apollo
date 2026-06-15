from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.shaders import lit_with_shadows_shader
import random, time

app = Ursina()

ground = Entity(
    model='plane',
    texture='white_cube',
    scale=(300, 1, 300),
    color=color.green,
    texture_scale=(100, 100),
    collider='box'
)

# player = FirstPersonController(
#     speed=25,
#     ceiling_raycast=True
# )

class RebuiltFirstPersonController(FirstPersonController):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.gravity = 0 
        self.velocity_y = 0
        self.jump_force = 12
        self.gravity_strength = 35
    def input(self, key):
        if key == "space" and self.grounded:
            self.velocity_y = self.jump_force
            self.grounded = False
            return
        super().input(key)
    def update(self):
        super().update()

        if not self.grounded:
            self.velocity_y -= self.gravity_strength * time.dt
        else:
            self.velocity_y = max(0, self.velocity_y)
        self.y += self.velocity_y * time.dt

        # if hasattr(self, 'jumping') and self.jumping:
        ceiling_hit = boxcast(
            self.world_position + Vec3(0, self.height, 0),
            direction=Vec3(0, 1, 0),
            distance=0.3,
            thickness=(0.8, 0.8),
            ignore=(self,)
        )
        if ceiling_hit.hit and self.velocity_y > 0:
            self.velocity_y = 0
            self.y = ceiling_hit.point.y - self.height


lootBox = Entity(
    model="cube",
    texture="brick",
    scale=1,
    color=color.gold,
    collider="box",
    position=(8, 4.5, 12)
)


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

def buildWalls():
    wall1 = Wall("Wall1", 'cube', 'white_cube', (1, 9, 9), color.gray,  (1, 1), 'box', (5.5, 4.5, 10.5))
    wall2 = Wall("Wall2", 'cube', 'white_cube', (9, 9, 1), color.gray,  (1, 1), 'box', (9.5, 4.5, 14.5))
    wall3 = Wall("Wall3", 'cube', 'white_cube', (1, 9, 9), color.gray,  (1, 1), 'box', (14.5, 4.5, 10.5))
    wall4 = Wall("Wall4", 'cube', 'white_cube', (2, 1, 2), color.gray,  (1, 1), 'box', (13, 0.5, 11))
    wall5 = Wall("Wall5", 'cube', 'white_cube', (2, 1, 2), color.gray,  (1, 1), 'box', (13, 1.5, 13))
    wall6 = Wall("Wall6", 'cube', 'white_cube', (2, 3, 2), color.gray,  (1, 1), 'box', (11, 1.5, 13))
    wall7 = Wall("Wall7", 'cube', 'white_cube', (4, 4, 4), color.gray,  (1, 1), 'box', (8, 2, 12))

buildWalls()

bullets_1 = []
bullets_2 = []
bullets_3 = []

mag_1 = 10
mag_2 = 15
mag_3 = 35

global_score = 0
global_health = 100

fireRate3 = 0.05
cooldown_timer = 0.0

dummies = []
followers = []

gun_NoModel = Entity(parent=camera, model='pistol', color=color.gray, origin_y=-0.5, scale= (0.2, 0.2, 0.2), position= (1.5, -1.5, 2.5), rotation=(0, -90, 0), overlay=True, add_to_scene_entities=False, render_queue=1)
gun_NoModel_2 = Entity(parent=camera, model='cube', color=color.green, origin_y=-0.5, scale= (0.5, 0.5, 2), position= (2, -1, 2.5), overlay=True,)
gun_NoModel_3 = Entity(parent=camera, model='Assault Rifle.glb', color=color.red, origin_y=-0.5, scale= (0.5, 0.5, 2), position= (2, -1, 2.5), rotation=(0, -110, 0), overlay=True,)
gun_NoModel_2.enabled = False
gun_NoModel_3.enabled = False

gun_NoModel.collider = None
gun_NoModel_2.collider = None
gun_NoModel_3.collider = None

gun_NoModel.intersects = False
enable_gun_3 = False

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

player.gun_1 = gun_NoModel
player.gun_2 = gun_NoModel_2
player.gun_3 = gun_NoModel_3

player.ignore_list.append(gun_NoModel)

# x, y, z = 5, 5, 6

UI_Bullet_Counter_1 = Text(
    text=f"Ammo Gun 1: {mag_1}",
    scale=1,
    position=(-0.85, 0.45),
    parent=camera.ui,
    color=color.white
)
UI_Bullet_Counter_2 = Text(
    text=f"Ammo Gun 2: {mag_2}",
    scale=1,
    position=(-0.85, 0.40),
    parent=camera.ui,
    color=color.white
)
UI_Bullet_Counter_3 = Text(
    text=f"Ammo Gun 3: {mag_3}",
    scale=1,
    position=(-0.85, 0.35),
    parent=camera.ui,
    color=color.white
)
UI_Score_Counter = Text(
    text=f"Score: {global_score}",
    scale=1,
    position=(0.0, 0.45),
    parent=camera.ui,
    color=color.white
)

UI_Health_Counter = Text(
    text=f"Health: {global_health}",
    scale=1.5,
    position=(-0.85, -0.4),
    parent=camera.ui,
    color=color.white
)

def handleDeath():
    global global_score, global_health
    global_score = 0
    UI_Score_Counter.text = f"Score: {global_score}"
    player.x = 0
    player.y= 0
    player.z= 0
    global_health = 100
    UI_Health_Counter.text = f"Health: {global_health}"


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
def generateFollower():
    for i in range(random.randint(5, 15)):
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
# quit_button.enabled = escape_menu_toggle

def final_menu():
    global escape_menu_toggle
    escape_menu_toggle = True

    escape_menu_toggle = not escape_menu_toggle
    mouse.locked = not escape_menu_toggle
    player.enabled = not escape_menu_toggle

    if 'win_message' in globals():
        # destroy(win_message)
        pass

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

class Bullet(Entity):
    def __init__(self, color_def, **kwargs):
        super().__init__(
            parent=scene,
            model='cube',
            scale=0.1,
            color=color_def,
            collider='box',
            **kwargs
        )
        self.speed = 400
        self.lifetime = 2.5
    def update(self):
        global global_score
        self.lifetime -= time.dt
        if self.lifetime <= 0:
            destroy(self)
            return
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

def reload_1():
    global mag_1
    mag_1 = 10;UI_Bullet_Counter_1.text = f"Ammo Gun 1: {mag_1}"
def reload_2():
    global mag_2
    mag_2 = 15;UI_Bullet_Counter_2.text = f"Ammo Gun 2: {mag_2}"
def reload_3():
    global mag_3
    mag_3 = 35;UI_Bullet_Counter_3.text = f"Ammo Gun 3: {mag_3}"

weaponToggle = False
def disableWeapon():
    global weaponToggle,weapon 
    print(f"DISABLED WEAPON: {weapon}")
    weaponToggle = not weaponToggle
    if weaponToggle == False:
        if weapon == 1:
            gun_NoModel.enabled = False

def input(key):
    # print(key)
    global escape_menu_toggle, weapon, mag_1, mag_2, mag_3, admin_menu_toggle, enable_gun_3
    if key == 'escape':
        escape_menu_toggle = not escape_menu_toggle
        mouse.locked = not escape_menu_toggle
        player.enabled = not escape_menu_toggle
        # quit_button.enabled = not escape_menu_toggle
        menu.enabled = escape_menu_toggle


#                                                or key == 'left mouse down' and player.gun_2
    if key == 'left mouse down':
        # bullet = Entity(parent=gun_NoModel, model='cube', scale=.1, position=(0, 0.5, 0), speed = 3, color=color.red, collider='box')
        # bullet = Entity(parent=camera, model='cube', scale=.1, position=(0, 0.5, 0), speed = 3, color=color.red, collider='box')
        if weapon == 1 and mag_1 > 0:
            Bullet(color.black, position=camera.world_position + gun_NoModel.forward, rotation=camera.world_rotation)
            # bullet_1.rotation = camera.world_rotation
            # bullets_1.append(bullet_1)
            gun_NoModel.blink(color.white)

            mag_1 -= 1
            UI_Bullet_Counter_1.text = f"Ammo Gun 1: {mag_1}"
            print(mag_1)
        elif weapon == 2 and mag_2 > 0:
            Bullet(color.green, position=camera.world_position + gun_NoModel_2.forward, rotation=camera.world_rotation)
            gun_NoModel_2.blink(color.white)
            mag_2 -= 1
            UI_Bullet_Counter_2.text = f"Ammo Gun 2: {mag_2}"
            print(mag_2)
        elif weapon == 3:
            pass
        
    if key == 'right mouse down' and player.gun_3:
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
    if key == 'z':
        dash(15, 1)
    if key == 'v':
        dash(15, 0)
    if key == 'r':
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
    if key == 'e':
        lootBoxRaycast = raycast(camera.world_position, camera.forward, distance=10, ignore=(player,))
        if lootBoxRaycast.hit:
            if lootBoxRaycast.entity == lootBox:
                lootBox.enabled = False
                enable_gun_3 = True


print(f"CAMERA INT {camera.y}")
print(f"PLAYER HEIGHT: {player.height}")
print(f"PLAYER XT: {player.x}")

followerSpeed = 3

def update():
    global mag_3, cooldown_timer, fireRate3, weapon, global_health, followerSpeed, generateNewFollowerToggle, enable_gun_3
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
        UI_Bullet_Counter_1.color = color.green
    elif weapon == 2:
        gun_NoModel.enabled = False
        gun_NoModel_2.enabled = True
        gun_NoModel_3.enabled = False
        UI_Bullet_Counter_2.color = color.green
        UI_Bullet_Counter_1.color = color.white
        UI_Bullet_Counter_3.color = color.white
    elif weapon == 3 and enable_gun_3:
        gun_NoModel.enabled = False
        gun_NoModel_2.enabled = False
        gun_NoModel_3.enabled = True
        UI_Bullet_Counter_3.color = color.green
        UI_Bullet_Counter_2.color = color.white
        UI_Bullet_Counter_1.color = color.white

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
            UI_Bullet_Counter_3.text = f"Ammo Gun 3: {mag_3}"
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
                if distToSame < 1.2:
                    pushBack = f.position - otherF.position
                    if pushBack.length() > 0:
                        moveVector += pushBack.normalized() * 1.5
            moveVector = moveVector.normalized()

            move_x = playerDirection.x * time.dt * followerSpeed
            move_z = playerDirection.z * time.dt * followerSpeed

            wallHitCheck = raycast(
                origin=f.position + Vec3(0, 1, 0),
                direction=Vec3(playerDirection.x, 0, playerDirection.z),
                distance=1.2,
                ignore=(f, player)
            )
            if not wallHitCheck.hit:
                f.x += move_x
                f.z += move_z

            f.look_at(player)
            f.rotation_x = 0
            f.rotation_z = 0
            f.rotation_y += 90
            if distance(f, player) < 1.5:
                global_health -= 10
                print(f"DAMAGED HEALTH: {global_health}")
                UI_Health_Counter.text = f"Health: {global_health}"
                # player.position += playerDirection * -2
        if f.y <= -25:
            print("FELL OFF")
            f.y = 0
    if player.y <= -25:
        print("TERRAIN TERRAIN")
        handleDeath()

    if len(followers) <= 0 and not generateNewFollowerToggle:
        # print("NEW FOLLOWERS")
        # spawning_wave = True
        # invoke(generateFollower, delay=2.5)
        # generateFollower()
        pass

    if len(dummies) == 0:
        # generate_dummies()
        pass

scene.colliders_visible = True
app.run()

# Glory to God the Father, God the Son, and God the Holy Spirit, the one and only True God, the Holy Trinity, for whom without I can do nothing.
# Romans 11:36