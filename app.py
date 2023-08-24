from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

question_number = 0
responses = []

@app.get("/")
def homepage():

    return render_template("survey_start.html", survey_title=survey.title, survey_instructions=survey.instructions)


@app.post("/answer_question")
def answer_question():

    if question_number < len(survey.questions)-1:
        return redirect(f"/question/{question_number}")


    return redirect("completion.html")


@app.get("/question/<int:question_number>")
def get_first_question(question_number):

    return render_template("question.html", question=survey.questions[question_number])
