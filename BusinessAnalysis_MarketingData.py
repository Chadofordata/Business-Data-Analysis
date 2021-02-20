import pandas as pd
import numpy as nm
import scipy as sci
import sklearn as skl
import requests
import datetime
path='../Data/' #path of the files


# function to convert csv files to dataframes
def csv_to_dataframe(file_name):
    file_cust = file_name+'.csv'  # file name
    file_name = pd.read_csv(path + file_cust)
    return file_name

# function to see the columns in the dataframes
def detect_columns(dataframe,name):
    columns = []
    for col in dataframe.columns:
        columns.append(col)
    print(f'columns in {name} data: ', columns)
    columns.clear()

def get_df_name(dataframe):
    """
    Purpose of func: obtaining the name of DataFrame
    Source of func: https://stackoverflow.com/questions/31727333/get-the-name-of-a-pandas-dataframe
    """
    name = [ x for x in globals() if globals()[ x ] is dataframe ][ 0 ]
    return name

orders=csv_to_dataframe('orders')
customers=csv_to_dataframe('customers')
marketing=csv_to_dataframe('marketing')
#print(marketing.head())

orders_col=detect_columns(orders,get_df_name(orders))
orders['OrderYear'] = pd.DatetimeIndex(orders['Tdate']).year
orders['OrderMonth'] = pd.DatetimeIndex(orders['Tdate']).month
cust_col=detect_columns(customers,get_df_name(customers))
markt_col=detect_columns(marketing,get_df_name(marketing))
#listing the column names

#Combining customers and marketing data but keep the customer data as it is (left join)
cust_ordDf = pd.merge(customers,orders,on='CID',how='left').fillna(0)


pivoting=pd.pivot_table(cust_ordDf[['State','Tdate','OrderMonth','OrderYear','Cdisc','Ddisc','Lprice','Mcost','Odisc','Pdisc','Usales','returnAmount']],
                        index=['State','OrderYear','OrderMonth'],
                        aggfunc=nm.mean)
#print(pivoting.to_string())

#Calculating pocket price based on the formula as follows: 𝑃𝑝𝑟𝑖𝑐𝑒=𝐿𝑝𝑟𝑖𝑐𝑒×(1−𝑇𝑑𝑖𝑠𝑐) and 𝑇𝑑𝑖𝑠𝑐 is a total discount

pivoting['Tprice'] = pivoting['Cdisc']+pivoting['Pdisc']+pivoting['Odisc']+pivoting['Ddisc']
pivoting['Pprice'] =pivoting['Lprice']*(1-pivoting['Tprice'])

print(pivoting.to_string())
