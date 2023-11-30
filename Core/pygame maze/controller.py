from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
import visualiser
import generator
import solver
import time
import wfcgenerator

class MazeScreen(Screen):
    def __init__(self, maze, **kwargs):
        super(MazeScreen, self).__init__(**kwargs)
        self.maze = maze
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(Label(text='Maze Visualization'))
        # layout.add_widget(visualiser.get_canvas())  # Assuming get_canvas() returns the Kivy canvas
        back_button = Button(text='Back to Main Menu', on_press=self.go_to_main_menu)
        layout.add_widget(back_button)
        self.add_widget(layout)

    def go_to_main_menu(self, instance):
        self.manager.current = 'main_menu'

class MainMenu(Screen):
    def __init__(self, settings, **kwargs):
        super(MainMenu, self).__init__(**kwargs)
        self.settings = settings
        layout = BoxLayout(orientation='vertical')
        self.start_button = Button(text=self.get_start_button_text(), on_press=self.start_pressed)
        settings_button = Button(text='Settings', on_press=self.go_to_settings)
        layout.add_widget(Label(text='Maze App'))
        layout.add_widget(self.start_button)
        layout.add_widget(settings_button)
        self.add_widget(layout)

    def get_start_button_text(self):
        if self.settings_are_configured():
            return 'Start'
        else:
            return 'Start with Default Settings'

    def settings_are_configured(self):
        return all(value != '' for value in self.settings.values())

    def start_pressed(self, instance):
        if self.settings_are_configured():
            x_cells = int(self.settings['x_cells'])
            y_cells = int(self.settings['y_cells'])

            match self.settings['generator_method']:
                case "df":
                    maze = generator.newMaze(x_cells, y_cells)
                case "wfc":
                    maze = wfcgenerator.newMaze(x_cells, y_cells)

            win_width = int(self.settings['window_size_x'])
            win_height = int(self.settings['window_size_y'])

            visual = visualiser.MazeVisualiser(win_width, win_height, x_cells, y_cells)
            solve = solver.MazeSolver(visual, maze, x_cells, y_cells)
            
            visual.drawMaze(maze)

            # Switch to the MazeScreen for visualization
            maze_screen = MazeScreen(maze, name='maze_screen')
            self.manager.add_widget(maze_screen)
            self.manager.current = 'maze_screen'

            visual.visMaze()


        
            if self.settings['solve']:
                method = self.settings['method']
                match method:
                    case "bfs":
                        solutionspeed = float(self.settings['solutionspeed'])
                        solve.solveMazebfs(solutionspeed)
                    case "lefthand":
                        solve.solveMazelefthand()
                    case "amogus":
                        solve.solveFindAmogus()


            # Add any additional logic you need after starting the maze
            #has while true so run last to keep still image of finished maze without crashing
            time.sleep(0.5)
            visual.threadStop()


    def go_to_settings(self, instance):
        self.manager.transition.direction = "left"
        self.manager.current = 'settings'

class Settings(Screen):
    def __init__(self, main_menu, **kwargs):
        super(Settings, self).__init__(**kwargs)
        self.main_menu = main_menu
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(Label(text='Settings'))
        
        # Window Size X
        layout.add_widget(Label(text='Window Width'))
        self.window_size_input_x = TextInput(text=str(self.main_menu.settings['window_size_x']))
        layout.add_widget(self.window_size_input_x)

        # Window Size Y
        layout.add_widget(Label(text='Window Height'))
        self.window_size_input_y = TextInput(text=str(self.main_menu.settings['window_size_y']))
        layout.add_widget(self.window_size_input_y)

        # X Cells
        layout.add_widget(Label(text='X Cells'))
        self.x_cells_input = TextInput(text=str(self.main_menu.settings['x_cells']))
        layout.add_widget(self.x_cells_input)

        # Y Cells
        layout.add_widget(Label(text='Y Cells'))
        self.y_cells_input = TextInput(text=str(self.main_menu.settings['y_cells']))
        layout.add_widget(self.y_cells_input)

        # Generator Method
        layout.add_widget(Label(text='Generator Method'))
        self.generator_method_input = TextInput(text=self.main_menu.settings['generator_method'])
        layout.add_widget(self.generator_method_input)

        # Solve Method
        layout.add_widget(Label(text='Solve Method'))
        self.solve_method_input = TextInput(text=self.main_menu.settings['method'])
        layout.add_widget(self.solve_method_input)

        # Solution Speed
        layout.add_widget(Label(text='Solution Speed (in ms, higher is slower(best choice is below 0.01))'))
        self.solve_speed = TextInput(text=self.main_menu.settings['solutionspeed'])
        layout.add_widget(self.solve_speed)

        save_button = Button(text='Save Settings', on_press=self.save_settings)
        back_button = Button(text='Back to Main Menu', on_press=self.go_to_main_menu)
        layout.add_widget(save_button)
        layout.add_widget(back_button)
        self.add_widget(layout)


    def save_settings(self, instance):
        # Update the settings dictionary with the new values
        self.main_menu.settings['window_size_x'] = self.window_size_input_x.text
        self.main_menu.settings['window_size_y'] = self.window_size_input_y.text
        self.main_menu.settings['x_cells'] = self.x_cells_input.text
        self.main_menu.settings['y_cells'] = self.y_cells_input.text
        self.main_menu.settings['generator_method'] = self.generator_method_input.text
        self.main_menu.settings['method'] = self.solve_method_input.text
        self.main_menu.settings['solutionspeed'] = self.solve_speed.text
        # Update the start button text in the main menu
        self.main_menu.start_button.text = self.main_menu.get_start_button_text()

        # Go back to the main menu screen
        self.go_to_main_menu(self)

    def go_to_main_menu(self, instance):
        self.manager.transition.direction = "right"
        self.manager.current = 'main_menu'

class MazeApp(App):
    def build(self):
        settings = {
            'window_size_x': '1280',
            'window_size_y': '720',
            'x_cells': '50',
            'y_cells': '50',
            'generator_method': 'wfc',
            'solve': True,
            'method': 'amogus',
            'solutionspeed': '0.00',
        }
        sm = ScreenManager()
        main_menu = MainMenu(settings, name='main_menu')
        settings_screen = Settings(main_menu, name='settings')
        sm.add_widget(main_menu)
        sm.add_widget(settings_screen)
        return sm

if __name__ == '__main__':
    MazeApp().run()


