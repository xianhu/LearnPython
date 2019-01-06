# _*_ coding: utf-8 _*_

"""
Dash实例
"""

import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input

from Dash.app import app
from Dash.apps import app1, app2, app3


# 创建布局
app.layout = html.Div([
    # The memory store will always get the default on page refreshes
    dcc.Store(id="memory"),
    # The local store will take the initial data
    # only the first time the page is loaded
    # and keep it until it is cleared.
    dcc.Store(id="local", storage_type="local"),
    # Same as the local store but will lose the data
    # when the browser/tab closes.
    dcc.Store(id="session", storage_type="session"),

    dcc.Location(id="url", refresh=False),
    dbc.Navbar(children=[
        dbc.NavItem(dbc.NavLink("Link", href="#")),
        dbc.DropdownMenu(children=[
            dbc.DropdownMenuItem("Entry 1"),
            dbc.DropdownMenuItem("Entry 2"),
            dbc.DropdownMenuItem(divider=True),
            dbc.DropdownMenuItem("Entry 3")
        ], nav=True, in_navbar=True, label="Menu"),
    ], brand="Demo", brand_href="/", sticky="top", color="light"),
    html.Div(id="page-content")
])


@app.callback(Output("page-content", "children"), [
    Input("url", "pathname")
])
def display_page(pathname):
    if pathname == "/":
        return dbc.Container(children=[
            dcc.Link("Navigate to '/app1'", href="/app1"),
            html.Br(),
            dcc.Link("Navigate to '/app2'", href="/app2"),
            html.Br(),
            dcc.Link("Navigate to '/app3'", href="/app3"),
        ])
    if pathname == "/app1":
        return app1.layout
    elif pathname == "/app2":
        return app2.layout
    elif pathname == "/app3":
        return app3.layout
    else:
        return "404"


if __name__ == "__main__":
    app.run_server(host="0.0.0.0", debug=True)
