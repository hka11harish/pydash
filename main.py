

import dash
import dash_html_components as html
import pandas as pd
#import dash_core_components as dcc
from dash import dcc
import plotly.express as px
from dash.dependencies import Output
from dash.dependencies import Input
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
app = dash.Dash(__name__)


# Create a data frame
df = px.data.tips()

# Load the dataset
data = pd.read_csv("Cars Mock Data.csv",usecols=['Purchase Date','Sale Price'])
data2 = pd.read_csv("Cars Mock Data.csv",usecols=['Purchase Date','Sale Price','Make'])

# Convert dates to datetime format
data['Purchase Date'] = pd.to_datetime(data['Purchase Date'])
data2['Purchase Date'] = pd.to_datetime(data2['Purchase Date'])


# Filter year from date
data['Year'] = data['Purchase Date'].dt.year
data2['Year'] = data2['Purchase Date'].dt.year

# Filtering year 2020 from year for fig2
filtered_data = data2[data2['Year'] == 2020]


# Grouping Data by Year with sum of Sale Price
grouped_data=data.groupby('Year')['Sale Price'].sum()

df_year=pd.DataFrame({
'year':grouped_data.index,
'sales':grouped_data.values

})

# Grouping Data by Make with sum of Sale Price
grouped_data2=filtered_data.groupby('Make')['Sale Price'].sum()

df_make=pd.DataFrame({
'Make':grouped_data2.index,
'sales':grouped_data2.values

})


# Create graph to show sales each year
fig = px.line(df_year, x="year", y="sales",title="Car Sales historical data")
fig.update_layout(template="plotly_dark")
fig.update_layout(
    xaxis_dtick="M1",
    xaxis_tickformat="%b\n%Y",
    hovermode="x",
)

# Create a graph to show sales of each Make on 2020
fig2 = px.bar(df_make, x="Make", y="sales",title="Car Sales 2020 by Makers")
fig2.update_layout(template="plotly_dark")
fig2.update_layout(
    xaxis_dtick="M1",
    xaxis_tickformat="%b\n%Y",
    hovermode="x",
)
# Create a dropdown menu with the years as options
year_options = []
for year in df_year['year'].unique():
  year_options.append({'label': str(year), 'value': year})

# Create a dropdown component
dropdown = dcc.Dropdown(
  id='year-dropdown',
  options=year_options,
  value=df_year['year'].min()
)

# Create a callback that updates the dropdown
@app.callback(
  Output('sales-graph', 'figure'),
  Input('year-dropdown', 'value')
)
def update_graph(year):
  year = int(year)
  filtered_df = df_year[df_year['year'] == year]
  figure = px.bar(filtered_df, x="year", y="sales")
  figure.update_layout(xaxis_range=[year, year])
  figure.update_layout(template="plotly_dark")
  figure.update_layout(
      xaxis_dtick="M1",
      xaxis_tickformat="%b\n%Y",
      hovermode="x",
  )
  return figure

# Create a text box
sales_textbox = html.Div(
    id="sales-textbox",
    style=dict(
        **{
            "font-size": "20px",
            "background-color": "black",
            "color": "#ffffff",
            "font-family": "Plotly+Dark",
            "text-align": "center",
        },
        **{
            "template": "plotly_dark",
        },
    ),
)

# Create a callback that updates the text box
@app.callback(
    Output("sales-textbox", "children"), Input("year-dropdown", "value")
)
def update_textbox(year):
    filtered_df = df_year[df_year["year"] == year]
    sales = filtered_df["sales"].sum()
    return f"SALES FOR {year}: $ {sales} "

