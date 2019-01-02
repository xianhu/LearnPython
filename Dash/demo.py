# _*_ coding: utf-8 _*_

"""
Dash实例
"""

import dash
import datetime
from dash.dependencies import Output, Input, State
from Dash.components import *
from Dash.config import *

# 创建应用
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.scripts.config.serve_locally = True

# 创建布局
app.layout = html.Div(children=[
    # DIV布局 ========================================================================================
    dbc.Row(children=dbc.Col(html.Div("单独的DIV", className="border border-primary bg-light rounded p-2 m-2"))),
    dbc.Row(children=[
        dbc.Col(html.Div("One of three columns", className="bg-secondary p-2 m-2")),
        dbc.Col(html.Div("One of three columns", className="bg-secondary p-2 m-2")),
        dbc.Col(html.Div("One of three columns", className="bg-secondary p-2 m-2")),
    ], no_gutters=True),
    dbc.Row(children=[
        dbc.Col(html.Div("One of 4 columns", className="bg-info p-2 m-2"), width=3),
        dbc.Col(html.Div("Two of 4 columns", className="bg-info p-2 m-2")),
        dbc.Col(html.Div("One of 4 columns", className="bg-info p-2 m-2"), width=3),
    ], no_gutters=True),
    dbc.Row(children=dbc.Col(html.Div("A single, half-width column, width=6", className="bg-secondary p-2 m-2"), width=6)),
    dbc.Row(children=dbc.Col(html.Div("An automatically sized column", className="bg-secondary p-2 m-2"), width="auto")),

    html.Br(), html.Br(),
    # 显示文字 ========================================================================================
    html.Div(children=[
        html.H1(children="Hello Dash H1"),
        html.H2(children="Hello Dash H2"),
        html.H3(children="Hello Dash H3"),
        html.H4(children=["This is a heading with a badge! ", dbc.Badge("New!", color="success")]),
        html.P(children=html.A(children="这是一个百度链接", href="http://baidu.com")),
        html.Label(children="这是一个Lable", className="text-info"),
        dcc.Markdown(children=markdown_text),
    ], className="p-2 m-2"),

    html.Div(children=[
        dbc.Alert("primary!", color="primary"),
        dbc.Alert("secondary!", color="secondary"),
        dbc.Alert("success!", color="success"),
        dbc.Alert("info!", color="info"),
        dbc.Alert("warning!", color="warning"),
        dbc.Alert("danger!", color="danger"),
    ], className="p-2 m-2"),

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
    ]), className="p-2 m-2"),

    # 按钮触发类 ========================================================================================
    html.Div(children=[
        dbc.Button("Primary", color="primary", className="mr-2"),
        dbc.Button("Secondary", color="secondary", className="mr-2"),
        dbc.Button("Success", color="success", className="mr-2"),
        dbc.Button("Info", color="info", className="mr-2"),
        dbc.Button("Warning", color="warning", className="mr-2"),
        dbc.Button("Danger", color="danger", className="mr-2"),
        dbc.Button("outline", size="sm", outline=True, className="mr-2"),
        dbc.Button("outline", size="md", outline=True, className="mr-2"),
        dbc.Button("outline", size="lg", outline=True, className="mr-2"),
    ], className="p-2 m-2"),

    html.Div(children=[
        dbc.Button("Open collapse", id="collapse-button"),
        dbc.Collapse(
            dbc.Card(dbc.CardBody("This content is hidden in the collapse")),
            id="collapse"
        )
    ], className="p-2 m-2"),

    html.Div(children=[
        dbc.Button("Toggle fade", id="fade-button"),
        dbc.Fade(
            dbc.Card(dbc.CardBody(dbc.CardText("This content fades in and out"))),
            id="fade", is_in=True, appear=False,
        ),
    ], className="p-2 m-2"),

    html.Div(children=[
        html.P(["Click on the word ", html.Span("popover", id="popover-target", className="text-info")]),
        dbc.Popover([
            dbc.PopoverHeader("Popover header"),
            dbc.PopoverBody("Popover body"),
        ], id="popover", is_open=False, target="popover-target"),
    ], className="p-2 m-2"),

    html.Div(children=[
        html.P([
            "I wonder what ", html.Span("floccinaucinihilipilification", id="tooltip-target", className="text-info"), " means?",
        ]),
        dbc.Tooltip(
            "Noun: rare, the action or habit of estimating something as worthless.",
            target="tooltip-target",
            placement="auto",  # top, left, bottom, right
        ),
    ], className="p-2 m-2"),

    html.Div(children=dcc.ConfirmDialogProvider(
        id="confirm",
        children=dbc.Button("ConfirmDialogProvider", color="primary"),
        message="Danger danger! Are you sure you want to continue?"
    ), className="p-2 m-2"),

    html.Div(children=dbc.Row(children=[
        dbc.Col(dbc.DropdownMenu(label="Menu-md", bs_size="md", children=drop_down_list)),
        dbc.Col(dbc.DropdownMenu(label="Menu-lg", bs_size="lg", children=drop_down_list)),
        dbc.Col(dbc.DropdownMenu(label="Menu-sm", bs_size="sm", children=drop_down_list)),
        dbc.Col(dbc.DropdownMenu(label="Menu-down", direction="down", children=drop_down_list)),
        dbc.Col(dbc.DropdownMenu(label="Menu-left", direction="left", children=drop_down_list)),
        dbc.Col(dbc.DropdownMenu(label="Menu-right", direction="right", children=drop_down_list)),
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
    ], no_gutters=True), className="p-2 m-2"),

    html.Br(), html.Br(),
    # 输入类 ========================================================================================
    html.Div(children=[
        dbc.Input(placeholder="A medium(large, small) input...", bs_size="md", className="mb-2"),
        dbc.Input(placeholder="Valid input...", valid=True, className="mb-2"),
        dbc.Input(placeholder="Invalid input...", invalid=True, className="mb-2"),
        dbc.Input(value=10, type="number", className="mb-2"),
        dcc.Textarea(placeholder="Enter a value...", className="w-75"),
    ], className="p-2 m-2"),

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
            dbc.InputGroupAddon(dbc.Button("Random name", id="input-group-button"), addon_type="prepend"),
            dbc.Input(id="input-group-button-input", placeholder="name"),
        ], className="mb-2"),
        dbc.InputGroup([
            dbc.DropdownMenu(drop_down_list, label="Generate", addon_type="prepend"),
            dbc.Input(id="input-group-dropdown-input", placeholder="name"),
        ]),
    ], className="p-2 m-2"),

    html.Br(), html.Br(),
    # 表单类 ========================================================================================
    dbc.Form(children=[email_input, password_input], className="p-2 m-2 bg-light"),
    dbc.Form(children=[email_input_row, password_input_row], className="p-2 m-2 bg-light"),
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
    ], inline=True, className="p-2 m-2 bg-light"),

    html.Br(), html.Br(),
    # 表单类 ========================================================================================
    html.Div(children=[
        dbc.Label("Slider", html_for="slider"),
        dcc.Slider(min=0, max=9, marks={i: "Label {}".format(i) if i == 1 else str(i) for i in range(1, 6)}, value=5),
        html.Br(),
        dbc.Label("RangeSlider", html_for="range-slider"),
        dcc.RangeSlider(count=1, min=-5, max=10, step=0.5, value=[-3, 7])
    ], className="p-2 m-2"),

    html.Div(children=[
        dbc.Label("Progress", html_for="progress"),
        dbc.Progress(id="progress", value=0, striped=True, animated=True),
        dcc.Interval(id="interval", interval=250, n_intervals=0),
    ], className="p-2 m-2"),
    html.Div(children=[
        radioitems, checklist, radioitems_inline, checklist_inline
    ], className="p-2 m-2"),

    html.Br(), html.Br(),
    # 展示类 ========================================================================================
    dbc.ListGroup(children=[
        dbc.ListGroupItem("ListGroupItem ListGroupItem"),
        dbc.ListGroupItem("Internal link", href="/l/components/list_group"),
        dbc.ListGroupItem("External link", href="https://google.com"),
        dbc.ListGroupItem("Disabled link", href="https://google.com", disabled=True),
        dbc.ListGroupItem("Button", id="button-item", n_clicks=0, action=True),
    ], className="p-2 m-2"),

    dbc.ListGroup(children=[
        dbc.ListGroupItem("The primary item", color="primary"),
        dbc.ListGroupItem("A secondary item", color="secondary"),
        dbc.ListGroupItem("A successful item", color="success"),
        dbc.ListGroupItem("A warning item", color="warning"),
        dbc.ListGroupItem("A dangerous item", color="danger"),
        dbc.ListGroupItem("An informative item", color="info"),
    ], className="p-2 m-2"),

    dbc.ListGroup(children=[
        dbc.ListGroupItem([
            dbc.ListGroupItemHeading("This item has a heading"),
            dbc.ListGroupItemText("And some text underneath"),
        ]),
        dbc.ListGroupItem([
            dbc.ListGroupItemHeading("This item also has a heading"),
            dbc.ListGroupItemText("And some more text underneath too"),
        ]),
    ], className="p-2 m-2"),

    html.Br(), html.Br(),
    # Tab实例 ========================================================================================
    html.Div(children=dbc.Tabs([
        dbc.Tab(tab1_content, label="Tab 1"),
        dbc.Tab(tab2_content, label="Tab 2"),
    ]), className="p-2 m-2"),

    html.Div(children=[
        dbc.Tabs([
            dbc.Tab(label="Tab 1", tab_id="tab-1"),
            dbc.Tab(label="Tab 2", tab_id="tab-2"),
        ], id="tabs", active_tab="tab-1"),
        html.Div(id="content")
    ], className="p-2 m-2"),

    html.Br(), html.Br(),
    # 表格Table ========================================================================================
    html.Div(children=generate_table(df), className="p-2 m-2"),
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
    app.run_server(host="0.0.0.0", debug=True)
