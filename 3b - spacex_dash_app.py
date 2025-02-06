# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
import dash_core_components as dcc
import dash_html_components as html
from dash import Dash, dcc, html, Input, Output
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                dcc.Dropdown(id='site-dropdown',  
                                options=[{'label': 'All Sites', 'value': 'ALL'},{'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'}, {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'}, {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},{'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}],
                                value='ALL',
                                placeholder="Select a Launch Site here",
                                searchable=True
                                ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(id='payload-slider', min=0, max=10000, step=1000, 
                                    marks={0: '0',  1000:'1000', 2000:'2000', 3000:'3000', 4000:'4000', 5000:'5000', 6000:'6000', 7000:'7000', 8000:'8000', 9000:'9000', 10000:'10000'},
                                    value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        pie = px.pie(values=filtered_df.groupby('Launch Site')['class'].mean(), 
                     names=filtered_df.groupby('Launch Site')['Launch Site'].first(), 
        title='Total Success Launches by Site')
    else:
        # return the outcomes piechart for a selected site
        selected_df = filtered_df.loc[filtered_df['Launch Site'] == str(entered_site)]
        pie = px.pie(values = selected_df['class'].value_counts(normalize=True),
        names=selected_df['class'].unique(), 
        title='Total Success Launches for Site {}'.format(entered_site))
    return pie

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'), Input(component_id="payload-slider", component_property="value")])
def get_scatter_chart(entered_site):
    filtered_df = spacex_df[(spacex_df['Payload Mass (kg)']>=payload_slider[0])
        &(spacex_df['Payload Mass (kg)']<=payload_slider[1])]
    if entered_site == 'ALL':
        scatter = px.scatter(filtered_df, x = "Payload Mass (kg)", y = "class",
        color="Booster Version Category",
        title='Correlation Between Payload and Success for All Sites')
    else:
        # return the outcomes piechart for a selected site
        selected_df = spacex_df.loc[spacex_df['Launch Site'] == str(entered_site)]
        filtered_df = selected_df[(selected_df['Payload Mass (kg)']>=payload_slider[0])
        &(selected_df['Payload Mass (kg)']<=payload_slider[1])]
        scatter = px.scatter(filtered_df, x = "Payload Mass (kg)", y = "class",
        color="Booster Version Category",
        title='Correlation Between Payload and Success for Site {}'.format(entered_site))
    return scatter

# Run the app
if __name__ == '__main__':
    app.run_server()
