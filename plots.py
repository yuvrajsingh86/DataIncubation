from flask import Flask, render_template
import random
# imports for Bokeh plotting
from bokeh.plotting import figure
from bokeh.resources import CDN
from bokeh.embed import file_html, components
# imports for matplotlib plotting
import tempfile
import matplotlib
matplotlib.use('Agg') # this allows PNG plotting
import matplotlib.pyplot as plt
app = Flask(__name__)
@app.route('/')
def indexPage():

    api_url = 'https://www.quandl.com/api/v1/datasets/WIKI/%s.json' % stock
    session = requests.Session()
    session.mount('http://', requests.adapters.HTTPAdapter(max_retries=3))
    raw_data = session.get(api_url)
    plot = figure(tools=TOOLS,
                  title='Data from Quandle WIKI set',
                  x_axis_label='date',
                  x_axis_type='datetime')

    script, div = components(plot)
    return render_template('graph.html', script=script, div=div)
