# _*_ coding: utf-8 _*_

"""
定义通用组件
"""

import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from Dash.config import *

# ---------------------------------------------------------------------------------------
drop_down_list = [
    dbc.DropdownMenuItem("First"),
    dbc.DropdownMenuItem(divider=True),
    dbc.DropdownMenuItem("Links", header=True),
    dbc.DropdownMenuItem("Internal link", href="/l/components/alerts"),
    dbc.DropdownMenuItem("External link", href="https://baidu.com"),
    dbc.DropdownMenuItem(divider=True),
    dbc.DropdownMenuItem("Disabled", disabled=True),
    dbc.DropdownMenuItem("Active", active=True)
]


# ---------------------------------------------------------------------------------------
email_input = dbc.FormGroup(children=[
    dbc.Label("Email", html_for="example-email"),
    dbc.Input(type="email", id="example-email", placeholder="Enter email"),
    dbc.FormText("Are you on email? You simply have to be these days", color="secondary"),
])

password_input = dbc.FormGroup(children=[
    dbc.Label("Password", html_for="example-password"),
    dbc.Input(type="password", id="example-password", placeholder="Enter password"),
    dbc.FormText("A password stops mean people taking your stuff", color="secondary"),
])


# ---------------------------------------------------------------------------------------
email_input_row = dbc.FormGroup(children=[
    dbc.Label("Email", html_for="example-email", width=2),
    dbc.Col(dbc.Input(type="email", id="example-email-row", placeholder="Enter email"), width=10)
], row=True)

password_input_row = dbc.FormGroup(children=[
    dbc.Label("Password", html_for="example-password", width=2),
    dbc.Col(dbc.Input(type="password", id="example-password-row", placeholder="Enter password"), width=10)
], row=True)


# ---------------------------------------------------------------------------------------
radioitems = dbc.FormGroup(children=[
    dbc.Label("Choose one"),
    dbc.RadioItems(options=[
        {"label": "Option 1", "value": 1},
        {"label": "Option 2", "value": 2},
    ], value=1)
], style={"backgroundColor": color_success_light})

checklist = dbc.FormGroup(children=[
    dbc.Label("Choose a bunch"),
    dbc.Checklist(options=[
        {"label": "Option 1", "value": 1},
        {"label": "Option 2", "value": 2},
    ], values=[]),
], style={"backgroundColor": color_info_light})


# ---------------------------------------------------------------------------------------
radioitems_inline = dbc.FormGroup(children=[
    dbc.Label("Choose one"),
    dbc.RadioItems(options=[
        {"label": "Option 1", "value": 1},
        {"label": "Option 2", "value": 2},
    ], value=1, inline=True),
], style={"backgroundColor": color_success_light})

checklist_inline = dbc.FormGroup(children=[
    dbc.Label("Choose a bunch"),
    dbc.Checklist(options=[
        {"label": "Option 1", "value": 1},
        {"label": "Option 2", "value": 2},
    ], values=[], inline=True),
], style={"backgroundColor": color_info_light})


# ---------------------------------------------------------------------------------------
tab1_content = dbc.Card(
    dbc.CardBody([
        dbc.CardText("This is tab 1!"),
        dbc.Button("Click here", color="success"),
    ]), className="mt-1",
)

tab2_content = dbc.Card(
    dbc.CardBody([
        dbc.CardText("This is tab 2!"),
        dbc.Button("Don't click here", color="danger"),
    ]), className="mt-1",
)


def generate_table(dataframe, max_rows=10):
    """
    创建表
    """
    # Header
    header = [html.Thead(html.Tr([html.Th(col) for col in dataframe.columns]))]

    # Row
    rows = []
    for i in range(max_rows):
        td_list = []
        for index, col in enumerate(dataframe.columns):
            if index == 1:
                td_list.append(html.Td(dcc.Link(dataframe.iloc[i][col], href=dataframe.iloc[i][col])))
            else:
                td_list.append(html.Td(dataframe.iloc[i][col]))
        rows.append(html.Tr(td_list))
    body = [html.Tbody(rows)]

    return dbc.Table(header + body, striped=True, bordered=True, hover=True)
