from flask import render_template
from . import public


# index
@public.route('/')
def index():
    return render_template('public/index.html')
