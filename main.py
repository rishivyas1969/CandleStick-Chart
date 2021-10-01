from flask import Flask, render_template

app=Flask(__name__)

@app.route('/')
def home():

    from pandas_datareader import data
    import datetime
    from bokeh.plotting import figure, show, output_file
    from bokeh.embed import components
    from bokeh.resources import CDN

    start = datetime.datetime.today() - datetime.timedelta(int(365/2))
    end = datetime.datetime.today()

    df = data.DataReader(name='APPL', data_source='yahoo', start=start, end=end)

    def inc_dec(o, c):
        if c>o:
            value='Increased'
        elif c<o:
            value='Decreased'
        else:
            value='Equal'
        return value

    df['Status'] = [inc_dec(o, c) for o, c in zip(df.Open, df.Close)]
    df['Middle'] = (df.Open+df.Close)/2
    df['Height'] = abs(df.Open-df.Close)

    p = figure(x_axis_type='datetime', width=1600, height=600, sizing_mode='scale_width')
    p.title.text = 'CandleStick Chart'
    p.grid.grid_line_alpha = 0.3

    hours_12 = 12*60*60*1000

    p.segment(df.index, df.High, df.index, df.Low, color='black')

    p.rect(df.index[df.Status=='Increased'], df.Middle[df.Status=='Increased'],
        hours_12, df.Height[df.Status=='Increased'], fill_color='green', line_color='black')

    p.rect(df.index[df.Status=='Decreased'], df.Middle[df.Status=='Decreased'],
        hours_12, df.Height[df.Status=='Decreased'], fill_color='red', line_color='black')

    script, div = components(p)
    cdn_js = CDN.js_files[0]

    return render_template("home.html", script=script, div=div, cdn_js=cdn_js)

@app.route('/about/')
def about():
    return render_template("about.html")

if __name__ == '__main__':
    app.run(debug=True)