# Preload installations and csv grabs in terminal prior to using project space.
    # pip3 install pandas dash
    # wget "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv"
    # wget "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/labs/module_3/spacex_dash_app.py"
    # python3 spacex_dash_app.py

# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the spacex data into pandas dataframe
spacex_data = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_data['Payload Mass (kg)'].max()
min_payload = spacex_data['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
        style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
    # Add a drop-down input for Launch Sites
    dcc.Dropdown(id='site_dropdown',
        options=[{'label':'All Sites','value':'ALL'},
            {'label':'CCAFS LC-40','value':'CCAFS LC-40'},
            {'label':'CCAFS SLC-40','value':'CCAFS SLC-40'},
            {'label':'VAFB SLC-4E','value':'VAFB SLC-4E'},
            {'label':'KSC LC-39A','value':'KSC LC-39A'}],
        value='ALL',
        placeholder='Select a launch site here',
        searchable=True),
html.Br(),

# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
                Input(component_id='site_dropdown', component_property='value'))
def get_pie_chart (site_dropdown):
    filtered_df = spacex_data
    if site_dropdown == 'ALL':
        fig = px.pie(spacex_data,
                    values='class',
                    names='Launch Site',
                    title='Total Success Launches')
        return fig
    else:
        filtered_df = spacex_data[spacex_data['Launch Site'] == site_dropdown]
        filtered_df = filtered_df.groupby(['Launch Site','class']).size().reset_index(name='class count')
        fig=px.pie(filtered_df,
                    values='class count',
                    names='class',
                    title="Total Success Launches for site")
        return fig

# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart',component_property='figure'),
                [Input(component_id='site_dropdown',component_property='value'),
                Input(component_id='payload-slider',component_property='value')])

def scatter (site_dropdown,payload):
    low,high=payload
    mask=(spacex_data['Payload Mass (kg)']>low)&(spacex_data['Payload Mass (kg)']<high)
    filtered_df = spacex_data[mask]
    if site_dropdown == 'ALL':
        fig = px.scatter(spacex_data, x='Payload Mass (kg)', y='class',
                            color='Booster Version Category',
                            title='Payload vs. Outcome for All Sites')
        return fig
    else:
        filtered_df1 = filtered_df[filtered_df['Launch Site']==site_dropdown]
        fig = px.scatter (filtered_df1, x='Payload Mass (kg)', y='class',
                            color='Booster Version Category',
                            title='Payload and Booster Versions for site')
        return fig

# Run the app
if __name__ == '__main__':
    app.run_server()