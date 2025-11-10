import pygame
import sys
import random
import time
import os

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Get the directory of the script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Game states
MENU = 0
OFFICE = 1
CAMERA = 2

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Five Nights at Freddy's - Custom Edition")

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Font
font = pygame.font.SysFont(None, 24)

# Game variables
game_state = MENU
power = 10000
hour = 0
time_left = 60  # 1 hour in seconds
animatronics = []  # List of animatronics
left_door_closed = False
right_door_closed = False
left_light_on = False
right_light_on = False

# Placeholder for animatronics (using rectangles for now)
class Animatronic:
    def __init__(self, name, start_pos, ai_level, direction=1):
        self.name = name
        self.pos = start_pos
        self.ai_level = ai_level
        self.movement_timer = 0
        self.at_door = False
        self.jumpscare_timer = 0
        self.direction = direction  # 1 for right (left anim), -1 for left (right anim)
        self.start_pos = start_pos

    def move(self, left_door_closed, right_door_closed):
        # Simple AI: move towards office based on AI level
        if random.randint(1, 20) <= self.ai_level:
            if not self.at_door:
                self.pos = (self.pos[0] + self.direction * random.randint(1, 2), self.pos[1])
                if self.direction == 1 and self.pos[0] >= 50:  # Left anim reached left door
                    self.at_door = True
                    self.pos = (50, self.pos[1])
                elif self.direction == -1 and self.pos[0] <= 750:  # Right anim reached right door
                    self.at_door = True
                    self.pos = (750, self.pos[1])
            elif self.at_door:
                # If at door and door is closed, go away
                if (self.pos[1] < 350 and left_door_closed) or (self.pos[1] >= 350 and right_door_closed):
                    self.at_door = False
                    self.pos = self.start_pos
                    self.jumpscare_timer = 0

# Create animatronics
animatronics.append(Animatronic("Friend1", (-100, 300), 1, 1))  # Starts from left path, goes to left door
animatronics.append(Animatronic("Friend2", (900, 400), 1, -1))  # Starts from right path, goes to right door

# Load images (with error handling for missing PNGs)
try:
    office_img = pygame.image.load(os.path.join(script_dir, 'assets', 'Office.png'))
    office_img = pygame.transform.scale(office_img, (600, 200))
except:
    office_img = None

try:
    camera_img = pygame.image.load(os.path.join(script_dir, 'assets', 'Camera.png'))
    camera_img = pygame.transform.scale(camera_img, (700, 500))
except:
    camera_img = None

try:
    anim1_img = pygame.image.load(os.path.join(script_dir, 'assets', 'Animatronic1.jpg'))
    anim1_img = pygame.transform.scale(anim1_img, (50, 50))
except:
    anim1_img = None

try:
    anim2_img = pygame.image.load(os.path.join(script_dir, 'assets', 'Animatronic2.jpg'))
    anim2_img = pygame.transform.scale(anim2_img, (50, 50))
except:
    anim2_img = None

try:
    menu_img = pygame.image.load(os.path.join(script_dir, 'assets', 'menu.jpg'))
    menu_img = pygame.transform.scale(menu_img, (800, 600))
except:
    menu_img = None

# Load sounds with error handling
try:
    camera_sound = pygame.mixer.Sound(os.path.join(script_dir, 'sounds', 'camera_sound.mp3'))
except:
    camera_sound = None

try:
    door_sound = pygame.mixer.Sound(os.path.join(script_dir, 'sounds', 'door_sound.mp3'))
except:
    door_sound = None

try:
    light_sound = pygame.mixer.Sound(os.path.join(script_dir, 'sounds', 'light_sound.mp3'))
except:
    light_sound = None

try:
    jumpscare_sound = pygame.mixer.Sound(os.path.join(script_dir, 'sounds', 'Animatronic1_Jumpscare.mp3'))
    print("Jumpscare sound loaded successfully")
