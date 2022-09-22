from dash import Dash, dcc, html, Input, Output
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc

df = pd.read_csv('data/ventout.csv')

df3 = df.drop(columns = ["Unnamed: 0","no"])
df0 = pd.melt(df3,id_vars = "t")

fig3 = px.scatter(
    x =df3["compstat"],
    y =df3["compstat"],
    title = "Bivariate graph"
)

graph7 = dcc.Graph(id = "graph-output",figure ={})

tab2c = html.Div(
     [

             html.H5("Choose X-axis variable"),
             dcc.Dropdown(
                 df0["variable"].unique(),
                 "compstat",
                 id = "t2-xaxis",
             ),
             html.Br(),
             html.H5("Choose Y-axis variable"),
             dcc.Dropdown(
                 df0["variable"].unique(),
                 "compstat",
                 id = "t2-yaxis",
             ),
             html.Br(),
             graph7,
             html.H5("OOPS")

     ]
)

@tab2.callback(
    Output(component_id = "graph-output" ,component_property = "figure" ),
    Input(component_id ="t2-xaxis",component_property="value"),
    Input(component_id ="t2-yaxis",component_property = "value")
)
def update_graph7(x,y):
    print(x)
    print(y)