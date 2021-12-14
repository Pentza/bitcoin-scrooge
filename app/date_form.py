from flask_wtf import FlaskForm
from wtforms.fields import DateField

class DateRangeForm(FlaskForm):
    start_date = DateField()
    end_date = DateField()
