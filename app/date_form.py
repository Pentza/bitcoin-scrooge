from datetime import date
from flask_wtf import FlaskForm
from wtforms.fields import DateField, SubmitField

class DateRangeForm(FlaskForm):
    start_date = DateField('Start Date', default=date.today)
    end_date = DateField('End Date', default=date.today)
    submit = SubmitField('Submit')

    def validate_on_submit(self):
        start = self.start_date.data
        end = self.end_date.data

        if start > end:
            return False

        today = date.today()
        if start > today or end > today:
            return False

        return True
