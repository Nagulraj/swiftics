from email.utils import collapse_rfc2231_value
from this import d
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import numpy as np
import pandas as pd
import json
import plotly
import plotly.express as px
import plotly.graph_objects as go
import random

df = pd.DataFrame({})

app = Flask(__name__)

app.config['UPLOAD_FOLDER']	= "static/datasets/"

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/upload")
def upload():
    return render_template('upload.html')

    '''
     file_location = app.config['UPLOAD_FOLDER'] + "id-cards/" 
        file_list = []
        for f in files:
            filename = secure_filename(f.filename.split('.')[0] + '-' + get_timestamp() + '.' + f.filename.split('.')[-1])
            f.save( file_location + filename )
            file_list.append(file_location + filename)
    '''

@app.route("/plot_choose", methods=["POST"])
def plot_choose():
    f = request.files['csv']
    file_location = app.config['UPLOAD_FOLDER']
    if f.filename.split('.')[1] == 'csv':
        f.save(file_location + secure_filename(f.filename))
    else:
        return "<h1>Incorrect File Format</h1>"
    global df
    df = pd.read_csv(file_location+f.filename)
    df = df.dropna(how = "any")

    global csv_location 
    csv_location = file_location+secure_filename(f.filename)
    # print(csv_location)

    return render_template('plot.html', cols=list(df.columns), tables = [df.head().to_html(classes='data')])

@app.route("/plot_choose/<csv>")
def plot_choose_sample(csv):
    global df
    fi = "static/datasets/"+csv+".csv"
    df = pd.read_csv(fi)

    df = df.dropna(how = "any")

    return render_template('plot.html', cols=list(df.columns), tables = [df.head().to_html(classes='data')])

@app.route("/plot", methods=["POST"])
def plot():
    global  df
    x_ax = str(request.form['x_axis']).strip()
    y_ax = str(request.form['y_axis']).strip()
    plot = str(request.form['plot_type']).strip()

    # global col_1
    # global col_2
    # global chart_name
    
    # col_1 = x_ax
    # col_2 = y_ax
    # chart_name = chart

    # if plot == 'scatter':
    #     fig = px.scatter(x = df[x_ax], y = df[y_ax])
    
    # elif plot == 'line':
    #     dff = df.groupby(x_ax)[y_ax].sum().reset_index()
    #     fig = px.scatter(dff, x = x_ax, y = y_ax)
    #     fig.data[0].update(mode='markers+lines')

    # elif plot == 'bar':
    #     dff = df.groupby(x_ax)[y_ax].sum().reset_index()
    #     fig = px.bar(dff, x = x_ax, y = y_ax, color = y_ax)
    
    # elif plot == "sunburst":
    #     fig = px.sunburst(df, path=[x_ax, y_ax])

    # elif plot == "corelation":
    #     fig = px.scatter_matrix(df[[x_ax, y_ax]])

    # elif plot == "table":
    #     if(str(df[x_ax].dtype)=="object" and str(df[y_ax].dtype)=="object"):
            
    #         fig = go.Figure(data=[go.Table(
    #                 header=dict(values=list(df[[x_ax, y_ax]].columns.values),
    #                             line_color='darkslategray',
    #                             fill_color='lightskyblue',
    #                             align='left'),
    #                 cells=dict(values=[df[x_ax], df[y_ax]],
    #                         line_color='darkslategray',
    #                         fill_color='lightcyan',
    #                         align='left'))])
    #     else:
    #         if(str(df[x_ax].dtype)=="object"):

    #             dff = df.groupby(x_ax)[y_ax].sum().reset_index()
    #         else:

    #             dff = df.groupby(y_ax)[x_ax].sum().reset_index()

    #         fig = go.Figure(data=[go.Table(
    #                 header=dict(values=list(dff.columns.values),
    #                             line_color='darkslategray',
    #                             fill_color='lightskyblue',
    #                             align='center'),
    #                 cells=dict(values=[dff[x_ax], dff[y_ax]],
    #                         line_color='darkslategray',
    #                         fill_color='lightcyan',
    #                         align='center'))])

    # fig.write_html(f"{id1}.html", include_plotlyjs="cdn")
    # plotly.offline.plot(fig, filename = f"/static/html/{id1}.html")

    entries_dict={}
    id1 = random.randint(80000000,90000000)
    id1 = str(id1)
    
    # fig.write_html(f"./static/html/{id1}.html", include_plotlyjs="cdn")
    
    # web = "http://127.0.0.1:3000/static/html/"+id1+".html"
    # figure = fig.write_html(f"/static/html/{id}.html", include_plotlyjs="cdn")
    id_entries = {}
    id_entries['csv_location'] = csv_location
    id_entries['col_1'] =  x_ax
    id_entries['col_2'] = y_ax
    id_entries['chart_name'] = plot
    id_entries["web"] = "https://swiftics.herokuapp.com/plot/"+id1
    # id_entries['web'] = web
    # id_entries['web'] = fig_html
    entries_dict[id1] = id_entries 
    
    with open("entries.json") as f:
        data = json.load(f)

    with open("entries.json","w") as of:    
        try:
                
            data ["entries"].append(entries_dict)
        except:
            data = {
                "entries" : [entries_dict]
                }
        json.dump(data,of)


    # graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        
    return render_template('output.html',id  =  id1,link = id_entries['web'] ) 

