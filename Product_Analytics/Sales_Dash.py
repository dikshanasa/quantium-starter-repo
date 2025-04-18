import pandas as pd
import glob
import dash
from dash import dcc, html
from dash import dash_table
from dash.dependencies import Input, Output
import plotly.express as px
from datetime import datetime

# Data Processing - Combine all CSVs into one DataFrame
csv_files = glob.glob("../data/daily_sales_data_*.csv")
df_list = [pd.read_csv(file) for file in csv_files]
df = pd.concat(df_list, ignore_index=True)

# Convert 'date' to datetime and clean 'price'
df['date'] = pd.to_datetime(df['date'])
df['price'] = df['price'].str.replace('$', '', regex=False).astype(float)  # Remove $ and convert to float
df['total_sales'] = df['price'] * df['quantity']  # Now a numerical calculation



# Initialize the Dash app
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX])


# Define the app layout
app.layout = html.Div(
    style={'backgroundColor': '#f4f4f4', 'padding': '20px'},
    children=[
        html.H1(
            "SoulFood Product Performance Dashboard",
            style={'textAlign': 'center', 'color': '#333', 'marginBottom': '30px'}
        ),
        html.Div(
            style={'display': 'flex', 'flexWrap': 'wrap', 'gap': '20px', 'marginBottom': '30px'},
            children=[
                html.Div(
                    style={'flex': '1', 'minWidth': '200px'},
                    children=[
                        html.Label("Select Product(s):", style={'fontWeight': 'bold', 'display': 'block', 'marginBottom': '5px'}),
                        dcc.Dropdown(
                            id='product-dropdown',
                            options=[{'label': i, 'value': i} for i in df['product'].unique()],
                            value=df['product'].unique().tolist(),
                            multi=True,
                            style={'borderRadius': '5px', 'borderColor': '#ccc'}
                        ),
                    ]
                ),
                html.Div(
                    style={'flex': '1', 'minWidth': '200px'},
                    children=[
                        html.Label("Select Region(s):", style={'fontWeight': 'bold', 'display': 'block', 'marginBottom': '5px'}),
                        dcc.Dropdown(
                            id='region-dropdown',
                            options=[{'label': i, 'value': i} for i in df['region'].unique()],
                            value=df['region'].unique().tolist(),
                            multi=True,
                            style={'borderRadius': '5px', 'borderColor': '#ccc'}
                        ),
                    ]
                ),
                html.Div(
                    style={'flex': '2', 'minWidth': '300px'},
                    children=[
                        html.Label("Select Date Range:", style={'fontWeight': 'bold', 'display': 'block', 'marginBottom': '5px'}),
                        dcc.DatePickerRange(
                            id='date-picker-range',
                            start_date=df['date'].min().date(),
                            end_date=df['date'].max().date(),
                            display_format='YYYY-MM-DD',
                            style={'borderRadius': '5px', 'borderColor': '#ccc'}
                        ),
                    ]
                ),
            ]
        ),
        html.Div(
            style={'display': 'flex', 'flexWrap': 'wrap', 'gap': '20px', 'marginBottom': '30px'},
            children=[
                html.Div(
                    id='total-sales-kpi',
                    style={'flex': '1', 'minWidth': '200px', 'backgroundColor': 'white', 'padding': '15px', 'borderRadius': '5px', 'boxShadow': '0 2px 4px rgba(0, 0, 0, 0.1)'},
                    children=[
                        html.H3("Total Sales", style={'color': '#555'}),
                        html.P(id='total-sales-value', style={'fontSize': '24px', 'fontWeight': 'bold', 'color': '#28a745'}),
                    ]
                ),
                html.Div(
                    id='total-quantity-kpi',
                    style={'flex': '1', 'minWidth': '200px', 'backgroundColor': 'white', 'padding': '15px', 'borderRadius': '5px', 'boxShadow': '0 2px 4px rgba(0, 0, 0, 0.1)'},
                    children=[
                        html.H3("Total Quantity Sold", style={'color': '#555'}),
                        html.P(id='total-quantity-value', style={'fontSize': '24px', 'fontWeight': 'bold', 'color': '#007bff'}),
                    ]
                ),
                html.Div(
                    id='average-price-kpi',
                    style={'flex': '1', 'minWidth': '200px', 'backgroundColor': 'white', 'padding': '15px', 'borderRadius': '5px', 'boxShadow': '0 2px 4px rgba(0, 0, 0, 0.1)'},
                    children=[
                        html.H3("Average Price", style={'color': '#555'}),
                        html.P(id='average-price-value', style={'fontSize': '24px', 'fontWeight': 'bold', 'color': '#ffc107'}),
                    ]
                ),
            ]
        ),
        html.Div(
            style={'display': 'flex', 'flexWrap': 'wrap', 'gap': '20px', 'marginBottom': '30px'},
            children=[
                html.Div(
                    style={'flex': '2', 'minWidth': '500px', 'backgroundColor': 'white', 'padding': '15px', 'borderRadius': '5px', 'boxShadow': '0 2px 4px rgba(0, 0, 0, 0.1)'},
                    children=[
                        html.H3("Total Sales Trend Over Time", style={'color': '#555'}),
                        dcc.Graph(id='sales-trend-graph'),
                    ]
                ),
                html.Div(
                    style={'flex': '1', 'minWidth': '300px', 'backgroundColor': 'white', 'padding': '15px', 'borderRadius': '5px', 'boxShadow': '0 2px 4px rgba(0, 0, 0, 0.1)'},
                    children=[
                        html.H3("Total Sales by Product", style={'color': '#555'}),
                        dcc.Graph(id='sales-by-product-bar'),
                    ]
                ),
            ]
        ),
        html.Div(
            style={'display': 'flex', 'flexWrap': 'wrap', 'gap': '20px', 'marginBottom': '30px'},
            children=[
                html.Div(
                    style={'flex': '1', 'minWidth': '300px', 'backgroundColor': 'white', 'padding': '15px', 'borderRadius': '5px', 'boxShadow': '0 2px 4px rgba(0, 0, 0, 0.1)'},
                    children=[
                        html.H3("Sales Distribution by Region", style={'color': '#555'}),
                        dcc.Graph(id='sales-by-region-pie'),
                    ]
                ),
                html.Div(
                    style={'flex': '1', 'minWidth': '400px', 'backgroundColor': 'white', 'padding': '15px', 'borderRadius': '5px', 'boxShadow': '0 2px 4px rgba(0, 0, 0, 0.1)'},
                    children=[
                        html.H3("Product Performance (Average Price vs. Total Quantity)", style={'color': '#555'}),
                        dcc.Graph(id='product-performance-scatter'),
                    ]
                ),
            ]
        ),
        html.Div(
            style={'backgroundColor': 'white', 'padding': '15px', 'borderRadius': '5px', 'boxShadow': '0 2px 4px rgba(0, 0, 0, 0.1)'},
            children=[
                html.H3("Detailed Sales Data", style={'color': '#555'}),
                dash_table.DataTable(
                    id='sales-data-table',
                    columns=[{"name": col, "id": col} for col in df.columns],
                    data=df.to_dict('records'),
                    filter_action="native",
                    sort_action="native",
                    style_table={'height': '300px', 'overflowY': 'auto'},
                    style_header={
                        'backgroundColor': '#f0f0f0',
                        'fontWeight': 'bold',
                        'textAlign': 'left'
                    },
                    style_cell={
                        'textAlign': 'left'
                    },
                    style_data_conditional=[
                        {
                            'if': {'row_index': 'odd'},
                            'backgroundColor': '#f9f9f9',
                        }
                    ]
                ),
            ]
        ),
    ]
)

