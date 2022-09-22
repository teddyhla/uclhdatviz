import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
from plotly.subplots import make_subplots
# import dash


# from tab2 import tab2c
# import necessary packages

app = Dash(__name__)

# declare key df in global environment ----
df = pd.read_csv('data/ventout.csv')
# ventilator variables df
df1 = pd.read_csv("data/df1.csv")
# abg values df
df2 = df1.iloc[:10]
# subset to the correct abg values
# do necessary maths to calculate some values / data cleaning
dfname = "JOHN SMITH"
# this would be a patient name variable

###
df3 = df.drop(columns = ["Unnamed: 0","no"])

df0 = pd.melt(df3,id_vars = "t")


##### make figures ----


fig1 = make_subplots(
    rows=4,
    cols=1,
    shared_xaxes=True,
    vertical_spacing=0.075,
    subplot_titles= ("minute volume","tidal volume","resp rate","Psupp"),
    x_title="Time"
)

fig1.add_trace(
    go.Scatter(
        x=df["t"], y=df["mv"],
        name = "minute volume"
    ),
    row=1, col=1,
)

fig1.add_trace(
    go.Scatter(x=df["t"], y=df["tv"],
               name = "tidal volume"
               ),
    row=2, col=1,
)

fig1.add_trace(
    go.Scatter(x=df["t"], y=df["rrset"],
               name ="set resp rate",
               ),
    row=3, col=1,
)

fig1.add_trace(
    go.Scatter(x=df["t"], y=df["psupp"],
               name = "Pressure Support",
               ),
    row=4, col=1,
)

fig1.layout.title = "Ventilator variable trends"
fig1.update_layout(
    hovermode="x unified",
    font_family="Arial",
    font_color = "green",
    showlegend = False,
    #legend = dict (
    #    orientation = "v",
     #   yanchor = "bottom",
     #   y = 1.02,
      #  xanchor = "right",
       # x =1
    #)
)

fig1.update_xaxes(matches="x",)
fig1.update_traces(xaxis="x1")
fig1.update_layout(
    width = 500,
    height = 500,
    margin = dict(l = 25, r =25, b = 50, t= 50, pad =4 ),
    paper_bgcolor = "LightSteelBlue"
)
#fig1.update_annotations(yshift=0,xshift=-200,align="center")

####fig 2------
fig2 = make_subplots(
    rows=3,
    cols=1,
    shared_xaxes=True,
    vertical_spacing=0.075,
    subplot_titles= ("pH","pO2","pCO2"),
    x_title="Time"
)

fig2.add_trace(
    go.Scatter(
        x=df2["t"], y=df2["ph"],
        name = "pH"
    ),
    row=1, col=1,
)

fig2.add_trace(
    go.Scatter(x=df2["t"], y=df2["co2"],
               name = "co2"
               ),
    row=2, col=1,
)

fig2.add_trace(
    go.Scatter(x=df2["t"], y=df2["o2"],
               name ="o2",
               ),
    row=3, col=1,
)

fig2.layout.title = "ABG  trends"
fig2.update_layout(
    hovermode="x unified",
    font_family="Arial",
    font_color = "green",
    showlegend = False,
    #legend = dict (
    #    orientation = "v",
     #   yanchor = "bottom",
     #   y = 1.02,
      #  xanchor = "right",
       # x =1
    #)
)

fig2.update_xaxes(matches="x",)
fig2.update_traces(xaxis="x1")
fig2.update_layout(
    width = 500,
    height = 500,
    margin = dict(l = 25, r =25, b = 50, t= 50, pad =4 ),
    paper_bgcolor = "white"
)

# add hover function
##### ----
app = Dash(__name__, external_stylesheets=[dbc.themes.LUMEN])
# launching app

graph1 = dbc.CardBody(dcc.Graph(id='vent_graph', figure=fig1))
graph2 = dbc.CardBody(dcc.Graph(id="abg_graph", figure=fig2))
graph3 = dbc.CardBody(html.H4(id="hover-data1"))
graph4 = dbc.CardBody(html.H4(id="click-data1"))
graph5 = dbc.CardBody(html.H4(id="hover-data2"))
graph6 = dbc.CardBody(html.H4(id="click-data2"))
#make several "cards" where the graphs lives

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Page 1", href="#")),
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("More pages", header=True),
                dbc.DropdownMenuItem("References", href="#"),
            ],
            nav=True,
            in_navbar=True,
            label="More",
        ),
    ],
    brand="ventVisuals",
    brand_href="#",
    color="primary",
    dark=True,
)
#simply nav bar to put some links

