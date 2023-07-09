import pandas as pd
import plotly.express as px  # (version 4.7.0 or higher)
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output  # pip install dash (version 2.0.0 or higher)


app = Dash(__name__)


# ------------------------------------------------------------------------------
# App layout

df=pd.read_csv('with_iso_alpha_education.csv')

app.layout = html.Div([

    html.H1("How Have Global Education Levels Changed Since 1870?", style={'text-align': 'center'}),

    dcc.Dropdown(id="slct_view",
                 options=[
                     {"label": "Completed Primary Education", "value": "completed_primary"},
                     {"label": "Completed Secondary Education", "value": "completed_secondary"},
                     {"label": "Completed Teritary Education", "value":"completed_tertiary"},
                     {"label": "Average Years Total Schooling", "value": "avg_years_total_schooling" }],
                 multi=False,
                 value="avg_years_total_schooling",
                 style={'width': "40%"}
                 ),

    html.Div(id='output_container', children=[]),
    html.Br(),

    dcc.Graph(id='education_map', figure={})

])


# Callback
# Connect dropdown (input) to visuals (output)
@app.callback(
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='education_map', component_property='figure')],
    [Input(component_id='slct_view', component_property='value')] # must be value not label
)
def update_graph(option_slctd):
    # update the visual based on the dropdown option selected


    app.logger.info(option_slctd)
    print(option_slctd)
    print(type(option_slctd))

    container = "You are viewing: {}".format(option_slctd)

    # the plotly vis
    fig = px.choropleth(
                        data_frame=df,
                        animation_frame='year',
                        color=option_slctd, 
                        locations="iso_alpha",
                        color_continuous_scale=px.colors.diverging.Geyser_r,
                        hover_data= ['country'],
                        range_color=[0, df[option_slctd].max()] # calibrate the scale to the right range
                        )

    return container, fig


# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)
