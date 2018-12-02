import logging
from flask_wtf import FlaskForm,RecaptchaField
from wtforms import TextField, SubmitField, TextAreaField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, URL
from server.models import db,Log,User

def logError(message):
    logging.error(message)

class LoginForm(FlaskForm):
    username=TextField('Username')
    password=PasswordField('Password')
    submit=SubmitField('Sign In')

    def validate(self):
        
        check_validate = super(LoginForm, self).validate()

        if not check_validate:
            return False
        logging.error('username is %s'%(self.username))
        user=User.query.filter_by(username=self.username.data).first()#self.username.data).first()
        if not user:
            logError('username %s: Invalid username or password'%self.username.data)
            self.username.errors.append(
                'Invalid username or password'
            )

            return False
        
        flag = self.password.data == 'acacac'
        logError('form.password = acacac is %s'%flag)
        if not user.checkPassword(self.password.data):
            logError('password %s:Invalid username or password'%self.password.data)
            self.username.errors.append(
                'Invalid username or password'
            )

            return False
        
        return True

class RegisterForm(FlaskForm):
    username = TextField('Username',[DataRequired(),Length(max=20)])
    password = PasswordField('Password',[DataRequired(),Length(min=3,max=16)])
    confirm = PasswordField('Confirm Password',[DataRequired(),EqualTo('password')])

    #recaptcha = RecaptchaField()

    def validate(self):
        check_validate = super(RegisterForm, self).validate()
        logError('%s - %s - %s'%(self.username.data, self.password.data, self.confirm.data))
        if not check_validate:
            logError('Form: validate was false')
            return False

        user = User.query.filter_by(username = self.username.data).first()

        if user:
            logError('Username %s: User with that name already exists'%self.username)
            self.username.errors.append(
                "User with that name already exists"
            )
            return False
        logError('rigister successful: username :%s, password :%s'%(self.username.data, self.password.data)) 
        return True

class LogForm(FlaskForm):
    info = TextField('Info')

    def validate(self):
        check_validate = super(LogForm, self).validate()

        if not check_validate:
            logError('Logs info was wrong.')
            return False
        
        return True     


class ResetPWDForm(FlaskForm):
    username = TextField('Username',[DataRequired()])
    old_pwd = TextField(
       'Old Password',
       validators=[DataRequired(),Length(min=6,max=16)]
    )
    new_pwd = TextField(
       'New Password',
       validators=[DataRequired(),Length(min=6,max=16)]
    )
    confirm_pwd = TextField(
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

        if not self.check_password(user.password, self.old_pwd.data):
            self.old_pwd.errors.append(
                'Incorrect password'
            )
            return False

        return True


    
class ResetNameForm(FlaskForm):
    new_name = TextField(
       'New Username',
       validators=[DataRequired(),Length(min=4,max=16)]
    )

