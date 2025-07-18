
import numpy as np
from math import pi, sqrt
import pandas as pd
def calc_pfd_2pi_3_mode(field_dataframe:pd.DataFrame):###R:cm, ErMV/m, H:A/m
    """Calulate the power factor density (pfd) for a given cavity."""
    # Placeholder for actual pfd calculation logic
    Er= field_dataframe['Er'].to_numpy()* 1e6  # Convert Er from MV/m to V/m
    R= field_dataframe['R'].to_numpy()/100.0  # Convert R from cm to m
    H= field_dataframe['H'].to_numpy()
    
    n=len(R)
    if n<2:
        dr=1.0
    else:
        dr=R[1]-R[0]
    S=0
    for i in range(n):
        S = S + (2*pi*dr/sqrt(3)) * (H[i]*Er[i]*R[i])

    return S  

if __name__ == "__main__":
    df=pd.read_csv("test/processed_field_data/processed_field_data.csv")
    s=calc_pfd_2pi_3_mode(df)
    print(f"Calculated Power Factor Density (pfd) for 2Pi/3 mode: {s} W/m")