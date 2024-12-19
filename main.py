import random
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window


# First Page - Introduction screen
class WelcomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation="vertical", spacing=10, padding=10)

        layout.add_widget(Label(text="Welcome to the Guessing Game!", font_size=32, bold=True, size_hint=(1, 0.2)))

        description = "This is a number guessing game.\nMade by Biraj Malla.\n\nTry to guess the number between 1 and 100."
        layout.add_widget(Label(text=description, font_size=24, size_hint=(1, 0.5)))

        start_button = Button(text="Start Game", font_size=24, size_hint=(1, 0.2))
        start_button.bind(on_press=self.start_game)
        layout.add_widget(start_button)

        self.add_widget(layout)

    def start_game(self, instance):
        """Transition to the Game Screen"""
        self.manager.current = "game_screen"


# Second Page - Game screen
class GameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.target_number = random.randint(1, 100)
        self.attempts = 0

        # Layout for the game screen
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Instruction Label
        self.instruction = Label(text="Guess the number between 1 and 100", font_size=24, size_hint=(1, 0.1))
        self.layout.add_widget(self.instruction)

        # Text input for guess
        self.guess_input = TextInput(hint_text="Enter your guess", font_size=24, size_hint=(1, 0.1))
        self.layout.add_widget(self.guess_input)

        # Feedback label
        self.feedback = Label(text="", font_size=24, size_hint=(1, 0.1))
        self.layout.add_widget(self.feedback)

        # Submit button
        self.submit_button = Button(text="Submit Guess", font_size=24, size_hint=(1, 0.1))
        self.submit_button.bind(on_press=self.check_guess)
        self.layout.add_widget(self.submit_button)

        # New game button
        self.new_game_button = Button(text="New Game", font_size=24, size_hint=(1, 0.1))
        self.new_game_button.bind(on_press=self.new_game)
        self.layout.add_widget(self.new_game_button)

        # Set background color to make it attractive
        Window.clearcolor = (0.5, 0.7, 1, 1)  # Light blue background color

        # Add the layout to the screen
        self.add_widget(self.layout)

    def check_guess(self, instance):
        try:
            user_guess = int(self.guess_input.text)
        except ValueError:
            self.feedback.text = "Please enter a valid number!"
            return

        self.attempts += 1

        if user_guess < self.target_number:
            self.feedback.text = "Too low! Try again."
        elif user_guess > self.target_number:
            self.feedback.text = "Too high! Try again."
        else:
            self.feedback.text = f"Correct! You guessed the number in {self.attempts} attempts."
            self.show_popup(f"You guessed the number in {self.attempts} attempts! Well done.")

    def new_game(self, instance):
        self.target_number = random.randint(1, 100)
        self.attempts = 0
        self.guess_input.text = ""
        self.feedback.text = ""
        self.instruction.text = "Guess the number between 1 and 100"

    def show_popup(self, message):
        popup_layout = GridLayout(cols=1, padding=10)
        popup_label = Label(text=message, font_size=18)
        popup_layout.add_widget(popup_label)

        close_button = Button(text="Close", font_size=18, size_hint=(1, 0.2))
        close_button.bind(on_press=self.close_popup)
        popup_layout.add_widget(close_button)

        self.popup = Popup(title="Congratulations", content=popup_layout, size_hint=(None, None), size=(400, 300))
        self.popup.open()

    def close_popup(self, instance):
        self.popup.dismiss()
        self.new_game(instance)


# Screen Manager to manage both screens
class GuessNumberApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(WelcomeScreen(name="welcome_screen"))
        sm.add_widget(GameScreen(name="game_screen"))
        return sm


if __name__ == "__main__":
    GuessNumberApp().run()