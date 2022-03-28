#coding=utf-8
import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input

# import datetime as dt
# import pandas as pd
# import pathlib
# import pygsheets

import plotly_express as px

#############################################
# 資料處理
from get_data import get_data

# 座位圖顏色
def SetColor(x):
    if(x == '1'):
        return "#000"
    elif(x == '0'):
        return "#e6e6e6"

ddata = get_data(0)

def plot(ddata):
    fig = px.scatter(ddata,
            x = 'sit_x',
            y = 'sit_y',
            range_x = [-2,14.5],
            range_y = [-2,13.5],
            hover_name = '姓名',
        #    color = 'status',
            # title = 'A區',
            hover_data={
                "sit_x" :False,
                "sit_y":False,
                '座位':ddata.index,
            #    '小組':[ddata['小組']]
            })
    fig.update_layout(
        autosize=False,
        # width=700,
        # height=650,
        yaxis={'visible': False, 'showticklabels': False},
        xaxis={'visible': False, 'showticklabels': False},
        plot_bgcolor='#ffffff' ,# 圖表背景顏色
        # showlegend=False
        )
    fig.update_traces(
        marker={'size': 10,'symbol':'arrow-up','color':list(map(SetColor, ddata['status']))}
    )
    fig.add_layout_image(
        dict(
            source="assets/seat_img.jpg",
            xref="x",
            yref="y",
            x=-6,
            y=16,
            sizex=20*1.414,
            sizey=20,
            sizing="stretch",
            opacity=0.5,
            layer="below")
    )
    return fig

fig = plot(get_data(0))
#############################################
#網頁

app = dash.Dash(__name__,
    external_stylesheets=[dbc.themes.LUX],
    title="seatapp",
    meta_tags=[{'name': 'viewport',
        'content': 'width=device-width, initial-scale=1.0'}])

server = app.server
data = get_data(1)

'''
# Navbar
Navbar = dbc.Navbar([
    dbc.Col(html.Img(src=app.get_asset_url('logo.png'), height="70px")),
    # dbc.NavbarBrand("TNCC", className="navbar-brand"), 
    dbc.NavLink("sheet", href="https://docs.google.com/spreadsheets/xxxxx", className="nav-link active")
    ],
    color = "light",
    light=True
    )
'''

# Card 現場人數
Card_ps = dbc.Card([
    dbc.CardBody([
        html.H5(children = '現場人數', className="card-title text-center"),
        html.H1(dbc.CardLink(id = 'num' ,children = 0
                    ,href = 'https://docs.google.com/spreadsheets/xxxxx'
                    ,external_link = True
                    ,className = "text-primary ")
                    ,className = "p-3 text-center border border-primary font-weight-bold")
      ])
    ])

# Card 準時人數
Card_Ops = dbc.Card([
        dbc.CardBody([
            html.H5(children = '準時人數', className="card-title text-center"),
            html.H1(dbc.Card(id = 'Ops' ,children = 0,className = "p-3 text-primary text-center border border-primary font-weight-bold"))
        ])
    ])

# Card 遲到人數
Card_Lps = dbc.Card([
        dbc.CardBody([
            html.H5(children = '遲到人數', className="card-title text-center"),
            html.H1(dbc.Card(id = 'Lps' ,children = 0,className = "p-3 text-primary text-center border border-primary font-weight-bold"))
        ])
    ])

# Graph_seat
Graph_seat = dbc.Card([
            dcc.Graph(id='seat_graph',figure=fig,config={'displayModeBar':False})
    ],className="align-self-center")

# ListGroup 各小組到場人數
ListGroup_P = dbc.ListGroup(
    id = 'ListGroup_P',
    children=[
    dbc.ListGroupItem(
        children = [g, dbc.Badge(data['小組'].value_counts()[g] , className="badge bg-light")], 
        className="d-flex justify-content-between align-items-center") for g in data['小組'].unique()
])

# Table_list
Table_seat = dash_table.DataTable(
    id='Table_seat',
    columns=[{'name': str(x), 'id': str(x), 'deletable': False, 'renamable': False}for x in data.columns],
    data=data.to_dict('records'),
    # editable=True,
    # row_deletable=True,
    # filter_action="native",
    sort_action="native",  # give user capability to sort columns
    sort_mode="single",  # sort across 'multi' or 'single' columns
    page_action='none',  # render all of the data at once. No paging.
    style_table={'height': '300px', 'overflowY': 'auto'},
    style_cell={'textAlign': 'left', 'minWidth': '50px', 
                'width': '50px', 'maxWidth': '50px',
                'backgroundColor': '#fff',
                'color': '#000'},
    style_header={'backgroundColor': '#fff'},
)


app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            dbc.CardDeck([
                Card_ps,
                Card_Ops,
                Card_Lps
            ],className = "m-3")
        ])
    ],className = "mt-3 border border-primary"),
    html.Br(),
    dbc.Row([
        dbc.Col([
            dbc.Card([ListGroup_P],className="my-3"),
            dbc.Card([Table_seat],className="my-3")
            ],className = "ml-4"
            ),

        dbc.Col([
            html.Div([Graph_seat],className="my-3")
            ],width=8)
    ],className = "border border-primary"
    ),dcc.Interval(id='updates', n_intervals=0, interval=1000*10)
])

@app.callback(
    [Output('seat_graph', 'figure'),
    Output('Table_seat', 'columns'),
    Output('Table_seat', 'data'),
    Output('ListGroup_P','children'),
    Output('num', 'children'),
    Output('Ops','children'),
    Output('Lps','children')],

    Input('updates', 'n_intervals'),
    prevent_initial_call=True
)
def update_graph(n_intervals):
    fig = plot(get_data(0))

    data = get_data(1)
    Table_seat_columns = [{'name': str(x), 'id': str(x), 'deletable': False, 'renamable': False}for x in data.columns]
    Table_seat_data = data.to_dict('records')

    listgroupitem = [dbc.ListGroupItem(
            children = [g, dbc.Badge(data['小組'].value_counts()[g] , className="badge bg-light")], 
            className="d-flex justify-content-between align-items-center") for g in data['小組'].unique()]
    
    if '1' in ddata['status'].value_counts():
        ps = ddata['status'].value_counts()['1']
    else:
        ps = 0

    if 'L' in ddata['p'].value_counts():
        Lps = ddata['p'].value_counts()['L']
    else:
        Lps = 0

    Ops = ps-Lps
    return fig, Table_seat_columns, Table_seat_data, listgroupitem, ps, Ops, Lps



if __name__ == '__main__':
  app.run_server(debug=True)
