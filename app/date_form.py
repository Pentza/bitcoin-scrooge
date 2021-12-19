from flask_wtf import FlaskForm
from wtforms.fields import DateField, SubmitField
from datetime import datetime

class DateRangeForm(FlaskForm):
    start_date = DateField('Start Date')
    end_date = DateField('End Date')
    submit = SubmitField('Submit')

    # def validate_start_date(form, field):
    #     if field.data > datetime
