from datetime import datetime
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import pandas as pd
from dash.dependencies import Input, Output, State
import io
import base64
import dash_table
import warnings
import plotly.graph_objects as go

warnings.filterwarnings("ignore")


def dateparse(date):
    return datetime.strptime(date, "%Y-%m-%d")


# def parse_df_contents(contents, filename, last_modified):
#     content_type, content_string = contents.split(',')
#     decoded = base64.b64decode(content_string)
#     if 'csv' in filename:
#         df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
#     elif 'xlsx' in filename:
#         df = pd.read_excel(io.StringIO(decoded))
#     else:
#         return html.Div(["There was an error processing the file"])
#     return html.Div([
#         html.H4([datetime.fromtimestamp((last_modified))]),
#         dash_table.DataTable(
#             data=df.to_dict('records'),
#             columns=[{'name': i, 'id': i} for i in df.columns]
#         )
#     ])


def graph_1(data, ae, start_date, end_date):
    data = data[data['AE'] == ae]
    if start_date is not None and end_date is not None:
        data = data[data['nDate'].between(dateparse(start_date), dateparse(end_date))]
    else:
        dt = datetime.now()
        dt = datetime(dt.year, dt.month, dt.day - (dt.day - 1))
        data = data[data['nDate']>=dt]
    data['Avg Productivity'] = np.mean(data['Productivity'])
    nprod70 = data[data['Productivity'] > 70]['Productivity'].count()
    # data = data[data['nDate'].between(dateparse(start_date),dateparse(end_date))]
    # plot_data = plot_data[plot_data['Month']==month]
    return {'data': [
        {'x': data['Day'], 'y': data['Productivity'], 'type': 'line', 'name': 'Productivity',
         'text': 'Number of time optimum productivity reached is: ' + str(nprod70)},
        {'x': data['Day'], 'y': data['Avg Productivity'], 'type': 'line', 'name': 'Average Productivity'}],
        'layout': {'plot_bgcolor': 'white', 'paper_bgcolor': 'whitesmoke', 'title': 'Productivity Chart',
                   'font': {'color': 'black'}, 'hovermode': 'closest', 'legend': {'x': 0, 'y': 5},
                   'xaxis': {'title': 'Days -->'}, 'yaxis': {'title': 'Productivity (in %) -->'},
                   'margin': {'l': 30, 't': 30, 'b': 30, 'r': 20},
                   'textfont': {'color': 'white'}}
    }


def graph_2(data, ae, start_date, end_date):
    data = data[data['AE'] == ae]
    if start_date is not None and end_date is not None:
        data = data[data['nDate'].between(dateparse(start_date), dateparse(end_date))]
    else:
        dt = datetime.now()
        dt = datetime(dt.year, dt.month, dt.day - (dt.day - 1))
        data = data[data['nDate'] >= dt]
    data['Avg TP'] = np.mean(data['TP'])
    data['Avg TC'] = np.mean(data['TC'])
    return {'data': [
        {'x': data['Day'], 'y': data['Avg TC'], 'type': 'line', 'name': 'Average TC'},
        {'x': data['Day'], 'y': data['TC'], 'type': 'line', 'name': 'TC'},
        {'x': data['Day'], 'y': data['TP'], 'type': 'line', 'name': 'TP'},
        {'x': data['Day'], 'y': data['Avg TP'], 'type': 'line', 'name': 'Average TP'}],
        'layout': {'plot_bgcolor': 'white', 'paper_bgcolor': 'whitesmoke', 'title': 'Metrics Chart',
                   'font': {'color': 'black'},
                   'hovermode': 'closest', 'legend': {'x': 0, 'y': 5},
                   'xaxis': {'title': 'Days -->'}, 'yaxis': {'title': 'Quantity (in pcs) -->'},
                   'margin': {'l': 30, 't': 30, 'b': 30, 'r': 20}}
    }