@app.route("/plot/<id>", methods=["GET"])
def get_plot(id):


    x_ax,y_ax,plot =    read_json(id)  


    if plot == 'scatter':
        fig = px.scatter(x = df[x_ax], y = df[y_ax])
    
    elif plot == 'line':
        dff = df.groupby(x_ax)[y_ax].sum().reset_index()
        fig = px.scatter(dff, x = x_ax, y = y_ax)
        fig.data[0].update(mode='markers+lines')

    elif plot == 'bar':
        dff = df.groupby(x_ax)[y_ax].sum().reset_index()
        fig = px.bar(dff, x = x_ax, y = y_ax, color = y_ax)
    
    elif plot == "sunburst":
        fig = px.sunburst(df, path=[x_ax, y_ax])

    elif plot == "corelation":
        fig = px.scatter_matrix(df[[x_ax, y_ax]])

    elif plot == "table":
        if(str(df[x_ax].dtype)=="object" and str(df[y_ax].dtype)=="object"):
            
            fig = go.Figure(data=[go.Table(
                    header=dict(values=list(df[[x_ax, y_ax]].columns.values),
                                line_color='darkslategray',
                                fill_color='lightskyblue',
                                align='left'),
                    cells=dict(values=[df[x_ax], df[y_ax]],
                            line_color='darkslategray',
                            fill_color='lightcyan',
                            align='left'))])
        else:
            if(str(df[x_ax].dtype)=="object"):

                dff = df.groupby(x_ax)[y_ax].sum().reset_index()
            else:

                dff = df.groupby(y_ax)[x_ax].sum().reset_index()

            fig = go.Figure(data=[go.Table(
                    header=dict(values=list(dff.columns.values),
                                line_color='darkslategray',
                                fill_color='lightskyblue',
                                align='center'),
                    cells=dict(values=[dff[x_ax], dff[y_ax]],
                            line_color='darkslategray',
                            fill_color='lightcyan',
                            align='center'))])

    # fig.write_html(f"{id1}.html", include_plotlyjs="cdn")
    # plotly.offline.plot(fig, filename = f"/static/html/{id1}.html")

    # entries_dict={}
    # id1 = random.randint(80000000,90000000)
    # id1 = str(id1)
    
    # # fig.write_html(f"./static/html/{id1}.html", include_plotlyjs="cdn")
    
    # # web = "http://127.0.0.1:3000/static/html/"+id1+".html"
    # # figure = fig.write_html(f"/static/html/{id}.html", include_plotlyjs="cdn")
    # id_entries = {}
    # id_entries['csv_location'] = csv_location
    # id_entries['col_1'] =  x_ax
    # id_entries['col_2'] = y_ax
    # id_entries['chart_name'] = plot
    # # id_entries['web'] = web
    # # id_entries['web'] = fig_html
    # entries_dict[id1] = id_entries 
    
    # with open("entries.json") as f:
    #     data = json.load(f)

    # with open("entries.json","w") as of:    
    #     try:
                
    #         data ["entries"].append(entries_dict)
    #     except:
    #         data = {
    #             "entries" : [entries_dict]
    #             }
    #     json.dump(data,of)


    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    

    return render_template('output2.html',plot=graphJSON, cols = list(df.columns), tables = [df.head().to_html(classes='data')])

def read_json(id):

    f = open('entries.json')
  

    entries_dict = json.load(f)
  
    


# prresult_dict={}
    entries_dict = entries_dict["entries"]
    for entries in entries_dict:
        for entry in entries:
            if id == entry:
            # x_axis = entry["col_1"]
            # print(entries[entry])
                entry_dict = entries[entry]
                x_axis = entry_dict["col_1"]
                y_axis = entry_dict["col_2"]
                csv_location = entry_dict["csv_location"]
                plot = entry_dict["chart_name"]

    return x_axis,y_axis,plot



if __name__ == "__main__":
    app.run(debug=True, port=3000)
