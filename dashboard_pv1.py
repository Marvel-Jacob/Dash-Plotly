import pandas as pd
import numpy as np
from datetime import datetime
import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import warnings
warnings.filterwarnings("ignore")

def dateparse(date):
	return datetime.strptime(date,"%Y-%m-%d")

def graph_1(data,ae,start_date,end_date):
	data = data[data['AE']==ae]
	if start_date is not None and end_date is not None:
		data = data[data['nDate'].between(dateparse(start_date),dateparse(end_date))]
	data['Avg Productivity'] = np.mean(data['Productivity'])
	nprod70 = data[data['Productivity']>70]['Productivity'].count()
	# data = data[data['nDate'].between(dateparse(start_date),dateparse(end_date))]
	# plot_data = plot_data[plot_data['Month']==month]
	return  {'data':[
		{'x':data['Day'],'y':data['Productivity'],'type':'line','name':'Productivity',
		'text':'Number of time optimum productivity reached is: '+str(nprod70)},
		{'x':data['Day'],'y':data['Avg Productivity'],'type':'line','name':'Average Productivity'}],
		'layout': {'plot_bgcolor':'lightgray','paper_bgcolor':'lightgray','title':'Productivity Chart',
		'font':{'color':'black'}, 'hovermode':'closest','legend':{'x':0,'y':5},
		'xaxis':{'title':'Days -->'},'yaxis':{'title':'Productivity (in %) -->'}}
		}
def graph_2(data,ae,start_date,end_date):
	data = data[data['AE']==ae]
	if start_date is not None and end_date is not None:
		data = data[data['nDate'].between(dateparse(start_date),dateparse(end_date))]
	data['Avg TP'] = np.mean(data['TP'])
	data['Avg TC'] = np.mean(data['TC'])
	return {'data':[
		{'x':data['Day'],'y':data['Avg TC'],'type':'line','name':'Average TC'},
		{'x':data['Day'],'y':data['TC'],'type':'line','name':'TC'},
		{'x':data['Day'],'y':data['TP'],'type':'line','name':'TP'},
		{'x':data['Day'],'y':data['Avg TP'],'type':'line','name':'Average TP'}],
		'layout': {'plot_bgcolor':'lightgray','paper_bgcolor':'lightgray','title':'Metrics Chart','font':{'color':'black'},
		'hovermode':'closest','legend':{'x':0,'y':5},
		'xaxis':{'title':'Days -->'},'yaxis':{'title':'Quantity (in pcs) -->'}}
		}
def graph_3(data,ae,start_date,end_date):
	data = data[data['AE']==ae]
	if start_date is not None and end_date is not None:
		data = data[data['nDate'].between(dateparse(start_date),dateparse(end_date))]
	data['Avg TB'] = np.mean(data['TB'])
	data['Avg TB/PC'] = data['Avg TB']/data['TP']
	return {'data':[
		{'x':data['Day'],'y':data['TB'],'type':'line','name':'TB'},
		{'x':data['Day'],'y':data['Avg TB'],'type':'line','name':'Avg TB'},
		{'x':data['Day'],'y':data['Avg TB/PC'],'type':'line','name':'Avg TB/PC'}],
		'layout': {'plot_bgcolor':'lightgray','paper_bgcolor':'lightgray','title':'TB Chart','font':{'color':'black'},
		'hovermode':'closest','legend':{'x':0,'y':5},
		'xaxis':{'title':'Days -->'},'yaxis':{'title':'Quantity (in pcs) -->'}}
		}
def graph_4(data,ae,date):
	data = data[data['AE']==ae]
	if date is not None:
		data = data[data['nDate']==dateparse(date)]
	return {'data':[
	{'x':data['Day'],'y':data['TC'],'type':'bar','name':'TC'},
	{'x':data['Day'],'y':data['TP'],'type':'bar','name':'TP'},
	{'x':data['Day'],'y':data['Productivity'],'type':'bar','name':'Productivity'}],
	'layout':{'plot_bgcolor':'lightgray','paper_bgcolor':'lightgray','title':"TP/TC/Productivity",'font':{'color':'black'},
	'hovermode':'closest','legend':{'x':0,'y':5},
	'xaxis':{'title':'Days -->'},'yaxis':{'title':'Count / Productivity (in %) -->'}}
	}
