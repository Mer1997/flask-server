from flask_wtf import Form,RecaptchaField
from wtforms import StringField, TextAreaField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, URL

class LoginForm(Form):
    username=StringField('Username',[DataRequired(),Length(max=255)])
    password=PasswordField('Password',[DataRequired()])

    def validate(self):
        check_validate = super(LoginForm, self).validate()

        if not check_validate:
            return False

        user=User.query.filter_by(username=self.username.data).first()
        if not user:
            self.username.errors.append(
                'Invalid username or password'
            )

            return False
        
        if not self.user.check_password(self.password.data):
            self.username.errors.append(
                'Invalid username or password'
            )

            return False
        
        return True

class RegisterForm(Form):
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


class ResetPWDForm(Form):
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


    
class ResetNameForm(Form):
    new_name = StringField(
       'New Username',
       validators=[DataRequired(),Length(min=4,max=16)]
    )