# --- Callbacks to Update KPIs ---
@app.callback(
    Output('total-sales-value', 'children'),
    Output('total-quantity-value', 'children'),
    Output('average-price-value', 'children'),
    Input('product-dropdown', 'value'),
    Input('region-dropdown', 'value'),
    Input('date-picker-range', 'start_date'),
    Input('date-picker-range', 'end_date'),
)
def update_kpis(product_names, regions, start_date, end_date):
    filtered_df = df[
        (df['product'].isin(product_names)) &
        (df['region'].isin(regions)) &
        (df['date'] >= pd.to_datetime(start_date)) &
        (df['date'] <= pd.to_datetime(end_date))
    ]
    total_sales = filtered_df['total_sales'].sum()
    total_quantity = filtered_df['quantity'].sum()
    average_price = filtered_df['price'].mean() if not filtered_df.empty else 0
    return f'{total_sales:,.2f}', f'{total_quantity:,}', f'${average_price:,.2f}'

# --- Callback to Update Sales Trend Graph ---
@app.callback(
    Output('sales-trend-graph', 'figure'),
    Input('product-dropdown', 'value'),
    Input('region-dropdown', 'value'),
    Input('date-picker-range', 'start_date'),
    Input('date-picker-range', 'end_date'),
)
def update_sales_trend(product_names, regions, start_date, end_date):
    filtered_df = df[
        (df['product'].isin(product_names)) &
        (df['region'].isin(regions)) &
        (df['date'] >= pd.to_datetime(start_date)) &
        (df['date'] <= pd.to_datetime(end_date))
    ]
    sales_by_date = filtered_df.groupby('date')['total_sales'].sum().reset_index()
    if sales_by_date.empty:
        fig = px.line(title="No Data Available")
    else:
        fig = px.line(
            sales_by_date,
            x='date',
            y='total_sales',
            title="Total Sales Trend Over Time",
            labels={'total_sales': 'Total Sales', 'date': 'Date'}
        )
    fig.update_layout(plot_bgcolor='white', paper_bgcolor='white', font_color='#333')
    return fig