row_content_1 = navbar
#id_1 = html.H5(id="my-output")
id_1 = dbc.Card(
    [
        dbc.CardHeader("Pt details"),
        dbc.CardBody(
            [
                html.H4(id ="my-output",className = "card-title"),
                html.P("Length of stay",className = "card-text")
            ]
        )
    ], style = {"width":"22rem"}
)
#row_content_2 = html.H5(dfname, className="card-title")
#tab_1_contents = [id_1,graph1, graph2]
tab_1_contents = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(html.Div("some information")),
                dbc.Col(id_1)
            ],
            justify= "end",
        ),
        dbc.Row(
            [
                dbc.Col(graph1),
                dbc.Col(graph2),
            ],
            justify = "between",
        ),
        dbc.Row(
            [
                dbc.Col(graph3),
                dbc.Col(graph5),
            ],
            justify = "start",
        ),
        dbc.Row(
            [
                dbc.Col(graph4),
                dbc.Col(graph6),
            ]
        ),
        html.Br(),
        html.H3("Bi-variate graphs"),
        dcc.Dropdown(df0["variable"].unique(),id = "t2xaxis",placeholder = "select X axis"),
        dcc.Dropdown(df0["variable"].unique(),id = "t2yaxis",placeholder = "Select Y axis"),
        dcc.Graph(id = "graph-output",figure ={})
    ]
)

app.layout = html.Div(
    [
        navbar,
        html.Br(),
        dcc.Dropdown(["Patient-1","Patient-2","Patient-3"],value = "Patient-2",id="selected_pt"),
        html.Br(),
        dbc.Tabs(
            [dbc.Tab([html.Br(),tab_1_contents], label="Tab 1"),
                dbc.Tab("tab2c",label="Tab 2"),
                dbc.Tab("future content", label="Tab 3")
            ]),

    ]
)


# here is call back function for graph1's slider
@app.callback(
    Output('my-output',component_property="children"),
    Input('selected_pt',component_property="value"))
def update_pt(selected_pt):
    '''custom func allow callback'''
    return f"Selected Patient : {selected_pt} \n ICU days : icu days"


@app.callback(
    Output("hover-data1","children"),
    Input("vent_graph","hoverData"))
def display_hover_data(hoverData):
    if hoverData["points"][0]["curveNumber"] == 0:
        return ["Minute Volume at Time: ",hoverData["points"][0]["x"]," ","= ",hoverData["points"][0]["y"]]
    elif hoverData["points"][0]["curveNumber"] == 1:
        return ["Tidal Volume at Time: ", hoverData["points"][0]["x"], " ", "= ", hoverData["points"][0]["y"]]
    elif hoverData["points"][0]["curveNumber"] == 2:
        return ["Respiratory Rate at Time: ", hoverData["points"][0]["x"], " ", "= ", hoverData["points"][0]["y"]]
    elif hoverData["points"][0]["curveNumber"] == 3:
        return ["Pressure Support at Time: ", hoverData["points"][0]["x"], " ", "= ", hoverData["points"][0]["y"]]

@app.callback(
    Output("click-data1","children"),
    Input("vent_graph","clickData"))
def display_click_data(clickData):
    if clickData["points"][0]["curveNumber"] == 0 :
        return ["Minute Volume at Time ", clickData["points"][0]["x"]," ","Value: ", clickData["points"][0]["y"]]
    elif clickData["points"][0]["curveNumber"] == 1 :
        return ["Tidal Volume at Time ", clickData["points"][0]["x"], " ", "Value: ", clickData["points"][0]["y"]]
    elif clickData["points"][0]["curveNumber"] == 2:
        return ["Resp Rate at Time ", clickData["points"][0]["x"], " ", "Value: ", clickData["points"][0]["y"]]
    elif clickData["points"][0]["curveNumber"] == 3:
        return ["Pressure Support at Time ", clickData["points"][0]["x"], " ", "Value: ", clickData["points"][0]["y"]]


@app.callback(
    Output("hover-data2","children"),
    Input("abg_graph","hoverData"))
def display_hover_data(hoverData):
    if hoverData["points"][0]["curveNumber"] == 0:
        return ["ABG pH value at: ",hoverData["points"][0]["x"]," ","=  ",hoverData["points"][0]["y"]]
    elif hoverData["points"][0]["curveNumber"] == 1 :
        return ["ABG pO2 value at: ",hoverData["points"][0]["x"]," ","=  ",hoverData["points"][0]["y"]]
    elif hoverData ["points"][0]["curveNumber"] == 2 :
        return ["ABG pCO2 value at ", hoverData["points"][0]["x"]," ","= ",hoverData ["points"][0]["y"]]

@app.callback(
    Output("click-data2","children"),
    Input("abg_graph","clickData"))
def display_click_data(clickData):
    if clickData["points"][0]["curveNumber"] == 0 :
        return ["ABG pH value at Time: ", clickData["points"][0]["x"]," ","Value: ", clickData["points"][0]["y"]]
    elif clickData["points"][0]["curveNumber"] == 1 :
        return ["ABG pO2 value at Time: ", clickData["points"][0]["x"], " ", "Value: ", clickData["points"][0]["y"]]
    elif clickData["points"][0]["curveNumber"] == 2 :
        return ["ABG pCO2 value at Time: ", clickData["points"][0]["x"], " ", "Value: ", clickData["points"][0]["y"]]

@app.callback(
    Output("graph-output",component_property = "figure"),
    Input(component_id = "t2xaxis",component_property= "value"),
    Input(component_id = "t2yaxis",component_property= "value")
)
def bvg(a,b):
    print(a)
    print(type(a))
    print(b)
    print(type(b))
    dff = df3.sort_values(by="t")
    fig = px.scatter(dff, x = a ,y =b , title = f"{a} vs. {b}",color = "t")
    return fig


# here initialising the app
if __name__ == '__main__':
    app.run_server(debug=True)
