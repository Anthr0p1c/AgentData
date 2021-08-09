"""
David Grant
2021/07/27
PROJ-009
Manager data analysis portal
"""

# Return a list of agent first and last names from dataFrame
def GetAgentNames(agentData):
    agentList=[{"label":"All","value":"All"}]
    fname = []
    lname = []
    for x in agentData["AgtFirstName"]:
        fname.append(x)
    for x in agentData["AgtLastName"]:
        lname.append(x)
    for x in range(len(fname)):
        name = fname[x] + " " + lname[x]
        agentList.append({"label":name,"value":name})
    return agentList