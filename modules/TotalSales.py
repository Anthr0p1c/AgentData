"""
David Grant
2021/07/27
PROJ-009
Manager data analysis portal
"""

import plotly.express as px


# Total sales data displayed as line graph, sales volume over time
def TotalSales(startDate,endDate,salesData): 
    # Sort dataFrame by date and user selection
    tempSalesData = salesData
    tempSalesData["TripStart"] = tempSalesData["TripStart"].astype("str")
    totalSales = tempSalesData.groupby("TripStart").sum()[["BasePrice", "AgencyCommission"]]
    totalSales = totalSales.loc[startDate:endDate]

    # Display as line graph
    totalSalesFig = px.line(totalSales, x=totalSales.index, y="BasePrice", title="Total sales over time")
    totalSalesFig.update_layout(xaxis_title="Date", yaxis_title="Total Sales Volume")
    return totalSalesFig
