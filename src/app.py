import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import altair as alt
import pandas as pd


# Read in global data
df = pd.read_csv("data/processed/clean_data.csv",  index_col=0)

# Setup app and layout/frontend
app = dash.Dash(
    __name__, external_stylesheets=[dbc.themes.BOOTSTRAP]
)
server = app.server
app.layout = dbc.Container([
    html.H2('U.S. city crime visualizer'),
    dbc.Row([
        dbc.Col([
            dbc.Row([html.Label([
                'Year range',
                dcc.RangeSlider(
                    id="yrange",
                    min=1975,
                    max=2015,
                    value=[1975, 2015],  # REQUIRED to show the plot on the first page load
                    step=1,
                    marks={1975: '1975', 2015: '2015'},
                ),
            ])]),
            dbc.Row([html.Label([
                'State',
                dcc.Dropdown(
                    id="state",
                    value="California",  # REQUIRED to show the plot on the first page load
                    options=[{"label": st_name, "value": st_name} for st_name in df["state_name"].unique()],
                ),
            ])]),

            dbc.Row(html.Label([
                'City',
                dcc.Dropdown(
                    id="city",
                    value="Los Angeles",  # REQUIRED to show the plot on the first page load
                    options=[{"label": col, "value": col} for col in
                             df[df["state_name"] == "California"]["city_name"].unique()],
                ),
            ])),

            dbc.Row(html.Label([
                'Year',
                dcc.Dropdown(
                    id="year",
                    value=2014,  # REQUIRED to show the plot on the first page load
                    options=[{"label": col, "value": col} for col in df["year"].unique()],
                ),
            ]))
        ],md = 1),

        dbc.Col([
            html.Iframe(
            id="scatter",
            style={"border-width": "0", "width": "100%", "height": "400px"},
        )])
    ])
])


@app.callback(
    Output("city", "options"),
    Input("state", "value"),
)
def city(state):
    opts=[{"label": col, "value": col} for col in df[df["state_name"] == state]["city_name"].unique()]
    return opts

# Set up callbacks/backend
@app.callback(Output("scatter", "srcDoc"),
              Input("state", "value"),
              Input("city", "value"),
              Input("year", "value"),
              Input("yrange","value"))
def plot_altair(state,city,year,yrange):

    df_select = df.loc[(df.city_name == city)
    & (df.state_name == state)
    & (df.year == year)]
    df_data_plot=df_select.loc[:, "homs_per_100k":"agg_ass_per_100k"]
    df_data_plot=df_data_plot.mean(axis=0).to_frame().reset_index()
    df_data_plot.columns=["type", "value"]
    df_data_plot['type']=df_data_plot['type'].replace(
        ['homs_per_100k', 'rape_per_100k', 'rob_per_100k', 'agg_ass_per_100k'],
        ['Homicide', 'Rape', 'Robbery', 'Aggravated Assault'])

    df_select_line = df.loc[(df.city_name == city)
                     & (df.state_name == state)
                     & (df.year >= yrange[0])
                     & (df.year <= yrange[1])]

    bar=alt.Chart(df_data_plot, title="City violent crime in 4 categories at year of interest").mark_bar(
    ).encode(alt.X("type", title="Violent Crime"),
             alt.Y("value", title="Crime per 100K"),
             alt.Color("type", title="Crime type"))

    text=bar.mark_text(dy=-5).encode(text=alt.Text('value', format='.2f'))

    line = alt.Chart(df_select_line, title = "Total  violent crimes at city of interest V.S. Years").mark_line(
        interpolate='monotone').encode(
        alt.X('year:O', title="Year"),
        alt.Y('violent_per_100k', title="Violent crime per 100k")).properties(height = 250,width = 700)

    chart = line | (bar+text).properties(height = 250,width = 280)

    return chart.to_html()


if __name__ == "__main__":
    app.run_server(debug=True)