def graph_3(data, ae, start_date, end_date):
    data = data[data['AE'] == ae]
    if start_date is not None and end_date is not None:
        data = data[data['nDate'].between(dateparse(start_date), dateparse(end_date))]
    else:
        dt = datetime.now()
        dt = datetime(dt.year, dt.month, dt.day - (dt.day - 1))
        data = data[data['nDate'] >= dt]
    data['Avg TB'] = np.mean(data['TB'])
    data['Avg TB/PC'] = data['Avg TB'] / data['TP']
    return {'data': [
        {'x': data['Day'], 'y': data['TB'], 'type': 'line', 'name': 'TB'},
        {'x': data['Day'], 'y': data['Avg TB'], 'type': 'line', 'name': 'Avg TB'},
        {'x': data['Day'], 'y': data['Avg TB/PC'], 'type': 'line', 'name': 'Avg TB/PC'}],
        'layout': {'plot_bgcolor': 'white', 'paper_bgcolor': 'whitesmoke', 'title': 'TB Chart',
                   'font': {'color': 'black'},
                   'hovermode': 'closest', 'legend': {'x': 0, 'y': 5},
                   'xaxis': {'title': 'Days -->'}, 'yaxis': {'title': 'Quantity (in pcs) -->'},
                   'margin': {'l': 30, 't': 30, 'b': 30, 'r': 20}}
    }


def graph_4(data, ae, date):
    data = data[data['AE'] == ae]
    if date is not None:
        data = data[data['nDate'] == dateparse(date)]
    else:
        dt = datetime.now()
        dt = datetime(dt.year, dt.month, dt.day - (dt.day - 1))
        data = data[data['nDate'] >= dt]
    return {'data': [
        {'x': data['Day'], 'y': data['TC'], 'type': 'bar', 'name': 'TC'},
        {'x': data['Day'], 'y': data['TP'], 'type': 'bar', 'name': 'TP'},
        {'x': data['Day'], 'y': data['Productivity'], 'type': 'line', 'name': 'Productivity',
         'line': {'color': 'green'}}],
        'layout': {'plot_bgcolor': 'white', 'paper_bgcolor': 'whitesmoke', 'title': "TP/TC/Productivity",
                   'font': {'color': 'black'},
                   'hovermode': 'closest', 'legend': {'x': 0, 'y': 5},
                   'xaxis': {'title': 'Days -->'}, 'yaxis': {'title': 'Count / Productivity (in %) -->'},
                   'margin': {'l': 30, 't': 30, 'b': 30, 'r': 20}}
    }


def graph_5(data, ae, date):
    data = data[data['AE'] == ae]
    if date is not None:
        data = data[data['nDate'] == dateparse(date)]
    else:
        dt = datetime.now()
        dt = datetime(dt.year, dt.month, dt.day - (dt.day - 1))
        data = data[data['nDate'] >= dt]
    return {'data': [
        {'x': data['Day'], 'y': data['TB'], 'type': 'bar', 'name': 'TB'}],
        'layout': {'plot_bgcolor': 'white', 'paper_bgcolor': 'whitesmoke', 'title': "TB", 'font': {'color': 'black'},
                   'hovermode': 'closest', 'legend': {'x': 0, 'y': 5},
                   'xaxis': {'title': 'Days -->'}, 'yaxis': {'title': 'Quantity (in pcs) -->'},
                   'margin': {'l': 30, 't': 30, 'b': 30, 'r': 20}}
    }


def graph_6(data, ae):
    data = data[data['AE'] == ae]
    data['Beat Name'] = data['Beat Name'].apply(lambda x: x[:23])
    labels = data['Beat Name']
    values = data['Date']
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.5)])
    fig.update_layout(margin={'l': 5, 'r': 5, 't': 5, 'b': 5, 'pad': 2}, paper_bgcolor='whitesmoke',
                      legend={'font': {'color': 'black'}})
    return fig


