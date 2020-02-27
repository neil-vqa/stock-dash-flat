import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objects as do
from plotly.subplots import make_subplots
from dash.dependencies import Input, Output
from data import data_parse
from datetime import datetime
from pytz import timezone


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])
app.title='Market Movers of the Day'
server = app.server

navbar = dbc.NavbarSimple(
	[
        dbc.NavItem(id='date_current', style={'marginTop':8,'color':'#FFFFFF'}),
        dbc.DropdownMenu(
            nav=True,
            in_navbar=True,
            label="Data Sources",
            children=[
                dbc.DropdownMenuItem("Yahoo! Finance", href='https://finance.yahoo.com/'),
                dbc.DropdownMenuItem("IEX Cloud", href='https://iexcloud.io/'),
                dbc.DropdownMenuItem(divider=True),
                dbc.DropdownMenuItem("Developer: nvqa", href='https://neil-vqa.github.io/data-viz/'),
            ],
        ),
    ],
    brand="MARKET MOVERS",
    brand_style={'color':'#FFFFFF','fontSize':25},
    sticky="top",
    color="primary",
    dark=True
)


body = dbc.Container(
		[
        	dbc.Row([
        		dbc.Col(html.H5("Top 3 Gainers of the Day"),md=9),
        		dbc.Col(dbc.Button("Refresh Dashboard", id="refresh-button", color="primary"),md=2)
        		], align="center", justify="between"),
        	dbc.Row([
        		dbc.Col(html.Div(dcc.Graph(id="plot1")),lg=4),
        		dbc.Col(html.Div(dcc.Graph(id="plot2")),lg=4),
        		dbc.Col(html.Div(dcc.Graph(id="plot3")),lg=4)
        	], className="mt-3", no_gutters=True),
        	dbc.Row([
               dbc.Col(html.Div(dcc.Graph(id="plot4")),md=6),
               dbc.Col([
               	dbc.Row(dbc.Col(html.Div(dcc.Graph(id="plot5"))),className="mt-3"),
               	dbc.Row(dbc.Col(html.Div(dcc.Graph(id="plot6"))),className="mt-3")
               ],md=6)
          ], className="mt-3", no_gutters=True, align="center"),
          dbc.Row([
        		dbc.Col(html.H5("Top 3 Losers of the Day"))], className="mt-5"),
          dbc.Row([
        		dbc.Col(html.Div(dcc.Graph(id="plotA")),lg=4),
        		dbc.Col(html.Div(dcc.Graph(id="plotB")),lg=4),
        		dbc.Col(html.Div(dcc.Graph(id="plotC")),lg=4)
        ], className="mt-2", no_gutters=True),
        dbc.Row([
        		dbc.Col(html.H5("Top 3 Most Active of the Day"))], className="mt-4"),
          dbc.Row([
        		dbc.Col(html.Div(dcc.Graph(id="plotX")),lg=4),
        		dbc.Col(html.Div(dcc.Graph(id="plotY")),lg=4),
        		dbc.Col(html.Div(dcc.Graph(id="plotZ")),lg=4)
        ], className="mt-2", no_gutters=True),
        dbc.Row([
        		dbc.Col(html.H6("nvqa.business@gmail.com | Please contact the developer for any concerns."))], className="mt-5")
        ], fluid=False, className="mt-4")
        

app.layout = html.Div([navbar, body])

