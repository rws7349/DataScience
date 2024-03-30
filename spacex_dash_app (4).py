# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
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
                                dcc.Dropdown(id='site-dropdown',
                                    options=[
                                    {'label': 'All Sites', 'value': 'ALL'},
                                    {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                    {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                    {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                    {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}
                                    ],
                                    value='ALL',
                                    placeholder="Select the launch site",
                                    searchable=True
                                ),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(id='payload-slider',
                                    min=0, max=max_payload, step=1000,
                                    marks={0: '0',1000: '1000',2000: '2000',3000: '3000',4000: '4000',
                                            5000: '5000',6000: '6000',7000: '7000',8000: '8000',9000: '9000',10000: '10000',},
                                    value=[min_payload, max_payload]),
                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    # filter the dataset for the selection
    if entered_site == 'ALL' :
        filtered_df = spacex_df
    else:    
        filtered_df = spacex_df[spacex_df['Launch Site']==entered_site]
    #print('Site Entered:',entered_site)
    #print(filtered_df)   
    # Create the Pie chart for the selection    
    if entered_site == 'ALL':
        fig = px.pie(filtered_df, values='class', 
        names='Launch Site', 
        title='% of Successful Launches across all Sites')
        return fig
    else:
        if entered_site == 'CCAFS LC-40':
            #print(filtered_df['class'].value_counts(dropna=False))
            fig = px.pie(filtered_df['class'].value_counts(dropna=False), values='count',  
            names='count', 
            title='CCAFS LC-40 - Launch Rate (Blue=Success, Red-Failure)')
            return fig
        else:
            if entered_site == 'VAFB SLC-4E':
                fig = px.pie(filtered_df['class'].value_counts(dropna=False), values='count',  
                names='count',              
                title='VAFB SLC-4E - Launch Rate (Blue=Success, Red-Failure)')
                return fig
            else:
                if entered_site == 'KSC LC-39A':
                    fig = px.pie(filtered_df['class'].value_counts(dropna=False), values='count', 
                    names='count', 
                    title='KSC LC-39A - Launch Rate (Blue=Success, Red-Failure)')
                    return fig
                else:
                    if entered_site == 'CCAFS SLC-40':
                        fig = px.pie(filtered_df['class'].value_counts(dropna=False), values='count', 
                        names='count', 
                        title='CCAFS SLC-40 - Launch Rate (Blue=Success, Red-Failure)')
                        return fig
                    else:
                        print('Dropdown Selection not found... Contact Support...')
       # return the outcomes piechart for a selected site
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'), 
              Input(component_id="payload-slider", component_property="value")])
def get_scatter_chart(entered_site,selected_payload_range):
    print('payload:',selected_payload_range[0],selected_payload_range[1])
    # filter the dataset for the selection
    if entered_site == 'ALL' :
        filtered_df = spacex_df
        filtered2_df = filtered_df[filtered_df['Payload Mass (kg)']>=selected_payload_range[0]]
        filtered3_df = filtered2_df[filtered2_df['Payload Mass (kg)']<=selected_payload_range[1]]
    else:    
        filtered_df = spacex_df[spacex_df['Launch Site']==entered_site]
        filtered2_df = filtered_df[filtered_df['Payload Mass (kg)']>=selected_payload_range[0]]
        filtered3_df = filtered2_df[filtered2_df['Payload Mass (kg)']<=selected_payload_range[1]]
 
    #print('Site Entered:',entered_site)
    #print(filtered_df)   
    # Create the Scatter chart for the selection    
    if entered_site == 'ALL':
        fig = px.scatter(filtered3_df, x="Payload Mass (kg)", y="class", color="Booster Version Category",title='All Sites - Payload Mass Vs Launch Success (1) or Failure (0)')
        #fig = px.pie(filtered_df, values='class', 
        #names='Launch Site', 
        #title='% of Successful Launches across all Sites')
        return fig
    else:
        if entered_site == 'CCAFS LC-40':
            #print(filtered_df['class'].value_counts(dropna=False))
            fig = px.scatter(filtered3_df, x="Payload Mass (kg)", y="class", color="Booster Version Category",title='CCAFS LC-40 - Payload Mass Vs Launch Success (1) or Failure (0)')
            return fig
        else:
            if entered_site == 'VAFB SLC-4E':
                fig = px.scatter(filtered3_df, x="Payload Mass (kg)", y="class", color="Booster Version Category",title='VAFB SLC-4E - Payload Mass Vs Launch Success (1) or Failure (0)')
                return fig
            else:
                if entered_site == 'KSC LC-39A':
                    fig = px.scatter(filtered3_df, x="Payload Mass (kg)", y="class", color="Booster Version Category",title='KSC LC-39A - Payload Mass Vs Launch Success (1) or Failure (0)')
                    return fig
                else:
                    if entered_site == 'CCAFS SLC-40':
                        fig = px.scatter(filtered3_df, x="Payload Mass (kg)", y="class", color="Booster Version Category",title='CCAFS SLC-40 - Payload Mass Vs Launch Success (1) or Failure (0)')
                        return fig
                    else:
                        print('Dropdown Selection not found... Contact Support...')

# Run the app
if __name__ == '__main__':
    app.run_server()