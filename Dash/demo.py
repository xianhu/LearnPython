# _*_ coding: utf-8 _*_

"""
Dash实例
"""

import datetime
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input, State
from Dash.config import *
from Dash.components import drop_down_list
from Dash.components import email_input, password_input, email_input_row, password_input_row
from Dash.components import radioitems, checklist, radioitems_inline, checklist_inline
from Dash.components import tab1_content, tab2_content
from Dash.components import generate_table


# 创建应用
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.scripts.config.serve_locally = True

# 创建布局
app.layout = html.Div(children=[
    # DIV布局 ========================================================================================
    dbc.Row(children=dbc.Col(
        html.Div("单独的DIV", style={"backgroundColor": color_primary_light, "height": 100, "padding": 20, "margin": 5})
    )),
    dbc.Row(children=[
        dbc.Col(html.Div("One of three columns", style={"backgroundColor": color_info_light, "margin": 5})),
        dbc.Col(html.Div("One of three columns", style={"backgroundColor": color_info_light, "margin": 5})),
        dbc.Col(html.Div("One of three columns", style={"backgroundColor": color_info_light, "margin": 5})),
    ], no_gutters=True),

    html.Div(children=[
        dbc.Row(dbc.Col(html.Div("A single, half-width column, width=6"), width=6), style={"backgroundColor": color_primary_light, "margin": 5}),
        dbc.Row(dbc.Col(html.Div("An automatically sized column"), width="auto"), style={"backgroundColor": color_secondary_light, "margin": 5}),
        dbc.Row([
            dbc.Col(html.Div("One of four columns"), width=3, style={"backgroundColor": color_danger_light}),
            dbc.Col(html.Div("Two of four columns"), style={"backgroundColor": color_info_light}),
            dbc.Col(html.Div("One of four columns"), width=3, style={"backgroundColor": color_warning_light}),
        ], style={"margin": 5}),
    ]),

    html.Br(), html.Br(),
    # 显示文字 ========================================================================================
    html.Div(children=[
        html.H1(children="Hello Dash H1"),
        html.H2(children="Hello Dash H2"),
        html.H3(children="Hello Dash H3"),
        html.H4(children="Hello Dash H4"),
        html.P(children=html.A(children="这是一个百度链接", href="http://baidu.com")),
        html.Label(children="这是一个Lable"),
        html.H4(["This is a heading with a badge! ", dbc.Badge("New!", color="success")]),
        dcc.Markdown(children=markdown_text),
    ], style={"margin": 5}),

    html.Div(children=[
        dbc.Alert("primary!", color="primary"),
        dbc.Alert("secondary!", color="secondary"),
        dbc.Alert("success!", color="success"),
        dbc.Alert("info!", color="info"),
        dbc.Alert("warning!", color="warning"),
        dbc.Alert("danger!", color="danger"),
    ], style={"margin": 5}),

    html.Br(), html.Br(),
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
        ], outline=True, color="primary")),
    ]), style={"margin": 5}),

    html.Br(), html.Br(),
    # 按钮触发类 ========================================================================================
    # className: mr-1, m代表margin，r代表right，1代表距离，一般用于一行中元素的排列(mt, mb, ml, mr)
    html.Div(children=[
        dbc.Button("Primary", color="primary", className="mr-1"),
        dbc.Button("Secondary", color="secondary", className="mr-2"),
        dbc.Button("Success", color="success", className="mr-3"),
        dbc.Button("Info", color="info", className="mr-4"),
        dbc.Button("Warning", color="warning", className="mr-5"),
        dbc.Button("Danger", color="danger", className="mr-1"),
    ], style={"margin": 5}),

    html.Div(children=[
        dbc.Button("Open collapse", id="collapse-button"),
        dbc.Collapse(
            dbc.Card(dbc.CardBody("This content is hidden in the collapse")),
            id="collapse"
        )
    ], style={"margin": 5, "marginTop": 20}),

    html.Div(children=[
        dbc.Button("Toggle fade", id="fade-button"),
        dbc.Fade(
            dbc.Card(dbc.CardBody(dbc.CardText("This content fades in and out"))),
            id="fade",
            is_in=True,
            appear=False,
        ),
    ], style={"margin": 5}),

    html.Div(children=[
        html.P(["Click on the word ", html.Span("popover", id="popover-target")]),
        dbc.Popover([
            dbc.PopoverHeader("Popover header"),
            dbc.PopoverBody("Popover body"),
        ], id="popover", is_open=False, target="popover-target"),
    ], style={"margin": 5, "backgroundColor": color_secondary_light}),

    html.Div(children=[
        html.P([
            "I wonder what ",
            html.Span("floccinaucinihilipilification", id="tooltip-target", style={"color": color_info}),
            " means?",
        ]),
        dbc.Tooltip(
            "Noun: rare, the action or habit of estimating something as worthless.",
            target="tooltip-target",
            placement="auto",  # top, left, bottom, right
        ),
    ], style={"margin": 5}),

    html.Div(children=dcc.ConfirmDialogProvider(
        dbc.Button("ConfirmDialogProvider", color="primary"),
        id="confirm",
        message="Danger danger! Are you sure you want to continue?"
    ), style={"margin": 5}),

    html.Div(children=dbc.Row(children=[
        dbc.Col(dbc.DropdownMenu(label="Menu-md", bs_size="md", children=drop_down_list)),
        dbc.Col(dbc.DropdownMenu(label="Menu-lg", bs_size="lg", children=drop_down_list)),
        dbc.Col(dbc.DropdownMenu(label="Menu-sm", bs_size="sm", children=drop_down_list)),
        dbc.Col(dbc.DropdownMenu(label="Menu-down", bs_size="md", direction="down", children=drop_down_list)),
        dbc.Col(dbc.DropdownMenu(label="Menu-left", bs_size="md", direction="left", children=drop_down_list)),
        dbc.Col(dbc.DropdownMenu(label="Menu-right", bs_size="md", direction="right", children=drop_down_list)),
        dbc.Col(dcc.Dropdown(options=[
            {"label": "New York City", "value": "NYC"},
            {"label": u"Montréal", "value": "MTL"},
            {"label": "San Francisco", "value": "SF"}
        ], value="MTL")),
        dbc.Col(dcc.Dropdown(options=[
            {"label": "New York City", "value": "NYC"},
            {"label": u"Montréal", "value": "MTL"},
            {"label": "San Francisco", "value": "SF"}
        ], value="MTL", multi=True), width=3)
    ], no_gutters=True), style={"margin": 5, "backgroundColor": color_secondary_light}),

    html.Br(), html.Br(),
    # 输入类 ========================================================================================
    html.Div(children=[
        dbc.Input(placeholder="A large input...", bs_size="lg", className="mb-3"),
        dbc.Input(placeholder="A medium input...", className="mb-3"),
        dbc.Input(placeholder="A small input...", bs_size="sm", className="mb-3"),
        dbc.Input(placeholder="Valid input...", valid=True, className="mb-3"),
        dbc.Input(placeholder="Invalid input...", invalid=True, className="mb-3"),
        dcc.Textarea(placeholder="Enter a value...", style={"width": "50%"}),
    ], style={"margin": 5}),

    html.Div(children=[
        dbc.InputGroup([
            dbc.InputGroupAddon("@", addon_type="prepend"),
            dbc.Input(placeholder="username, size=lg"),
        ], size="lg", className="mb-3"),
        dbc.InputGroup([
            dbc.Input(placeholder="username, size=md"),
            dbc.InputGroupAddon("@example.com", addon_type="append"),
        ], className="mb-3"),
        dbc.InputGroup([
            dbc.InputGroupAddon("$", addon_type="prepend"),
            dbc.Input(placeholder="Amount, size=sm", type="number"),
            dbc.InputGroupAddon(".00", addon_type="append"),
        ], size="sm", className="mb-3"),
        dbc.InputGroup([
            dbc.InputGroupAddon(dbc.Button("Random name", id="input-group-button"), addon_type="prepend"),
            dbc.Input(id="input-group-button-input", placeholder="name"),
        ], className="mb-3"),
        dbc.InputGroup([
            dbc.DropdownMenu(drop_down_list, label="Generate", addon_type="prepend"),
            dbc.Input(id="input-group-dropdown-input", placeholder="name"),
        ]),
    ], style={"margin": 5}),

    html.Br(), html.Br(),
    # 表单类 ========================================================================================
    dbc.Form(children=[email_input, password_input], style={"margin": 20, "backgroundColor": color_secondary_light}),
    dbc.Form(children=[email_input_row, password_input_row], style={"margin": 20, "backgroundColor": color_secondary_light}),
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
            dbc.DatePickerSingle(id="date-picker-inline", date=datetime.date(2018, 10, 17))
        ], className="mr-3"),
        dbc.FormGroup([
            dbc.Label("Date", className="mr-2"),
            dcc.DatePickerRange(id="date-picker-range", start_date=datetime.datetime(1997, 5, 3), end_date_placeholder_text="Select!")
        ], className="mr-3"),
    ], inline=True, style={"margin": 20, "backgroundColor": color_secondary_light}),

    html.Br(), html.Br(),
    html.Div(children=[
        dbc.Label("Slider", html_for="slider"),
        dcc.Slider(min=0, max=9, marks={i: "Label {}".format(i) if i == 1 else str(i) for i in range(1, 6)}, value=5),
        html.Br(),
        dbc.Label("RangeSlider", html_for="range-slider"),
        dcc.RangeSlider(count=1, min=-5, max=10, step=0.5, value=[-3, 7])
    ], style={"margin": 5}),

    html.Div(children=[
        dbc.Progress(id="progress", value=0, striped=True, animated=True),
        dcc.Interval(id="interval", interval=250, n_intervals=0),
    ], style={"margin": 5}),

    html.Div(children=[radioitems, checklist, radioitems_inline, checklist_inline], style={"margin": 5}),

    html.Br(), html.Br(),
    # 展示类 ========================================================================================
    dbc.ListGroup(children=[
        dbc.ListGroupItem("ListGroupItem ListGroupItem"),
        dbc.ListGroupItem("Internal link", href="/l/components/list_group"),
        dbc.ListGroupItem("External link", href="https://google.com"),
        dbc.ListGroupItem("Disabled link", href="https://google.com", disabled=True),
        dbc.ListGroupItem("Button", id="button-item", n_clicks=0, action=True),
    ], style={"margin": 20}),

    dbc.ListGroup(children=[
        dbc.ListGroupItem("The primary item", color="primary"),
        dbc.ListGroupItem("A secondary item", color="secondary"),
        dbc.ListGroupItem("A successful item", color="success"),
        dbc.ListGroupItem("A warning item", color="warning"),
        dbc.ListGroupItem("A dangerous item", color="danger"),
        dbc.ListGroupItem("An informative item", color="info"),
    ], style={"margin": 20}),

    dbc.ListGroup(children=[
        dbc.ListGroupItem([
            dbc.ListGroupItemHeading("This item has a heading"),
            dbc.ListGroupItemText("And some text underneath"),
        ]),
        dbc.ListGroupItem([
            dbc.ListGroupItemHeading("This item also has a heading"),
            dbc.ListGroupItemText("And some more text underneath too"),
        ]),
    ], style={"margin": 20}),

    html.Br(), html.Br(),
    # Tab实例 ========================================================================================
    html.Div(children=dbc.Tabs([
        dbc.Tab(tab1_content, label="Tab 1"),
        dbc.Tab(tab2_content, label="Tab 2"),
    ]), style={"margin": 5, "backgroundColor": color_secondary_light}),

    html.Div(children=[
        dbc.Tabs([
            dbc.Tab(label="Tab 1", tab_id="tab-1"),
            dbc.Tab(label="Tab 2", tab_id="tab-2"),
        ], id="tabs", active_tab="tab-1"),
        html.Div(id="content")
    ], style={"margin": 5, "backgroundColor": color_secondary_light}),

    html.Br(), html.Br(),
    # 表格Table ========================================================================================
    html.Div(children=generate_table(df), style={"margin": 5}),
])


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
    return min(n % 110, 100)


@app.callback(Output("content", "children"), [
    Input("tabs", "active_tab")
])
def switch_tab(at):
    if at == "tab-1":
        return tab1_content
    elif at == "tab-2":
        return tab2_content
    return html.P("This shouldn't ever be displayed...")


if __name__ == "__main__":
    app.run_server(debug=True)