def rangeddate(id):
    return dcc.DatePickerRange(
        id=id,
        display_format="DD/MM/Y",
        min_date_allowed=datetime(2020, 5, 1),
        max_date_allowed=datetime.now(),
        updatemode='bothdates',
        start_date_placeholder_text="Start Date",
        end_date_placeholder_text="End Date",
        calendar_orientation="horizontal")


def singledate(id):
    return dcc.DatePickerSingle(
        id=id,
        display_format="DD/MM/Y",
        min_date_allowed=datetime(2020, 5, 1),
        max_date_allowed=datetime.now(),
        placeholder="Select date",
        calendar_orientation="horizontal"
    )


def render_cards(card1, card2, card3, card4):
    return [
        html.Div([
            html.H4(id="card1-header", children=['Total number of stores']),
            html.H2(id=card1)
        ], className="style-card1"),
        html.Div([
            html.H4(id="card2-header", children=['Total Beats']),
            html.H2(id=card2)
        ], className="style-card2"),
        html.Div([
            html.H4(id="card3-header", children=["Total DB's"]),
            html.H2(id=card3)
        ], className="style-card3"),
        html.Div([
            html.H4(id="card4-header", children=['Total Orders']),
            html.H2(id=card4)
        ], className="style-card4"),
    ]


executives = pd.read_csv('executives.csv')
try:
    file_url = "https://docs.google.com/spreadsheets/d/e/2PACX-fs1hWXcZ_GRwyB-P1OBarCC_Ry/pub?gid=151&single=true&output=csv" #dummy url
    master_data = pd.read_csv(file_url)
except:
    print('Reading from local storage')
    filename = 'sales_master.csv'
    master_data = pd.read_csv(filename)

master_data.drop_duplicates(inplace=True)
master_data = master_data.reset_index().drop('index', axis=1)
master_data = pd.merge(master_data, executives, on='AE')
master_data[['State', 'DB Name', 'Store Category', 'Date', 'DB District', 'DB State']] = master_data[
    ['State', 'DB Name', 'Store Category', 'Date', 'DB District', 'DB State']].fillna(' ')
master_data[['Day', 'Qty']] = master_data[['Day', 'Qty']].fillna(0)
master_data['Qty'] = master_data['Qty'].apply(lambda x: int(x))
master_data['Beat+Store'] = master_data['Beat Name'] + " - " + master_data['Store Name']

ae_data = master_data[['State', 'AE']].drop_duplicates().sort_values(by='State', ascending=True)
ae_list = {i: [] for i in ae_data['State']}
for i, j in zip(ae_data['State'], ae_data['AE']):
    if j not in ae_list[i]:
        ae_list[i].append(j)
    ae_list[i].sort()

# ----------------------------------------To deal with date format-------------------------------
# master_data['Date'] = pd.to_datetime(master_data['Date'], format = "%d/%m/%Y")
# master_data['Date'] = master_data['Date'].apply(lambda x: x.split(' ')[0].strip() if " " in x else x.strip())
# apply(lambda x:datetime.strptime(x,"%d/%m/%Y") if x!=" " else " ")
# for i in range(len(master_data['Date'])):
# 	print(i)
# print(str(i) + ' - ' + str(master_data['Date'][i]))
# print(master_data['Date'][i])
# print(datetime.strptime(master_data['Date'][i][:10],"%d/%m/%Y"))
# print(master_data['Date'][i].split('/')[1])
# ---------------------------------------------------------------------------------------------

plot_data = master_data[['State', 'AE', 'Beat Name', 'DB Name', 'Beat+Store', 'Store Name', 'Store Category',
                         'Date', 'Qty', 'Productive Call']]

group_cols = ['State', 'AE', 'Beat Name', 'Date', 'Productive Call']

plot_data = plot_data.groupby(group_cols).agg(
    TB=pd.NamedAgg(column="Qty", aggfunc="sum"),
    TC=pd.NamedAgg(column="Store Name", aggfunc="nunique")).reset_index()

plot_data = pd.pivot_table(plot_data, index=['State', 'AE', 'Beat Name',
                                             'Date'], columns='Productive Call', values=['TB', 'TC']).reset_index()

