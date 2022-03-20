from tkinter import *
from quiz_brain import QuizBrain
from question_model import Question
import os
import sys

THEME_COLOR = "#375362"


class QuizInterface:

    def __init__(self, quiz_brain: QuizBrain, question_category):
        self.quiz = quiz_brain
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
                                    text=f"{question_category}",
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


        def true_pressed():
            user_answer = "true"
            if quiz_brain.check_answer(user_answer):
                answer_correct = True
                self.was_answer_correct(answer_correct)
            else:
                answer_correct = False
                self.was_answer_correct(answer_correct)


        def false_pressed():
            user_answer = "false"
            if quiz_brain.check_answer(user_answer):
                answer_correct = True
                self.was_answer_correct(answer_correct)
            else:
                answer_correct = False
                self.was_answer_correct(answer_correct)

        true_button_image = PhotoImage(file="images/true.png")
        false_button_image = PhotoImage(file="images/false.png")
        self.true_button = Button(image=true_button_image,
                                  command=true_pressed,
                                  bg=THEME_COLOR,
                                  highlightthickness=0,
                                  )
        self.true_button.grid(column=1, row=4, padx=20, pady=10)
        self.false_button = Button(image=false_button_image,
                                   command=false_pressed,
                                   bg=THEME_COLOR, highlightthickness=0,
                                   )
        self.false_button.grid(column=2, row=4, padx=20, pady=10)


        self.get_next_question()


        self.window.mainloop()


    def change_settings(self):
        pass


    def play_again(self):
        os.execv(sys.executable, ['main.py'] + sys.argv)


    def quit_game(self):
        quit()


    def game_over_screen(self):
        options_button = Button(text="Options")
        options_button.configure(width=10, activebackground=THEME_COLOR, fg=THEME_COLOR)
        play_again_button = Button(text="Play Again", command=self.play_again)
        play_again_button.configure(width=12, activebackground=THEME_COLOR, fg=THEME_COLOR)
        quit_button = Button(text="Quit", command=self.quit_game)
        quit_button.configure(width=10, activebackground=THEME_COLOR, fg=THEME_COLOR)

        self.window = self.main_canvas.create_window(15, 225, anchor=SW, window=options_button)
        self.window = self.main_canvas.create_window(106, 225, anchor=SW, window=play_again_button)
        self.window = self.main_canvas.create_window(210, 225, anchor=SW, window=quit_button)


    def was_answer_correct(self, answer_correct):
        if answer_correct:
            self.score += 1
            self.main_canvas.config(bg="green")
            self.answer_feedback_label.config(text='Correct!')
            self.score_label.config(text=f'Score: {self.score} ')
            self.change_question()

        else:
            self.main_canvas.config(bg="red")
            self.answer_feedback_label.config(text='Incorrect!')
            self.change_question()


    def get_next_question(self):
        if self.quiz.still_has_questions():
            self.main_canvas.config(bg="white")
            self.answer_feedback_label.config(text='')
            q_text = self.quiz.next_question()
            self.main_canvas.itemconfig(self.quiz_text, text=q_text, font=("Ariel", 16, "normal"))
            self.true_button['state'] = 'normal'
            self.false_button['state'] = 'normal'
        else:
            self.answer_feedback_label.config(text='')
            self.main_canvas.config(bg="white")
            self.main_canvas.itemconfig(self.quiz_text,
                                        text=f'\nQuiz finished! '
                                             f'\n\nYou got {self.score} '
                                             f'out of {len(self.quiz.question_list)} questions correct! ')

            self.game_over_screen()


    def change_question(self):
        self.true_button['state'] = 'disabled'
        self.false_button['state'] = 'disabled'
        self.window.after(1000, self.get_next_question)
