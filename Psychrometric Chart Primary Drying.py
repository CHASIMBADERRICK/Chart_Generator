# -*- coding: utf-8 -*-
"""
Created on Wed Sep 15 22:11:01 2021

@author: derrick
"""

  
''' This is a translated version of the visual basic psych function in
 our xls template to a python code function psychropy()
 The function and subfunctions defined herein come with no warranty or
 certification of fitness for any purpose
 Do not use these functions for conditions outside boundaries defined
 by their original sources.
 Subfunctions use equations from the following sources:
    ASHRAE Fundamentals, 2005, SI Edition
    Singh et al. "Numerical Calculations of Psychrometric Properties
        on a Calculator". Building and Environment, 37, 2002.
 The function will calculate various properties of moist air. Properties
 calculated include Wet Bulb, Dew Point, Relative Humidity, Humidity
 Ratio, Vapor Pressure, Degree of Saturation, enthalpy, specific volume
 of dry air, and moist air density.
 The function requires input of: barometric pressure, and two other
 parameters, We recomend that one of these be Tdb and if not using that
 the other two must be h and HR.  These parameters along with Tdb can
 be Twb, DP, RH, or two mentioned previously.
 Sytax for function as follows:
 psych(P,intype0,invalue0,intype1,invalue1,outtype,unittype)
 Where:
 P is the barometric pressure in PSI or Pa .
 intypes     indicator string for the corresponding
                     invalue parameter (ie Tdb, RH etc.)
 invalues    is the actual value associated with the type of parameter
                     (ie value of Wet bulb, Dew point, RH, or Humidity
                     Ratio etc.)
 outType     indicator string for the corresponding invalue parameter
 unittype    is the optional unit selector.  Imp for Imperial, SI for
                     SI.  Imp is default if omitted.
 valid intypes:
 Tdb    Dry Bulb Temp            F or C                       Valid for Input
  *** it is highly Recommended Tdb be used as an input (can only
              output/not use, if both other inputs are h and HR)
 Twb    Web Bulb Temp            F or C                       Valid for Input
 DP     Dew point                F or C                       Valid for input
 RH     RH                       between 0 and 1              Valid for input
 W      Humidity Ratio           Mass Water/ Mass Dry Air     Valid for input
 h      Enthalpy                 BTU/lb dry air or kJ/kg DA   Valid for input
  ***Warning 0 state for Imp is ~0F, 0% RH ,and  1 ATM, 0 state
              for SI is 0C, 0%RH and 1 ATM
 valid outtypes:
 Tdb    Dry Bulb Temp            F or C                       Valid for Input
   ***it is highly Recommended Tdb be used as an input (can only
              output/not use, if both other inputs are h and HR)
 Twb    Web Bulb Temp            F or C                       Valid for Input
 DP     Dew point                F or C                       Valid for input
 RH     Relative Humidity        between 0 and 1              Valid for input
 W      Humidity Ratio           Mass Water/ Mass Dry Air     Valid for input
 h      Enthalpy                 BTU/lb dry air or kJ/kg DA   Valid for input
   ***Warning 0 state for Imp is ~0F, 0% RH ,and  1 ATM, 0 state
               for SI is 0C, 0%RH and 1 ATM
 WVP    Water Vapor Pressure     PSI or Pa
 Dsat   Degree of Saturation     between 0 and 1
 s      NOT VALID, Should be entropy
 SV     Specific Volume          ft^3/lbm or m^3/kg dry air
 MAD    Moist Air Density        lb/ft^3 or kg/m^3 (I changed this unit on 15 Sep 2021 at 2155hrs)
 The corresponding numbers associated with the types in the excel VB program:
 The Numbers for inType and outType are
 1 Web Bulb Temp            F or C                        Valid for Input
 2 Dew point                F or C                        Valid for input
 3 RH                       between 0 and 1               Valid for input
 4 Humidity Ratio           Mass Water/ Mass Dry Air      Valid for input
 5 Water Vapor Pressure     PSI or Pa
 6 Degree of Saturation     between 0 and 1
 7 Enthalpy                 BTU/lb dry air or kJ/kg dry air
     Warning 0 state for IP is ~0F, 0% RH ,and  1 ATM, 0 state
              for SI is 0C, 0%RH and 1 ATM
 8 NOT VALID, Should be entropy
 9 Specific Volume          ft**3/lbm or m**3/kg dry air
 10 Moist Air Density       lb/ft**3 or m**3/kg"""
 this python version adds the capability to use Enthalpy in the place of Tdb
 modified Syntax to be psychro(p,in0type,in0,in1type,in1,outtype,units)
 where p is pressure
 in0type is the type of the first input variable
 in0 is the value
 in1type is the type of the first input variable
 in1 is the value
 outtype is the type for the output variable
 units is the specified units (ie Imp or SI)
 '''

