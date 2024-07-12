import datetime
import os
import random
import pygame

# Initialize the Pygame library
pygame.init()

# Set the game icon
icon_image = pygame.image.load("game_files/DinoWallpaper.png")
pygame.display.set_icon(icon_image)

# Load images for the running, jumping, and ducking animations
RUNNING = [
    pygame.image.load(os.path.join("game_files/Dino", "DinoRun1.png")),
    pygame.image.load(os.path.join("game_files/Dino", "DinoRun2.png")),
]
JUMPING = pygame.image.load(os.path.join("game_files/Dino", "DinoJump.png"))
DUCKING = [
    pygame.image.load(os.path.join("game_files/Dino", "DinoDuck1.png")),
    pygame.image.load(os.path.join("game_files/Dino", "DinoDuck2.png")),
]

# Load images for obstacles and background elements
SMALL_CACTUS = [
    pygame.image.load(os.path.join("game_files/Cactus", "SmallCactus1.png")),
    pygame.image.load(os.path.join("game_files/Cactus", "SmallCactus2.png")),
    pygame.image.load(os.path.join("game_files/Cactus", "SmallCactus3.png")),
]
LARGE_CACTUS = [
    pygame.image.load(os.path.join("game_files/Cactus", "LargeCactus1.png")),
    pygame.image.load(os.path.join("game_files/Cactus", "LargeCactus2.png")),
    pygame.image.load(os.path.join("game_files/Cactus", "LargeCactus3.png")),
]
BIRD = [
    pygame.image.load(os.path.join("game_files/Bird", "Bird1.png")),
    pygame.image.load(os.path.join("game_files/Bird", "Bird2.png")),
]
CLOUD = pygame.image.load(os.path.join("game_files/Other", "Cloud.png"))
BACKGROUND = pygame.image.load(os.path.join("game_files/Other", "Track.png"))
FONT_COLOR = (0, 0, 0)  # Default font color

# Global Constants
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("T-Rex Game")  # Set the game window title


