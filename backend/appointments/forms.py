from flask_wtf import FlaskForm
from wtforms import SelectField, DateField, TimeField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, Optional

class BookForm(FlaskForm):
    doctor_id = SelectField("Doctor", coerce=int, validators=[DataRequired()])
    date = DateField("Date", validators=[DataRequired()], format="%Y-%m-%d")
    time = TimeField("Time", validators=[DataRequired()], format="%H:%M")
    reason = TextAreaField("Reason", validators=[Optional(), Length(max=255)])
    submit = SubmitField("Book")
