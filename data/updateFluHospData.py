#mcandrew

import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import datetime
from epiweeks import Week

if __name__ == "__main__":

    apilink = "https://healthdata.gov/resource/g62h-syeh.csv"
    data = pd.read_csv(apilink)

    target = data.loc[:,["state","date","previous_day_admission_influenza_confirmed"]]
    target["date"] = pd.to_datetime(target["date"])
    target["date"] = target["date"] - datetime.timedelta(days=1)
    
    def addCases(x,varin,varout):
        return pd.Series({"{:s}".format(varout):x[varin].sum()})
    natData = target.groupby(["date"]).apply(lambda x: addCases(x,"previous_day_admission_influenza_confirmed","previous_day_admission_influenza_confirmed"))
    natData.index = pd.to_datetime(natData.index)

    natData["EW"]    = [Week.fromdate(_).cdcformat() for _ in natData.index]
    natData["EWiso"] = [Week.fromdate(_).isoformat() for _ in natData.index]
    
    natDataWeekly = natData.groupby(["EW"]).apply( lambda x: addCases(x,"previous_day_admission_influenza_confirmed","previous_day_admission_influenza_confirmed"))

    natDataWeekly["location"] = "US"

    varOrder = ["location","previous_day_admission_influenza_confirmed"]

    natDataWeekly = natDataWeekly[varOrder]
    natDataWeekly.to_csv("./fluHospData.csv",mode="w",header=True,index=True)
    
    for state,stateData in target.groupby(["state"]):
        stateData["EW"]    = [Week.fromdate(_).cdcformat() for _ in stateData["date"]]
        stateData["EWiso"] = [Week.fromdate(_).isoformat() for _ in stateData["date"]]
    
        stateDataWeekly = stateData.groupby(["EW"]).apply( lambda x: addCases(x,"previous_day_admission_influenza_confirmed","previous_day_admission_influenza_confirmed"))

        stateDataWeekly = stateDataWeekly.sort_index()
        stateDataWeekly["location"] = state

        stateDataWeekly = stateDataWeekly[varOrder]
        stateDataWeekly.to_csv("./fluHospData.csv",mode="a",header=False,index=True)
