# -*- coding: utf-8 -*-
"""
Created on Thu Jun 10 14:48:59 2021

@author: NDH00126
"""

import pandas as pd

df = pd.read_csv("C:/Maneesh/Pre_Buying_Activity/python_dashboard/00_NYC_open_data/CMBND_1.csv",low_memory=False)

lst_attrbts=['TST_DRV.VHCL_FEATR_MAPNG.FEATR.FEATR_NM','TST_DRV.VHCL_FEATR_MAPNG.VHCL_MDL_LIST.VHCL_CLR','TRVL_TYP.TRVL_TYP_NM','CSTMR_AGE','CSTMR_JOB']

# df['TST_DRV.VHCL_FEATR_MAPNG.VHCL_MDL_LIST.VHCL_VRNT'].unique()

def avg_lst(my_lst_avg):
    """

    Parameters
    ----------
    my_lst_avg : list
        List of count of each unique values in the data set.

    Returns
    -------
    smp_dict : dictionary
        Dictionary with key as each count, value as average of group without this key value.

    """
    smp_dict={}
    for i in range(len(my_lst_avg)):
        my_lst_avg_1=my_lst_avg[:]
        j=my_lst_avg_1.pop(i)
        smp_dict[j]=sum(my_lst_avg_1)/len(my_lst_avg_1)
    # print(smp_dict)
    return smp_dict

def key_influencer(lst_attrbts,df,varient,model):    
    """

    Parameters
    ----------
    lst_attrbts : list
        List of attributes to be cross checked for influence.
    df : dataframe
        Dataframe of input dataset.
    varient : string
        Varient name against which comaparison is held.
    model : string
        Model name against which comparison is held.

    Returns
    -------
    my_dict : dictionary
        The dictionary with key as key influencer and value as ratio of influence.

    """
    my_dict={}
    for i in lst_attrbts:
        my_lst_avg=[]
        my_lst_nm=[]
        my_lst_val={}
        for j in df[i].unique():
            # print(i)
            # print(j)
            # print(i,j,len(df[(df[i]==j) & (df['TST_DRV.VHCL_FEATR_MAPNG.VHCL_MDL_LIST.VHCL_VRNT']=='XV')]))
            # my_lst.append([j,len(df[(df[i]==j) & (df['TST_DRV.VHCL_FEATR_MAPNG.VHCL_MDL_LIST.VHCL_VRNT']=='XV')])])
            ln=len(df[(df[i]==j) & (df['TST_DRV.VHCL_FEATR_MAPNG.VHCL_MDL_LIST.VHCL_VRNT']==varient)])
            ln_mdl=len(df[(df[i]==j) & (df['TST_DRV.VHCL_FEATR_MAPNG.VHCL_MDL_LIST.VHCL_NM']==model)])
            if ln_mdl==0:
                my_lst_val[j]=0
                my_lst_avg.append(0)
            else:
                my_lst_val[j]=(ln/ln_mdl)*100
                my_lst_avg.append((ln/ln_mdl)*100)
        my_dict_avg= avg_lst(my_lst_avg)
        for k in my_lst_val:
            if my_lst_val[k] in sorted(my_lst_val.values(),reverse=True)[:3]:
                # print('k=',k,'my_lst_val[k]=',my_lst_val[k],'my_dict_avg[my_lst_val[k]]=',my_dict_avg[my_lst_val[k]])
                # my_lst_nm.append([k,my_lst_val[k],my_dict_avg[my_lst_val[k]]])
                if my_dict_avg[my_lst_val[k]] != 0:
                    # print('k=',k,'my_lst_val[k]=',my_lst_val[k],'my_dict_avg[my_lst_val[k]]=',my_dict_avg[my_lst_val[k]])
                    # my_lst_nm.append([k,(my_lst_val[k]/my_dict_avg[my_lst_val[k]])])
                # else:
                    my_lst_nm.append([k,(my_lst_val[k]/my_dict_avg[my_lst_val[k]])])
        my_dict[i]=my_lst_nm
    return my_dict




def display_prediction(models):    
    """

    Parameters
    ----------
    models : dictionary
        Dictionary consist upof key influencers and their individual ratios.

    Returns
    -------
    None.

    """
    for i in models:
        for j in models[i]:
            if j== 'CSTMR_AGE':
                c='Customer Age'
            elif j=='CSTMR_JOB':
                c='Customer Job'
            elif j=='TRVL_TYP.TRVL_TYP_NM':
                c='Commuter type'
            elif j=='TST_DRV.VHCL_FEATR_MAPNG.FEATR.FEATR_NM':
                c='Feature'
            elif j=='TST_DRV.VHCL_FEATR_MAPNG.VHCL_MDL_LIST.VHCL_CLR':
                c='Color'
            for k in models[i][j]:
                # print('i=',i,'j=',j,'k=',k)
                # print('Variant:',i,'Feature:',k[0],'Affinity:',k[1]/k[2])
                print("When",c,"is",k[0],"likelihood of Varient to be '",i,"' is",k[1],"times.")
                # break
            # break
        # break


#Invoking the key influencer prediction using function calls
models={}
for i in df['TST_DRV.VHCL_FEATR_MAPNG.VHCL_MDL_LIST.VHCL_NM'].unique():
    for j in df['TST_DRV.VHCL_FEATR_MAPNG.VHCL_MDL_LIST.VHCL_VRNT'].unique():
        pred=key_influencer(lst_attrbts,df,j,i)   
        models[j]=pred 

#Display function for key influencers
display_prediction(models)