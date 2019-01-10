# _*_ coding: utf-8 _*_

"""
导航栏
"""

import dash_html_components as html
import dash_bootstrap_components as dbc
PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"

# 通用组件
nav_item1 = dbc.NavItem(children=dbc.NavLink("首页", href="/"))
nav_item2 = dbc.NavItem(children=dbc.NavLink("app1", href="/app1"))
nav_item3 = dbc.NavItem(children=dbc.NavLink("app2", href="/app2"))
nav_item4 = dbc.NavItem(children=dbc.NavLink("app3", href="/app3"))
nav_item5 = dbc.NavItem(children=dbc.NavLink("app4", href="/app4"))
drop_down = dbc.DropdownMenu(children=[
    dbc.DropdownMenuItem("More", header=True),
    dbc.DropdownMenuItem("Entry app1", href="/app1"),
    dbc.DropdownMenuItem("Entry app2", href="/app2"),
    dbc.DropdownMenuItem(divider=True),
    dbc.DropdownMenuItem("Entry app3", href="/app3"),
    dbc.DropdownMenuItem("Entry app4", href="/app4"),
], nav=True, in_navbar=True, label="Menu")
nav_item_list = [nav_item1, nav_item2, nav_item3, nav_item4, nav_item5, drop_down]

# 定义不同的导航栏
navbar_default = dbc.NavbarSimple(children=nav_item_list, brand="Dash", brand_href="#", sticky="top")

navbar_custom = dbc.Navbar(children=dbc.Container(children=[
    dbc.NavbarBrand("Dash", href="#"),
    # dbc.NavbarToggler(id="navbar-toggler1"),
    dbc.Collapse(children=dbc.Nav(nav_item_list, className="ml-auto", navbar=True), navbar=True),
]))

navbar_logo = dbc.Navbar(children=dbc.Container(children=[
    html.A(dbc.Row(children=[
        dbc.Col(html.Img(src=PLOTLY_LOGO, height="30px")),
        dbc.Col(dbc.NavbarBrand("Dash", className="ml-2")),
    ], align="center", no_gutters=True), href="https://plot.ly"),
    # dbc.NavbarToggler(id="navbar-toggler2"),
    dbc.Collapse(children=dbc.Nav(nav_item_list, className="ml-auto", navbar=True), navbar=True),
]), color="dark", dark=True)

navbar_search = dbc.Navbar(children=dbc.Container(children=[
    dbc.NavbarBrand("Search", href="#"),
    # dbc.NavbarToggler(id="navbar-toggler3"),
    dbc.Collapse(children=dbc.Row(children=[
        dbc.Col(dbc.Input(type="search", placeholder="Search")),
        # set width of button column to auto to allow search box to take up remaining space.
        dbc.Col(dbc.Button("Search", color="primary", className="ml-2"), width="auto"),
    ], align="center", no_gutters=True, className="ml-auto flex-nowrap"), navbar=True),
    # keep button and search box on same row (flex-nowrap).
    # align everything on the right with left margin (ml-auto).
]))
