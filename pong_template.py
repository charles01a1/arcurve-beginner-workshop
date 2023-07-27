import pygame
def main():
   pygame.init()
   pygame.display.set_mode((700, 600))
   pygame.display.set_caption('pong game')   
   screen = pygame.display.get_surface() 
   game = Game(screen)
   game.play() 
   pygame.quit() 


class Ball():
    def __init__(self, ball_color, ball_radius, ball_center, ball_velocity, screen):
        self.color = pygame.Color(ball_color)
        self.radius = ball_radius
        self.center = ball_center
        self.velocity = ball_velocity
        self.screen = screen
    
    def move(self,size):
        # Handle the movement of the ball
        pass
            
    def check_left_wall_collision(self):
        return self.center[0] < self.radius

    def check_right_wall_collision(self):
        return self.center[0]+ self.radius > self.screen.get_width()
        

    def draw(self):
        pygame.draw.circle(self.screen, self.color, self.center, self.radius)

    def paddle_collison_update(self, paddle1, paddle2):
        # Handle the paddle ball collision
        pass


class Paddle():
    def __init__(self, paddle_y, paddle_x, paddle_width, paddle_height, screen):
        self.screen = screen
        self.x = paddle_x
        self.y = paddle_y
        self.height = paddle_height
        self.width = paddle_width
        self.color = pygame.Color('white')
        self.rect = pygame.Rect(self.x,self.y,self.width,self.height)
        
    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.rect)

    def move(self, velocity, size):
        top_of_screen = 0
        self.rect.move_ip(velocity)
        if self.rect.bottom >= size[1]:
            self.rect.bottom = self.screen.get_height()
        if self.rect.top <= top_of_screen:
            self.rect.top = top_of_screen

    def check_collision(self, point):
        return self.rect.collidepoint(point)


class Game():
    def __init__(self, screen):
        self.screen = screen
        self.bg_color = pygame.Color('black')
        self.close_clicked = False
        self.continue_game = True
        self.size = self.screen.get_size()

        self.ball_center = [350,250]
        self.ball_velocity = [-1,1]
        self.ball = Ball('white', 6, self.ball_center, self.ball_velocity, self.screen)
        
        self.paddle1_velocity =  [0,0]
        self.paddle1 = Paddle(self.size[1]//2 , 100, 10, 70, self.screen)

        self.paddle2_velocity = [0,0]
        self.paddle2 = Paddle(self.size[1]//2, self.size[0] - 100, 10, 70, self.screen)
        
        self.left_score = 0
        self.right_score = 0
        
    def play(self):
        while not self.close_clicked: 
            self.draw() 
            self.handle_events()
            if self.continue_game:
                self.update()
                self.decide_continue()

    def decide_continue(self):
        if self.left_score == 11 or self.right_score == 11:
            self.continue_game = False
        
    def update_scores(self):
        left_wall_collision = self.ball.check_left_wall_collision()
        right_wall_collsion = self.ball.check_right_wall_collision()
        if left_wall_collision:
            self.right_score += 1
        if right_wall_collsion:
            self.left_score += 1

    def display_scores(self):
        left_score_string =  str(self.left_score)
        right_score_string =  str(self.right_score)
        text_color = pygame.Color('white')        
        text_font = pygame.font.SysFont('', 100)
        left_score_image = text_font.render(left_score_string, True, text_color)
        right_score_image = text_font.render(right_score_string, True, text_color)
        left_score_pos = (0,0)
        right_score_pos = (self.size[0] - 75,0)
        self.screen.blit(left_score_image, left_score_pos)
        self.screen.blit(right_score_image, right_score_pos)

    def handle_events(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT: 
                self.close_clicked = True    
            if event.type == pygame.KEYDOWN:
                self.handle_keydown(event)
            if event.type == pygame.KEYUP:
                self.handle_keyup(event)
    
    def handle_keyup(self, event):
        if event.key == pygame.K_q or event.key == pygame.K_a:  
            self.paddle1_velocity = [0,0]
        if event.key == pygame.K_p or event.key == pygame.K_l: 
            self.paddle2_velocity = [0,0]
                   
    def handle_keydown(self, event):
        if event.key == pygame.K_q:  
           self.paddle1_velocity =  [0,-1]
        if event.key == pygame.K_a:  
            self.paddle1_velocity =  [0,1]
        if event.key == pygame.K_p:  
            self.paddle2_velocity = [0,-1]
        if event.key == pygame.K_l:  
            self.paddle2_velocity = [0,1]
            
    def draw(self):      
        self.screen.fill(self.bg_color)
        self.paddle1.draw()
        self.paddle2.draw()
        self.ball.draw()
        self.display_scores()
        pygame.display.update()

    def update(self):
        self.ball.move(self.size)
        self.paddle1.move(self.paddle1_velocity, self.size)
        self.paddle2.move(self.paddle2_velocity, self.size)
        self.ball.paddle_collison_update(self.paddle1, self.paddle2)
        self.update_scores()

main()
