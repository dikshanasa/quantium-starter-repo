#!/usr/bin/env python
# coding: utf-8

# In[13]:





# In[19]:


import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

# the path to the formatted data file
DATA_PATH = "/Users/dikshanasa/Desktop/Quantium/quantium-starter-repo/data/pink_morsel_sales.csv"
COLORS = {
    "primary": "#F8BBD0",  # Light Pink
    "secondary": "#E91E63",  # Deep Pink
    "accent": "#FF4081",   # Hot Pink
    "font": "#37474F"      # Dark Gray
}

# load in data
data = pd.read_csv(DATA_PATH)
data['date'] = pd.to_datetime(data['date'])
data = data.sort_values(by="date")

# initialize dash
dash_app = dash.Dash(__name__)

# create the visualization
def generate_figure(chart_data):
    line_chart = px.line(chart_data, x="date", y="sales", title="Pink Morsel Sales Trend")
    line_chart.update_layout(
        title_font_size=24,
        title_x=0.5,
        plot_bgcolor="white",
        paper_bgcolor=COLORS["primary"],
        font_color=COLORS["font"],
        xaxis=dict(
            title="Date",
            gridcolor="#f0f0f0",
            linecolor=COLORS["secondary"]
        ),
        yaxis=dict(
            title="Sales",
            gridcolor="#f0f0f0",
            linecolor=COLORS["secondary"]
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    line_chart.update_traces(line=dict(color=COLORS["accent"], width=2))
    return line_chart

# create the visualization component
visualization = dcc.Graph(
    id="visualization",
    figure=generate_figure(data)
)

# create the header
header = html.H1(
    "Pink Morsel Sales Dashboard",
    id="header",
    style={
        "background-color": COLORS["secondary"],
        "color": "white",
        "padding": "1.5rem",
        "border-radius": "10px",
        "margin-bottom": "1.5rem",
        "text-align": "center",
        "font-family": "sans-serif"
    }
)

# region picker
region_picker = dcc.RadioItems(
    ["north", "east", "south", "west", "all"],
    "all",
    id="region_picker",
    inline=True,
    labelStyle={'display': 'inline-block', 'margin-right': '15px'},
    style={
        'textAlign': 'center',
        'font-size': '1.2rem',
        'color': COLORS['font'],
        'margin-bottom': '1rem'
    }
)

region_picker_wrapper = html.Div(
    [html.Label("Select Region:", style={'font-weight': 'bold', 'margin-right': '10px', 'color': COLORS['font']}),
     region_picker],
    style={'display': 'flex', 'justify-content': 'center', 'align-items': 'center'}
)

# define the region picker callback
@dash_app.callback(
    Output(visualization, "figure"),
    Input(region_picker, "value")
)
def update_graph(region):
    # filter the dataset
    if region == "all":
        trimmed_data = data.copy()
    else:
        trimmed_data = data[data["region"] == region].copy()

    # generate a new line chart with the filtered data
    figure = generate_figure(trimmed_data)
    return figure

# define the app layout
dash_app.layout = html.Div(
    [header, visualization, region_picker_wrapper],
    style={
        "display": "flex",
        "flex-direction": "column",
        "align-items": "center",
        "background-color": COLORS["primary"],
        "padding": "2rem",
        "border-radius": "15px",
        "font-family": "sans-serif"
    }
)

# this is only true if the module is executed as the program entrypoint
if __name__ == '__main__':
    dash_app.run_server(debug=True, use_reloader=False)


# In[ ]:
app = dash_app





