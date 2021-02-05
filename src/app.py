import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import altair as alt
import pandas as pd
from datetime import datetime

# Read in global data
df = pd.read_csv("data/processed/clean_data.csv",  index_col=0)

# Setup app and layout/frontend
app = dash.Dash(
    __name__, external_stylesheets=[dbc.themes.BOOTSTRAP]
)
server = app.server
collapse = html.Div(
    [
        dbc.Button(
            "Learn more",
            id="collapse-button",
            className="mb-3",
            outline=False,
            style={
                "margin-top": "10px",
                "width": "150px",
                "background-color": "white",
                "color": "steelblue",
            },
        ),
    ]
)


@app.callback(
    Output("collapse", "is_open"),
    [Input("collapse-button", "n_clicks")],
    [State("collapse", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


app.layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        html.H1(
                                            "U.S. city crime visualization",
                                            style={
                                                "color": "white",
                                                "text-align": "left",
                                                "font-size": "48px",
                                            },
                                        ),
                                        dbc.Collapse(
                                            html.P(
                                                """
                        The bar chart is by default set to show the summative results of the state of California at 2015
                        and the line chart is to show the evolutions of summative results of the state of California """,
                                                style={
                                                    "color": "white",
                                                    "width": "100%",
                                                },
                                            ),
                                            id="collapse",
                                        ),
                                    ],
                                    md=10,
                                ),
                                dbc.Col([collapse]),
                            ]
                        )
                    ],
                    style={
                        "backgroundColor": "steelblue",
                        "border-radius": 3,
                        "padding": 15,
                        "margin-top": 20,
                        "margin-bottom": 20,
                        "margin-right": 15,
                        "width": 3000,
                    },
                )
            ]
        ),
        html.Br(),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Div(
                            [
                                html.H6("State:"),
                                dcc.Dropdown(
                                    id="state",
                                    value="California",  # REQUIRED to show the plot on the first page load
                                    options=[
                                        {"label": st_name, "value": st_name}
                                        for st_name in df["state_name"].unique()
                                    ],
                                ),
                            ]
                        ),
                        html.Div(
                            [
                                html.H6("City:"),
                                dcc.Dropdown(
                                    id="city",
                                    value=None,  # REQUIRED to show the plot on the first page load
                                    options=[
                                        {"label": col, "value": col}
                                        for col in df[df["state_name"] == "California"][
                                            "city_name"
                                        ].unique()
                                    ],
                                ),
                            ]
                        ),
                        html.Div(
                            [
                                html.H6("Year:"),
                                dcc.Dropdown(
                                    id="year",
                                    value=2015,  # REQUIRED to show the plot on the first page load
                                    options=[
                                        {"label": col, "value": col}
                                        for col in df["year"].unique()
                                    ],
                                ),
                            ]
                        ),
                    ],
                    md=2,
                    style={
                        "background-color": "#e6e6e6",
                        "padding": 10,
                        "border-radius": 3,
                    },
                ),
                dbc.Col(
                    [
                        html.Iframe(
                            id="bar_chart",
                            style={
                                "border-width": "0",
                                "width": "140%",
                                "height": "400px",
                            },
                        )
                    ],
                    md=3.8,
                ),
                dbc.Col(
                    [
                        html.Iframe(
                            id="line_chart",
                            style={
                                "border-width": "0",
                                "width": "140%",
                                "height": "400px",
                            },
                        ),
                        html.Div(
                            [
                                html.H6("Year range"),
                                dcc.RangeSlider(
                                    id="yrange",
                                    min=1975,
                                    max=2015,
                                    value=[
                                        1975,
                                        2015,
                                    ],  # REQUIRED to show the plot on the first page load
                                    step=1,
                                    marks={
                                        1975: "1975",
                                        1980: "1980",
                                        1985: "1985",
                                        1990: "1990",
                                        1995: "1995",
                                        2000: "2000",
                                        2005: "2005",
                                        2010: "2010",
                                        2015: "2015",
                                    },
                                ),
                            ],
                            style={"width": "102%"},
                        ),
                    ]
                ),
            ]
        ),
        html.Hr(),
        html.P(
            f"""
            This dashboard was made by Team 25 of UBC MDS 2020 Cohort, the GitHub source can be found at https://github.com/UBC-MDS/mds532_viz_group25.
            The latest dashboard was updated at {datetime.now().date()}
        """
        ),
    ]
)


