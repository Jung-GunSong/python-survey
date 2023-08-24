from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

app.config['SECRET_KEY'] = "secret-key-yes-very-secret"


@app.get("/")
def homepage():

    session["question_number"] = 0
    session["responses"] = []

    return render_template("survey_start.html", survey_title=survey.title, survey_instructions=survey.instructions)


@app.post("/answer_question")
def answer_question():

    cur_question_number = session["question_number"]

    cur_answer = request.form.get("answer")

    if cur_answer:
        session["responses"].append(cur_answer)
    print("Cur Answer", cur_answer)

    if cur_question_number < len(survey.questions):
        session["question_number"] += 1
        return redirect(f"/question/{cur_question_number}")

    return redirect("/completion")


@app.get("/question/<int:question_number>")
def get_first_question(question_number):

    return render_template("question.html", question=survey.questions[question_number])


@app.get("/completion")
def get_completion_message():

    return render_template("completion.html", responses=session["responses"])