import math
import pandas as pd
from pandas import DataFrame, Series
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('seaborn-whitegrid')
import warnings
from labellines import labelLine, labelLines #Used for plotting inline labels
from textwrap import wrap



def Part_press(P, W):
    ''' Function to compute partial vapor pressure in [kPa]
        From page 6.9 equation 38 in ASHRAE Fundamentals handbook (2005)
            P = ambient pressure [kPa]
            W = humidity ratio [kg/kg dry air]
    '''
    result = P * W / (0.62198 + W)
    return result


def Sat_press(Tdb):
    ''' Function to compute saturation vapor pressure in [kPa]
        ASHRAE Fundamentals handbood (2005) p 6.2, equation 5 and 6
            Tdb = Dry bulb temperature [degC]
            Valid from -100C to 200 C
    '''

    C1 = -5674.5359
    C2 = 6.3925247
    C3 = -0.009677843
    C4 = 0.00000062215701
    C5 = 2.0747825E-09
    C6 = -9.484024E-13
    C7 = 4.1635019
    C8 = -5800.2206
    C9 = 1.3914993
    C10 = -0.048640239
    C11 = 0.000041764768
    C12 = -0.000000014452093
    C13 = 6.5459673

    TK = Tdb + 273.15  # Converts from degC to degK
    #    print(isinstance(Tdb, (DataFrame, Series)))
    if isinstance(Tdb, (DataFrame, Series, np.ndarray)):
        result = Tdb.copy() * 0
        less_zero = TK <= 273.15
        greater_zero = TK > 273.15

        result[less_zero] = np.exp(
            C1 / TK[less_zero] + C2 + C3 * TK[less_zero] + C4 * TK[less_zero] ** 2 + C5 * TK[less_zero] ** 3 +
            C6 * TK[less_zero] ** 4 + C7 * np.log(TK[less_zero])) / 1000

        result[greater_zero] = np.exp(
            C8 / TK[greater_zero] + C9 + C10 * TK[greater_zero] + C11 * TK[greater_zero] ** 2 + C12 * TK[
                greater_zero] ** 3 +
            C13 * np.log(TK[greater_zero])) / 1000

    else:

        if TK <= 273.15:
            result = math.exp(C1 / TK + C2 + C3 * TK + C4 * TK ** 2 + C5 * TK ** 3 +
                              C6 * TK ** 4 + C7 * math.log(TK)) / 1000
        else:
            result = math.exp(C8 / TK + C9 + C10 * TK + C11 * TK ** 2 + C12 * TK ** 3 +
                              C13 * math.log(TK)) / 1000
    return result


def Hum_rat(Tdb, Twb, P):
    ''' Function to calculate humidity ratio [kg H2O/kg air]
        Given dry bulb and wet bulb temp inputs [degC]
        ASHRAE Fundamentals handbood (2005)
            Tdb = Dry bulb temperature [degC]
            Twb = Wet bulb temperature [degC]
            P = Ambient Pressure [kPa]
    '''

    Pws = Sat_press(Twb)
    Ws = 0.62198 * Pws / (P - Pws)  # Equation 23, p6.8

    if isinstance(Tdb, (DataFrame, Series, np.ndarray)) and isinstance(Twb, (DataFrame, Series, np.ndarray)):
        result = Tdb.copy() * 0
        greater_zero = Tdb >= 0
        less_zero = Tdb < 0

        result[greater_zero] = (((2501 - 2.326 * Twb[greater_zero]) * Ws[greater_zero] - 1.006 * (
                Tdb[greater_zero] - Twb[greater_zero])) /
                                (2501 + 1.86 * Tdb[greater_zero] - 4.186 * Twb[greater_zero]))  # Equation 35, p6.9

        result[less_zero] = (
                ((2830 - 0.24 * Twb[less_zero]) * Ws[less_zero] - 1.006 * (Tdb[less_zero] - Twb[less_zero])) /
                (2830 + 1.86 * Tdb[less_zero] - 2.1 * Twb[less_zero]))  # Equation 37, p6.9

    else:
        if Tdb >= 0:  # Equation 35, p6.9
            result = (((2501 - 2.326 * Twb) * Ws - 1.006 * (Tdb - Twb)) /
                      (2501 + 1.86 * Tdb - 4.186 * Twb))
        else:  # Equation 37, p6.9
            result = (((2830 - 0.24 * Twb) * Ws - 1.006 * (Tdb - Twb)) /
                      (2830 + 1.86 * Tdb - 2.1 * Twb))
    return result


