from wtforms import Form, StringField, PasswordField, validators


class RegistrationForm(Form):
    username = StringField('Username', [
        validators.DataRequired(),
        validators.length(min=4, max=25)
    ])


    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match'),
        validators.length(min=6, max=25)
     ])
    confirm = PasswordField('Repeat Password', [
        validators.DataRequired()
        ])
