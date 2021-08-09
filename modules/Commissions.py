"""
David Grant
2021/07/27
PROJ-009
Manager data analysis portal
"""

import plotly.graph_objects as go
import pandas as pd

# Total and average commission displayed as a pie chart
def Commissions(startDate,endDate,salesData):
    # Sort dataFrame by data and user selection
    commissions = salesData
    commissions["TripStart"] = commissions["TripStart"].astype("str")
    commissions = commissions.groupby("TripStart").sum()[["AgencyCommission"]]
    commissions = commissions.loc[startDate:endDate]
    commissions = commissions["AgencyCommission"]

    # Get total and average commissions
    totalCommission = 0
    averageCommission = 0
    for x in commissions:
        totalCommission += x
    averageCommission = totalCommission / len(commissions)

    # Display as pie chart
    commissions = go.Figure(data=[
        go.Pie(labels=["Total Commission","Average Commission"],values=[int(totalCommission),int(averageCommission)],
        )
    ])
    commissions.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=20)
    return commissions