def Hum_rat2(Tdb, RH, P):
    ''' Function to calculate humidity ratio [kg H2O/kg air]
        Given dry bulb and wet bulb temperature inputs [degC]
        ASHRAE Fundamentals handbood (2005)
            Tdb = Dry bulb temperature [degC]
            RH = Relative Humidity [Fraction or %]
            P = Ambient Pressure [kPa]
    '''
    Pws = Sat_press(Tdb)
    result = 0.62198 * RH * Pws / (P - RH * Pws)  # Equation 22, 24, p6.8
    return result


def Rel_hum(Tdb, Twb, P):
    ''' Calculates relative humidity ratio
        ASHRAE Fundamentals handbood (2005)
            Tdb = Dry bulb temperature [degC]
            Twb = Wet bulb temperature [degC]
            P = Ambient Pressure [kPa]
    '''

    W = Hum_rat(Tdb, Twb, P)
    result = Part_press(P, W) / Sat_press(Tdb)  # Equation 24, p6.8
    return result


def Rel_hum2(Tdb, W, P):
    ''' Calculates the relative humidity given:
            Tdb = Dry bulb temperature [degC]
            P = ambient pressure [kPa]
            W = humidity ratio [kg/kg dry air]
    '''

    Pw = Part_press(P, W)
    Pws = Sat_press(Tdb)
    result = Pw / Pws
    return result


def Wet_bulb(Tdb, RH, P):
    ''' Calculates the Wet Bulb temp given:
            Tdb = Dry bulb temperature [degC]
            RH = Relative humidity ratio [Fraction or %]
            P = Ambient Pressure [kPa]
        Uses Newton-Rhapson iteration to converge quickly
    '''

    W_normal = Hum_rat2(Tdb, RH, P)
    result = Tdb

    ' Solves to within 0.001% accuracy using Newton-Rhapson'
    # Hum_Rate(Tdb, Twb, P)
    W_new = Hum_rat(Tdb, result, P)

    if isinstance(Tdb, (DataFrame, Series, np.ndarray)) and isinstance(RH, (DataFrame, Series, np.ndarray)):
        if isinstance(Tdb, np.ndarray):
            remaining_idx = np.where(Tdb != None)[0]
            # remaining_idx = np.ones(Tdb.shape, dtype=bool)
        else:
            remaining_idx = Tdb.index

        result = Tdb.copy()
        i = 0
        while remaining_idx.size > 0:
            if i == 8:
                warnings.warn("Wet bulb convergence taking longer than usual. Something *might* be wrong")
            W_new2 = Hum_rat(Tdb[remaining_idx], result[remaining_idx] - 0.001, P)
            dw_dtwb = (W_new[remaining_idx] - W_new2) / 0.001
            result[remaining_idx] -= (W_new[remaining_idx] - W_normal[remaining_idx]) / dw_dtwb
            W_new[remaining_idx] = Hum_rat(Tdb[remaining_idx], result[remaining_idx], P)

            remaining_idx = np.where(np.abs((W_new - W_normal) / W_normal) > 0.00001)[0]
            i += 1
            # remaining_idx = (np.abs(W_new - W_normal) / W_normal) > 0.00001

    else:
        while abs((W_new - W_normal) / W_normal) > 0.00001:
            W_new2 = Hum_rat(Tdb, result - 0.001, P)
            dw_dtwb = (W_new - W_new2) / 0.001
            result = result - (W_new - W_normal) / dw_dtwb
            W_new = Hum_rat(Tdb, result, P)

    return result


def Enthalpy_Air_H2O(Tdb, W):
    ''' Calculates enthalpy in kJ/kg (dry air) given:
            Tdb = Dry bulb temperature [degC]
            W = Humidity Ratio [kg/kg dry air]
        Calculations from 2005 ASHRAE Handbook - Fundamentals - SI P6.9 eqn 32
    '''

    result = 1.006 * Tdb + W * (2501 + 1.86 * Tdb)
    return result


