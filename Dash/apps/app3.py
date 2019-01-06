# _*_ coding: utf-8 _*_

"""
app3实例
"""

import json
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input
from Dash.app import app


# 创建layout
layout = dbc.Container(children=[
    dcc.Graph(
        id="basic-interactions",
        figure={
            "data": [{
                "x": [1, 2, 3, 4],
                "y": [4, 1, 3, 5],
                "text": ["a", "b", "c", "d"],
                "customdata": ["c.a", "c.b", "c.c", "c.d"],
                "name": "Trace 1",
                "mode": "markers",
                "marker": {"size": 12}
            }, {
                "x": [1, 2, 3, 4],
                "y": [9, 4, 1, 4],
                "text": ["w", "x", "y", "z"],
                "customdata": ["c.w", "c.x", "c.y", "c.z"],
                "name": "Trace 2",
                "mode": "markers",
                "marker": {"size": 12}
            }]
        }
    ),

    html.Div(children=dbc.Row(children=[
        dbc.Col(children=dbc.Card([
            dbc.CardHeader("Hover Data"),
            dbc.CardBody([
                dbc.CardText(html.Pre(id="hover-data")),
            ]),
        ])),
        dbc.Col(children=dbc.Card([
            dbc.CardHeader("Click Data"),
            dbc.CardBody([
                dbc.CardText(html.Pre(id="click-data")),
            ]),
        ])),
        dbc.Col(children=dbc.Card([
            dbc.CardHeader("Selected Data"),
            dbc.CardBody([
                dbc.CardText(html.Pre(id="selected-data")),
            ]),
        ])),
        dbc.Col(children=dbc.Card([
            dbc.CardHeader("Zoom and Relayout Data"),
            dbc.CardBody([
                dbc.CardText(html.Pre(id="relayout-data")),
            ]),
        ])),
    ]), className="mt-2"),
])


@app.callback(Output("hover-data", "children"), [
    Input("basic-interactions", "hoverData")
])
def display_hover_data(hover_data):
    return json.dumps(hover_data, indent=2)


@app.callback(Output("click-data", "children"), [
    Input("basic-interactions", "clickData")
])
def display_click_data(click_data):
    return json.dumps(click_data, indent=2)


@app.callback(Output("selected-data", "children"), [
    Input("basic-interactions", "selectedData")
])
def display_selected_data(selected_data):
    return json.dumps(selected_data, indent=2)


@app.callback(Output("relayout-data", "children"), [
    Input("basic-interactions", "relayoutData")
])
def display_selected_data(relayout_data):
    return json.dumps(relayout_data, indent=2)
