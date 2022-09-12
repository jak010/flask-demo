from datetime import datetime

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import config
from application.models import Question, Answer

db = SQLAlchemy()

app = Flask(__name__)
app.config.from_object(config)

db.init_app(app)

# ORM
# with app.app_context():
#     question1 = Question(subject='안녕하세요', content='가입 인사드립니다 ^^')
#     db.session.add(question1)
#     question2 = Question(subject='질문 있습니다', content='ORM이 궁금합니다')
#     db.session.add(question2)
#
#     q = Question(subject='pybo가 무엇인가요?', content='pybo에 대해서 알고 싶습니다.', create_date=datetime.now())
#     db.session.add(q)
#     db.session.commit()
#
#     q = Question(subject='플라스크 모델 질문입니다.', content='id는 자동으로 생성되나요?', create_date=datetime.now())
#     db.session.add(q)
#     db.session.commit()
#
#     q = Question.query.get(2)
#     q.subject = 'Flask Model Question'
#     db.session.commit()
#
#     q = Question.query.get(1)
#     db.session.delete(q)
#     db.session.commit()
#
#     # 답변 저장하기
#     q = Question.query.get(2)
#     a = Answer(question=q, content='네 자동으로 생성됩니다.', create_date=datetime.now())
#     db.session.add(a)
#     db.session.commit()

# Test Setup
from application.models import Question
from datetime import datetime

with app.app_context():

    for i in range(300):
        q = Question(subject="테스트 데이터 입니다[%03d]" % i, content="내용무", create_date=datetime.now())
        db.session.add(q)

    db.session.commit()
