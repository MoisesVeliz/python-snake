import arcade, settings, random


class SuperSnake(arcade.Window):
    
    def __init__(self, width, height, title):
        
        super().__init__(width, height, title)
        super().set_update_rate(1 / settings.FPS)
        arcade.set_background_color(arcade.color.BLUE_GREEN)
        # 
        self.screen_width = width
        self.screen_height = height
        
        self.screen_padding = None
        
        self.punto_init_x = None
        self.punto_init_y = None

        self.punto_final_x = None
        self.punto_final_y = None
        
        self.cell_width  = None
        self.cell_height = None
        
        self.offset = None
        
        self.x_list = None
        self.y_list = None
        
        self.grid = None
        
        self.grid_shape_list = None
        
        self.start_point_x = None
        self.start_point_y = None
        
        self.grid_col = None
        self.grid_row = None
        
        self.snake_head_coord = None
        
        self.direction = None
        
        self.snake_segment_list = None
        
        self.snake_speed = 7
        
        self.snake_cicle = 5
        
        self.apple_coord = []
        
        self.score = None
        
        self.collision_with_apple = None
        
        self.grid_center_x =None
        self.grid_center_y = None
        self.grid_width = None
        self.grid_height = None

            
    def setup(self):
        self.screen_padding = settings.WINDOWS_PADDING
        
        self.punto_init_x = 0 + self.screen_padding
        self.punto_init_y = 0 + self.screen_padding

        self.punto_final_x = self.screen_width - self.screen_padding
        self.punto_final_y = self.screen_height - self.screen_padding
        
        self.cell_width  = (self.punto_final_x // settings.CELL_SIZE) // settings.COL
        self.cell_height = (self.punto_final_y // settings.CELL_SIZE) // settings.ROW

        self.grid_width = (self.cell_width * settings.COL - (settings.COL))
        self.grid_height = (self.cell_height * settings.ROW - settings.ROW)
        
        self.grid_center_x = self.width // 2
        self.grid_center_y = self.height // 2
        
        self.offset = [
            self.cell_width // 2,
            self.cell_height // 2
        ]
        
        self.grid = []
        
        self.grid_shape_list =  arcade.ShapeElementList()
        self.point_shape_list =  arcade.ShapeElementList()
        
        self.start_point_x = self.screen_padding
        self.start_point_y = self.screen_padding
        
        self.grid_col = settings.COL
        self.grid_row = settings.ROW
        
        self.snake_head_coord = [1, 1]
        
        self.direction = arcade.key.UP
        
        self.counter_limit  = 0
        self.snake_shape_list = arcade.ShapeElementList()
        
        self.snake_segment_list = [[250, 250], [250, 250]]
        
        self.apple_shape = arcade.Shape()
        
        self.score = 0
        
        self.collision_with_apple = False
        
        self.create_grid()
        self.create_apple()
        
    def on_draw(self):
        
        self.clear()
        
        self.grid_shape_list.draw()
        self.snake_shape_list.draw()
        self.apple_shape.draw()
        self.score_draw()
        self.walls_draw()
    
    def on_key_press(self, symbol: int, modifiers: int):
        
        if symbol == arcade.key.UP:
            self.direction = arcade.key.UP
        elif symbol == arcade.key.RIGHT:
            self.direction = arcade.key.RIGHT
        elif symbol == arcade.key.DOWN:
            self.direction = arcade.key.DOWN
        elif symbol == arcade.key.LEFT:
            self.direction = arcade.key.LEFT
    
    def update(self, delta_time: float):
        if self.snake_check_collision(): 
            self.collision_with_apple = True
            self.create_apple() 
            self.score += 1
        self.snake_move()
        self.snake_draw()  
                
    def create_grid(self):
        for x in range(self.punto_init_x, self.punto_final_x, self.cell_width):
            list = []
            for y in range(self.punto_init_y, self.punto_final_y, self.cell_height):
                list.append([x + self.offset[0], y + self.offset[1]])
                # self.grid_shape_list.append(
                #     arcade.create_rectangle_outline(x + self.offset[0], y + self.offset[1], self.cell_width, self.cell_height, arcade.color.AERO_BLUE)
                # )
            self.grid.append(list)
        
    def spawn_snake(self):
        return
        self.snake_segment_list = [[5,5], [5,6]]
     
    def snake_move(self):
        self.counter_limit += 1
        if self.counter_limit < self.snake_speed:
            return
        
        self.counter_limit = 0
        
        
        if self.direction == arcade.key.UP:
            self.snake_head_coord[1] += 1
        elif self.direction == arcade.key.RIGHT:
            self.snake_head_coord[0] += 1
        elif self.direction == arcade.key.DOWN:
            self.snake_head_coord[1] -= 1
        elif self.direction == arcade.key.LEFT:
            self.snake_head_coord[0] -= 1
        
        p = self.grid[self.snake_head_coord[0]][self.snake_head_coord[1]]

        self.snake_segment_list.insert(0, p)

        if self.collision_with_apple == False:
            self.snake_segment_list.pop()
        else:
            self.collision_with_apple = False  
        
    def snake_draw(self):
        self.snake_shape_list = arcade.ShapeElementList()
        
        for t in self.snake_segment_list:
            self.snake_shape_list.append(
                arcade.create_rectangle(
                    t[0],
                    t[1],
                    self.cell_width,
                    self.cell_height,
                    arcade.color.YELLOW
                    )
            )
            
    def create_apple(self):    
        print(len(self.grid))
        primer_nivel = self.grid[random.randint(0, settings.COL - 3)]
        segundo_nivel = primer_nivel[random.randint(0, settings.ROW - 3)]
        self.apple_coord = [segundo_nivel[0], segundo_nivel[1]]
        self.apple_shape = arcade.create_rectangle(
            segundo_nivel[0],
            segundo_nivel[1],
            self.cell_width,
            self.cell_height,
            arcade.color.RED
        )
        
    def snake_check_collision(self):
        snake_head_coord = []
        if len(self.snake_segment_list):
            snake_head_coord = self.snake_segment_list[0]
        if snake_head_coord== self.apple_coord:
            return True
        return False
        
    def score_draw(self):
       arcade.draw_text(f"Score: {self.score}", 0, self.height - 15, arcade.color.BLACK, 15) 
        
    def walls_draw(self):
        arcade.create_rectangle_outline(self.grid_center_x, self.grid_center_y, self.grid_width, self.grid_height, arcade.color.BLACK, 5).draw()
        
        
class Snake(arcade.Shape):
    
    def __init__(self):
        pass
    
    def move():
        pass
    
class Apple(arcade.Shape):
    
    def __init__(self):
        pass
    
    def respawn(self):
        pass

class Wall(arcade.Shape):
    def __init__(self):
        pass
    
class Score():
    
    def __init__(delf):
        pass      
    
def main():
    
    game = SuperSnake(
        settings.WINDOWS_WIDTH,
        settings.WINDOWS_HEIGHT,
        settings.WINDOWS_TITLE
    )
    game.setup()
    
    arcade.run()
    
if __name__ == "__main__":
    main()
    
    
# StartGame()
#  SpawnSnake()
#   snakeLen()
#  SpawnApple()
#  RespawnApplet()
#  
#  
# 
# 
# 
# 