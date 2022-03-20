from tkinter import *
from quiz_brain import QuizBrain
from question_model import Question
from data import TriviaData


THEME_COLOR = "#375362"


class QuizInterface:

    def __init__(self):
        self.possible_category = None
        self.triviadata = TriviaData(self.possible_category)
        self.question_category = self.triviadata.question_data[0]['category']
        self.question_bank = self.make_question_bank(self.possible_category)
        self.quiz_brain = QuizBrain(self.question_bank)
        self.score = 0

        self.window = Tk()
        self.window.title("Quizler")
        self.window.geometry('350x475+500+150')
        self.window.configure(pady=15,
                              bg=THEME_COLOR,
                              highlightthickness=0,
                              )

        self.catagory_label = Label(self.window,
                                    bg=THEME_COLOR,
                                    fg="yellow",
                                    text=f"{self.question_category}",
                                    font=("Ariel", 12),
                                    pady=10,
                                    )
        self.catagory_label.grid(column=1, row=1)

        self.score_label = Label(self.window,
                                 bg=THEME_COLOR,
                                 fg="yellow",
                                 text=f'Score: {self.score}',
                                 font=("Ariel", 12),
                                 pady=10,
                                 )
        self.score_label.grid(column=2, row=1)

        self.answer_feedback_label = Label(self.window,
                                           bg=THEME_COLOR,
                                           fg="yellow",
                                           text="",
                                           font=("Ariel", 10, "bold"),
                                           )
        self.answer_feedback_label.grid(column=1, row=3, columnspan=2)

        self.main_canvas = Canvas(width=300,
                                  height=250,
                                  bg="white",
                                  highlightthickness=2,
                                  )
        self.quiz_text = self.main_canvas.create_text(150, 100,
                                                      width=280,
                                                      text="test",
                                                      fill=THEME_COLOR,
                                                      font=("Ariel", 18),
                                                      )
        self.main_canvas.grid(column=1, row=2, columnspan=2, padx=22, pady=5)

        true_button_image = PhotoImage(file="images/true.png")
        false_button_image = PhotoImage(file="images/false.png")
        self.true_button = Button(image=true_button_image,
                                  command=self.true_pressed,
                                  bg=THEME_COLOR,
                                  highlightthickness=0,
                                  )
        self.true_button.grid(column=1, row=4, padx=20, pady=10)
        self.false_button = Button(image=false_button_image,
                                   command=self.false_pressed,
                                   bg=THEME_COLOR, highlightthickness=0,
                                   )
        self.false_button.grid(column=2, row=4, padx=20, pady=10)

        self.get_next_question()
        self.window.mainloop()


    def true_pressed(self):
        answer_correct = self.quiz_brain.check_answer("True")
        self.was_answer_correct(answer_correct)


    def false_pressed(self):
        answer_correct = self.quiz_brain.check_answer("False")
        self.was_answer_correct(answer_correct)


    def make_question_bank(self, possible_category):
        question_bank = []
        question_data = TriviaData(possible_category).get_question_data()
        self.question_category = question_data[0]['category']
        for question in question_data:
            question_text = question["question"]
            question_answer = question["correct_answer"]
            new_question = Question(question_text, question_answer)
            question_bank.append(new_question)
        return question_bank


    def change_settings(self):
        self.window.geometry('500x475')

        self.sorted_trivia_data = {
            'General Knowledge': 9, 'Film': 11, 'Music': 12, 'Television': 14, 'Video Games': 15,
            'Science & Nature': 17, 'Science: Computers': 18, 'Science: Mathematics': 19,
            'Mythology': 20, 'Sports': 21, 'Geography': 22, 'History': 23, 'Politics': 24,
            'Animals': 27, 'Vehicles': 28,
        }
        self.category_options = Listbox(self.window, height=16)
        for category in self.sorted_trivia_data:
            self.category_options.insert(END, category)
        self.category_options.grid(column=3, row=2)
        self.category_options_label = Label(self.window,
                                            bg=THEME_COLOR,
                                            fg="yellow",
                                            text="Select Category:",
                                            font=("Ariel", 10),
                                            )
        self.category_options_label.grid(column=3, row=1)


    def play_again(self):
        try:
            for item in self.category_options.curselection():
                self.possible_category = self.sorted_trivia_data[self.category_options.get(item)]
            self.category_options.destroy()
            self.category_options_label.destroy()
        except:
            pass
        self.window.geometry('350x475')
        self.options_button.destroy()
        self.play_again_button.destroy()
        self.quit_button.destroy()
        self.question_bank = self.make_question_bank(self.possible_category)
        self.quiz_brain = QuizBrain(self.question_bank)
        self.score = 0
        self.score_label.config(text=f'Score: {self.score} ')
        self.catagory_label.config(text=f"{self.question_category}")
        self.get_next_question()


    @staticmethod
    def quit_game():
        quit()

    # noinspection PyAttributeOutsideInit
    def game_over_screen(self):
        self.options_button = Button(text="Options", command=self.change_settings)
        self.options_button.configure(width=10, activebackground=THEME_COLOR, fg=THEME_COLOR)
        self.play_again_button = Button(text="Play Again", command=self.play_again)
        self.play_again_button.configure(width=12, activebackground=THEME_COLOR, fg=THEME_COLOR)
        self.quit_button = Button(text="Quit", command=self.quit_game)
        self.quit_button.configure(width=10, activebackground=THEME_COLOR, fg=THEME_COLOR)

        self.main_canvas.create_window(15, 225, anchor=SW, window=self.options_button)
        self.main_canvas.create_window(106, 225, anchor=SW, window=self.play_again_button)
        self.main_canvas.create_window(210, 225, anchor=SW, window=self.quit_button)


    def get_next_question(self):
        if self.quiz_brain.still_has_questions():
            self.main_canvas.config(bg="white")
            self.answer_feedback_label.config(text='')
            q_text = self.quiz_brain.next_question()
            self.main_canvas.itemconfig(self.quiz_text, text=q_text, font=("Ariel", 16, "normal"))
            self.true_button['state'] = 'normal'
            self.false_button['state'] = 'normal'
        else:
            self.answer_feedback_label.config(text='')
            self.main_canvas.config(bg="white")
            self.main_canvas.itemconfig(self.quiz_text,
                                        text=f'\nQuiz finished! '
                                             f'\n\nYou got {self.score} '
                                             f'out of {len(self.quiz_brain.question_list)} questions correct! ')

            self.game_over_screen()


    def was_answer_correct(self, answer_correct):
        self.true_button['state'] = 'disabled'
        self.false_button['state'] = 'disabled'
        if answer_correct:
            self.score += 1
            self.main_canvas.config(bg="green")
            self.answer_feedback_label.config(text='Correct!')
            self.score_label.config(text=f'Score: {self.score} ')
        else:
            self.main_canvas.config(bg="red")
            self.answer_feedback_label.config(text='Incorrect!')
        self.window.after(1000, self.get_next_question)
