# _*_ coding: utf-8 _*_

"""
Dash实例
"""

import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input

from Dash.app import app
from Dash.apps import app1, app2, app3, app4
from Dash.advcom.navbar import nav_item1, nav_item2, drop_down, PLOTLY_LOGO

# 创建布局
app.layout = html.Div([
    # The memory store will always get the default on page refreshes
    dcc.Store(id="memory"),
    # The local store will take the initial data only the first time the page is loaded, and keep it until it is cleared.
    dcc.Store(id="local", storage_type="local"),
    # Same as the local store but will lose the data when the browser/tab closes.
    dcc.Store(id="session", storage_type="session"),

    dcc.Location(id="url", refresh=False),

    # 定义一个较为复杂的导航栏
    dbc.Navbar(children=dbc.Container(children=[
        html.A(dbc.Row(children=[
            dbc.Col(html.Img(src=PLOTLY_LOGO, height="30px")),
            dbc.Col(dbc.NavbarBrand("DashDemo", className="ml-2")),
        ], align="center", no_gutters=True), href="https://plot.ly"),
        dbc.Collapse(children=dbc.Nav([nav_item1, nav_item2, drop_down], navbar=True), navbar=True),
        dbc.Collapse(children=dbc.Row(children=[
            dbc.Col(dbc.Input(type="search", placeholder="Search")),
            dbc.Col(dbc.Button("Search", color="primary", className="ml-2"), width="auto"),
        ], align="center", no_gutters=True, className="ml-auto flex-nowrap"), navbar=True),
    ]), color="light", light=True),
    html.Div(id="page-content"),
])


@app.callback(Output("page-content", "children"), [
    Input("url", "pathname")
])
def display_page(pathname):
    if pathname == "/":
        return dbc.Container(children=[
            dcc.Link("Navigate to '/app1'，布局相关", href="/app1"),
            html.Br(),
            dcc.Link("Navigate to '/app2'，组件相关", href="/app2"),
            html.Br(),
            dcc.Link("Navigate to '/app3'，画图相关", href="/app3"),
            html.Br(),
            dcc.Link("Navigate to '/app4'，dash-table", href="/app4"),
        ])
    if pathname == "/app1":
        return app1.layout
    elif pathname == "/app2":
        return app2.layout
    elif pathname == "/app3":
        return app3.layout
    elif pathname == "/app4":
        return app4.layout
    else:
        return dbc.Container(html.H4("404, page not found", className="text-center pt-5"))


if __name__ == "__main__":
    app.run_server(host="0.0.0.0", debug=True)