# --- Callback to Update Sales by Product Bar Chart ---
@app.callback(
    Output('sales-by-product-bar', 'figure'),
    Input('product-dropdown', 'value'),
    Input('region-dropdown', 'value'),
    Input('date-picker-range', 'start_date'),
    Input('date-picker-range', 'end_date'),
)
def update_sales_by_product(product_names, regions, start_date, end_date):
    filtered_df = df[
        (df['product'].isin(product_names)) &
        (df['region'].isin(regions)) &
        (df['date'] >= pd.to_datetime(start_date)) &
        (df['date'] <= pd.to_datetime(end_date))
    ]
    sales_by_product = filtered_df.groupby('product')['total_sales'].sum().sort_values(ascending=False).reset_index()
    if sales_by_product.empty:
        fig = px.bar(title="No Data Available")
    else:
        fig = px.bar(
            sales_by_product,
            x='product',
            y='total_sales',
            title="Total Sales by Product",
            labels={'total_sales': 'Total Sales', 'product': 'Product'}
        )
    fig.update_layout(plot_bgcolor='white', paper_bgcolor='white', font_color='#333')
    return fig

# --- Callback to Update Sales by Region Pie Chart ---
@app.callback(
    Output('sales-by-region-pie', 'figure'),
    Input('product-dropdown', 'value'),
    Input('region-dropdown', 'value'),
    Input('date-picker-range', 'start_date'),
    Input('date-picker-range', 'end_date'),
)
def update_sales_by_region(product_names, regions, start_date, end_date):
    filtered_df = df[
        (df['product'].isin(product_names)) &
        (df['region'].isin(regions)) &
        (df['date'] >= pd.to_datetime(start_date)) &
        (df['date'] <= pd.to_datetime(end_date))
    ]
    sales_by_region = filtered_df.groupby('region')['total_sales'].sum().reset_index()
    if sales_by_region.empty:
        fig = px.pie(title="No Data Available")
    else:
        fig = px.pie(
            sales_by_region,
            names='region',
            values='total_sales',
            title="Sales Distribution by Region",
            labels={'total_sales': 'Total Sales', 'region': 'Region'},
            hole=0.3
        )
    fig.update_layout(plot_bgcolor='white', paper_bgcolor='white', font_color='#333')
    return fig

# --- Callback to Update Product Performance Scatter Plot ---
@app.callback(
    Output('product-performance-scatter', 'figure'),
    Input('product-dropdown', 'value'),
    Input('region-dropdown', 'value'),
    Input('date-picker-range', 'start_date'),
    Input('date-picker-range', 'end_date'),
)
def update_product_performance(product_names, regions, start_date, end_date):
    filtered_df = df[
        (df['product'].isin(product_names)) &
        (df['region'].isin(regions)) &
        (df['date'] >= pd.to_datetime(start_date)) &
        (df['date'] <= pd.to_datetime(end_date))
    ]
    product_performance = filtered_df.groupby('product').agg(
        average_price=('price', 'mean'),
        total_quantity=('quantity', 'sum')
    ).reset_index()
    if product_performance.empty:
        fig = px.scatter(title="No Data Available")
    else:
        fig = px.scatter(
            product_performance,
            x='average_price',
            y='total_quantity',
            size='total_quantity',
            color='product',
            hover_name='product',
            title="Product Performance (Average Price vs. Total Quantity)",
            labels={'average_price': 'Average Price', 'total_quantity': 'Total Quantity', 'product': 'Product'}
        )
    fig.update_layout(plot_bgcolor='white', paper_bgcolor='white', font_color='#333')
    return fig

# --- Callback to Update Data Table ---
@app.callback(
    Output('sales-data-table', 'data'),
    Input('product-dropdown', 'value'),
    Input('region-dropdown', 'value'),
    Input('date-picker-range', 'start_date'),
    Input('date-picker-range', 'end_date'),
)
def update_table(product_names, regions, start_date, end_date):
    filtered_df = df[
        (df['product'].isin(product_names)) &
        (df['region'].isin(regions)) &
        (df['date'] >= pd.to_datetime(start_date)) &
        (df['date'] <= pd.to_datetime(end_date))
    ]
    return filtered_df.to_dict('records')

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
