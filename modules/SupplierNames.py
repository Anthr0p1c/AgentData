"""
David Grant
2021/07/27
PROJ-009
Manager data analysis portal
"""

# Return a list of supplier names from dataFrame
def GetSupplierNames(supplierData):
    supplierList=[{"label":"All","value":"All"}]
    for x in supplierData["SupName"]:
        supplierList.append({"label":x,"value":x})
    return supplierList