class Dinosaur:
    X_POSITION = 80
    Y_POSITION = 310
    Y_POSITION_DUCK = 340
    JUMP_VELOCITY = 8.5

    def __init__(self):
        """Initialize the Dinosaur object."""
        self.ducking_images = DUCKING
        self.running_images = RUNNING
        self.jumping_image = JUMPING
        self.is_ducking = False
        self.is_running = True
        self.is_jumping = False
        self.step_index = 0
        self.jump_velocity = self.JUMP_VELOCITY
        self.image = self.running_images[0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POSITION
        self.dino_rect.y = self.Y_POSITION

    def update(self, user_input):
        """Update the dinosaur's state based on user input."""
        if self.is_ducking:
            self.duck()
        if self.is_running:
            self.run()
        if self.is_jumping:
            self.jump()

        if self.step_index >= 10:
            self.step_index = 0

        if (user_input[pygame.K_UP] or user_input[pygame.K_SPACE]) and not self.is_jumping:
            self.is_ducking = False
            self.is_running = False
            self.is_jumping = True
        elif user_input[pygame.K_DOWN] and not self.is_jumping:
            self.is_ducking = True
            self.is_running = False
            self.is_jumping = False
        elif not (self.is_jumping or user_input[pygame.K_DOWN]):
            self.is_ducking = False
            self.is_running = True
            self.is_jumping = False

    def duck(self):
        """Animate the dinosaur ducking."""
        self.image = self.ducking_images[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POSITION
        self.dino_rect.y = self.Y_POSITION_DUCK
        self.step_index += 1

    def run(self):
        """Animate the dinosaur running."""
        self.image = self.running_images[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POSITION
        self.dino_rect.y = self.Y_POSITION
        self.step_index += 1

    def jump(self):
        """Animate the dinosaur jumping."""
        self.image = self.jumping_image
        if self.is_jumping:
            self.dino_rect.y -= self.jump_velocity * 4
            self.jump_velocity -= 0.8
        if self.jump_velocity < -self.JUMP_VELOCITY:
            self.is_jumping = False
            self.jump_velocity = self.JUMP_VELOCITY

    def draw(self, screen):
        """Draw the dinosaur on the screen."""
        screen.blit(self.image, (self.dino_rect.x, self.dino_rect.y))


class Cloud:
    def __init__(self):
        """Initialize the Cloud object."""
        self.x = SCREEN_WIDTH + random.randint(800, 1000)
        self.y = random.randint(50, 100)
        self.image = CLOUD
        self.width = self.image.get_width()

    def update(self):
        """Update the cloud's position."""
        self.x -= game_speed
        if self.x < -self.width:
            self.x = SCREEN_WIDTH + random.randint(2500, 3000)
            self.y = random.randint(50, 100)

    def draw(self, screen):
        """Draw the cloud on the screen."""
        screen.blit(self.image, (self.x, self.y))


class Obstacle:
    def __init__(self, image, obstacle_type):
        """Initialize an obstacle object."""
        self.image = image
        self.type = obstacle_type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH

    def update(self):
        """Update the obstacle's position."""
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop()

    def draw(self, screen):
        """Draw the obstacle on the screen."""
        screen.blit(self.image[self.type], self.rect)


class SmallCactus(Obstacle):
    def __init__(self, image):
        """Initialize a small cactus obstacle."""
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 325


class LargeCactus(Obstacle):
    def __init__(self, image):
        """Initialize a large cactus obstacle."""
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 300


class Bird(Obstacle):
    BIRD_HEIGHTS = [250, 290, 320]

    def __init__(self, image):
        """Initialize a bird obstacle."""
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = random.choice(self.BIRD_HEIGHTS)
        self.index = 0

    def draw(self, screen):
        """Draw the bird obstacle on the screen."""
        if self.index >= 9:
            self.index = 0
        screen.blit(self.image[self.index // 5], self.rect)
        self.index += 1


def main():
    """Main function to run the T-Rex game."""
    global game_speed, x_position_bg, y_position_bg, points, obstacles
    run = True
    clock = pygame.time.Clock()
    player = Dinosaur()
    cloud = Cloud()
    game_speed = 20
    x_position_bg = 0
    y_position_bg = 380
    points = 0
    font = pygame.font.Font("freesansbold.ttf", 20)
    obstacles = []
    death_count = 0
    pause = False

    def score():
        """Display and update the score."""
        global points, game_speed
        points += 1
        if points % 100 == 0:
            game_speed += 1
        current_time = datetime.datetime.now().hour

        try:
            with open("score.txt", "r") as f:
                score_ints = [int(x) for x in f.read().split()]
                highscore = max(score_ints)
        except FileNotFoundError:
            highscore = 0

        if points > highscore:
            highscore = points

        text = font.render("High Score: " + str(highscore) + "  Points: " + str(points), True, FONT_COLOR)
        text_rect = text.get_rect()
        text_rect.center = (900, 40)
        SCREEN.blit(text, text_rect)

    def menu(death_count):
        """Display the menu and handle game restart."""
        global points
        global FONT_COLOR
        run = True
        while run:
            current_time = datetime.datetime.now().hour
            if 7 < current_time < 19:
                FONT_COLOR = (0, 0, 0)
                SCREEN.fill((255, 255, 255))
            else:
                FONT_COLOR = (255, 255, 255)
                SCREEN.fill((128, 128, 128))
            font = pygame.font.Font("freesansbold.ttf", 30)

            if death_count == 0:
                text = font.render("Press any Key to Start", True, FONT_COLOR)
            elif death_count > 0:
                text = font.render("Press any Key to Restart", True, FONT_COLOR)
                score = font.render("Your Score: " + str(points), True, FONT_COLOR)
                score_rect = score.get_rect()
                score_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
                SCREEN.blit(score, score_rect)

                with open("score.txt", "a") as f:
                    f.write(str(points) + "\n")

            text_rect = text.get_rect()
            text_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            SCREEN.blit(text, text_rect)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    main()

    def background():
        """Scroll the background."""
        global x_position_bg, y_position_bg
        image_width = BACKGROUND.get_width()
        SCREEN.blit(BACKGROUND, (x_position_bg, y_position_bg))
        SCREEN.blit(BACKGROUND, (image_width + x_position_bg, y_position_bg))
        if x_position_bg <= -image_width:
            SCREEN.blit(BACKGROUND, (image_width + x_position_bg, y_position_bg))
            x_position_bg = 0
        x_position_bg -= game_speed

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        current_time = datetime.datetime.now().hour
        if 7 < current_time < 19:
            FONT_COLOR = (0, 0, 0)
            SCREEN.fill((255, 255, 255))
        else:
            FONT_COLOR = (255, 255, 255)
            SCREEN.fill((128, 128, 128))

        user_input = pygame.key.get_pressed()

        player.update(user_input)

        if not pause:
            background()

            cloud.update()
            cloud.draw(SCREEN)

            player.draw(SCREEN)

            if len(obstacles) == 0:
                if random.randint(0, 2) == 0:
                    obstacles.append(SmallCactus(SMALL_CACTUS))
                elif random.randint(0, 2) == 1:
                    obstacles.append(LargeCactus(LARGE_CACTUS))
                elif random.randint(0, 2) == 2:
                    obstacles.append(Bird(BIRD))

            for obstacle in obstacles:
                obstacle.draw(SCREEN)
                obstacle.update()
                if player.dino_rect.colliderect(obstacle.rect):
                    pygame.time.delay(2000)
                    death_count += 1
                    menu(death_count)

            score()

        pygame.display.update()
        clock.tick(30)


# Run the game
if __name__ == "__main__":
    main()
