from crypt import methods
from flask import render_template, current_app as app, request, redirect, url_for, flash
from app import db, mail
from flask_login import current_user, login_required
from flask_mail import Message

@app.route('/', methods=['GET', 'POST'])
def home():
    if current_user.is_authenticated:
        print(current_user)
    if request.method == 'POST':
        return redirect(url_for('home'))
    return render_template('main/home.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        form_data = request.form
        msg = Message(
            subject='[ADR Evaluation Consulting] Contact form inquiry',
            recipients=[app.config.get('MAIL_RECIPIENT')],
            sender=app.config.get('MAIL_RECIPIENT'),
            body=render_template('email/message.txt', data=form_data),
            # html=render_template('email/message.html', data=form_data),
            reply_to=form_data.get('email')
        )
        mail.send(msg)
        flash('Thank you for your inquiry. Please give us 48 hours to get back to you')
        return redirect(request.referrer)
    return render_template('main/contact.html')

@app.route('/about')
def about():
    return render_template('main/about.html')

