"""
David Grant
2021/07/27
PROJ-009
Manager data analysis portal
"""

import plotly.graph_objects as go
import pandas as pd
import dash_table
from datetime import date

# Return table of popular packages
def PopularPackages(packagesData):
    name = []
    startDate = []
    endDate = []
    description = []
    basePrice = []
    agencyCommission = []

    # Convert dec128 to float
    packagesData["PkgBasePrice"] = packagesData["PkgBasePrice"].astype(str).astype(float)
    packagesData["PkgAgencyCommission"] = packagesData["PkgAgencyCommission"].astype(str).astype(float)

    for x in packagesData["PkgName"]:
        name.append(x)
    for x in packagesData["PkgStartDate"]:
        startDate.append(x)
    for x in packagesData["PkgEndDate"]:
        endDate.append(x)
    for x in packagesData["PkgDesc"]:
        description.append(x)
    for x in packagesData["PkgBasePrice"]:
        basePrice.append(x)
    for x in packagesData["PkgAgencyCommission"]:
        agencyCommission.append(x)

    # Create table with packages data
    packagesList = go.Figure(data=[
        go.Table(header=dict(values=['Package Name', 'Start Date', 'End Date', 'Description', 'Base Price', 'Agency Commission']),
                 cells=dict(values=[name,pd.to_datetime(startDate),pd.to_datetime(endDate),description,basePrice,agencyCommission]))
    ])
    return packagesList