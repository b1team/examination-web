from app.routers.user import user
from app.models.user import Storage
from app.routers.user import render_template, request
from random import shuffle
from jinja2 import environment
import multitimer
import time


def filter_shuffle(seq):
    try:
        result = list(seq)
        shuffle(result)
        return result
    except:
        return seq
environment.DEFAULT_FILTERS['shuffle'] = filter_shuffle


@user.route("/exam", methods=['GET'])
def show_exam():
    def job(t):
        while t:
            mins, secs = divmod(t, 60)
            ti = '{:02d}:{:02d}'.format(mins, secs)
            print(ti, end="\r")
            time.sleep(1)
            t -= 1
        timer.stop()

    timer = multitimer.MultiTimer(interval=1, function=job, kwargs={"t": 10})
    exams = Storage.objects()
    timer.start()
    return render_template("exam.html", exams=exams)


@user.route('/exam', methods=["POST"])
def check_answer():
    ques = request.form.to_dict()
    result = []
    for question, answer in ques.items():
        q = Storage.objects(Id=question).first()
        if q:
            if str(q.correct_answer) == answer:
                result.append(answer)
    return f"correct answer {len(result)}"
