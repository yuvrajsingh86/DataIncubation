from flask import Flask, render_template
import pandas as pd
from datetime import date
from bokeh.plotting import figure
from bokeh.charts import Bar, output_file, show,output_notebook,Line
from pandas.tseries.offsets import *
from bokeh.embed import file_html, components
from bokeh.models import HoverTool, BoxSelectTool
from bokeh.plotting import figure, ColumnDataSource
from collections import OrderedDict
from bokeh._legacy_charts import Horizon, TimeSeries
from bokeh.models import BoxAnnotation


startDate=(date.today() - DateOffset(months=1)).strftime('%Y-%m-%d')
endDate=date.today().strftime('%Y-%m-%d')
df1= pd.read_csv('https://www.quandl.com/api/v3/datasets/WIKI/FB.csv?api_key=D3ofFdxSzyPA7ZUz1h6n&start_date='+startDate+'&end_date='+endDate,parse_dates=["Date"])
df2=pd.read_csv('https://www.quandl.com/api/v3/datasets/WIKI/IBM.csv?api_key=D3ofFdxSzyPA7ZUz1h6n&start_date='+startDate+'&end_date='+endDate,parse_dates=["Date"])
df3= pd.read_csv('https://www.quandl.com/api/v3/datasets/WIKI/MSFT.csv?api_key=D3ofFdxSzyPA7ZUz1h6n&start_date='+startDate+'&end_date='+endDate,parse_dates=["Date"])
df4=pd.read_csv('https://www.quandl.com/api/v3/datasets/WIKI/AAPL.csv?api_key=D3ofFdxSzyPA7ZUz1h6n&start_date='+startDate+'&end_date='+endDate,parse_dates=["Date"])
df1["Average"]=df1[['Open','High','Low','Close']].mean(axis=1).astype(float).values
df2["Average"]=df2[['Open','High','Low','Close']].mean(axis=1).astype(float).values
df3["Average"]=df3[['Open','High','Low','Close']].mean(axis=1).astype(float).values
df4["Average"]=df4[['Open','High','Low','Close']].mean(axis=1).astype(float).values
df1['Volitility']=(df1['Average'] - df1['Average'].shift()).fillna(0)
df2['Volitility']=(df2['Average'] - df2['Average'].shift()).fillna(0)
df3['Volitility']=(df3['Average'] - df3['Average'].shift()).fillna(0)
df4['Volitility']=(df4['Average'] - df4['Average'].shift()).fillna(0)

app = Flask(__name__)
@app.route('/')
def indexPage():


    hover = HoverTool(
        tooltips=[

            ("Price", "$y")

        ]
    )


    p = figure(plot_width=1000, plot_height=400,x_axis_type="datetime", tools=[hover],title="Stock Price")
    p.outline_line_width = 7
    p.outline_line_alpha = 0.3
    p.outline_line_color = "navy"
    p.xaxis.axis_label = "Date"
    p.yaxis.axis_label = "Price"
    data=ColumnDataSource(df1)

    p.line('Date','Open',
       line_color="gray", line_width=1, legend="Open",source=data)
    p.circle('Date', 'Open', size=5,color="gray", alpha=0.5,source=data)

    p.line('Date', 'High',
       line_color="green", line_width=1, legend="High",source=data)
    p.circle('Date', 'High', size=5,color="green", alpha=0.5,source=data)

    p.line('Date', 'Low',
       line_color="red", line_width=1, legend="Low",source=data)
    p.circle('Date', 'Low', size=5,color="red", alpha=0.5,source=data)

    p.line('Date', 'Close',
       line_color="black", line_width=1, legend="Close",source=data)
    p.circle('Date', 'Close', size=5,color="black", alpha=0.5,source=data)
    p.legend.orientation = "top_left"

    script1, div1 = components(p)

    q = figure(width=800, height=400, x_axis_type="datetime")
    q.line(df1['Date'], df1['Volitility'], color='red',  legend="Facebook")
    q.legend.orientation = "top_left"

    low_box = BoxAnnotation(plot=q, top=-2, fill_alpha=0.1, fill_color='red')
    mid_box = BoxAnnotation(plot=q, bottom=-2, top=2, fill_alpha=0.1, fill_color='green')
    high_box = BoxAnnotation(plot=q, bottom=2, fill_alpha=0.1, fill_color='red')

    q.renderers.extend([low_box, mid_box, high_box])

    q.title = "Volatility in last month"
    q.xgrid[0].grid_line_color=None
    q.ygrid[0].grid_line_alpha=0.5
    q.xaxis.axis_label = 'Date'
    q.yaxis.axis_label = 'Value'

    xyvalues = OrderedDict(
    Close=df1['Close'],
    Date=df1['Date'],
    Open=df1['Open'],
    Average=df1['Average'],
    )

    # later, we build a dict containing the grouped data
    hp = Horizon(
        xyvalues, index='Date',
        title="horizon plot using stock inputs",
        width=800, height=300
    )
    script1, div1 = components(p)
    script2, div2 = components(q)

    return render_template('graph.html', script1=script1, div1=div1,script2=script2, div2=div2)

@app.route('/comparison')
def login():
    hover2 = HoverTool(
    tooltips=[

        ("Volatility", "$y")

    ]
    )

    xyvalues = OrderedDict(
    Date=df1['Date'],
    FaceBook = df1['Close'],
    Apple=df4['Close'],
    MSFT=df3['Close'],
    IBM=df2['Close'],
    )

    t = TimeSeries(
        xyvalues, width=800,height=800,index='Date', legend=True,
        title="Comparison of Stocks", ylabel='Prices')


    r = figure(width=800, height=400, x_axis_type="datetime",tools=[hover2])
    r.line(df1['Date'], df1['Volitility'], color='red',  legend="Facebook")
    r.line(df2['Date'], df2['Volitility'], color='blue', legend="IBM")
    r.line(df3['Date'], df3['Volitility'], color='brown', legend="MicroSoft")
    r.line(df4['Date'], df4['Volitility'], color='green', legend="Apple")
    r.legend.orientation = "top_left"

    low_box = BoxAnnotation(plot=r, top=-2, fill_alpha=0.1, fill_color='red')
    mid_box = BoxAnnotation(plot=r, bottom=-2, top=2, fill_alpha=0.1, fill_color='green')
    high_box = BoxAnnotation(plot=r, bottom=2, fill_alpha=0.1, fill_color='red')

    r.renderers.extend([low_box, mid_box, high_box])

    r.title = "Volatility in last month"
    r.xgrid[0].grid_line_color=None
    r.ygrid[0].grid_line_alpha=0.5
    r.xaxis.axis_label = 'Date'
    r.yaxis.axis_label = 'Value'

    script3, div3 = components(t)
    script4, div4 = components(r)
    return render_template('compare.html', script3=script3, div3=div3,script4=script4, div4=div4)



if __name__ == '__main__':
     app.debug = True
     app.run(port=33507)
