from app.routers.user import user, request
from app.models.user import Storage, Answer


@user.route("/question", methods=["POST"])
def create_question():
    question_info = request.form.to_dict()
    result = []
    for index, an in enumerate("ABCD", start=0):
        result.append(Answer(id=index, value=question_info.get(f"answer{an}")))
    exam = Storage(
        ques=question_info.get("question"),
        answ=result,
        correct_answer=question_info.get("key"),
        level=question_info.get('level')
    )
    exam.save()
    return 'ok'