def T_drybulb_calc(h, W):
    ''' Calculates dry bulb Temp in deg C given:
            h = enthalpy [kJ/kg K]
            W = Humidity Ratio [kg/kg dry air]
        back calculated from enthalpy equation above
        ***Warning 0 state for Imp is ~0F, 0% RH ,and  1 ATM, 0 state
              for SI is 0C, 0%RH and 1 ATM
    '''
    result = (h - (2501 * W)) / (1.006 + (1.86 * W))
    return result


def Dew_point(P, W):
    ''' Function to compute the dew point temperature (deg C)
        From page 6.9 equation 39 and 40 in ASHRAE Fundamentals handbook (2005)
            P = ambient pressure [kPa]
            W = humidity ratio [kg/kg dry air]
        Valid for Dew Points less than 93 C
    '''

    C14 = 6.54
    C15 = 14.526
    C16 = 0.7389
    C17 = 0.09486
    C18 = 0.4569
    Pw = Part_press(P, W)
    alpha = np.log(Pw)
    Tdp1 = C14 + C15 * alpha + C16 * alpha ** 2 + C17 * alpha ** 3 + C18 * Pw ** 0.1984
    Tdp2 = 6.09 + 12.608 * alpha + 0.4959 * alpha ** 2

    if isinstance(Tdp1, (DataFrame, Series, np.ndarray)) and isinstance(Tdp2, (DataFrame, Series, np.ndarray)):
        # Make zero matrix of correct size
        result = np.zeros(Tdp1.shape)

        # Get indexes where Tdp is above freezing, then assign the answer
        Tdp1_index = np.where(Tdp1 >= 0)
        result[Tdp1_index] = Tdp1[Tdp1_index]

        # Get indexes where Tdp is below freezing, then assign the answer
        Tdp2_index = np.where(Tdp1 < 0)
        result[Tdp2_index] = Tdp2[Tdp2_index]

    else:
        if Tdp1 >= 0:
            result = Tdp1
        else:
            result = Tdp2
    return result


def Dry_Air_Density(P, Tdb, W):
    ''' Function to compute the dry air density (kg_dry_air/m**3), using pressure
        [kPa], temperature [C] and humidity ratio
        From page 6.8 equation 28 ASHRAE Fundamentals handbook (2005)
        [rho_dry_air] = Dry_Air_Density(P, Tdb, w)
        Note that total density of air-h2o mixture is:
        rho_air_h2o = rho_dry_air * (1 + W)
        gas constant for dry air
    '''

    R_da = 287.055
    result = 1000 * P / (R_da * (273.15 + Tdb) * (1 + 1.6078 * W))
    return result


