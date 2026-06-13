from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import random

app = Ursina()

ground = Entity(
    model='plane',
    texture='white_cube',
    scale=(100, 1, 100),
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
# player = RebuiltFirstPersonController(
#     speed = 25
# )



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



class Wall():
    def __init__(self,Name, model_type, texture_type, scale_def, color_def, texture_scale_def, collider_type, position_all,rotation_def):
        self.entity = Entity(
            model=model_type,
            texture=texture_type,
            scale=scale_def,
            color=color_def,
            texture_scale=texture_scale_def,
            collider=collider_type,
            position=position_all,
            # rotation_x=rotation_def
            rotation=rotation_def
        )

Wall1 = Wall("wall1", 'cube', 'white_cube', (1, 9, 9), color.gray,  (9, 9), 'box', (2.5, 4.5, 5.5), (90, 0, 0))
Wall1 = Wall("wall1", 'cube', 'white_cube', (1, 9, 9), color.gray,  (9, 9), 'box', (7.5, 4.5, 9.5), (0, 90, 0))
Wall1 = Wall("wall1", 'cube', 'white_cube', (1, 9, 9), color.gray,  (9, 9), 'box', (11.5, 4.5, 5.5), (90, 0, 0))


bullets_1 = []
bullets_2 = []
bullets_3 = []

mag_1 = 10
mag_2 = 15
mag_3 = 25

dummies = []

gun_NoModel = Entity(parent=camera, model='cube', color=color.black, origin_y=-0.5, scale= (0.5, 0.5, 2), position= (2, -1, 2.5), collider='box')
gun_NoModel_2 = Entity(parent=camera, model='cube', color=color.green, origin_y=-0.5, scale= (0.5, 0.5, 2), position= (2, -1, 2.5), collider='box')
gun_NoModel_3 = Entity(parent=camera, model='cube', color=color.red, origin_y=-0.5, scale= (0.5, 0.5, 2), position= (2, -1, 2.5), collider='box')
gun_NoModel_2.enabled = False
gun_NoModel_3.enabled = False

player = FirstPersonController(
    speed = 25,
    model='cube',
    y=0
)

player.gun_1 = gun_NoModel
player.gun_2 = gun_NoModel_2
player.gun_3 = gun_NoModel_3

# x, y, z = 5, 5, 6

def generate_dummies():
    for i in range(9):
        x = random.choice([3, 4, 5, 6, 9])
        y = random.choice([3, 4, 5, 6, 9])
        z = random.choice([3, 4, 5, 6, 9])

        dummy = Entity(model='cube', color=color.white,texture='target.png',scale=(1,1,0.1),dx=0.05, position=(x,y,z), collider='box')
        dummies.append(dummy)
generate_dummies()

quit_button.on_click = application.quit
escape_menu_toggle = False
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

def dash(MoveDistance):
    MoveDistance
    dashHitInfo = raycast(player.position + Vec3(0, 1, 0), player.forward, distance=MoveDistance, ignore=(player,))
    if dashHitInfo.hit:
        finalMoveDistance = dashHitInfo.distance - 0.5
    else:
        finalMoveDistance = MoveDistance
        player.y += 3

    targetPosition = player.position + (player.forward * finalMoveDistance)
    player.animate_position(targetPosition, duration=0.1, curve=curve.linear)

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
            destroy(self)
        else:
            self.position += self.forward * distThisFrame

def input(key):
    global escape_menu_toggle, weapon, mag_1, mag_2, mag_3
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
            print(mag_1)
        elif weapon == 2 and mag_2 > 0:
            Bullet(color.green, position=camera.world_position + gun_NoModel_2.forward, rotation=camera.world_rotation)
            gun_NoModel_2.blink(color.white)
            mag_2 -= 1
            print(mag_2)
        elif weapon == 3 and mag_3 > 0:
            Bullet(color.red, position=camera.world_position + gun_NoModel_3.forward, rotation=camera.world_rotation)
            gun_NoModel_3.blink(color.white)
            mag_3 -= 1
            print(mag_3)
    if key == 'right mouse down' and player.gun_3:
        # print("RIGHT BUTTON")
        camera.z = 5
    if key == 'right mouse up' and player.gun_3:
        # print("RIGHT BUTTON")
        camera.z = 0
    if key == '1':
        print("weapon 1 ")
        weapon = 1
        gun_NoModel.enabled = True
        gun_NoModel_2.enabled = False
        gun_NoModel_3.enabled = False
    if key == '2':
        print("weapon 2 ")
        weapon = 2
        gun_NoModel.enabled = False
        gun_NoModel_2.enabled = True
        gun_NoModel_3.enabled = False
    if key == '3':
        print("weapon 3 ")
        weapon = 3
        gun_NoModel.enabled = False
        gun_NoModel_2.enabled = False
        gun_NoModel_3.enabled = True
    # if key == "control":
    #     print("Crouch")
    #     player.camera_pivot.y -= 1
    if key == 'control' or key == 'left control':
        camera.y = -0.5
    if key == 'control up' or key == 'left control up':
        camera.y = 0
    if key == 'z':
        dash(15)
    if key == 'r':
        if weapon == 1:
            mag_1 = 10
        if weapon == 2:
            mag_2 = 15
        if weapon == 3:
            mag_3 = 25
print(f"CAMERA INT {camera.y}")
print(f"PLAYER HEIGHT: {player.height}")
print(f"PLAYER XT: {player.x}")

def update():
    if held_keys["shift"]:
        player.speed = 35
    else:
        player.speed = 25

    if player.y <= -25:
        print("TERRAIN TERRAIN")
        player.y = 5
        player.x = 0
        player.z = 0
    if len(dummies) == 0:
        generate_dummies()

app.run()