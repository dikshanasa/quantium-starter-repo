import dash
from dash import html

app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.H1(children='Hello Quantium!'),
    html.P(children='This is a simple Dash app setup.')
])

if __name__ == "__main__":
    app.run(debug=True)