def psych(P, in0Type, in0Val, in1Type, in1Val, outType, unitType='SI', index=None):
    '''
    Input Parameters: 
Enter Pressure in Pa, Enter Input Value Types in ' ' and value after comma.
Twb,DP,RH,W,h,Tdb,DP,h,WVP,Dsat,SV,MAD
Enter Output type in ' '. Enter 'SI'.

Twb    Web Bulb Temp            F or C                       Valid for Input
 DP     Dew point                F or C                       Valid for input
 RH     RH                       between 0 and 1              Valid for input
 W      Humidity Ratio           Mass Water/ Mass Dry Air     Valid for input
 h      Enthalpy                 BTU/lb dry air or kJ/kg DA   Valid for input
  ***Warning 0 state for Imp is ~0F, 0% RH ,and  1 ATM, 0 state
              for SI is 0C, 0%RH and 1 ATM
 valid outtypes:
 Tdb    Dry Bulb Temp            F or C                       Valid for Input
   ***it is highly Recommended Tdb be used as an input (can only
              output/not use, if both other inputs are h and HR)
 Twb    Web Bulb Temp            F or C                       Valid for Input
 DP     Dew point                F or C                       Valid for input
 RH     Relative Humidity        between 0 and 1              Valid for input
 W      Humidity Ratio           Mass Water/ Mass Dry Air     Valid for input
 h      Enthalpy                 BTU/lb dry air or kJ/kg DA   Valid for input
   ***Warning 0 state for Imp is ~0F, 0% RH ,and  1 ATM, 0 state
               for SI is 0C, 0%RH and 1 ATM
 WVP    Water Vapor Pressure     PSI or Pa
 Dsat   Degree of Saturation     between 0 and 1
 s      NOT VALID, Should be entropy
 SV     Specific Volume          ft^3/lbm or m^3/kg dry air
 MAD    Moist Air Density 
    '''
    isAPanda = False
    # Check if dataframe or series then change into ndarray
    # Also save the index and ensure floats.

    if isinstance(in0Val, (DataFrame, Series, np.ndarray)):
        if not isinstance(in0Val, np.ndarray):
            in0Val = in0Val.to_numpy().astype(
                float)  # In the future, we probably don't want to overwrite this variable.
            isAPanda = True
        else:
            in0Val = in0Val.astype(float)
            isANumpy = True

    if isinstance(in1Val, (DataFrame, Series, np.ndarray)):
        if not isinstance(in1Val, np.ndarray):
            in1Val = in1Val.to_numpy().astype(
                float)  # In the future, we probably don't want to overwrite this variable.
            isAPanda = True
        else:
            in1Val = in1Val.astype(float)
            isANumpy = True

    if type(in0Val) != type(in1Val):
        warnings.warn("Input data types do not match, this may cause weird results")

    if in0Type != 'h' and in0Type != 'W' and in0Type != 'Tdb':
        outVal = 'NAN'
    elif in0Type == in1Type:
        outVal = 'NAN'

    if unitType == 'SI':
        P = P / 1000  # converts P to kPa
        if in0Type == 'Tdb':  # assign the first input
            Tdb = in0Val
        elif in0Type == 'W':
            W = in0Val
        elif in0Type == 'h':
            h = in0Val

        if in1Type == 'Tdb':  # assign the second input
            Tdb = in1Val
        elif in1Type == 'Twb':
            Twb = in1Val
        elif in1Type == 'DP':
            Dew = in1Val
        elif in1Type == 'RH':
            RH = in1Val
        elif in1Type == 'W':
            W = in1Val
        elif in1Type == 'h':
            h = in1Val
    else:  # converts to SI if not already
        P = (P * 4.4482216152605) / (0.0254 ** 2 * 1000)
        if in0Type == 'Tdb':
            Tdb = (in0Val - 32) / 1.8
        elif in0Type == 'W':
            W = in0Val
        elif in0Type == 'h':
            h = ((in0Val * 1.055056) / 0.45359237) - 17.884444444

        if in1Type == 'Tdb':
            Tdb = (in1Val - 32) / 1.8
        elif in1Type == 'Twb':
            Twb = (in1Val - 32) / 1.8
        elif in1Type == 'DP':
            Dew = (in1Val - 32) / 1.8
        elif in1Type == 'RH':
            RH = in1Val
        elif in1Type == 'W':
            W = in1Val
        elif in1Type == 'h':
            h = ((in1Val * 1.055056) / 0.45359237) - 17.884444444

    if in0Type == 'h' and in1Type == 'W':  # calculate Tdb if not given
        Tdb = T_drybulb_calc(h, W)
    elif in0Type == 'W' and in1Type == 'h':
        Tdb = T_drybulb_calc(h, W)

    if outType == 'RH' or outType == 'Twb':  # Find RH
        if in1Type == 'Twb':  # given Twb
            RH = Rel_hum(Tdb, Twb, P)
        elif in1Type == 'DP':  # given Dew
            RH = Sat_press(Dew) / Sat_press(Tdb)
        # elif in1Type == 'RH':                   # given RH
        # RH already Set
        elif in1Type == 'W':  # given W
            RH = Part_press(P, W) / Sat_press(Tdb)
        elif in1Type == 'h':
            W = (1.006 * Tdb - h) / (-(2501 + 1.86 * Tdb))
            RH = Part_press(P, W) / Sat_press(Tdb)

    else:
        if in0Type != 'W':  # Find W
            if in1Type == 'Twb':  # Given Twb
                W = Hum_rat(Tdb, Twb, P)
            elif in1Type == 'DP':  # Given Dew
                W = 0.621945 * Sat_press(Dew) / (P - Sat_press(Dew))
                ' Equation taken from eq 20 of 2009 Fundemental chapter 1'
            elif in1Type == 'RH':  # Given RH
                W = Hum_rat2(Tdb, RH, P)
            # elif in1Type == 'W':               # Given W
            # W already known
            elif in1Type == 'h':  # Given h
                W = (1.006 * Tdb - h) / (-(2501 + 1.86 * Tdb))
                ' Algebra from 2005 ASHRAE Handbook - Fundamentals - SI P6.9 eqn 32'
        else:
            print('invalid input varilables')

    # P, Tdb, and W are now availible

    if outType == 'Tdb':
        outVal = Tdb
    elif outType == 'Twb':  # Request Twb
        outVal = Wet_bulb(Tdb, RH, P)
    elif outType == 'DP':  # Request Dew
        outVal = Dew_point(P, W)
    elif outType == 'RH':  # Request RH
        outVal = RH
    elif outType == 'W':  # Request W
        outVal = W
    elif outType == 'WVP':  # Request Pw
        outVal = Part_press(P, W) * 1000
    elif outType == "DSat":  # Request deg of sat
        outVal = W / Hum_rat2(Tdb, 1, P)
        'the middle arg of Hum_rat2 is suppose to be RH.  RH is suppose to be 100%'
    elif outType == 'h':  # Request enthalpy
        outVal = Enthalpy_Air_H2O(Tdb, W)
    elif outType == 's':  # Request entropy
        outVal = 5 / 0
        'don\'t have equation for Entropy, so I divided by zero to induce an error.'
    elif outType == 'SV':  # Request specific volume
        outVal = 1 / (Dry_Air_Density(P, Tdb, W))
    elif outType == 'MAD':  # Request density
        outVal = Dry_Air_Density(P, Tdb, W) * (1 + W)

    if unitType == 'Imp':  # Convert to Imperial units
        if outType == 'Tdb' or outType == 'Twb' or outType == 'DP':
            outVal = 1.8 * outVal + 32
        elif outType == 'WVP':
            outVal = outVal * 0.0254 ** 2 / 4.448230531
        elif outType == 'h':
            outVal = (outVal + 17.88444444444) * 0.45359237 / 1.055056
        elif outType == 'SV':
            outVal = outVal * 0.45359265 / ((12 * 0.0254) ** 3)
        elif outType == 'MAD':
            outVal = outVal * (12 * 0.0254) ** 3 / 0.45359265

    if isAPanda:
        outVal = pd.Series(outVal)
        if index is not None:
            try:
                outVal.index = index
            except Exception as exp:
                print("Error occurred when setting index to output: {}".format(str(exp)))

    return outVal


