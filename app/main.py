from flask import Blueprint, render_template
from .date_form import DateRangeForm

main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'])
def index():
    date_form = DateRangeForm()

    return render_template('index.html', date_form=date_form)
