import arcade, settings, random

class InstructionView(arcade.View):
    
    def on_show_view(self):
        """ This is run once when we switch to this view """
        arcade.set_background_color(arcade.csscolor.DARK_SLATE_BLUE)

        # Reset the viewport, necessary if we have a scrolling game and we need
        # to reset the viewport back to the start so we can see what we draw.
        arcade.set_viewport(0, self.window.width, 0, self.window.height)
    def on_draw(self):
        """ Draw this view """
        self.clear()
        arcade.draw_text("Super Snake", self.window.width / 2, self.window.height / 2,
                         arcade.color.WHITE, font_size=30, anchor_x="center")
        arcade.draw_text("Precione ENTER para continuar", self.window.width / 2, self.window.height / 2-75,
                         arcade.color.WHITE, font_size=20, anchor_x="center")
        
    def on_key_press(self, symbol: int, modifiers: int):
        """ If the user presses the mouse button, start the game. """
        
        if symbol == arcade.key.ENTER:
            game_view = GameView()
            game_view.setup()
            self.window.show_view(game_view)
   
class GameOver(arcade.View):
    def on_show_view(self):
        """ This is run once when we switch to this view """
        arcade.set_background_color(arcade.csscolor.DARK_SLATE_BLUE)

        # Reset the viewport, necessary if we have a scrolling game and we need
        # to reset the viewport back to the start so we can see what we draw.
        arcade.set_viewport(0, self.window.width, 0, self.window.height)
    def on_draw(self):
        """ Draw this view """
        self.clear()
        arcade.draw_text("Game Over", self.window.width / 2, self.window.height / 2,
                         arcade.color.WHITE, font_size=50, anchor_x="center")
        arcade.draw_text("ESCAPE ir al inicio", self.window.width / 2, self.window.height / 2-75,
                         arcade.color.WHITE, font_size=20, anchor_x="center")
        
        arcade.draw_text("ENTER para reintentar", self.window.width / 2, self.window.height / 2-75 -75,
                         arcade.color.WHITE, font_size=20, anchor_x="center")
        
    def on_key_press(self, symbol: int, modifiers: int):
        """ If the user presses the mouse button, start the game. """
        
        if symbol == arcade.key.ENTER:
            game_view = GameView()
            game_view.setup()
            self.window.show_view(game_view)
        elif symbol == arcade.key.ESCAPE:
            menu_view = InstructionView()
            self.window.show_view(menu_view)