@app.callback(
    Output("city", "options"),
    Input("state", "value"),
)
def city(state):
    opts = [
        {"label": col, "value": col}
        for col in df[df["state_name"] == state]["city_name"].unique()
    ]
    return opts


# Set up bar chart


@app.callback(
    Output("bar_chart", "srcDoc"),
    Input("state", "value"),
    Input("city", "value"),
    Input("year", "value"),
)
def plot_altair(state, city, year):

    if city == None:
        df_select = df.loc[(df.state_name == state) & (df.year == year)]
        t = "Summative violent crimes in four categories"
    else:
        df_select = df.loc[
            (df.city_name == city) & (df.state_name == state) & (df.year == year)
        ]
        t = "Violent crimes in four categories of the city"

    df_data_plot = df_select.loc[:, "homs_per_100k":"agg_ass_per_100k"]
    df_data_plot = df_data_plot.sum(axis=0).to_frame().reset_index()
    df_data_plot.columns = ["type", "value"]
    df_data_plot["type"] = df_data_plot["type"].replace(
        ["homs_per_100k", "rape_per_100k", "rob_per_100k", "agg_ass_per_100k"],
        ["Homicide", "Rape", "Robbery", "Aggravated Assault"],
    )

    bar = (
        alt.Chart(df_data_plot, title=t)
        .mark_bar()
        .encode(
            alt.X("type", title="Violent Crime", axis=alt.Axis(labelAngle=-45)),
            alt.Y("value", title="Crime per 100K"),
            alt.Color("type", legend=None),
        )
    )

    text = bar.mark_text(dy=-5).encode(text=alt.Text("value", format=".2f"))

    chart = (bar + text).properties(height=250, width=250)

    return chart.to_html()


# Set up line chart
@app.callback(
    Output("line_chart", "srcDoc"),
    Input("state", "value"),
    Input("city", "value"),
    Input("yrange", "value"),
)
def plot_altair(state, city, yrange):

    if city == None:
        df_select = df.loc[
            (df.state_name == state) & (df.year >= yrange[0]) & (df.year <= yrange[1])
        ]
        df_data_plot = df_select.loc[
            :,
            [
                "year",
                "violent_per_100k",
                "homs_per_100k",
                "rape_per_100k",
                "rob_per_100k",
                "agg_ass_per_100k",
            ],
        ]
        df_data_plot = df_data_plot.groupby(["year"]).sum().reset_index(level=[0])
        t = "Summative violent crimes of cities in the state"

    else:
        df_select = df.loc[
            (df.state_name == state)
            & (df.city_name == city)
            & (df.year >= yrange[0])
            & (df.year <= yrange[1])
        ]
        df_data_plot = df_select.loc[
            :,
            [
                "year",
                "violent_per_100k",
                "homs_per_100k",
                "rape_per_100k",
                "rob_per_100k",
                "agg_ass_per_100k",
            ],
        ]
        t = "Violent crimes of the city"

    line_plot = pd.melt(
        df_data_plot,
        id_vars=["year"],
        value_vars=[
            "violent_per_100k",
            "homs_per_100k",
            "rape_per_100k",
            "rob_per_100k",
            "agg_ass_per_100k",
        ],
    )
    line_plot = line_plot.rename(columns={"variable": "type"})
    line_plot["type"] = line_plot["type"].replace(
        [
            "violent_per_100k",
            "homs_per_100k",
            "rape_per_100k",
            "rob_per_100k",
            "agg_ass_per_100k",
        ],
        ["Total", "Homicide", "Rape", "Robbery", "Aggravated Assault"],
    )

    line = (
        alt.Chart(
            line_plot,
            title=t,
        )
        .mark_line(point=True)
        .encode(
            alt.X("year:O", title="Year"),
            alt.Y("value", title="Crime per 100k"),
            alt.Color(
                "type",
                title="Type",
                scale=alt.Scale(scheme="tableau10"),
                legend=alt.Legend(orient="bottom", title=None),
            ),
            tooltip=[
                "type",
                "year",
                "value",
            ],
        )
        .properties(height=250, width=550)
    )

    chart = line

    return chart.to_html()


if __name__ == "__main__":
    app.run_server(debug=True)
