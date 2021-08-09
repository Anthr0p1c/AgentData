"""
David Grant
2021/07/27
PROJ-009
Manager data analysis portal
"""

import plotly.graph_objects as go
import pandas as pd

# Sales per suppliers
def SupplierSales(supplierName,startDate,endDate,supplierData, productSupplierData, salesData):

    # Check if selection is by supplier name or all
    if "All" not in supplierName: 
        supplierSales = supplierData.loc[supplierData["SupName"]==supplierName]
    else:
        supplierSales = supplierData

    # Merge tables by common keys
    supplierSales = pd.merge(supplierSales, productSupplierData, on="SupplierId")
    supplierSales = supplierSales.set_index("ProductSupplierId")
    supplierSales = pd.merge(supplierSales,salesData,on="ProductSupplierId")

    # Sort dataFrame by data and user selection
    supplierSales["TripStart"] = supplierSales["TripStart"].astype("str")
    supplierSales = supplierSales.groupby("TripStart").sum()[["BasePrice", "AgencyCommission"]]
    supplierSales = supplierSales.loc[startDate:endDate]    

    # Display as bar graph
    supplierSales = go.Figure(data=[
        go.Bar(x=supplierSales.index,y=supplierSales["BasePrice"], text=supplierSales["BasePrice"], textposition="auto", name="Base Price"),
        go.Bar(x=supplierSales.index,y=supplierSales["AgencyCommission"], text=supplierSales["AgencyCommission"], textposition="auto", name="Agency Commission")])
    supplierSales.update_layout(barmode='stack', xaxis_title="Date", yaxis_title="Sales Volume", title="Sales by supplier")
    return supplierSales