class GameView(arcade.View):
    
    def __init__(self):
        
        super().__init__()
        # super().set_update_rate(1 / settings.FPS)
        arcade.set_background_color(arcade.color.BLUE_GREEN)
        # 
        self.screen_width = settings.WINDOWS_WIDTH
        self.screen_height = settings.WINDOWS_HEIGHT
        
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
        
        self.snake_speed = 5
        
        self.snake_cicle = 5
        
        self.apple_coord = []
        
        self.score = None
        
        self.collision_with_apple = None
        
        self.grid_center_x =None
        self.grid_center_y = None
        self.grid_width = None
        self.grid_height = None
        
        self.play = None

            
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
        
        self.grid_center_x = self.screen_width // 2
        self.grid_center_y = self.screen_height // 2
        
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
        self.snake_shape_border_list = arcade.ShapeElementList()
        
        self.snake_segment_list = []
        
        self.apple_shape = arcade.Shape()
        
        self.score = 0
        
        self.collision_with_apple = False
        self.play = True
        
        self.create_grid()
        self.create_apple()
        self.spawn_snake()
        
    def on_draw(self):
        
        self.clear()
        
        self.grid_shape_list.draw()
        self.snake_shape_list.draw()
        self.snake_shape_border_list.draw()
        self.apple_shape.draw()
        self.score_draw()
        self.walls_draw()
        
        if self.play == False:
            arcade.draw_text('Pausa', self.window.width / 2, self.window.height / 2, arcade.color.WHITE, 40, anchor_x="center")
            arcade.draw_text('ESCAPE para salir', self.window.width / 2, self.window.height / 2 -75, arcade.color.WHITE, 20, anchor_x="center")

    
    def on_key_press(self, symbol: int, modifiers: int):
        
        if symbol == arcade.key.UP and self.direction != arcade.key.DOWN:
            self.direction = arcade.key.UP
        elif symbol == arcade.key.RIGHT and self.direction != arcade.key.LEFT:
            self.direction = arcade.key.RIGHT
        elif symbol == arcade.key.DOWN and self.direction != arcade.key.UP:
            self.direction = arcade.key.DOWN
        elif symbol == arcade.key.LEFT and self.direction != arcade.key.RIGHT:
            self.direction = arcade.key.LEFT
        if symbol == arcade.key.SPACE:
            if self.play:
                self.play = False
            else:
                self.play = True
        if self.play == False and symbol == arcade.key.ESCAPE:
            menu_view = InstructionView()
            self.window.show_view(menu_view)
    
    def update(self, delta_time: float):
        if self.play == False:
            return
        if self.snake_check_collision_with_apple(): 
            self.collision_with_apple = True
            self.create_apple() 
            self.score += 1
        if self.snake_ckeck_collision_with_body():
            game_over_view = GameOver()
            self.window.show_view(game_over_view)
            return
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
        directions = [
            arcade.key.UP,
            arcade.key.RIGHT,
            arcade.key.DOWN,
            arcade.key.LEFT
            ]
        self.snake_segment_list.clear()
        coord_x = random.randint(5, settings.COL - 5)
        coord_y = random.randint(5, settings.ROW - 5)
        
        
        self.direction = random.choice(directions)
        self.snake_head_coord = [coord_x, coord_y]
        
        for i in range(1, 4):
            primer_nivel = self.grid[coord_x]
            segundo_nivel = primer_nivel[coord_y]
            self.snake_segment_list.append( [segundo_nivel[0], segundo_nivel[1]])
            if self.direction == arcade.key.UP:
                coord_y = coord_y - i
            elif self.direction == arcade.key.RIGHT:
                coord_x = coord_x - i
            elif self.direction == arcade.key.DOWN:
                coord_y = coord_y + i
            elif self.direction == arcade.key.LEFT:
                coord_x = coord_x + i
        # print(self.snake_segment_list)
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
            
        if (self.snake_head_coord[0] >  len(self.grid) - 1 or self.snake_head_coord[0] < 0) or (self.snake_head_coord[1] >  len(self.grid[0]) - 1 or self.snake_head_coord[1] < 0):
            self.spawn_snake()
            self.score = 0
            return
        
        p = self.grid[self.snake_head_coord[0]][self.snake_head_coord[1]]

        self.snake_segment_list.insert(0, p)

        if self.collision_with_apple == False:
            self.snake_segment_list.pop()
        else:
            self.collision_with_apple = False  
        
    def snake_draw(self):
        self.snake_shape_list = arcade.ShapeElementList()
        self.snake_shape_border_list = arcade.ShapeElementList()
        
        for t in self.snake_segment_list:
            self.snake_shape_list.append(
                arcade.create_rectangle(
                    t[0],
                    t[1],
                    self.cell_width,
                    self.cell_height,
                    arcade.color.YELLOW,
                    )
            )
            self.snake_shape_border_list.append(
                arcade.create_rectangle_outline(
                    t[0],
                    t[1],
                    self.cell_width,
                    self.cell_height,
                    arcade.color.BLACK,
                    )
            )
            
    def create_apple(self):    
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
        
    def snake_check_collision_with_apple(self):
        snake_head_coord = []
        if len(self.snake_segment_list):
            snake_head_coord = self.snake_segment_list[0]
        if snake_head_coord== self.apple_coord:
            return True
        return False
        
    def score_draw(self):
       arcade.draw_text(f"Score: {self.score}", 0, self.screen_height - 20, arcade.color.BLACK, 15) 
        
    def walls_draw(self):
        arcade.create_rectangle_outline(self.grid_center_x, self.grid_center_y, self.grid_width +5, self.grid_height +5, arcade.color.BLACK, 5).draw()
            
    def snake_ckeck_collision_with_body(self):
        head = self.snake_head_coord
        
        for idx in range(len(self.snake_segment_list)):
            if self.grid[head[0]][head[1]] == self.snake_segment_list[idx] and idx > 0:
                self.spawn_snake()
                self.score = 0
                return
            
def main():
    
    window = arcade.Window(
        settings.WINDOWS_WIDTH,
        settings.WINDOWS_HEIGHT,
        settings.WINDOWS_TITLE
    )
    start_view = InstructionView()
    window.show_view(start_view)
    # start_view.setup()
    
    arcade.run()
    
if __name__ == "__main__":
    main()