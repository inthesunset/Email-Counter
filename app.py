from flask import Flask, request, url_for, redirect, render_template, flash
from wtforms import Form
from collections import defaultdict

app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = '7f441a27d441f27567f441f2d6176e'

@app.route("/", methods = ['POST', 'GET'])
def welcome():
    form = Form(request.form)
    if request.method == 'POST':
        flash(email_count(request.form['emails']))
    return render_template('count_email.html', form = form)



def email_count(emails):
    # no multiple @, only one @ is allowed
    ret = 0
    email_set = set()
    for email in emails.strip().split():
        if '@' not in email:
            return email + ' is invalid, require @'
        if len(email.split('@')) > 2:
            return email + ' is invalid, only one @ is allowed'
        if not email.split('@')[0] or not email.split('@')[1]:
            return email + ' is invalid, characters must appear before and after @ sign'
        purified_email = ''
        for i, char in enumerate(email):
            if char not in ('.', '+', '@'):
                purified_email += char
            elif char == '@':
                purified_email += email[i:]
                break
            elif char == '.':
                continue
            elif char == '+':
                purified_email += '@' + email.split('@')[1]
                break
        if purified_email not in  email_set:
            email_set.add(purified_email)
    return 'We found ' + str(len(email_set)) + ' unique email(s)'


if __name__ == "__main__":
    app.run()
