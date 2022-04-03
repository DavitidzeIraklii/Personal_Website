import os
from flask import Flask, render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditorField
import smtplib
from datetime import datetime, date



app=Flask(__name__)
app.config['SECRET_KEY'] = '123'
ckeditor = (app)
Bootstrap(app)

MY_EMAIL = 'davitidzeiraklii@gmail.com'
PASSWORD = os.environ.get('PASSWORD')
TO_EMAIL = 'spaceduck1313@gmail.com'
currentYear = datetime.now().year

war_begins = date(2022, 2, 24)
today = date(datetime.now().year, datetime.now().month, datetime.now().day)
war_duration = str(today - war_begins).split(' ')[0]


class MessageForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired()])
    message = CKEditorField('message')
    submit = SubmitField('send message')

class Ok_Form(FlaskForm):
    submit = SubmitField('Ok')

@app.route('/', methods=['GET', 'POST'])
def main_page():
    form = MessageForm()
    if form.validate_on_submit():
        with smtplib.SMTP('smtp.gmail.com') as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=PASSWORD)
            connection.sendmail(from_addr=MY_EMAIL,
                                to_addrs=TO_EMAIL,
                                msg=f'Subject:Message from personal website\n\n{form.name.data} sends me from personal website {form.message.data}. Responde to {form.email.data}')
        return redirect(url_for('send_mes_page'))
    return render_template('index.html', form=form, year=currentYear, war=war_duration)

@app.route('/sendmessage', methods=['GET', 'POST'])
def send_mes_page():
    form = Ok_Form()
    if form.validate_on_submit():
        return redirect(url_for('main_page'))
    return render_template('SendedMes.html', form=form, year=currentYear)



if __name__ == '__main__':
    app.run(debug=True)