def graph_5(data,ae,date):
	data = data[data['AE']==ae]
	if date is not None:
		data = data[data['nDate']==dateparse(date)]
	return {'data':[
	{'x':data['Day'],'y':data['TB'],'type':'bar','name':'TB'}],
	'layout':{'plot_bgcolor':'lightgray','paper_bgcolor':'lightgray','title':"TB",'font':{'color':'black'},
	'hovermode':'closest','legend':{'x':0,'y':5},
	'xaxis':{'title':'Days -->'},'yaxis':{'title':'Quantity (in pcs) -->'}}
	}
def rangeddate(id):
	return dcc.DatePickerRange(
		id = id,
		display_format = "DD/MM/Y",
		min_date_allowed = datetime(2019,12,1),
		max_date_allowed = datetime.now(),
		updatemode = 'bothdates',
		start_date_placeholder_text = "Start Date",
		end_date_placeholder_text = "End Date",
		calendar_orientation = "horizontal")
def singledate(id):
	return dcc.DatePickerSingle(
		id = id,
		display_format = "DD/MM/Y",
		min_date_allowed = datetime(2019,12,1),
		max_date_allowed = datetime.now(),
		placeholder = "Select date",
		calendar_orientation = "horizontal"
		)

executives = pd.read_csv('executives.csv')
filename = 'master.csv'
master_data = pd.read_csv(filename)
master_data.drop_duplicates(inplace = True)
master_data = master_data.reset_index().drop('index',axis=1)
master_data = pd.merge(master_data,executives, on = 'AE')

master_data[['State','DB Name','Store Category','Date','DB District','DB State']] = master_data[['State','DB Name','Store Category','Date','DB District','DB State']].fillna(' ')
master_data[['Day','Qty']] = master_data[['Day','Qty']].fillna(0)
master_data['Qty'] = master_data['Qty'].astype('float64')
master_data['Beat+Store'] = master_data['Beat Name'] + " - " + master_data['Store Name']

ae_data = master_data[['State','AE']].drop_duplicates()
ae_list = {i:[] for i in ae_data['State']}
for i,j in zip(ae_data['State'],ae_data['AE']):
	if j not in ae_list[i]:
		ae_list[i].append(j) 
# print(ae_list)
# pos = 15
# plot_data = master_data[master_data['AE']==ae_list[pos]]

#----------------------------------------To deal with date format-------------------------------
# master_data['Date'] = pd.to_datetime(master_data['Date'], format = "%d/%m/%Y")
# master_data['Date'] = master_data['Date'].apply(lambda x: x.split(' ')[0].strip() if " " in x else x.strip())
# apply(lambda x:datetime.strptime(x,"%d/%m/%Y") if x!=" " else " ") 
# for i in range(len(master_data['Date'])):
# 	print(i)
	# print(str(i) + ' - ' + str(master_data['Date'][i]))
	# print(master_data['Date'][i])
	# print(datetime.strptime(master_data['Date'][i][:10],"%d/%m/%Y"))
	# print(master_data['Date'][i].split('/')[1])
#---------------------------------------------------------------------------------------------

plot_data = master_data[['State', 'DB Name', 'Beat+Store', 'Store Name', 'Store Category',
       'Date', 'Qty', 'Productive Call']]

group_cols = ['State', 'AE','Beat Name','Date','Productive Call']

plot_data = plot_data.groupby(group_cols).agg(
	TB = pd.NamedAgg(column = "Qty", aggfunc = "sum"),
	TC = pd.NamedAgg(column = "Store Name", aggfunc="nunique")).reset_index()

plot_data = pd.pivot_table(plot_data, index = ['State','AE','Beat Name',
	'Date'], columns = 'Productive Call', values = ['TB','TC']).reset_index()

