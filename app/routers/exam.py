from typing import List


from app.routers.user import (
    user,
    render_template,
    session,
    redirect,
    url_for,
    request,
    flash,
)
from app.models.exam import Exam, Question, StudentAnswer, Result
from app.models.storage import Storage
from app.models.room import Room
from bson import ObjectId
from random import choices, shuffle, sample
import itertools
from datetime import datetime


@user.route("/create-exam/<room_id>", methods=["GET"])
def show_exam_form(room_id: ObjectId):
    if session.get("user", None):
        if session["user"].get("classify") == "teacher":
            try:
                teacher_id = ObjectId(session["user"].get("user_id"))
                room = Room.objects(room_id=room_id).first()
                ques_of_teacher = Storage.objects(
                    **{
                        "teacher_id": teacher_id,
                        "subject_id": room.subject.subject_id,
                    }
                )
                all_ques = ques_of_teacher.count()
                easy_ques = ques_of_teacher.filter(level=1).count()
                medium_ques = ques_of_teacher.filter(level=2).count()
                hard_ques = ques_of_teacher.filter(level=3).count()
                return render_template(
                    "formExam.html",
                    room_id=room_id,
                    all_ques=all_ques,
                    easy_ques=easy_ques,
                    medium_ques=medium_ques,
                    hard_ques=hard_ques,
                )
            except Exception:
                return redirect(url_for("user.error"))
    return redirect(url_for("auth.login"))


def random_ques_level(level: int, num_of_ques: int, subject: ObjectId):
    teacher_id = ObjectId(session["user"].get("user_id"))
    storage = Storage.objects(
        **{"teacher_id": teacher_id, "subject_id": subject}
    )
    questions = list(storage.filter(level=level))
    shuffle(questions)
    return sample(questions, int(num_of_ques))


@user.route("/exam/<room_id>", methods=["POST"])
def create_exam(room_id: ObjectId):
    exam_info = request.form.to_dict()
    try:
        room = Room.objects(room_id=room_id).first()
        subject_id = room.subject.subject_id

        exam_name = exam_info.get("exam_name")
        number_of_ques = exam_info.get("num")
        easy_ques = random_ques_level(1, exam_info.get("num_easy"), subject_id)
        medium_ques = random_ques_level(
            2, exam_info.get("num_med"), subject_id
        )
        hard_ques = random_ques_level(3, exam_info.get("num_hard"), subject_id)

        user_id = ObjectId(session["user"].get("user_id"))
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
            teacher_id=user_id,
            exam_name=exam_name.strip().lower(),
            subject_id=room.subject.subject_id,
            duration=int(exam_info.get("duration")),
            questions=questions,
            create_at=datetime.now(),
        )
        exam.save()
        flash("Tạo bài thi thành công", "success")
        return redirect(request.referrer)
    except Exception:
        flash("Tạo bài thất bại", "error")
        return redirect(request.referrer)


@user.route("/exam", methods=["GET"])
def show_exam_question():
    if session.get("user", None):
        if session["user"].get("classify") == "student":
            try:
                param = request.args.to_dict()
                room_id = ObjectId(param.get("rid"))
                exam_id = ObjectId(param.get("eid"))
                user_id = ObjectId(session["user"].get("user_id"))
                student = Exam.objects(students__student_id=user_id, exam_id=exam_id).only("students__student_id", "students__total_point").first()
                if student is not None:
                    return render_template(
                        "score.html", score=student.students[0].total_point
                    )
                room = Room.objects(
                    **{"student__student_id": user_id, "room_id": room_id}
                ).first()
                questions = (
                    Exam.objects(room_id=room_id, exam_id=exam_id)
                    .only("questions")
                    .first()
                )

                student = StudentAnswer(student_id=user_id, total_point=0)
                Exam.objects(room_id=room_id, exam_id=exam_id).update_one(
                    push__students=student
                )
                return render_template(
                    "exam.html", questions=questions, room=room
                )
            except Exception:
                return redirect(url_for("user.error"))
    return redirect(url_for("auth.login"))


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


@user.route("/result", methods=["GET"])
def get_result():
    if session.get("user", None):
        if session["user"].get("classify") == "teacher":
            param = request.args.to_dict()
            user_id = ObjectId(session["user"].get("user_id"))
            try:
                exams = (
                    Exam.objects(
                        **{
                            "exam_id": ObjectId(param.get("eid")),
                            "teacher_id": user_id,
                        }
                    )
                    .only("students__student_id", "students__total_point")
                    .first()
                )
                room = Room.objects(room_id=ObjectId(param.get("rid"))).first()
                result = [
                    {
                        "student_name": student.student_name,
                        "total_point": exam.total_point,
                    }
                    for student in room.student
                    for exam in exams.students
                    if (student.student_id == exam.student_id)
                ]
                return render_template("rank.html", result=result)
            except Exception:
                return redirect(url_for("user.error"))
    return redirect(url_for("auth.login"))
