import pygame

class InputManager:
    def __init__(self):
        self.quit_requested    = False
        self.move_x            = 0
        self.rotate_cw         = False
        self.rotate_ccw        = False
        self.fast_drop         = False
        self.hold              = False
        self.pause_requested   = False
        self.restart_requested = False
        self.confirm           = False
        self.backspace         = False
        self.text_input        = ''

    def poll_events(self) -> None:
        self.move_x            = 0
        self.rotate_cw         = False
        self.rotate_ccw        = False
        self.hold              = False
        self.pause_requested   = False
        self.restart_requested = False
        self.confirm           = False
        self.backspace         = False
        self.text_input        = ''

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit_requested = True

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.quit_requested = True
                elif event.key == pygame.K_LEFT:
                    self.move_x = -1
                elif event.key == pygame.K_RIGHT:
                    self.move_x = 1
                elif event.key == pygame.K_UP:
                    self.rotate_cw = True
                elif event.key == pygame.K_z:
                    self.rotate_ccw = True
                elif event.key == pygame.K_SPACE:
                    self.hard_drop = True
                elif event.key in (pygame.K_c, pygame.K_LSHIFT, pygame.K_RSHIFT):
                    self.hold = True
                elif event.key == pygame.K_p:
                    self.pause_requested = True
                elif event.key == pygame.K_RETURN:
                    self.confirm = True
                    self.restart_requested = True
                elif event.key == pygame.K_BACKSPACE:
                    self.backspace = True
                elif event.unicode and event.unicode.isprintable():
                    self.text_input = event.unicode

        keys = pygame.key.get_pressed()
        self.fast_drop = keys[pygame.K_DOWN]