controls = dbc.Form(
    [
        html.P('Dropdown', style={
            'textAlign': 'center'
        }),
        dcc.Dropdown(
            id='dropdown',
            options=[{
                'label': 'Value One',
                'value': 'value1'
            }, {
                'label': 'Value Two',
                'value': 'value2'
            },
                {
                    'label': 'Value Three',
                    'value': 'value3'
                }
            ],
            value=['value1'],  # default value
            multi=True
        ),
        html.Br(),
        html.P('Range Slider', style={
            'textAlign': 'center'
        }),
        dcc.RangeSlider(
            id='range_slider',
            min=0,
            max=20,
            step=0.5,
            value=[5, 15]
        ),
        html.P('Check Box', style={
            'textAlign': 'center'
        }),
        dbc.Card([dbc.Checklist(
            id='check_list',
            options=[{
                'label': 'Value One',
                'value': 'value1'
            },
                {
                    'label': 'Value Two',
                    'value': 'value2'
                },
                {
                    'label': 'Value Three',
                    'value': 'value3'
                }
            ],
            value=['value1', 'value2'],
            inline=True
        )]),
        html.Br(),
        html.P('Radio Items', style={
            'textAlign': 'center'
        }),
        dbc.Card([dbc.RadioItems(
            id='radio_items',
            options=[{
                'label': 'Value One',
                'value': 'value1'
            },
                {
                    'label': 'Value Two',
                    'value': 'value2'
                },
                {
                    'label': 'Value Three',
                    'value': 'value3'
                }
            ],
            value='value1',
            style={
                'margin': 'auto'
            }
        )]),
        html.Br(),
        dbc.Button(
            id='submit_button',
            className="w-100",
            n_clicks=0,
            children='Submit',
            color='primary'
        ),
    ]
)

#Create buttons for each graph:
btn_sales = html.Button('Sales Over Time', id='btn-sales')
btn_makes = html.Button('Sales by Make', id='btn-makes')

SIDEBAR_STYLE = {
    'position': 'fixed',
    'top': 0,
    'left': 0,
    'bottom': 0,
    'width': '20%',
    'padding': '20px',
    'background-color': '#f8f9fa'
}

sidebar = html.Div(
    [
        html.H2('GLOBAL CAR SALES REPORT'),
        html.Hr(),
        dropdown,
        html.Hr(),
        btn_sales,
        html.H1(""),
        btn_makes,
        #controls
    ],
    style=SIDEBAR_STYLE,
)

@app.callback(
  Output('example-graph', 'style'),
  Input('btn-sales', 'n_clicks'),
  prevent_initial_call=True
)
def show_sales_graph(n_clicks):
    print(dash.callback_context)  # Print context
    print(n_clicks)  # Print n_clicks

    return {'display': 'block'}

@app.callback(
  Output('example-graph2', 'style'),
  Input('btn-makes', 'n_clicks'),
  State('n_clicks', 'data'),
  prevent_initial_call=True
)
def show_makes_graph(n_clicks):
    print(n_clicks)
    print(data)  # Prior n_clicks

    return {'display': 'block'}

ctx = dash.callback_context
print(ctx)

# Create the layout
content = html.Div(
    style={"template": "plotly_dark"},
    children=[
    #dcc.Dropdown(
    #    id="filter",
     #   options=[{"label" : year, "value":year} for year in df_year.columns[0:]],
      #  clearable=False
    #),
    #html.H5("select year",
     #       style=dict(
       # **{
      #      "font-size": "15px",
       #     "font-family": "Plotly+Dark",
        #},
        #**{
        #    "template": "plotly_dark",
        #},
    #),),
    #dropdown,
    sales_textbox,
    #dcc.Graph(id='sales-graph'),
    html.H1(""),
    dcc.Graph(
        id="example-graph",
        figure=fig,
        #style={'display':'none'}
    ),
    html.H1(""),
    dcc.Graph(
        id="example-graph2",
        figure=fig2,
        #style={'display':'none'}
    )
])
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = dbc.Container([

    dbc.Row([
        dbc.Col(sidebar, md=4),
        dbc.Col(content, md=8)
    ])

])
#app.layout = html.Div([sidebar,content])

# Run the app
if __name__ == "__main__":
    app.run(debug=True)