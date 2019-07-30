# -*- coding: utf-8 -*-
"""
Created on Tue May 14 13:58:42 2019

@author: gbessardon
"""
import requests
import numpy as np
def get_association_list(fnass):
    
    lista=open(fnass,'r')
    for l in lista:
        vallist=l.split('}')
    
    asso_unit_list=[]
    asso_symbol_list=[]
    asso_name_list=[]
    red_list=[]
    green_list=[]
    blue_list=[]
    for v in vallist:
        values=v.split(',')
        for val in values:
            if "Association_Unit" in val:
                temp=val.split(':')[1]
                asso_unit_list.append(temp[1:len(temp)-1])
            if "Association_Symbol" in val:
                temp=val.split(':')[1]
                asso_symbol_list.append(temp[1:len(temp)-1])
            if "Association_Name" in val:
                temp=val.split(':')[1]
                asso_name_list.append(temp[1:len(temp)-1])
            if "Red_Value"  in val:
                temp=val.split(':')[1]
                red_list.append(temp[1:len(temp)-1])
            if "Green_Value"  in val:
                temp=val.split(':')[1]
                green_list.append(temp[1:len(temp)-1])
            if "Blue_Value"  in val:
                temp=val.split(':')[1]
                blue_list.append(temp[1:len(temp)-1])
    return(asso_unit_list,asso_symbol_list)                

def getasso_serie(fnass):

    asso_unit_list,asso_symbol_list=get_association_list(fnass)
#    print(len(asso_unit_list))
    natID=[]
    placeID=[]
    corres_asso=[]
    for a in asso_unit_list:
        url='http://gis.teagasc.ie/soils/get_associations.php?assoc_id='+a
        r = requests.get(url)
        f=r.content 
        h=f.split('{')
        temp=h[1:len(h)]

        if len(temp)>1:
               for t in temp:
                   if "National_Series" in t:
                       for tt in t.split(','):
                           if  ("National_Series" in tt.split(':')[0]) and ("_Id" not in tt.split(':')[0]):
                               ptemp=tt.split(':')[1]                           
                               placeID.append(ptemp[1:len(ptemp)-1])

                           if  ("National_Series_Id" in tt.split(':')[0]) :
                               temporary=tt.split(':')[1]
                               corres_asso.append(a)
                               natID.append(temporary[1:len(temporary)-1])

    return(np.array(natID),np.array(placeID),np.array(corres_asso))
            
                           
                          
#
#fnass='/home/gbessardon/national_soils/get_all_associations.php'
#natID,placeID,corres_asso=getasso_serie(fnass)