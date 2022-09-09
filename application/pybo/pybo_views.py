from flask import Blueprint, render_template, url_for, request
from datetime import datetime
from werkzeug.utils import redirect
from app import db
from application.models import Question, Answer
from application.pybo.forms import QuestionForm, AnswerForm

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
    form = AnswerForm()
    question = Question.query.get_or_404(question_id)

    return render_template("question/question_detail.html", question=question, form=form)


@bp.route("/create", methods=('GET', 'POST'))
def pybo_create():
    form = QuestionForm()

    if request.method == 'POST' and form.validate_on_submit():
        question = Question(
            subject=form.subject.data,
            content=form.content.data,
            create_date=datetime.now()
        )
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('pybo.pybo_list'))

    print(form.errors)

    return render_template('question/question_form.html', form=form)


@bp.route('/create/<int:question_id>', methods=('POST',))
def create(question_id: int):
    form = AnswerForm()
    question = Question.query.get_or_404(question_id)
    if form.validate_on_submit():
        content = request.form['content']
        answer = Answer(content=content, create_date=datetime.now())
        question.answer_set.append(answer)
        db.session.commit()
        return redirect(url_for('question.detial', question_id=question_id))

    return render_template('question/question_detail.html', question=question, form=form)
