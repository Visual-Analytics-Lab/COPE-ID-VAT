from dash import dcc, html
import plotly.graph_objs as go
from django_plotly_dash import DjangoDash

# Create Dash app
app = DjangoDash('LineChartExample')

# Sample data
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
values = [10, 15, 13, 17, 22, 18]

# App layout
app.layout = html.Div([
    html.H3("Monthly Sales Overview"),
    dcc.Graph(
        id='line-chart',
        figure={
            'data': [
                go.Scatter(
                    x=months,
                    y=values,
                    mode='lines+markers',
                    name='Sales',
                    line=dict(shape='linear')
                )
            ],
            'layout': go.Layout(
                xaxis={'title': 'Month'},
                yaxis={'title': 'Sales ($k)'},
                margin={'l': 40, 'r': 10, 't': 40, 'b': 40},
                hovermode='closest'
            )
        }
    )
])