db_temp_start=0
db_temp_end=60

w_start=0
w_end=0.025


pressure=101500 #average atmospheric pressure in Naivasha

 # *************************************************************************
    # Independent variables for curve creation
rh_data= np.zeros(((db_temp_end - db_temp_start), 15))*np.nan #initialize an array to hold temperature and RH values. 100 rows and 11 columns (10 RH values and 1 temperature column)

#print (rh_data)

for db_temp in range(db_temp_start,db_temp_end+1):#arrange dry bulb temp from start to end and loop
    rh_data[db_temp-1,0]=db_temp
    
    for rh_value in range(10, 101, 10):#default was range(10, 101, 10)# RH lines
        
        rh_data[db_temp-1,int(rh_value/10)] =(psych(pressure, 'Tdb', db_temp, 'RH', rh_value/100 , 'W','SI'))
       

# Enthalpy lines
h_data = np.zeros(((db_temp_end - db_temp_start)*10, 15))*np.nan #initialize array to hold Enthalpy values 600 by 15 matrix
enthalpy_array = np.linspace(db_temp_start,db_temp_end,500)

for h_value in range(len(enthalpy_array)):
    h_data[h_value-1,0]=enthalpy_array[h_value]
    
    for h in range(10,111,10):
        h_data[h_value-1,int(h/10)] =(psych(pressure, 'Tdb', enthalpy_array[h_value], 'h', h , 'W','SI'))

# # Plotting
fig = plt.figure()
ax = plt.axes
ax = fig.add_subplot(111)
ax.grid(False)

rh_list = ["10%", "20%", "30%", "40%" , "RH=50%","60%" , "70%", "", "90%"]
h_list = ["10","20","30","40","50","60","70","80","Enthalpy = 90kJ/kg","100","110"]

for p in range(1,10):#start at 1 finish at 9
    
    ax.plot(rh_data[:,0], rh_data[:,p],color='skyblue',label=str(rh_list[p-1]),linewidth=0.8)
    #plt.plot(rh_data[:,0], rh_data[:,p], '0.5', linewidth=1)
    plt.plot(rh_data[:,0], rh_data[:,10],'skyblue', linewidth=1)
    #ax.plot(h_data[:,0], h_data[:,p], color='orange', label=str(h_list[p-1]),linewidth=1)


    
