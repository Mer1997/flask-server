import logging
from flask_wtf import FlaskForm,RecaptchaField
from wtforms import StringField, TextField, TextAreaField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, URL
from server.models import db,Log,User

def logError(message):
    logging.error(message)

class LoginForm(FlaskForm):
    username=TextField('Username')
    password=PasswordField('Password')

    def validate(self):
        
        check_validate = super(LoginForm, self).validate()

        if not check_validate:
            return False
        logging.error('username is %s'%(self.username))
        user=User.query.filter_by(username='mer').first()#self.username.data).first()
        if not user:
            logError('username %s: Invalid username or password'%self.username.data)
            self.username.errors.append(
                'Invalid username or password'
            )

            return False
        
        if not user.checkPassword(self.password.data):
            logError('password %s:Invalid username or password'%self.password.data)
            self.username.errors.append(
                'Invalid username or password'
            )

            return False
        
        return True

class RegisterForm(FlaskForm):
    username = StringField('Username',[DataRequired(),Length(max=20)])
    password = PasswordField('Password',[DataRequired(),Length(min=8,max=16)])
    confirm = PasswordField('Confirm Password',[DataRequired(),EqualTo('password')])

    recaptcha = RecaptchaField()

    def validate(self):
        check_validate = super(RegisterForm, self).validate()

        if not check_validate:
            return False

        user = User.query.filter_by(username = self.username.data).first()

        if user:
            self.username.errors.append(
                "User with that name already exists"
            )
            return False
    
        return True


class ResetPWDForm(FlaskForm):
    username = StringField('Username',[DataRequired()])
    old_pwd = StringField(
       'Old Password',
       validators=[DataRequired(),Length(min=6,max=16)]
    )
    new_pwd = StringField(
       'New Password',
       validators=[DataRequired(),Length(min=6,max=16)]
    )
    confirm_pwd = StringField(
       'Confirm Password',
       validators=[DataRequired(),EqualTo('new_pwd')]
    )
    def validate(self):
        check_validate = super(ResetPWDForm, self).validate()

        if not check_validate:
        
            self.old_pwd.errors.append('Invalid data.')
            return False

        user = User.query.filter_by(username = self.username.data).first()
        if not user:
            return False

        if not self.check_password(user.password, old_pwd):
            self.old_pwd.errors.append(
                'Incorrect password'
            )
            return False

        return True


    
class ResetNameForm(FlaskForm):
    new_name = StringField(
       'New Username',
       validators=[DataRequired(),Length(min=4,max=16)]
    )

