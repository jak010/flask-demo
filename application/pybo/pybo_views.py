from flask import Blueprint, render_template, url_for
from werkzeug.utils import redirect

from application.models import Question

bp = Blueprint("pybo", __name__, url_prefix='/pybo')


@bp.route('/')
def hello_pybo():
    return redirect(url_for("pybo.pybo_list"))


@bp.route('/list')
def pybo_list():
    question_list = Question.query.order_by(Question.create_date.desc())

    return render_template("question/question_list.html", question_list=question_list)


@bp.route('/detail/<int:question_id>')
def pybo_detail(question_id):
    question = Question.query.get_or_404(question_id)

    return render_template("question/question_detail.html", question=question)
