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
    """Starting page"""

    # Move these to answer_question(), we want to modify session data in a post
    session["question_number"] = 0
    session["responses"] = []

    return render_template("survey_start.html", survey_title=survey.title, survey_instructions=survey.instructions)
    # TODO: Just give the survey object for jinja to access

# Split this up to have 1 to start survey and 1 to answer the question
@app.post("/answer_question")
def answer_question():
    """Logic for answering a question"""

    cur_question_number = session["question_number"] # This is not needed, we could just extract this from len(responses)
    cur_answer = request.form.get("answer")
    cur_responses = session["responses"]

    if cur_answer:
        cur_responses.append(cur_answer)

    session["responses"] = cur_responses
    if cur_question_number < len(survey.questions):
        session["question_number"] += 1
        return redirect(f"/question/{cur_question_number}")

    return redirect("/completion")


@app.get("/question/<int:question_number>")
def get_first_question(question_number): # Rename this
    """Loads next question"""
    questions = survey.questions
    return render_template("question.html", question=questions[question_number])


@app.get("/completion")
def get_completion_message():
    """Loads completion message with results after last question"""
    # print("sessions responses before completion", session["responses"])
    return render_template(
        "completion.html",
        questions = survey.questions,
        responses = session["responses"]
    )