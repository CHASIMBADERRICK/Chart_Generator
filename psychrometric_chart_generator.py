# -*- coding: utf-8 -*-
"""
Created on Sun Nov 14 14:11:37 2021

@author: derrick
"""

import numpy as np
import CoolProp.CoolProp as CP
import matplotlib.pyplot as plt
from labellines import labelLine, labelLines #Used for plotting inline labels
from textwrap import wrap


#Define the x axis temperature limits. These are the only values to be changed
Tdb_start = 0.
Tdb_end = 60.


#Define the y axis humidity ratio limits. These are the only values to be changed
W_start = 0 #kg of water /kg of dry air
W_end = 30/1000 #kg of water /kg of dry air (grams/1000 to convert to kgs)

#Convert to Kelvin 
Tdb_start_eqn = Tdb_start +273.15
Tdb_end_eqn = Tdb_end +273.15


#*******************************************************#
## Define Specific Volume limits##
sv_start = CP.HAPropsSI("Vda","R",1,"P",101325,"Tdb",Tdb_start_eqn)
sv_end =CP.HAPropsSI("Vda","W",W_end,"P",101325,"Tdb",Tdb_end_eqn)
#*******************************************************#

#*******************************************************#
## Define Enthalpy limits##
Hda_start = CP.HAPropsSI("Hda","R",1/100,"P",101325,"Tdb",Tdb_start_eqn)/1000 #convert enthalpy to kJ/kg of dry air
Hda_end =CP.HAPropsSI("Hda","Vda",sv_end,"P",101325,"Tdb",Tdb_end_eqn)/1000 #convert enthalpy to kJ/kg of dry air
#*******************************************************#




fig = plt.figure()
ax = plt.axes
ax = fig.add_subplot(111)
ax.grid(False)

Tdbvec = np.linspace(Tdb_start, Tdb_end+1)+273.15 #Dry bulb tempersture vector

# Lines of constant relative humidity
for RH in np.arange(0.1, 1, 0.1):
    W = CP.HAPropsSI("W","R",RH,"P",101325,"T",Tdbvec)
    ax.plot(Tdbvec-273.15, W, color='#66c2a5', lw = 0.5)

# Saturation curve
W = CP.HAPropsSI("W","R",1,"P",101325,"T",Tdbvec)
ax.plot(Tdbvec-273.15, W, color='#66c2a5',label=str("100%"), lw=1.5)
labelLines(plt.gca().get_lines(),zorder=3)

# Lines of constant Vda. Limits are defined above
rh_list = ["10%", "20%", "30%", "40%" , "RH=50%","60%" , "70%", "", "90%"]
bold_counter=-1
bold_array=[]
for Vda in np.arange(sv_start, sv_end, 0.01):
    R = np.linspace(0,1)
    W = CP.HAPropsSI("W","R",R,"P",101325,"Vda",Vda)
    Tdb = CP.HAPropsSI("Tdb","R",R,"P",101325,"Vda",Vda)
    
    if abs(Vda % 0.05) < 0.01: 
        bold_counter+=1
        bold_array.append(Vda)
        # ax.plot(Tdb-273.15, W, color='#8da0cb',lw=1.5)
        ax.plot(Tdb-273.15, W, color='#8da0cb',lw=1.5, label=str("SV"))
        # labelLines(plt.gca().get_lines(),zorder=2.5)
    else:
        ax.plot(Tdb-273.15, W, color='#8da0cb', lw=0.5)

#Plot Labels for Vda thick lines

# R = np.linspace(0,1)
# W = CP.HAPropsSI("W","R",R,"P",101325,"Vda",bold_array[bold_counter-1])
# Tdb = CP.HAPropsSI("Tdb","R",R,"P",101325,"Vda",Vda)
# ax.plot(Tdb-273.15, W, color='#8da0cb',lw=1.5, label=str(bold_array[bold_counter-1]))
# # labelLines(plt.gca().get_lines(),zorder=2.5)