plot_data.columns = [str(i[0]) + str(i[1]) for i in plot_data.columns]
plot_data[['TC0', 'TC1']] = plot_data[['TC0', 'TC1']].fillna(0)
plot_data['TP'], plot_data['TC'], plot_data['TB'] = plot_data['TC1'], plot_data['TC0'] + plot_data['TC1'], plot_data[
    'TB1']

plot_data['Productivity'] = np.round((plot_data['TP'] / plot_data['TC']) * 100, 2)
plot_data = plot_data.drop(['TB0', 'TB1', 'TC0', 'TC1'], axis=1)

plot_data['nDate'] = plot_data['Date'].apply(lambda x: datetime.strptime(x[:10], "%d/%m/%Y") if x != " " else x)
plot_data['Day'] = plot_data['nDate'].apply(lambda x: int(x.day) if x != " " else 0)
plot_data = plot_data[plot_data['Day'] != 0]

plot_data = plot_data.sort_values(by='Day', ascending=True)
# plot_data.to_csv('../checkmaster.csv', index=False)

donut_data = plot_data[['State', 'AE', 'Beat Name', 'Date']]
donut_data = donut_data.groupby(['State', 'AE', 'Beat Name']).count().reset_index()

dsr_dashboard_layout = html.Div([
    html.Div([
        html.Div([
            html.H1(id="header", children="AE Performance Dashboard", className="header-style"),
            html.Div([
                # html.Div([
                #     dcc.Upload(
                #         id="upload-data",
                #         className="upload-template",
                #         children=html.Div(['Drag & Drop file or ', html.A('Select Files')]),
                #     ),
                # ]),
                html.Div([
                    dcc.Dropdown(
                        id='state',
                        options=[{'label': i, 'value': i} for i in ae_list.keys()],
                        placeholder="Select State"),
                ], className="style-state-dropdown"),
                html.Div([
                    dcc.Dropdown(
                        id='ae',
                        placeholder="Select AE"),
                ], className="style-ae-dropdown"),
                html.A('Click here to go to data', href='/dsr-dashboard/datatable', id='tablelink')
            ], className="style-dropdown-layout"),
        ], className="left-side-layout"),
        html.Div([
            html.Div([
                html.Div(
                    render_cards(card1="card1_value", card2="card2_value",
                                 card3="card3_value", card4="card4_value"), className="style-card-layout"
                ),
                html.Div([
                    dcc.Graph(id="graph6", className='style-g6', config={'autosizable': True})
                ])
            ], className="right-upper-layout"
            ),
            html.Hr(),
            html.Div([
                dcc.Tabs(id="tabs", value="tab-0", className="main-tab",
                         children=[
                             dcc.Tab(label='Productivity', value='tab-1', className="tab-style",
                                     selected_className="stab-style",
                                     children=[
                                         html.Div([rangeddate("dgraph1")], className="style-date-graph1"),
                                         html.Div([dcc.Graph(id='graph1', animate=True)], className="style-graph1")
                                     ]),
                             dcc.Tab(label='TC / TP Charts', value='tab-2', className="tab-style",
                                     selected_className="stab-style",
                                     children=[
                                         html.Div([rangeddate("dgraph2")], className="style-date-graph2"),
                                         html.Div([dcc.Graph(id='graph2', animate=True)], className="style-graph2")
                                     ]),
                             dcc.Tab(label='TB Charts', value='tab-3', className="tab-style",
                                     selected_className="stab-style",
                                     children=[
                                         html.Div([rangeddate("dgraph3")], className="style-date-graph3"),
                                         html.Div([dcc.Graph(id='graph3', animate=True)], className="style-graph3")
                                     ]),
                             dcc.Tab(label='DayWise Chart', value='tab-4', className="tab-style",
                                     selected_className="stab-style",
                                     children=[html.Div([
                                         singledate("dgraph4")], className="style-date-g4-g5"),
                                         html.Div([
                                             html.Div([dcc.Graph(id='graph4')], className="style-g4"),
                                             html.Div([dcc.Graph(id='graph5')], className="style-g5")
                                         ], className="style-g4-g5")
                                     ]
                                     ),
                         ], vertical=True)
            ], className="right-middle-layout"),
        ], className="right-side-layout"),
        # html.Div([
        #     html.H2('Under construction')
        # ], className="right-lower-layout")
    ], className="main-layout"),
], className="main-page")