@app.callback(
	[Output('plot1','figure'),
	Output('plot2','figure'),
	Output('plot3','figure'),
	Output('plot4','figure'),
	Output('plot5','figure'),
	Output('plot6','figure'),
	Output('plotA','figure'),
	Output('plotB','figure'),
	Output('plotC','figure'),
	Output('plotX','figure'),
	Output('plotY','figure'),
	Output('plotZ','figure'),
	Output('date_current','children')],
	[Input('refresh-button','n_clicks')]
)
def update_charts(n_clicks):
	data,datax,datay,data1,data2,data3,symbol = data_parse()
	
	tz = timezone('EST')
	date= datetime.now(tz)
	date_read = str(date)[:19] 
	date_now = "Trading as of {} Eastern Standard Time |".format(date_read)

	plot1 = do.Figure(do.Indicator(
			mode= 'number+delta',
			value= data[0]['latestPrice'],
			delta= {'reference': data[0]['previousClose'], 'relative': True},
			title = {"text": "<span style='font-size:0.95em;color:black'>{} | {}</span><br><span style='font-size:0.7em;color:gray'>{}</span>".format(data[0]['companyName'],symbol[0],data[0]['primaryExchange'])}
		)
	)
		
	plot2 = do.Figure(do.Indicator(
			mode= 'number+delta',
			value= data[1]['latestPrice'],
			delta= {'reference': data[1]['previousClose'], 'relative': True},
			title = {"text": "<span style='font-size:0.95em;color:black'>{} | {}</span><br><span style='font-size:0.7em;color:gray'>{}</span>".format(data[1]['companyName'],symbol[1],data[1]['primaryExchange'])}
		)
	)

	plot3 = do.Figure(do.Indicator(
			mode= 'number+delta',
			value= data[2]['latestPrice'],
			delta= {'reference': data[2]['previousClose'], 'relative': True},
			title = {"text": "<span style='font-size:0.95em;color:black'>{} | {}</span><br><span style='font-size:0.7em;color:gray'>{}</span>".format(data[2]['companyName'],symbol[2],data[2]['primaryExchange'])}
		)
	)

	plot1.update_layout(margin= do.layout.Margin(t=60,b=0), plot_bgcolor='#EAEAEA', paper_bgcolor='#F2F2F2', height=240)
	plot2.update_layout(margin= do.layout.Margin(t=60,b=0), plot_bgcolor='#EAEAEA', paper_bgcolor='#F2F2F2', height=240)
	plot3.update_layout(margin= do.layout.Margin(t=60,b=0), plot_bgcolor='#EAEAEA', paper_bgcolor='#F2F2F2', height=240)

	plot4 = do.Figure(do.Scatter(
			x= data1.index,
			y= data1['Close'],
			name='Close',
			fill='tozeroy',
			mode='lines',
			marker_color='#18bc9c'))

	plot5 = do.Figure(do.Bar(
			x= data1.index,
			y= data1['Volume'],
			name='Volume',
			marker_color='#18bc9c'))
			
	plot6 = do.Figure(do.Scatter(
			x= data1.index,
			y= data1['Close'],
			name= symbol[0],
			marker_color='#18bc9c'))
	plot6.add_trace(
		do.Scatter(
			x= data2.index,
			y= data2['Close'],
			name= symbol[1],
			marker_color='#3EBE51'
		))
	plot6.add_trace(
		do.Scatter(
			x= data3.index,
			y= data3['Close'],
			name= symbol[2],
			marker_color='#777877'
		))

	plot4.update_yaxes(showgrid=True,gridcolor='#F4EFEB',gridwidth=0.5)
	plot4.update_layout(margin= do.layout.Margin(t=30,b=15,r=10,l=0), title='Price ({})'.format(data[0]['companyName']), showlegend=False, plot_bgcolor='#ffffff', hovermode='x', height=450)
	plot5.update_layout(margin= do.layout.Margin(t=30,b=15,r=0,l=10), title='Volume ({})'.format(data[0]['companyName']), showlegend=False, plot_bgcolor='#ffffff', hovermode='x', height=225)
	plot6.update_layout(margin= do.layout.Margin(t=30,b=15,r=0,l=10), title='Price Trend Comparison', showlegend=False, plot_bgcolor='#ffffff', hovermode='x', height=225)

	plotA = do.Figure(do.Indicator(
			mode= 'number+delta',
			value= datax[0]['latestPrice'],
			delta= {'reference': datax[0]['previousClose'], 'relative': True},
			title = {"text": datax[0]['companyName']}))

	plotB = do.Figure(do.Indicator(
			mode= 'number+delta',
			value= datax[1]['latestPrice'],
			delta= {'reference': datax[1]['previousClose'], 'relative': True},
			title = {"text": datax[1]['companyName']}))
			
	plotC = do.Figure(do.Indicator(
			mode= 'number+delta',
			value= datax[2]['latestPrice'],
			delta= {'reference': datax[2]['previousClose'], 'relative': True},
			title = {"text": datax[2]['companyName']}))
			
	plotA.update_layout(margin= do.layout.Margin(t=40,b=0), plot_bgcolor='#EAEAEA', paper_bgcolor='#F2F2F2', height=200)
	plotB.update_layout(margin= do.layout.Margin(t=40,b=0), plot_bgcolor='#EAEAEA', paper_bgcolor='#F2F2F2', height=200)
	plotC.update_layout(margin= do.layout.Margin(t=40,b=0), plot_bgcolor='#EAEAEA', paper_bgcolor='#F2F2F2', height=200)

	plotX = do.Figure(do.Indicator(
			mode= 'number+delta',
			value= datay[0]['latestPrice'],
			delta= {'reference': datay[0]['previousClose'], 'relative': True},
			title = {"text": datay[0]['companyName']}))

	plotY = do.Figure(do.Indicator(
			mode= 'number+delta',
			value= datay[1]['latestPrice'],
			delta= {'reference': datay[1]['previousClose'], 'relative': True},
			title = {"text": datay[1]['companyName']}))

	plotZ = do.Figure(do.Indicator(
			mode= 'number+delta',
			value= datay[2]['latestPrice'],
			delta= {'reference': datay[2]['previousClose'], 'relative': True},
			title = {"text": datay[2]['companyName']}))
			
	plotX.update_layout(margin= do.layout.Margin(t=40,b=0), plot_bgcolor='#EAEAEA', paper_bgcolor='#F2F2F2', height=200)
	plotY.update_layout(margin= do.layout.Margin(t=40,b=0), plot_bgcolor='#EAEAEA', paper_bgcolor='#F2F2F2', height=200)
	plotZ.update_layout(margin= do.layout.Margin(t=40,b=0), plot_bgcolor='#EAEAEA', paper_bgcolor='#F2F2F2', height=200)

	return plot1,plot2,plot3,plot4,plot5,plot6,plotA,plotB,plotC,plotX,plotY,plotZ,date_now


if __name__=='__main__':
    app.run_server(debug=True)

