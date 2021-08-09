"""
David Grant
2021/07/27
PROJ-009
Manager data analysis portal
"""
import plotly.graph_objects as go
import pandas as pd

# Sales by agent, displayed as a bar graph, sales volume over time
def AgentSales(agentName,startDate,endDate,salesData,bookingData,customerData,agentData):
    # Merge tables by common key
    agentSales = pd.merge(salesData,bookingData,on="BookingId")
    agentSales = agentSales.set_index("CustomerId")
    agentSales = pd.merge(agentSales, customerData, on="CustomerId")
    agentSales = agentSales.set_index("AgentId")
    agentSales = pd.merge(agentSales,agentData,on="AgentId")
    
    # Check if selection by agent name or by all
    if "All" not in agentName:
        agentSales = agentSales.set_index("AgtLastName")
        agentName = agentName.split()[1]
        agentSales = agentSales.loc[agentName]

    # Arrange dataFrame by data and within range of user selection
    agentSales["TripStart"] = agentSales["TripStart"].astype("str")
    agentSales = agentSales.groupby("TripStart").sum()[["BasePrice", "AgencyCommission"]]
    agentSales = agentSales.loc[startDate:endDate]

    # Input data as bar graph
    agentSales = go.Figure(data=[
        go.Bar(x=agentSales.index,y=agentSales["BasePrice"], text=agentSales["BasePrice"], textposition="auto", name="Base Price"),
        go.Bar(x=agentSales.index,y=agentSales["AgencyCommission"], text=agentSales["AgencyCommission"], textposition="auto", name="Agency Commission")])
    agentSales.update_layout(barmode='stack', xaxis_title="Date", yaxis_title="Sales Volume", title="Sales by agent")
    return agentSales