import pandas as pd
import plotly.express as px  # (version 4.7.0 or higher)
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output  # dash (version 2.0.0 or higher)

# Create an instance of the Dash application
app = Dash(__name__)

# Load in data
df=pd.read_csv('with_iso_alpha_education.csv')
print(df.head())


# ------------------------------------------------------------------------------
# App layout


app.layout = html.Div([

    html.H1("How Have Global Education Levels Changed Since 1870?", style={'text-align': 'center'}),

    # Dash Core Component. Value for each option corresponds to a column in the DataFrame.
    dcc.Dropdown(id="slct_view",
                 options=[
                     {"label": "Completed Primary Education", "value": "completed_primary"},
                     {"label": "Completed Secondary Education", "value": "completed_secondary"},
                     {"label": "Completed Teritary Education", "value":"completed_tertiary"},
                     {"label": "Average Years Total Schooling", "value": "avg_years_total_schooling" }],
                 multi=False,
                 value="avg_years_total_schooling",
                 style={'width': "60%"}
                 ),

    html.Div(id='output_container', children=[]),
    
    html.Br(),

    # Dash Core Component
    dcc.Graph(id='education_map', figure={})

])

# ------------------------------------------------------------------------------
# Callbacks

# Callback decorator to connect dropdown (input) to visuals (output).
# Component_id links the functionality to the relevant components in the layout.
#
@app.callback(
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='education_map', component_property='figure')],
    [Input(component_id='slct_view', component_property='value')] 
)

def update_graph(option_slctd):
    """
    Creates a choropleth map of the world with the selected education metric.
    This funciton will get called whenever the dropdown menu is changed.
    """

    container = "You are viewing: {}".format(option_slctd)

   # Create the dynamic Plotly Express figure 
    fig = px.choropleth(
                        data_frame=df,
                        animation_frame='year',
                        color=option_slctd, #option_slct variable is passed from dropdown into this function
                        locations="iso_alpha",
                        color_continuous_scale=px.colors.diverging.Geyser_r,
                        hover_data= ['country'],
                        range_color=[0, df[option_slctd].max()] # calibrate the scale to the right range
                        )

    return container, fig


# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)