except Exception as e:
    try:
        jumpscare_sound = pygame.mixer.Sound(os.path.join(script_dir, 'sounds', 'Animatronic1_Jumpscare.m4a'))
        print("Jumpscare sound loaded successfully (M4A)")
    except Exception as e2:
        jumpscare_sound = None
        print(f"Failed to load jumpscare sound: {e}, {e2}")

# Menu scene
def draw_menu():
    screen.fill(BLACK)
    # Draw menu background
    if menu_img:
        screen.blit(menu_img, (0, 0))
    else:
        pygame.draw.rect(screen, (50, 50, 50), (0, 0, 800, 600))  # Placeholder

    # Draw menu text
    title_text = font.render("Five Nights at Freddy's", True, WHITE)
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 200))

    # Draw clickable buttons
    start_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, 340, 200, 40)
    quit_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, 390, 200, 40)

    pygame.draw.rect(screen, GREEN, start_button_rect)
    pygame.draw.rect(screen, RED, quit_button_rect)

    start_text = font.render("START GAME", True, BLACK)
    quit_text = font.render("QUIT", True, BLACK)

    screen.blit(start_text, (SCREEN_WIDTH // 2 - start_text.get_width() // 2, 350))
    screen.blit(quit_text, (SCREEN_WIDTH // 2 - quit_text.get_width() // 2, 400))

    return start_button_rect, quit_button_rect

# Office scene
def draw_office():
    screen.fill(BLACK)
    # Draw office background
    if office_img:
        screen.blit(office_img, (100, 200))
    else:
        pygame.draw.rect(screen, (50, 50, 50), (100, 200, 600, 200))  # Placeholder

    # Draw doors (left and right) with clickable buttons
    door_color_left = GREEN if left_door_closed else (100, 100, 100)
    door_color_right = GREEN if right_door_closed else (100, 100, 100)
    pygame.draw.rect(screen, door_color_left, (50, 250, 50, 100))  # Left door
    pygame.draw.rect(screen, door_color_right, (700, 250, 50, 100))  # Right door

    # Draw door buttons
    left_door_button = pygame.Rect(25, 220, 40, 30)
    right_door_button = pygame.Rect(735, 220, 40, 30)
    pygame.draw.rect(screen, RED, left_door_button)
    pygame.draw.rect(screen, RED, right_door_button)

    door_btn_text_left = font.render("DOOR", True, WHITE)
    door_btn_text_right = font.render("DOOR", True, WHITE)
    screen.blit(door_btn_text_left, (30, 225))
    screen.blit(door_btn_text_right, (740, 225))

    # Draw lights with clickable buttons
    if left_light_on:
        pygame.draw.circle(screen, WHITE, (75, 275), 20)  # Left light
    if right_light_on:
        pygame.draw.circle(screen, WHITE, (725, 275), 20)  # Right light

    # Draw light buttons
    left_light_button = pygame.Rect(25, 310, 40, 30)
    right_light_button = pygame.Rect(735, 310, 40, 30)
    pygame.draw.rect(screen, YELLOW, left_light_button)
    pygame.draw.rect(screen, YELLOW, right_light_button)

    light_btn_text_left = font.render("LIGHT", True, BLACK)
    light_btn_text_right = font.render("LIGHT", True, BLACK)
    screen.blit(light_btn_text_left, (27, 315))
    screen.blit(light_btn_text_right, (737, 315))

    # Draw camera toggle button
    camera_button = pygame.Rect(350, 10, 100, 30)
    pygame.draw.rect(screen, BLUE, camera_button)
    camera_text = font.render("CAMERA", True, WHITE)
    screen.blit(camera_text, (365, 15))

    # Draw animatronics at doors if they are there
    for i, anim in enumerate(animatronics):
        if anim.at_door:  # At door
            door_x = 50 if anim.direction == 1 else 750  # Left or right door position
            img = anim1_img if i == 0 else anim2_img
            if img:
                screen.blit(img, (door_x, anim.pos[1]))
            else:
                pygame.draw.rect(screen, RED, (door_x, anim.pos[1], 50, 50))  # Placeholder

    # Draw UI
    power_text = font.render(f"Power: {power}%", True, WHITE)
    screen.blit(power_text, (10, 10))

    hour_text = font.render(f"Hour: {hour + 1}", True, WHITE)
    screen.blit(hour_text, (10, 40))

    time_text = font.render(f"Time: {int(time_left // 60)}:{int(time_left % 60):02d}", True, WHITE)
    screen.blit(time_text, (10, 70))

    # Instructions
    instr_text = font.render("Click buttons or use keys: Space/Camera | X/V/Click Doors | Q/E/Click Lights", True, WHITE)
    screen.blit(instr_text, (10, 550))

    return left_door_button, right_door_button, left_light_button, right_light_button, camera_button

# Camera scene
def draw_camera():
    screen.fill(BLACK)
    # Draw camera view
    if camera_img:
        screen.blit(camera_img, (50, 50))
    else:
        pygame.draw.rect(screen, (30, 30, 30), (50, 50, 700, 500))  # Placeholder

    # Draw office toggle button
    office_button = pygame.Rect(350, 10, 100, 30)
    pygame.draw.rect(screen, GREEN, office_button)
    office_text = font.render("OFFICE", True, WHITE)
    screen.blit(office_text, (365, 15))

    # Draw animatronics on camera
    for i, anim in enumerate(animatronics):
        if (anim.direction == 1 and anim.pos[0] < 100) or (anim.direction == -1 and anim.pos[0] > 700):  # Still in hallway
            img = anim1_img if i == 0 else anim2_img
            if img:
                screen.blit(img, (anim.pos[0] + 50, anim.pos[1] + 50))
            else:
                pygame.draw.rect(screen, RED, (anim.pos[0] + 50, anim.pos[1] + 50, 50, 50))  # Placeholder

    # Draw camera UI
    cam_text = font.render("Camera System", True, WHITE)
    screen.blit(cam_text, (350, 40))

    return office_button

# Main game loop
running = True
while running:
    dt = clock.tick(60) / 1000.0  # Delta time in seconds

    # Get button rectangles for mouse clicks
    menu_buttons = None
    office_buttons = None
    camera_buttons = None

    if game_state == MENU:
        menu_buttons = draw_menu()
    elif game_state == OFFICE:
        office_buttons = draw_office()
    elif game_state == CAMERA:
        camera_buttons = draw_camera()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if game_state == MENU and menu_buttons:
                start_button, quit_button = menu_buttons
                if start_button.collidepoint(mouse_pos):  # Start game
                    game_state = OFFICE
                    # Reset game variables
                    power = 10000
                    hour = 0
                    time_left = 60
                    left_door_closed = False
                    right_door_closed = False
                    left_light_on = False
                    right_light_on = False
                    # Reset animatronics
                    animatronics[0].pos = (-100, 300)
                    animatronics[0].at_door = False
                    animatronics[0].jumpscare_timer = 0
                    animatronics[1].pos = (900, 400)
                    animatronics[1].at_door = False
                    animatronics[1].jumpscare_timer = 0
                elif quit_button.collidepoint(mouse_pos):  # Quit game
                    running = False
            elif game_state == OFFICE and office_buttons:
                left_door_btn, right_door_btn, left_light_btn, right_light_btn, camera_btn = office_buttons
                if left_door_btn.collidepoint(mouse_pos):  # Left door
                    if left_door_closed:
                        left_door_closed = False
                    else:
                        left_door_closed = True
                        power -= 5
                    if door_sound:
                        door_sound.play()
                elif right_door_btn.collidepoint(mouse_pos):  # Right door
                    if right_door_closed:
                        right_door_closed = False
                    else:
                        right_door_closed = True
                        power -= 5
                    if door_sound:
                        door_sound.play()
                elif left_light_btn.collidepoint(mouse_pos):  # Left light
                    left_light_on = not left_light_on
                    power -= 1
                    if light_sound:
                        light_sound.play()
                elif right_light_btn.collidepoint(mouse_pos):  # Right light
                    right_light_on = not right_light_on
                    power -= 1
                    if light_sound:
                        light_sound.play()
                elif camera_btn.collidepoint(mouse_pos):  # Camera toggle
                    game_state = CAMERA
                    power -= 1
                    if camera_sound:
                        camera_sound.play()
            elif game_state == CAMERA and camera_buttons:
                office_btn = camera_buttons
                if office_btn.collidepoint(mouse_pos):  # Office toggle
                    game_state = OFFICE
        elif event.type == pygame.KEYDOWN:
            if game_state == MENU:
                if event.key == pygame.K_RETURN:  # Start game
                    game_state = OFFICE
                    # Reset game variables
                    power = 10000
                    hour = 0
                    time_left = 60
                    left_door_closed = False
                    right_door_closed = False
                    left_light_on = False
                    right_light_on = False
                    # Reset animatronics
                    animatronics[0].pos = (-100, 300)
                    animatronics[0].at_door = False
                    animatronics[0].jumpscare_timer = 0
                    animatronics[1].pos = (900, 400)
                    animatronics[1].at_door = False
                    animatronics[1].jumpscare_timer = 0
                elif event.key == pygame.K_ESCAPE:  # Quit game
                    running = False
            elif game_state == OFFICE or game_state == CAMERA:
                if event.key == pygame.K_SPACE:  # Switch between camera and office
                    if game_state == OFFICE:
                        game_state = CAMERA
                        power -= 1  # Using camera drains power
                        if camera_sound:
                            camera_sound.play()
                    else:
                        game_state = OFFICE
                elif event.key == pygame.K_x:  # Left door
                    if left_door_closed:
                        left_door_closed = False
                    else:
                        left_door_closed = True
                        power -= 5  # Closing door drains power
                    if door_sound:
                        door_sound.play()
                elif event.key == pygame.K_v:  # Right door
                    if right_door_closed:
                        right_door_closed = False
                    else:
                        right_door_closed = True
                        power -= 5  # Closing door drains power
                    if door_sound:
                        door_sound.play()
                elif event.key == pygame.K_q:  # Left light
                    left_light_on = not left_light_on
                    power -= 1  # Using light drains power
                    if light_sound:
                        light_sound.play()
                elif event.key == pygame.K_e:  # Right light
                    right_light_on = not right_light_on
                    power -= 1  # Using light drains power
                    if light_sound:
                        light_sound.play()

    # Update game logic only if not in menu
    if game_state != MENU:
        time_left -= dt
        power -= dt * 0.1  # Power drains over time

        if power <= 0:
            # Power out - lose condition
            print("Power out! Game over!")
            game_state = MENU  # Return to menu

        if time_left <= 0:
            hour += 1
            time_left = 60
            if hour >= 6:
                # Win condition
                print("You survived the night!")
                game_state = MENU  # Return to menu

        # Update animatronics
        for anim in animatronics:
            anim.move(left_door_closed, right_door_closed)
            if anim.at_door and game_state == OFFICE:  # At door and player is in office
                if (anim.pos[1] < 350 and not left_door_closed) or (anim.pos[1] >= 350 and not right_door_closed):
                    anim.jumpscare_timer += dt
                    if anim.jumpscare_timer >= 3.0:  # 3 second delay before jumpscare
                        # Jump scare (placeholder)
                        print(f"Jump scare from {anim.name}!")
                        if jumpscare_sound:
                            print("Playing jumpscare sound...")
                            jumpscare_sound.play()
                            pygame.time.wait(2000)  # Wait 2 seconds for sound to play
                            print("Jumpscare sound finished")
                        else:
                            print("Jumpscare sound not loaded!")
                        game_state = MENU  # Return to menu
                else:
                    anim.jumpscare_timer = 0

    # Draw current scene (buttons are drawn in the event loop above)
    if game_state == MENU:
        pass  # Menu already drawn above
    elif game_state == OFFICE:
        pass  # Office already drawn above
    elif game_state == CAMERA:
        pass  # Camera already drawn above

    pygame.display.flip()

pygame.quit()
sys.exit()