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
import datetime as dt


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
        if (
            int(exam_info.get("num_easy")) == 0
            or int(exam_info.get("num_hard")) == 0
            or int(exam_info.get("num_hard")) == 0
        ):
            flash("Tạo bài thất bại", "error")
            return redirect(request.referrer)
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
        now = datetime.now()
        duration = int(exam_info.get("duration"))
        expire = now + dt.timedelta(minutes=duration)
        exam = Exam(
            room_id=room.room_id,
            teacher_id=user_id,
            exam_name=exam_name.strip().lower(),
            subject_id=room.subject.subject_id,
            duration=duration,
            questions=questions,
            create_at=now,
            expire_at=expire
        )
        exam.save()
        flash("Tạo bài thi thành công", "success")
        return redirect(request.referrer)
    except Exception as e:
        flash("Tạo bài thất bại", "error")
        return redirect(request.referrer)

def get_time():
    return int(datetime.now().timestamp())

def timeout(room_id, exam_id):
    exam = Exam.objects(room_id=room_id, exam_id=exam_id).only("expire_at").first()
    expire = exam.expire_at
    time_left = int(expire.timestamp()) - get_time()
    return int(time_left)

@user.route("/exam", methods=["GET"])
def show_exam_question():
    if session.get("user", None):
        if session["user"].get("classify") == "student":
            try:
                param = request.args.to_dict()
                username = session["user"].get("username")
                room_id = ObjectId(param.get("rid"))
                exam_id = ObjectId(param.get("eid"))
                user_id = ObjectId(session["user"].get("user_id"))
                student = (
                    Exam.objects(students__student_id=user_id, exam_id=exam_id)
                    .only(
                        "students__student_id",
                        "students__total_point",
                        "questions",
                    )
                    .first()
                )
                '''
                if student is not None:
                    for i in student.students:
                        if i.student_id == user_id:
                            numb_of_ques = len(student.questions)
                            correct = int(i.total_point // (10 / numb_of_ques))
                            return render_template(
                                "score.html",
                                score=i.total_point,
                                username=username,
                                numb_of_ques=numb_of_ques,
                                correct=correct,
                            )
                '''
                room = Room.objects(
                    **{"student__student_id": user_id, "room_id": room_id}
                ).first()
                questions = (
                    Exam.objects(room_id=room_id, exam_id=exam_id)
                    .only("questions", "duration")
                    .first()
                )
                student = StudentAnswer(student_id=user_id, total_point=0)
                Exam.objects(room_id=room_id, exam_id=exam_id).update_one(
                    push__students=student
                )
                time_left = timeout(room_id, exam_id)
                duration = questions.duration * 60
                return render_template(
                    "exam.html",
                    questions=questions,
                    room=room,
                    exam_id=exam_id,
                    duration=duration,
                    time_left = time_left
                )
            except Exception as e:
                return redirect(url_for("user.error"))
    return redirect(url_for("auth.login"))


@user.route("/result", methods=["POST"])
def check_answer():
    ques_info = request.form.to_dict()
    user_id = ObjectId(session["user"].get("user_id"))

    result = []
    answers = []
    param = request.args.to_dict()
    for question, answer in ques_info.items():
        q = Storage.objects(Id=question).first()
        answers.append(Result(question_id=question, answer_id=answer))
        if q:
            if str(q.correct_answer) == answer:
                result.append(answer)
    username = session["user"].get("username")
    exam = Exam.objects(students__student_id=user_id).only("questions").first()
    score = "{:.2f}".format((10 / len(exam.questions)) * len(result))
    Exam.objects.filter(
        students__student_id=user_id, exam_id=ObjectId(param.get("eid"))
    ).update(
        **{
            "push__students__$__answers": answers,
            "set__students__$__total_point": score,
        }
    )
    return render_template(
        "score.html",
        score=score,
        username=username,
        numb_of_ques=len(exam.questions),
        correct=len(result),
    )


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