# # Lines of constant wetbulb
# for Twb_C in np.arange(-16, 33, 2):
#     if Twb_C == 0:
#         continue
#     R = np.linspace(0.0, 1)
#     print(Twb_C)
#     Tdb = CP.HAPropsSI("Tdb","R",R,"P",101325,"Twb",Twb_C+273.15)
#     W = CP.HAPropsSI("W","R",R,"P",101325,"Tdb",Tdb)
#     plt.plot(Tdb-273.15, W, color='r', lw=1.5 if abs(Twb_C % 10) < 0.001 else 0.5)


# Lines of constant enthalpy
# h_list = ["10","20","30","40","50","60","70","80","Enthalpy = 90kJ/kg","100","110"]
# p=0
for H_val in np.arange(Hda_start, Hda_end, 5):
    # if H_val == 0:
    #     continue
    R = np.linspace(0.0, 1)
    print(H_val)
    Tdb = CP.HAPropsSI("Tdb","R",R,"P",101325,"Hda",H_val*1000)
    W = CP.HAPropsSI("W","R",R,"P",101325,"Tdb",Tdb)
    ax.plot(Tdb-273.15, W, color='#fc8d62', lw=1.5 if abs(H_val % 25) > 20 else 0.5 )
    # plt.plot(Tdb-273.15, W, color='#fc8d62', label=str(int(H_val)),linewidth=0.8  )
    # labelLines(plt.gca().get_lines(),zorder=3)
    # p+=1


#Plot Humidity ratio lines

step=-.025
for W in range (int(W_start*1000) , int(W_end*1000)+1,5):
    for   x in np.arange(55,-1,step):
        try:
            temp_db=x +273.15 # convert celsius to Kelvin
            RH = CP.HAPropsSI("RH","Tdb",temp_db,"P",101325,"W",W/1000)
            #print (x,"|",RH*100)
        
        except:
            # print("The last tried temp is: ", x-step, x)
            ax.plot([x-step,Tdb_end],[W/1000,W/1000],color='#a6d854',linewidth=0.5)
            break
    

#Draw Dry bulb temperature lines
step=0.01
last_Tdb = 0
T_step=5
for   temp in np.arange(Tdb_start,Tdb_end+1,T_step):
    for W in np.arange (int(W_start*1000) , int(W_end*1000)+1,step):
        
        try:
            
            temp_db=temp +273.15 # convert celsius to Kelvin
            RH = CP.HAPropsSI("RH","Tdb",temp_db,"P",101325,"W",W/1000)
            # print (W,"|",temp,"|",RH*100)
           
        except:
            print("The last tried W giving RH less than 100% is: ", W-step, W)
            ax.plot([temp,temp],[Tdb_start, (W-step)/1000],color='#66c2a5',linewidth=0.5)
          
            last_Tdb = temp
           
            break
        #Get Tdbs on flat part of curve
       

#Get Tdbs on flat part of curve
Tdb_array =np.arange(last_Tdb+T_step,Tdb_end+1,T_step)
l=len(Tdb_array)
# print(last_Tdb," ",l)
        
for temp in Tdb_array:
    ax.plot([temp,temp],[Tdb_start, (W_end)],color='#66c2a5',linewidth=0.5)


Tdb_array =np.arange(last_Tdb+T_step,Tdb_end+1,T_step)
print(Tdb_array)

#***********************************************************************#

c='magenta'
#Plot dryer design lines
ax.plot([25,35],[0.013898,0.020668],color=c) 
ax.plot([32,40],[0.01864,0.01864],color=c)
ax.plot([35,40],[0.020668,0.01864],color=c)


plt.xlabel('Dry Bulb Temperature (\u00B0C)')
plt.ylabel('W (kg water / kg dry air)', rotation='vertical')
ax.yaxis.set_label_position("right")
ax.yaxis.tick_right()
title = ax.set_title("\n".join(wrap("Psychrometric " 
                                    "chart ",55)))

plt.gca().xaxis.set_major_locator(plt.MultipleLocator(5))
plt.ylim(W_start,W_end)
plt.xlim(Tdb_start,Tdb_end)

fig.savefig("Psychrometric Chart.jpeg",format='jpeg', dpi=1200)
# plt.show()