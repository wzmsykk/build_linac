
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
def damping_coefficient(loss, pfd, D):
    """
    Calculate the damping coefficient for a cavity.

    Parameters:
    loss (float): Power loss in watts.
    pfd (float): Power factor density in watts per meter.
    D (float): Cavity length in cm.

    Returns:
    float: Damping coefficient.
    """
    return loss / (pfd * D*2*0.01)  # Convert D from cm to m
# def group_velocity(loss,u):
#     """
#     Calculate the group velocity of a cavity.

#     Parameters:
#     loss (float): Power loss in watts.
#     u (float): Energy stored in the cavity in joules.

#     Returns:
#     float: Group velocity in meters per second.
#     """
#     return loss / u
# def quality_factor(freq,D,u,loss):
#     """
#     Calculate the quality factor of a cavity.

#     Parameters:
#     freq (float): Resonant frequency in MHz.
#     D (float): Cavity length in cm.
#     u (float): Energy stored in the cavity in joules.
#     loss (float): Power loss in watts.

#     Returns:
#     float: Quality factor.
#     """
#     return (freq * 1e6 * D*0.01 * u*2*pi) / loss  # Convert MHz to Hz
if __name__ == "__main__":
    df=pd.read_csv("test/processed_field_data/PROCESSED_FIELD_DATA.csv")
    print(df)
    s=calc_pfd_2pi_3_mode(df)
    D = 3.332360255  # Example cavity length in meters
    print(f"Calculated Power Factor Density (pfd) for 2Pi/3 mode: {s} W/m")
    df2=pd.read_csv("test/processed_field_data/CAVITY_RESULT.csv")
    print(df2)
    # q=quality_factor(df2['Frequency'][0], D, df2['Stored energy'][0], df2['Power dissipation'][0])
    # vg=group_velocity(df2['Power dissipation'][0], df2['Stored energy'][0])
    alpha=damping_coefficient(df2['Power dissipation'][0], s, D)
    # print(f"Quality Factor: {q}")
    # print(f"Group Velocity: {vg} m/s")
    print(f"Damping Coefficient: {alpha} s^-1")
    print(f"Calculated Power Factor Density (pfd): {s} W/m")