display_data = plot_data[['State','AE','Beat Name','Date','TC','TP','TB','Productivity']]
table_layout = html.Div([
    html.H2('Data Table', className="datatable-header"),
    dash_table.DataTable(
        id = 'table',
        data = display_data.to_dict('records'),
        columns=[{'name': i, 'id': i} for i in display_data.columns],
        filter_action='native',
        sort_action='native',
        style_cell={
            'height':'auto',
            'whiteSpace':'normal',
            'lineHeight':'15px',
            'width':'100px'
        }
    )
])

index_page = html.Div([
    html.H4('Index Page'),
    dcc.Link('DSR Dashboard', id='dsr', href="/dsr-dashboard"),
    html.Br(),
    dcc.Link('Logistics Dashboard', id='log', href="/logistics-dashboard")
])

logistics_dashboard_layout = html.Div([
    html.H4('Page under construction')
])

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.MATERIA])
server = app.server
# app.layout = html.Div([
#     dcc.Location(id="url", refresh=False),
#     html.Div(id="page-content")
# ])
app.layout = dsr_dashboard_layout


@app.callback(Output('page-content', 'children'), [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/dsr-dashboard':
        return dsr_dashboard_layout
    elif pathname == '/logistics-dashboard':
        return logistics_dashboard_layout
    elif pathname == '/dsr-dashboard/datatable':
        return table_layout
    else:
        return index_page


@app.callback(
    [Output('card1_value', 'children'), Output('card2_value', 'children'), Output('card3_value', 'children'),
     Output('card4_value', 'children')],
    [Input('ae', 'value')]
)
def change_card_value(ae):
    data = master_data[master_data['AE'] == ae]
    return [
        len(set(data['Store Name'])),
        len(set(data['Beat Name'])),
        len(set(data['DB Name'])),
        sum(data['Qty'])
    ]


@app.callback(
    Output('ae', 'options'), [Input('state', 'value')])
def get_ae(value):
    if value != None:
        return [{'label': i, 'value': i} for i in ae_list[value]]
    else:
        return [{'label': 'Select State first', 'value': 'Nobody'}]


@app.callback(
    [Output('graph1', 'figure'), Output('graph2', 'figure'), Output('graph3', 'figure'),
     Output('graph4', 'figure'), Output('graph5', 'figure'), Output('graph6', 'figure')],
    [Input('dgraph1', 'start_date'), Input('dgraph1', 'end_date'),
     Input('dgraph2', 'start_date'), Input('dgraph2', 'end_date'), Input('dgraph3', 'start_date'),
     Input('dgraph3', 'end_date'),
     Input('dgraph4', 'date'), Input('ae', 'value')])
def render_graph(g1_startdate, g1_enddate, g2_startdate, g2_enddate, g3_startdate, g3_enddate, g4_date, ae_value):
    return [
        graph_1(data=plot_data, ae=ae_value, start_date=g1_startdate, end_date=g1_enddate),
        graph_2(data=plot_data, ae=ae_value, start_date=g2_startdate, end_date=g2_enddate),
        graph_3(data=plot_data, ae=ae_value, start_date=g3_startdate, end_date=g3_enddate),
        graph_4(data=plot_data, ae=ae_value, date=g4_date),
        graph_5(data=plot_data, ae=ae_value, date=g4_date),
        graph_6(data=donut_data, ae=ae_value)
    ]


if __name__ == '__main__':
    app.run_server(port=8050, debug=True, dev_tools_ui=False)