plot_data.columns = [str(i[0]) + str(i[1]) for i in plot_data.columns]
plot_data['TP'], plot_data['TC'], plot_data['TB'] = plot_data['TC1'], plot_data['TC0'] + plot_data['TC1'], plot_data['TB1']
plot_data['Productivity'] = np.round((plot_data['TP'] / plot_data['TC'])*100,2)
plot_data = plot_data.drop(['TB0','TB1','TC0','TC1'], axis = 1)

plot_data['nDate'] = plot_data['Date'].apply(lambda x:datetime.strptime(x[:10],"%d/%m/%Y") if x!=" " else x)
plot_data['Day'] = plot_data['nDate'].apply(lambda x :int(x.day) if x!=" " else 0)
plot_data = plot_data[plot_data['Day']!=0]

# Average calculations used to be here

plot_data = plot_data.sort_values(by='Day', ascending = True)
# plot_data.to_csv('checkmaster.csv', index = False)


app = dash.Dash(__name__,external_stylesheets = [dbc.themes.MATERIA])
server = app.server
app.layout = html.Div([
	html.H1(className = 'header-style', children = "Performance Dashboard"),
	html.Div([
		html.Div([
		dcc.Dropdown(
		id = 'state',
		options = [{'label':i, 'value':i} for i in ae_list.keys()],
		placeholder = "Select State"),
		]),
		html.Div([
		dcc.Dropdown(
		id = 'ae',
		placeholder = "Select AE"),
		]),
		dcc.Tabs(id = "tabs", value = "tab-0", children = [
			dcc.Tab(label='Productivity', value = 'tab-1', children = [rangeddate("dgraph1"),dcc.Graph(id = 'graph1',animate=True)]),
			dcc.Tab(label='TC / TP Charts', value = 'tab-2', children = [rangeddate("dgraph2"),dcc.Graph(id = 'graph2',animate=True)]),
			dcc.Tab(label='TB Charts', value = 'tab-3', children = [rangeddate("dgraph3"),dcc.Graph(id = 'graph3',animate=True)]),
			dcc.Tab(label = 'DayWise Chart', value = 'tab-4', children = [singledate("dgraph4"),
				html.Div([html.Div([dcc.Graph(id = 'graph4')],
					style={'display':'inline-block','width':'48%','align':'left','margin-left':'1%'}),
					html.Div([dcc.Graph(id='graph5')],style={'display':'inline-block','align':'right','width':'48%',
						'margin-left':'2%'})
					])
				]),			
			]),
		html.Div(id = "tab-contents", className='style-tab-contents'),
		],className='container'),
	], className='background')

@app.callback(
	Output('ae','options'),[Input('state','value')])
def get_ae(value):
	if value!=None:
		return [{'label':i,'value':i} for i in ae_list[value]]
	else:
		return [{'label':'Select State first','value':'Nobody'}]

@app.callback(
	[Output('graph1','figure'),Output('graph2','figure'),Output('graph3','figure'),
	Output('graph4','figure'),Output('graph5','figure')],
	[Input('dgraph1','start_date'),Input('dgraph1','end_date'),
	Input('dgraph2','start_date'),Input('dgraph2','end_date'),Input('dgraph3','start_date'),Input('dgraph3','end_date'),
	Input('dgraph4','date'),Input('ae','value')])
def render_graph(g1_startdate,g1_enddate,g2_startdate,g2_enddate,g3_startdate,g3_enddate,g4_date,ae_value):
	return [
	graph_1(data = plot_data, ae = ae_value, start_date = g1_startdate, end_date = g1_enddate),
	graph_2(data = plot_data, ae = ae_value, start_date = g2_startdate, end_date = g2_enddate),
	graph_3(data = plot_data, ae = ae_value, start_date = g3_startdate, end_date = g3_enddate),
	graph_4(data = plot_data, ae = ae_value, date = g4_date),
	graph_5(data = plot_data, ae = ae_value, date = g4_date)
	]

if __name__=='__main__':
	app.run_server(port = 8050, debug = True, dev_tools_ui=False)