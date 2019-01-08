# _*_ coding: utf-8 _*_

"""
app2实例
"""

import dash
import datetime
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input, State
from Dash.app import app

# 全局变量
markdown_text = """
### Dash and Markdown

Dash apps can be written in Markdown.
Dash uses the [CommonMark](http://commonmark.org/)
specification of Markdown.
Check out their [60 Second Markdown Tutorial](http://commonmark.org/help/)
if this is your first introduction to Markdown!
"""

# 构造components
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
    dbc.Input(type="email", placeholder="Enter email"),
    dbc.FormText("Are you on email? You simply have to be these days", color="secondary"),
])

password_input = dbc.FormGroup(children=[
    dbc.Label("Password", html_for="example-password"),
    dbc.Input(type="password", placeholder="Enter password"),
    dbc.FormText("A password stops mean people taking your stuff", color="secondary"),
])

# ---------------------------------------------------------------------------------------
email_input_row = dbc.FormGroup(children=[
    dbc.Label("Email", html_for="example-email-row", width=2),
    dbc.Col(dbc.Input(type="email", placeholder="Enter email"), width=10)
], row=True)

password_input_row = dbc.FormGroup(children=[
    dbc.Label("Password", html_for="example-password-row", width=2),
    dbc.Col(dbc.Input(type="password", placeholder="Enter password"), width=10)
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


# 创建layout
layout = dbc.Container(children=[
    # 显示文字 ========================================================================================
    html.Div(children=[
        html.H1(children="Hello Dash H1"),
        html.H2(children="Hello Dash H2"),
        html.H3(children="Hello Dash H3"),
        html.H4(children=[
            "This is a heading with a badge! ",
            dbc.Badge("New!", color="success")
        ]),
        html.P(children=html.A(children="这是一个百度链接", href="http://baidu.com")),
        html.Label(children="这是一个Lable", className="text-info"),
        html.Pre(children="这是一个Pre，常用来显示计算机代码"),
        dcc.Markdown(children=markdown_text),
    ], className="mt-2"),

    html.Div(children=[
        dbc.Alert("primary!", color="primary", id="alert_memory"),
        dbc.Alert("secondary!", color="secondary", id="alert_local"),
        dbc.Alert("success!", color="success", id="alert_session"),
        dbc.Alert("info!", color="info"),
        dbc.Alert("warning!", color="warning"),
        dbc.Alert("danger!", color="danger"),
    ], className="mt-2"),

    # 按钮类 ========================================================================================
    html.Div(children=[
        dbc.Button("Primary", color="primary", className="mr-2", id="button_memory"),
        dbc.Button("Secondary", color="secondary", className="mr-2", id="button_local"),
        dbc.Button("Success", color="success", className="mr-2", id="button_session"),
        dbc.Button("Info", color="info", className="mr-2"),
        dbc.Button("Warning", color="warning", className="mr-2"),
        dbc.Button("Danger", color="danger", className="mr-2"),
        dbc.Button("outline", color="primary", className="mr-2", size="sm", outline=True),
        dbc.Button("outline", color="secondary", className="mr-2", size="md", outline=True),
        dbc.Button("outline", color="success", className="mr-2", size="lg", outline=True),
        dbc.Button("outline", color="info", className="mr-2", size="md", outline=True),
        dbc.Button("outline", color="warning", className="mr-2", size="sm", outline=True),
    ], className="mt-2"),

    html.Div(children=dbc.ButtonGroup([
        dbc.Button("Primary", color="primary"),
        dbc.Button("Secondary", color="secondary"),
        dbc.Button("Success", color="success"),
        dbc.Button("Warning", color="warning"),
        dbc.Button("Danger", color="danger"),
        dbc.Button("Info", color="info"),
    ]), className="mt-2"),

    # 触发类 ========================================================================================
    html.Div(children=[
        dbc.Button("Open collapse", id="collapse-button"),
        dbc.Collapse(dbc.Card(dbc.CardBody("This content is hidden in the collapse")), id="collapse")
    ], className="mt-2"),

    html.Div(children=[
        dbc.Button("Toggle fade", id="fade-button"),
        dbc.Fade(dbc.Card(dbc.CardBody(dbc.CardText("This content fades in and out"))), id="fade", is_in=True, appear=False),
    ], className="mt-2"),

    html.Div(children=[
        html.P(children=["Click on the word ", html.Span("popover", id="popover-target", className="text-info")]),
        dbc.Popover([
            dbc.PopoverHeader("Popover header"),
            dbc.PopoverBody("Popover body"),
        ], id="popover", is_open=False, target="popover-target"),
    ], className="mt-2"),

    html.Div(children=[
        html.P([
            "I wonder what ",
            html.Span("floccinaucinihilipilification", id="tooltip-target", className="text-info"),
            " means?",
        ]),
        dbc.Tooltip(
            "Noun: rare, the action or habit of estimating something as worthless.",
            target="tooltip-target", placement="auto",  # top, left, bottom, right
        ),
    ], className="mt-2"),

    html.Div(children=dcc.ConfirmDialogProvider(
        id="confirm",
        children=dbc.Button("ConfirmDialogProvider", color="primary"),
        message="Danger danger! Are you sure you want to continue?"
    ), className="mt-2"),

    html.Div(children=dbc.Row(children=[
        dbc.Col(dbc.DropdownMenu(label="Menu-sm", bs_size="sm", children=drop_down_list), className="mr-2"),
        dbc.Col(dbc.DropdownMenu(label="Menu-md", bs_size="md", children=drop_down_list), className="mr-2"),
        dbc.Col(dbc.DropdownMenu(label="Menu-md", bs_size="lg", children=drop_down_list), className="mr-2"),
        dbc.Col(dbc.DropdownMenu(label="Menu-down", direction="down", children=drop_down_list), className="mr-2"),
        dbc.Col(dbc.DropdownMenu(label="Menu-left", direction="left", children=drop_down_list), className="mr-2"),
        dbc.Col(dbc.DropdownMenu(label="Menu-right", direction="right", children=drop_down_list), className="mr-2"),
    ], no_gutters=True), className="mt-2"),

    # 输入类 ========================================================================================
    html.Div(children=[
        dbc.Input(placeholder="A medium(large, small) input...", bs_size="md", className="mb-2"),
        dbc.Input(placeholder="Valid input...", valid=True, className="mb-2"),
        dbc.Input(placeholder="Invalid input...", invalid=True, className="mb-2"),
        dbc.Input(placeholder="Enter text", type="text", className="mb-2"),
        dbc.Input(placeholder="Enter password", type="password", className="mb-2"),
        dbc.Input(value=10, type="number", className="mb-2"),
        dbc.Input(value=10, type="range", className="mb-2"),
        dbc.Textarea(placeholder="Enter a value...", className="mb-2"),
        dbc.Textarea(placeholder="Enter a value...", className="mb-2", valid=True, bs_size="sm"),
    ], className="mt-2"),

    html.Div(children=[
        dbc.InputGroup([
            dbc.InputGroupAddon("@", addon_type="prepend"),
            dbc.Input(placeholder="username, size=lg"),
        ], size="lg", className="mb-2"),
        dbc.InputGroup([
            dbc.Input(placeholder="username, size=md"),
            dbc.InputGroupAddon("@example.com", addon_type="append"),
        ], className="mb-2"),
        dbc.InputGroup([
            dbc.InputGroupAddon("$", addon_type="prepend"),
            dbc.Input(placeholder="Amount, size=sm", type="number"),
            dbc.InputGroupAddon(".00", addon_type="append"),
        ], size="sm", className="mb-2"),
        dbc.InputGroup([
            dbc.InputGroupAddon(dbc.Button("Random name"), addon_type="prepend"),
            dbc.Input(placeholder="name"),
        ], className="mb-2"),
        dbc.InputGroup([
            dbc.DropdownMenu(drop_down_list, label="Generate", addon_type="prepend"),
            dbc.Input(placeholder="name"),
        ]),
    ], className="mt-2"),

    # 表单类 ========================================================================================
    dbc.Form(children=[email_input, password_input], className="mt-2 p-2 bg-light"),
    dbc.Form(children=[email_input_row, password_input_row], className="mt-2 p-2 bg-light"),
    dbc.Form(children=[
        dbc.FormGroup([
            dbc.Label("Email", className="mr-2"),
            dbc.Input(type="email", placeholder="Enter email")
        ], className="mr-3"),
        dbc.FormGroup([
            dbc.Label("Password", className="mr-2"),
            dbc.Input(type="password", placeholder="Enter password")
        ], className="mr-3"),
        dbc.FormGroup([
            dbc.Label("Date", className="mr-2"),
            dbc.DatePickerSingle(date=datetime.date(2018, 10, 17))
        ], className="mr-3"),
        dbc.FormGroup([
            dbc.Label("Date", className="mr-2"),
            dcc.DatePickerRange(start_date=datetime.datetime(1997, 5, 3), end_date_placeholder_text="Select!")
        ], className="mr-3"),
    ], inline=True, className="mt-2 p-2 bg-light"),

    # 表单类 ========================================================================================
    html.Div(children=[
        dbc.Label("Slider", html_for="slider"),
        dcc.Slider(min=0, max=9, marks={i: "Label {}".format(i) if i == 1 else str(i) for i in range(1, 6)}, value=5),
        html.Br(),
        dbc.Label("RangeSlider", html_for="range-slider"),
        dcc.RangeSlider(count=1, min=-5, max=10, step=0.5, value=[-3, 7])
    ], className="mt-2"),
    html.Div(children=[
        dbc.Label(children="Progress: 0", html_for="progress", id="progresstext"),
        dbc.Progress(id="progress", value=0, max=60, striped=True, animated=True),
        dcc.Interval(id="interval", interval=1000, n_intervals=0),
    ], className="mt-2"),
    html.Div(children=[radioitems, checklist, radioitems_inline, checklist_inline], className="mt-2"),

    html.Div(children=dbc.Row(children=[
        dbc.Col(dcc.Dropdown(options=[
            {"label": "New York City", "value": "NYC"},
            {"label": u"Montréal", "value": "MTL"},
            {"label": "San Francisco", "value": "SF"}
        ], value="MTL"), className="mr-2"),
        dbc.Col(dcc.Dropdown(options=[
            {"label": "New York City", "value": "NYC"},
            {"label": u"Montréal", "value": "MTL"},
            {"label": "San Francisco", "value": "SF"}
        ], value="MTL", multi=True), width=8)
    ], no_gutters=True), className="mt-2"),

    # 文件上传 ========================================================================================
    dcc.Upload(dbc.Button("Upload File"), className="mt-2"),
    dcc.Upload(children=html.Div([
        "Drag and Drop or ",
        html.A("Select Files")
    ], className="p-2 border border-secondary bg-light rounded text-center"), multiple=True, className="mt-2"),

    # 展示类 ========================================================================================
    dbc.ListGroup(children=[
        dbc.ListGroupItem("ListGroupItem"),
        dbc.ListGroupItem("Internal link", href="/l/components/list_group"),
        dbc.ListGroupItem("External link", href="https://google.com"),
        dbc.ListGroupItem("Disabled link", href="https://google.com", disabled=True),
        dbc.ListGroupItem("Button", n_clicks=0, action=True),
    ], className="mt-2"),

    dbc.ListGroup(children=[
        dbc.ListGroupItem("The primary item", color="primary"),
        dbc.ListGroupItem("A secondary item", color="secondary"),
        dbc.ListGroupItem("A successful item", color="success"),
        dbc.ListGroupItem("A warning item", color="warning"),
        dbc.ListGroupItem("A dangerous item", color="danger"),
        dbc.ListGroupItem("An informative item", color="info"),
    ], className="mt-2"),

    dbc.ListGroup(children=[
        dbc.ListGroupItem([
            dbc.ListGroupItemHeading("This item has a heading"),
            dbc.ListGroupItemText("And some text underneath"),
        ]),
        dbc.ListGroupItem([
            dbc.ListGroupItemHeading("This item also has a heading"),
            dbc.ListGroupItemText("And some more text underneath too"),
        ]),
    ], className="mt-2"),
])


# 创建回调函数：回调函数中不能出现全局变量
for store in ("memory", "local", "session"):
    @app.callback(Output(store, "data"), [
        Input("button_%s" % store, "n_clicks")
    ], [
        State(store, "data")
    ])
    def toggle_store_button(n_clicks, data):
        if n_clicks is None:
            raise dash.exceptions.PreventUpdate
        data = data or {"clicks": 0}
        data["clicks"] = data["clicks"] + 1
        return data

    @app.callback(Output("alert_%s" % store, "children"), [
        Input(store, "modified_timestamp")
    ], [
        State(store, "data"),
        State(store, "id")
    ])
    def toggle_store_change(ts, data, _id):
        if ts is None:
            raise dash.exceptions.PreventUpdate
        data = data or {}
        return "%s: %s" % (_id, data.get("clicks", 0))


@app.callback(Output("collapse", "is_open"), [
    Input("collapse-button", "n_clicks")
], [
    State("collapse", "is_open")
])
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


@app.callback(Output("fade", "is_in"), [
    Input("fade-button", "n_clicks")
], [
    State("fade", "is_in")
])
def toggle_fade(n, is_in):
    if not n:
        return True
    return not is_in


@app.callback(Output("popover", "is_open"), [
    Input("popover-target", "n_clicks")
], [
    State("popover", "is_open")
])
def toggle_popover(n, is_open):
    if n:
        return not is_open
    return is_open


@app.callback(Output("progress", "value"), [
    Input("interval", "n_intervals")
])
def advance_progress(n):
    return n % 61


@app.callback(Output("progresstext", "children"), [
    Input("progress", "value"),
])
def advance_text(value):
    return "Processtext: %d" % value
