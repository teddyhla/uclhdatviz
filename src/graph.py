from dash import dcc

def build_fig1():
    return fig1

fig1 = make_subplots(
    rows=4,
    cols=1,
    shared_xaxes=True,
    vertical_spacing=0.04,
)

fig1.add_trace(
    go.Scatter(x=df["t"], y=df["mv"]),
    row=1, col=1
)

fig1.add_trace(
    go.Scatter(x=df["t"], y=df["tv"]),
    row=2, col=1
)

fig1.add_trace(
    go.Scatter(x=df["t"], y=df["rrset"]),
    row=3, col=1
)

fig1.add_trace(
    go.Scatter(x=df["t"], y=df["psupp"]),
    row=4, col=1
)

fig1.layout.title = "ventilator variable trends"
fig1.update_layout(
    hovermode="x unified",
)
fig1.update_xaxes(matches="x")
fig1.update_traces(xaxis="x1")
