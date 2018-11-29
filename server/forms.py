from flask_wtf import Form
from wtforms import StringField, TextAreaField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, URL

class LoginForm(Form):
    username=StringField('Username',[DataRequired(),Length(max=255)])
    password=PasswordField('Password',[DataRequired()])

    def validate(self):
        check_validate = super(LoginForm, self).validate()

        if not check_validate:
            return False

        user=User.query.filter_by(username=self.username).first()
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
    old_pwd = StringField(
       'Old_pwd',
       validators=[DataRequired(),Length(min=6,max=16)]
    )
    new_pwd = StringField(
       'New_pwd',
       validators=[DataRequired(),Length(min=6,max=16)]
    )
    confirm_pwd = StringField(
       'Confirm_pwd',
       validators=[DataRequired(),Length(min=6,max=16)]
    )
    
class ResetNameForm(Form):
    new_name = StringField(
       'New_name',
       validators=[DataRequired(),Length(min=4,max=16)]
    )

