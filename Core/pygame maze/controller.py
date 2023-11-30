from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.dropdown import DropDown
import visualiser
import generator
import solver
import time
import wfcgenerator

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

        resolutiondropdown = DropDown()
        celldropdown = DropDown()
        gendropdown = DropDown()
        solvedropdown = DropDown()


        resolutions = [('720p', 1280, 720),
                        ('1080p', 1920, 1080),
                        ('1440p', 2560, 1440)]
        
        generator_methods = [("df","df"), 
                                ("wfc","wfc")]

        solver_methods = [("bfs","bfs"), 
                            ("lefthand","lefthand"), 
                            ("amogus","amogus")]
        
        cellLimits = [('50', 50,50),
                      ('100',100,100),
                      ('200',200,200),
                      ('300',300,300),
                      ('500',500,500),
                      ('1000',1000,1000),
                      ('1500',1500,1500)]
        
        self.x_cells = 100
        self.y_cells = 100
        self.gen_method = "df"
        self.solve_method = "bfs"
        self.resW = 1280
        self.resH = 720

        for option in resolutions:
            btn = Button(text=option[0], size_hint_y=None, height=100)
            btn.bind(on_release=lambda btn, opt=option: self.update_resolution(opt))
            btn.bind(on_release=resolutiondropdown.dismiss)
            resolutiondropdown.add_widget(btn)

        resButton = Button(text='Select Resolution', size_hint=(1, None))
        resButton.bind(on_release=resolutiondropdown.open)
        resolutiondropdown.bind(on_select=lambda instance, x: setattr(resButton, 'text', x))

        for option in generator_methods:
            btn = Button(text=option[0], size_hint_y=None, height=100)
            btn.bind(on_release=lambda btn, opt=option: self.update_gen_method(opt))
            btn.bind(on_release=gendropdown.dismiss)
            gendropdown.add_widget(btn)

        genButton = Button(text='Select generator method', size_hint=(1,None))
        genButton.bind(on_release=gendropdown.open)
        gendropdown.bind(on_select=lambda instance, x: setattr(genButton, 'text', x))

        for option in solver_methods:
            btn = Button(text=option[0], size_hint_y=None, height=100)
            btn.bind(on_release=lambda btn, opt=option: self.update_solve_method(opt))
            btn.bind(on_release=solvedropdown.dismiss)
            solvedropdown.add_widget(btn)

        solveButton = Button(text='Select Solving method', size_hint=(1,None))
        solveButton.bind(on_release=solvedropdown.open)
        solvedropdown.bind(on_select=lambda instance, x: setattr(solveButton, 'text', x))

        for option in cellLimits:
            btn = Button(text=option[0], size_hint_y=None, height=100)
            btn.bind(on_release=lambda btn, opt=option: self.update_cell_limits(opt))
            btn.bind(on_release=celldropdown.dismiss)
            celldropdown.add_widget(btn)

        cellButton = Button(text='Select cells amount', size_hint=(1,None))
        cellButton.bind(on_release=celldropdown.open)
        celldropdown.bind(on_select=lambda instance, x: setattr(cellButton, 'text', x))


        # Add widgets to the layout
        layout.add_widget(resButton)
        layout.add_widget(cellButton)
        layout.add_widget(genButton)
        layout.add_widget(solveButton)

        # Solution Speed
        layout.add_widget(Label(text='Solution Speed (in ms, higher is slower(best choice is below 0.01))'))
        self.solve_speed = TextInput(text=self.main_menu.settings['solutionspeed'])
        layout.add_widget(self.solve_speed)

        save_button = Button(text='Save Settings', on_press=self.save_settings)
        back_button = Button(text='Back to Main Menu', on_press=self.go_to_main_menu)
        layout.add_widget(save_button)
        layout.add_widget(back_button)
        self.add_widget(layout)

    def update_resolution(self, option):
        self.resW = option[1]
        self.resH = option[2]

    def update_gen_method(self, option):
        self.gen_method = option[1]

    def update_solve_method(self, option):
        self.solve_method = option[1]

    def update_cell_limits(self, option):
        self.x_cells = option[0]
        self.y_cells = option[1]

    def save_settings(self, instance):
        # Update the settings dictionary with the new values
        self.main_menu.settings['window_size_x'] = self.resW
        self.main_menu.settings['window_size_y'] = self.resH
        self.main_menu.settings['x_cells'] = self.x_cells
        self.main_menu.settings['y_cells'] = self.y_cells
        self.main_menu.settings['generator_method'] = self.gen_method
        self.main_menu.settings['method'] = self.solve_method
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
            'generator_method': 'df',
            'solve': True,
            'method': 'bfs',
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


