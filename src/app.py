import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import altair as alt
import pandas as pd
import numpy as np
from datetime import datetime
from vega_datasets import data


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
                        This is a dashboard visualization of violent crimes in U.S. cities.\n
                        The map is by default set to show the background map of U.S. cities, the bar chart is by default set to show the summative results of the state of California at 2015
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
                                html.H6("Crime Type:"),
                                dcc.Dropdown(
                                    id="crime_type",
                                    value=None,  # REQUIRED to show the plot on the first page load
                                    options=[
                                        {"label": col, "value": col}
                                        for col in ["Aggravated Assault", "Homicide", "Rape", "Robbery", "Total"]
                                    ],
                                ),
                            ]
                        ),
                        html.Div(
                            [
                                html.H6("Year:"),
                                dcc.Dropdown(
                                    id="year_maps",
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
                        id = 'maps',
                        style={'border-width': '0', 'width': '140%', 'height': '460px'})
                    ], 
                    md=8,
                ),
            ]      
        ),
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
    Input("yrange", "value")
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

# Create Map plot 

@app.callback(
    Output('maps', 'srcDoc'),
    Input('crime_type', 'value'),
    Input("year_maps", "value"))

def plot_map(crime_type, year_maps):
    # create background map:
    state_map = alt.topo_feature(data.us_10m.url, 'states')
    
    background = alt.Chart(state_map).mark_geoshape(
        fill='#F5F5F5',
        stroke='dimgray'
    ).project(
        'albersUsa'
    )
    
    # If no input
    if (crime_type is None):
        chart = (background).configure_view(
                height=420,
                width=850,
                strokeWidth=4,
                fill=None,
                stroke=None)
        return chart.to_html()

    # convert crime_type to corresponding colname
    crime_col = {
        "Aggravated Assault": "agg_ass_sum",
        "Homicide": "homs_sum", 
        "Rape": "rape_sum",
        "Robbery": "rob_sum",
        "Total": "violent_crime"
    }
    
     # set up colors:
    crime_color = {
    "Aggravated Assault": alt.Scale(domain=list(np.linspace(df.agg_ass_sum.min(), df.agg_ass_sum.max(), 9).astype(int)),
                range=['#7093B9', '#6584A7', '#5A7694', '#4E6782', '#43586F', '#384A5D', '#2D3B4A', '#222C37', '#161D25']),
    "Homicide": alt.Scale(domain=list(np.linspace(df.homs_sum.min(), df.homs_sum.max(), 9).astype(int)),
                range=['#F8AA5D', '#DF9954', '#C6884A', '#AE7741', '#956638', '#7C552F', '#634425', '#4A331C', '#322213']),
    "Rape": alt.Scale(domain=list(np.linspace(df.rape_sum.min(), df.rape_sum.max(), 9).astype(int)),
                range=['#EC8989', '#D47B7B', '#BD6E6E', '#A56060', '#8E5252', '#764545', '#5E3737', '#472929', '#2F1B1B']),
    "Robbery":alt.Scale(domain=list(np.linspace(df.rob_sum.min(), df.rob_sum.max(), 9).astype(int)),
                range=['#AAD4D1', '#99BFBC', '#88AAA7', '#779492', '#667F7D', '#556A69', '#445554', '#33403F', '#222A2A']),
    "Total": alt.Scale(domain=list(np.linspace(df.violent_crime.min(), df.violent_crime.max(), 9).astype(int)),
                range=['#77B56F', '#6BA364', '#5F9159', '#537F4E', '#476D43', '#3C5B38', '#30482C', '#243621', '#182416']),
    }
    
    # adding id
    state_ids = data.population_engineers_hurricanes()[['state', 'id']]
    state_ids = state_ids.rename(columns = {'state': 'State'})
    
    # obtain data based on input
    df_selected = df.loc[
        (df.year == year_maps),
        ["year", "state_name", crime_col[crime_type], "total_pop"]
    ].groupby(['state_name'], as_index = False).sum()
    
    df_selected = df_selected.rename(columns = {
        crime_col[crime_type] : crime_type,
        'year': 'Year',
        'total_pop': 'Population',
        'state_name': 'State'
    })
    
    df_complete = df_selected.merge(state_ids, on = 'State')

    
    # create foreground
    map_click = alt.selection_multi(fields=['State'])
    foreground = (alt.Chart(state_map).mark_geoshape().transform_lookup(
        lookup = 'id',
        from_ = alt.LookupData(
            df_complete,
            'id',
            ['State','Population', crime_type]
        )
    ).mark_geoshape(
        stroke='black',
        strokeWidth=0.5
    ).encode(
        color=alt.Color(crime_type+':Q', scale=crime_color[crime_type]), opacity=alt.condition(map_click, alt.value(1), alt.value(0.7)),
        tooltip=[alt.Tooltip('State:O'),
                 alt.Tooltip('Population:O'),
                 alt.Tooltip(crime_type+':O')]
    ).add_selection(map_click).project(
        type='albersUsa'
    ))


    chart = (background + foreground).configure_view(
                height=400,
                width=800,
                strokeWidth=4,
                fill=None,
                stroke=None)

    return chart.to_html()

if __name__ == "__main__":
    app.run_server(debug=True)
