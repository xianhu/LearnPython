# _*_ coding: utf-8 _*_

"""
定义通用组件
"""

import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

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
    dbc.Label("Email", html_for="example-email-row", width=2),
    dbc.Col(dbc.Input(type="email", id="example-email-row", placeholder="Enter email"), width=10)
], row=True)

password_input_row = dbc.FormGroup(children=[
    dbc.Label("Password", html_for="example-password-row", width=2),
    dbc.Col(dbc.Input(type="password", id="example-password-row", placeholder="Enter password"), width=10)
], row=True)


# ---------------------------------------------------------------------------------------
radioitems = dbc.FormGroup(children=[
    dbc.Label("Choose one"),
    dbc.RadioItems(options=[
        {"label": "Option 1", "value": 1},
        {"label": "Option 2", "value": 2},
    ], value=1)
], className="bg-light")

checklist = dbc.FormGroup(children=[
    dbc.Label("Choose a bunch"),
    dbc.Checklist(options=[
        {"label": "Option 1", "value": 1},
        {"label": "Option 2", "value": 2},
    ], values=[1, 2]),
], className="bg-light")


# ---------------------------------------------------------------------------------------
radioitems_inline = dbc.FormGroup(children=[
    dbc.Label("Choose one"),
    dbc.RadioItems(options=[
        {"label": "Option 1", "value": 1},
        {"label": "Option 2", "value": 2},
    ], value=1, inline=True),
], className="bg-light")

checklist_inline = dbc.FormGroup(children=[
    dbc.Label("Choose a bunch"),
    dbc.Checklist(options=[
        {"label": "Option 1", "value": 1},
        {"label": "Option 2", "value": 2},
    ], values=[1, 2], inline=True),
], className="bg-light")


# ---------------------------------------------------------------------------------------
tab1_content = dbc.Card(children=dbc.CardBody([
        dbc.CardText("This is tab 1!"),
        dbc.Button("Click here", color="success"),
    ])
)

tab2_content = dbc.Card(children=dbc.CardBody([
        dbc.CardText("This is tab 2!"),
        dbc.Button("Don't click here", color="danger"),
    ])
)


def generate_table(dataframe, max_rows=10):
    """
    创建表
    """
    # Header
    header = html.Thead(children=html.Tr([html.Th(col) for col in dataframe.columns[:10]]))

    # Row
    rows = []
    for i in range(max_rows):
        td_list = []
        for index, col in enumerate(dataframe.columns[:10]):
            if index == 1:
                td_list.append(html.Td(dcc.Link(dataframe.iloc[i][col], href=dataframe.iloc[i][col])))
            else:
                td_list.append(html.Td(dataframe.iloc[i][col]))
        rows.append(html.Tr(td_list))
    return dbc.Table([header, html.Tbody(rows)], striped=True, bordered=True, hover=True)