ax.plot(h_data[8:,0], h_data[8:,1], color='orange', label=str(h_list[0]),linewidth=1)  
ax.plot(h_data[47:,0], h_data[47:,2], color='orange', label=str(h_list[1]),linewidth=1)
ax.plot(h_data[85:,0], h_data[85:,3], color='orange', label=str(h_list[2]),linewidth=1)
ax.plot(h_data[118:,0], h_data[118:,4], color='orange', label=str(h_list[3]),linewidth=1)
ax.plot(h_data[147:,0], h_data[147:,5], color='orange', label=str(h_list[4]),linewidth=1)
ax.plot(h_data[172:,0], h_data[172:,6], color='orange', label=str(h_list[5]),linewidth=1)
ax.plot(h_data[195:,0], h_data[195:,7], color='orange', label=str(h_list[6]),linewidth=1)
ax.plot(h_data[215:,0], h_data[215:,8], color='orange', label=str(h_list[7]),linewidth=1)
ax.plot(h_data[233:,0], h_data[233:,9], color='orange', label=str(h_list[8]),linewidth=1)
ax.plot(h_data[27:,0], h_data[27:,10], color='orange', label=str(h_list[9]),linewidth=1)
ax.plot(h_data[27:,0], h_data[27:,11], color='orange', label=str(h_list[10]),linewidth=1)

labelLines(plt.gca().get_lines(), zorder=3)


    
    
plt.xlabel('Dry Bulb Temperature (\u00B0C)')
plt.ylabel('W (kg water / kg dry air)', rotation='vertical')

ax.yaxis.set_label_position("right")
ax.yaxis.tick_right()
title = ax.set_title("\n".join(wrap("Psychrometric " 
                                    "chart primary drying of macadamia nuts",55)))
plt.gca().xaxis.set_major_locator(plt.MultipleLocator(5))
# plt.text(50.3, 168.1, "Set Point")
ax.plot(25,0.014,marker=".",markersize=5,color="red") #point 1
ax.plot(32,0.01864,marker=".",markersize=5,color="red") # point 2
ax.plot(40,0.01864,marker=".",markersize=5,color="red") #point 3
ax.plot(35,0.020668,marker=".",markersize=5,color="red") #point 4


#plot dryer design lines
ax.plot([25,35],[0.013898,0.020668],color='magenta') 
ax.plot([32,40],[0.01864,0.01864],color='magenta')
ax.plot([35,40],[0.020668,0.01864],color='magenta')


#Plot Temperature Lines
for db_temp in range (0,61,5):
    ax.plot([db_temp,db_temp],[db_temp_start,psych(pressure, 'Tdb', db_temp, 'RH', 1 , 'W','SI')],color='0.1',linewidth=0.2)

    
# Humidity Ratio Lines
# for W in range (0,11,1):
#     my_h = psych(pressure, 'RH', 1, 'W', W/1000 , 'h','SI')
#     my_dry_bulb=T_drybulb_calc(my_h, W/1000)
#     ax.plot([my_dry_bulb,db_temp_end],[W/1000,W/1000],color='0.1',linewidth=0.2)

ax.plot([4,db_temp_end],[5/1000,5/1000],color='0.1',linewidth=0.2) 
ax.plot([14,db_temp_end],[10/1000,10/1000],color='0.1',linewidth=0.2) 
ax.plot([20.2,db_temp_end],[15/1000,15/1000],color='0.1',linewidth=0.2) 
ax.plot([24.9,db_temp_end],[20/1000,20/1000],color='0.1',linewidth=0.2) 
# Label of the points

plt.text(25.5,0.0135, "1",color="red")
plt.text(29.7,0.01804, "2",color="red")
plt.text(40.5,0.0178, "3",color="red")
plt.text(33.2,0.020668, "4",color="red")
# fig.tight_layout()
title.set_y(1.05)
fig.subplots_adjust(top=0.8)


plt.ylim(0,0.025)
plt.xlim(0,60)

# plt.xlabel('Tdb ($^\circ$C)')
# plt.ylabel('W (kg water / kg dry air)', rotation='vertical')

# plt.ylim(0,0.025)
fig.savefig("Psychrometric Chart Primary Drying.jpeg",format='jpeg', dpi=1200)
# plt.xlim(1,60)
