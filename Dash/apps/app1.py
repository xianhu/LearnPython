# _*_ coding: utf-8 _*_

"""
app1实例
"""

import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input
from Dash.app import app

# 全局变量
df = pd.read_csv("apps/data.csv")

# 构造components
tab1_content = dbc.Card(children=dbc.CardBody([
    dbc.CardText("This is tab 1!"),
    dbc.Button("Click here", color="success"),
]))

tab2_content = dbc.Card(children=dbc.CardBody([
    dbc.CardText("This is tab 2!"),
    dbc.Button("Don't click here", color="danger"),
]))


def generate_table(dataframe, max_rows=10, size="md"):
    """
    创建表
    """
    # Headers
    headers = [html.Th(col, className="text-center") if index != 1 else html.Th(col) for index, col in enumerate(dataframe.columns[:10])]

    # Rows
    rows = []
    for i in range(max_rows):
        td_list = []
        for index, col in enumerate(dataframe.columns[:10]):
            if index == 1:
                td_list.append(html.Td(dcc.Link(dataframe.iloc[i][col], href=dataframe.iloc[i][col])))
            else:
                td_list.append(html.Td(dataframe.iloc[i][col], className="text-center"))
        rows.append(html.Tr(td_list))
    return dbc.Table([html.Thead(html.Tr(headers)), html.Tbody(rows)], striped=True, bordered=True, hover=True, size=size)


# 创建layout
layout = dbc.Container(children=[
    # Tab实例 ========================================================================================
    html.Div(children=dbc.Tabs([
        dbc.Tab(tab1_content, label="Tab 1"),
        dbc.Tab(tab2_content, label="Tab 2"),
    ]), className="mt-2"),

    html.Div(children=[dbc.Tabs([
        dbc.Tab(label="Tab 1", tab_id="tab-1"),
        dbc.Tab(label="Tab 2", tab_id="tab-2"),
    ], id="tabs", active_tab="tab-1"),
        html.Div(id="content"),
    ], className="mt-2"),

    # DIV布局 ========================================================================================
    dbc.Row(children=dbc.Col(html.Div("单独的DIV", className="border border-primary bg-light rounded p-2 mt-2"))),
    dbc.Row(children=[
        dbc.Col(html.Div("One of three columns", className="bg-secondary p-2 mr-2 rounded")),
        dbc.Col(html.Div("One of three columns", className="bg-secondary p-2 rounded-top")),
        dbc.Col(html.Div("One of three columns", className="bg-secondary p-2 ml-2 rounded-bottom")),
    ], no_gutters=True, className="mt-2"),
    dbc.Row(children=[
        dbc.Col(html.Div("One of 4 columns", className="bg-info p-2 mr-2"), width=3),
        dbc.Col(html.Div("Two of 4 columns", className="bg-info p-2")),
        dbc.Col(html.Div("One of 4 columns", className="bg-info p-2 ml-2"), width=3),
    ], no_gutters=True, className="mt-2"),
    dbc.Row(children=dbc.Col(html.Div("A single, half-width column, width=6", className="bg-secondary p-2"), width=6), className="mt-2"),
    dbc.Row(children=dbc.Col(html.Div("An automatically sized column", className="bg-secondary p-2"), width="auto"), className="mt-2"),

    # 卡片类 ========================================================================================
    html.Div(children=dbc.Row(children=[
        dbc.Col(children=dbc.Card([
            dbc.CardHeader("Header"),
            dbc.CardBody([
                dbc.CardTitle("This card has a title"),
                dbc.CardText("And some text"),
            ]),
        ])),
        dbc.Col(children=dbc.Card([
            dbc.CardBody([
                dbc.CardTitle("This card has a title"),
                dbc.CardText("and some text, but no header"),
            ]),
        ], outline=True, color="primary")),
        dbc.Col(children=dbc.Card([
            dbc.CardBody([
                dbc.CardTitle("This card has a title"),
                dbc.CardText("and some text, and a footer!"),
            ]),
            dbc.CardFooter("Footer"),
        ], outline=True, color="danger")),
        dbc.Col(children=dbc.Card([
            dbc.CardBody([
                dbc.CardTitle("Card title"),
                dbc.CardSubtitle("Card subtitle")
            ]),
            dbc.CardImg(src="https://placeholdit.imgix.net/~text?txtsize=33&txt=318%C3%97180&w=318&h=180"),
            dbc.CardBody([
                dbc.CardText(
                    "Some quick example text to build on the "
                    "card title and make up the bulk of the "
                    "card's content."
                ),
                dbc.CardLink("A link", href="#"),
                dbc.CardLink("Another link", href="#"),
            ]),
        ])),
    ]), className="mt-2"),

    # 画图类 ========================================================================================
    dcc.Graph(id="example-graph", figure={
        "data": [
            {"x": [1, 2, 3], "y": [4, 1, 2], "type": "bar", "name": "SF"},
            {"x": [1, 2, 3], "y": [2, 4, 5], "type": "bar", "name": u"Montréal"},
        ],
        "layout": {
            "title": "Dash Data Visualization"
        }
    }, className="mt-2"),

    # 表格Table ========================================================================================
    html.Div(children=generate_table(df, size="sm"), className="mt-2"),
    html.Div(children=generate_table(df, size="md"), className="mt-2"),
])


# 创建回调函数：回调函数中不能出现全局变量
@app.callback(Output("content", "children"), [
    Input("tabs", "active_tab")
])
def switch_tab(at):
    if at == "tab-1":
        return tab1_content
    elif at == "tab-2":
        return tab2_content
    return html.P("This shouldn't ever be displayed...")
