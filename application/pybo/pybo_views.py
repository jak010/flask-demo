from datetime import datetime

from flask import Blueprint, render_template, url_for, request, flash
from werkzeug.utils import redirect
from werkzeug.security import generate_password_hash

from app import db
from application.models import Question, Answer, User
from application.pybo.forms import QuestionForm, AnswerForm, UserCreateForm

bp = Blueprint("pybo", __name__, url_prefix='/pybo')


@bp.route('/')
def hello_pybo():
    return redirect(url_for("pybo.pybo_list"))


@bp.route('/list')
def pybo_list():
    """ Pybo List API
    :Reference
        https://wikidocs.net/81054
    """
    page = request.args.get('page', type=int, default=1)

    question_list = Question.query.order_by(Question.create_date.desc())
    question_list = question_list.paginate(page, per_page=10)

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


@bp.route('/signup/', methods=('GET', 'POST'))
def signup():
    form = UserCreateForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if not user:
            user = User(username=form.username.data,
                        password=generate_password_hash(form.password1.data),
                        email=form.email.data)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('pybo.pybo_list'))
        else:
            flash('이미 존재하는 사용자입니다.')
    return render_template('auth/signup.html', form=form)
