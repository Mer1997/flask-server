from flask_wtf import Form
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Length

class PasswordForm(Form):
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
    
class UsernameForm(Form):
    new_name = StringField(
       'New_name',
       validators=[DataRequired(),Length(min=4,max=16)]
    )

