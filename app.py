"""
David Grant
2021/07/27
PROJ-009
Manager data analysis portal
"""





import dash
import dash_core_components as dcc
from dash_core_components.Dropdown import Dropdown
import dash_html_components as html
from numpy import append, array
from numpy.lib.function_base import average
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from readDB import ReadMongoData as db
from datetime import date
import datetime
from dash.dependencies import Output,Input,State

# Modules
from modules import TotalSales as totalSales
from modules import AgentSales as agentSales
from modules import SupplierSales as supplierSales
from modules import Commissions as commissions
from modules import AgentNames as agentNames
from modules import SupplierNames as supplierNames

# app = dash.Dash("app")
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server




# Sales data from baseprice and agencycommission
salesData = db.getBookingDetails()
salesData[["BasePrice", "AgencyCommission"]] = salesData[[
    "BasePrice", "AgencyCommission"]].astype(str).astype(float)

# Booking data
bookingData = db.getBookings()

# Agent data
agentData = db.getAgents()

# Customer data
customerData = db.getCustomers()

# Supplier data
supplierData = db.getSuppliers()

# Product Supplier data
productSupplierData = db.getProductsSuppliers()





# Dash html for selection menus
app.layout = html.Div([
    html.Div(
        className=("dropGraph"),
        children=[
            html.P('Travel Experts Manager Portal')
        ]),
    html.Div(
        className=("row"),
        children=[
            html.Div(
                className=("left"),
                children=[
                    html.Label(["Data type: "]),
                ]),
            html.Div(
                className=("center"),
                children=[
                    # Data type dropdown menu
                    dcc.Dropdown(
                        id="dropDown",
                        options=[
                            {'label': 'Total Sales And Commissions', 'value': "totalSales"},
                            {'label': 'Sales By Agents', 'value': "agentSales"},
                            {'label': 'Sales By Supplier', 'value': "supplierSales"},
                            {"label": "Total and Average Commissions", "value": "commissions"}
                ],
                    value="totalSales"),
        ]),
            html.Br(),
            html.Div(
                className=("row"),
                children=[
                    html.Div(
                        className=("left"),
                        children=[
                            html.Label(["Selection: "]),
                        ]),
                        html.Div(
                            className=("center"),
                            children=[
                                dcc.Dropdown(
                                    # Agent names from module
                                    id="agentDropDown",
                                    options=agentNames.GetAgentNames(agentData),
                                    value="All"
                                )
                            ]),
                ],
            ),
            html.Div(
                className="row",
                children=[
                    html.Div(
                        className=("left"),
                        children=[
                            html.Label(["Date: "]),
                        ]),
                    html.Div(
                        className=("center"),
                        children=[
                            # Date selection
                            dcc.DatePickerRange(
                                id='my-date-picker-range',
                                min_date_allowed=date(1995, 8, 5),
                                max_date_allowed=date(2022, 8, 5),
                                initial_visible_month=date(2021, 8, 5),
                                start_date=date(1995, 8, 5),
                                end_date=date(2022, 8, 5)
                            ),
                            html.Div(id='output-container-date-picker-range')
                        ]),
                    ])
        ]
    ),
    html.Br(),
    html.Div(
        className="dropGraph",
        children=[
        # Graph placeholder
        dcc.Graph(
            className="dropGraph-center",
            figure={},
            id='graph1',
        )]
    )
])





# Callbacks from selection changes - Update selection menu with either agent names or supplier names
@app.callback(
    Output("agentDropDown", "options"),
    Input("dropDown", "value")
)
def update_dropDown(dropDown):
    if dropDown=="agentSales":
        return agentNames.GetAgentNames(agentData)
    elif dropDown=="supplierSales":
        return supplierNames.GetSupplierNames(supplierData)
    else:
        return [{"label": "All", "value": "All"}]

# Callbacks from selection changes - Display graph based on selection
@app.callback(
    Output('graph1', 'figure'),
    [Input("dropDown", "value"),
     Input("agentDropDown", "value"),
     Input('my-date-picker-range', 'start_date'),
     Input('my-date-picker-range', 'end_date')]
)
def update_output(dropDown, agentDropDown, start_date, end_date):
    if start_date is not None:
        start_date_object = start_date
    if end_date is not None:
        end_date_object = end_date
    if dropDown=="totalSales":
        selectGraph=totalSales.TotalSales(start_date_object, end_date_object,salesData)
    elif dropDown=="agentSales":
        selectGraph=agentSales.AgentSales(agentDropDown, start_date_object, end_date_object,salesData,bookingData,customerData,agentData)
    elif dropDown=="supplierSales":
        selectGraph=supplierSales.SupplierSales(agentDropDown, start_date_object, end_date_object,supplierData, productSupplierData, salesData)
    else:
        selectGraph=commissions.Commissions(start_date_object, end_date_object,salesData)
    return selectGraph


    


if __name__ == '__main__':
    app.run_server(debug=False)