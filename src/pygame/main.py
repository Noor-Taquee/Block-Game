import pygame
import sys
# from logic import Body, state  <-- You'll import your stuff here

# 1. Setup
pygame.init()

WIDTH, HEIGHT = 800, 600
BgColor = (20, 20, 30)  # Dark space blue background
screen = pygame.display.set_mode((WIDTH, HEIGHT))

FPS = 60
clock = pygame.time.Clock()

pos = 0

# 2. Main Loop
while True:
  # Handle closing the window
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
      sys.exit()

  # 3. Logic (Update your physics here)
  # for body in state.bodies:
  #   body.update_position()

  # MARK: Rendering
  screen.fill(BgColor)

  # Draw a test planet (Surface, Color, Center, Radius)
  if pos < WIDTH:
    pos += 1
  else:
    pos = 0

  pygame.draw.circle(screen, (255, 200, 0), (pos, 400), 15)
  # pygame.draw.rect(screen, (20,20,20), rect=)

  pygame.display.flip()
  clock.tick(FPS)
