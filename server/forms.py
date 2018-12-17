import logging
from flask_wtf import FlaskForm,RecaptchaField
from wtforms import TextField, SubmitField, TextAreaField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, URL
from server.models import db,Log,User

def logError(message):
    logging.error(message)

class LoginForm(FlaskForm):
    username=TextField('Username',[DataRequired()])
    password=PasswordField('Password',[DataRequired()])

    def validate(self):
        
        check_validate = super(LoginForm, self).validate()

        if not check_validate:
            return False
        logging.info('username is %s'%(self.username))
        user=User.query.filter_by(username=self.username.data).first()
        if not user:
            logging.info('username %s: Invalid username or password'%self.username.data)
            self.username.errors.append('Invalid username or password')

            return False
        
        if not user.checkPassword(self.password.data):
            logging.info('password %s:Invalid username or password'%self.password.data)
            self.password.errors.append('Invalid username or password')

            return False
        
        return True

class RegisterForm(FlaskForm):
    username = TextField('Username',[DataRequired(),Length(min=4,max=20)])
    password = PasswordField('Password',[DataRequired(),Length(min=6,max=16)])
    confirm = PasswordField('Confirm Password',[DataRequired(),EqualTo('password')])

    recaptcha = RecaptchaField('Recaptcha')

    def validate(self):
        check_validate = super(RegisterForm, self).validate()
        logging.info('%s - %s - %s'%(self.username.data, self.password.data, self.confirm.data))
        if not check_validate:
            logging.info('Form: validate was false')
            return False

        user = User.query.filter_by(username = self.username.data).first()

        if user:
            logError('Username %s: User with that name already exists'%self.username)
            self.username.errors.append(
                "User with that name already exists"
            )
            return False
        logging.info('rigister successful: username :%s, password :%s'%(self.username.data, self.password.data)) 
        return True

class LogForm(FlaskForm):
    info = TextField('Info')

    def validate(self):
        check_validate = super(LogForm, self).validate()

        if not check_validate:
            logging.info('Logs info was wrong.')
            return False
        
        return True     


class ResetPWDForm(FlaskForm):
    old_pwd = TextField('Old Password',[DataRequired(),Length(min=6,max=16)])
    new_pwd = TextField('New Password',[DataRequired(),Length(min=6,max=16)])
    confirm_pwd = TextField('Confirm Password',[DataRequired(),EqualTo('new_pwd')])
    def validate(self):
        check_validate = super(ResetPWDForm, self).validate()

        if not check_validate:
        
            self.old_pwd.errors.append('Invalid data.')
            return False

        return True


    
class ResetNameForm(FlaskForm):
    new_name = TextField('New Username',[DataRequired(),Length(min=2,max=16)])
    def validate(self):
        check_validate = super(ResetNameForm,self).validate()

        if not check_validate:
            self.new_name.errors.append('Invalid data.')
            return False
        return True
