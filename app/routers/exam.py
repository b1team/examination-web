from typing import List
from app.routers.user import (
    user,
    render_template,
    session,
    redirect,
    url_for,
    request,
)
from app.models.exam import Exam, Question, StudentAnswer, Result
from app.models.storage import Storage
from app.models.room import Room
from bson import ObjectId
from random import choices, shuffle
import itertools


@user.route("/question-form", methods=["GET"])
def show_question_form():
    if session.get("user", None):
        if session["user"].get("classify") == "teacher":
            return render_template("createQuestion.html")
    return redirect(url_for("auth.login"))


@user.route("/exam-form", methods=["GET"])
def show_exam_form():
    if session.get("user", None):
        if session["user"].get("classify") == "teacher":
            return render_template("formExam.html")
    return redirect(url_for("auth.login"))


def random_ques_level(level: int, num_of_ques: int):
    storage = Storage.objects()
    questions = list(storage.filter(level=level))
    shuffle(questions)
    return choices(questions, k=int(num_of_ques))


@user.route("/exam", methods=["POST"])
def create_exam():
    exam_info = request.form.to_dict()

    number_of_ques = exam_info.get("num")

    easy_ques = random_ques_level(1, exam_info.get("num_easy"))
    medium_ques = random_ques_level(2, exam_info.get("num_med"))
    hard_ques = random_ques_level(3, exam_info.get("num_hard"))

    user_id = ObjectId(session["user"].get("user_id"))
    room = Room.objects(teacher__teacher_id=user_id).first()
    storage = list(itertools.chain(easy_ques, medium_ques, hard_ques))[
        : int(number_of_ques)
    ]
    questions = []
    for item in storage:
        questions.append(
            Question(
                question_id=item.Id,
                question_name=item.question,
                level=item.level,
                answer=item.answer,
                correct_answer=item.correct_answer,
            )
        )
    exam = Exam(
        room_id=room.room_id,
        duration=int(exam_info.get("duration")),
        questions=questions,
    )
    exam.save()
    return "ok"


@user.route("/exam/<room_id>", methods=["GET"])
def show_exam_question(room_id=None):
    try:
        if session.get("user", None):
            if session["user"].get("classify") == "student":
                user_id = ObjectId(session["user"].get("user_id"))
                room = Room.objects(
                    **{"student__student_id": user_id, "room_id": room_id}
                ).first()
                questions = (
                    Exam.objects(room_id=room_id).only("questions").first()
                )
                student = StudentAnswer(student_id=user_id, total_point=0)
                Exam.objects(room_id=room_id).update_one(
                    push__students=student
                )
                return render_template(
                    "exam.html", questions=questions, room=room
                )
        return redirect(url_for("auth.login"))
    except Exception:
        return redirect(url_for("user.error"))


@user.route("/result", methods=["POST"])
def check_answer():
    questio = request.form.to_dict()
    user_id = ObjectId(session["user"].get("user_id"))

    result = []
    answers = []
    for question, answer in questio.items():
        q = Storage.objects(Id=question).first()
        answers.append(Result(question_id=question, answer_id=answer))
        if q:
            if str(q.correct_answer) == answer:
                result.append(answer)
    exam = Exam.objects(students__student_id=user_id).only("questions").first()
    score = (10 / len(exam.questions)) * len(result)
    Exam.objects.filter(students__student_id=user_id).update(
        **{
            "push__students__$__answers": answers,
            "set__students__$__total_point": score,
        }
    )
    return render_template("score.html", score=score)
