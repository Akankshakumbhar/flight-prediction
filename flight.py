import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sn
import streamlit as st
import duckdb
st.title("flight prediction/EAD")
st.image("img.png", use_column_width=True)
st.video('')



with st.sidebar:
                uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type=['csv'])
                if uploaded_file is not None:
                                               df = pd.read_csv(uploaded_file)
                                               st.dataframe(df)
d=pd.read_csv(r"C:\Users\Star\Desktop\Stuffs(IMP)\Udemy Projects\Flight_price predictions\Data_Train.csv")
#st.dataframe(d)

'''if st.button(''):
    chart = ('bar', 'hist', 'boxplot', 'volinplot')
    chart_sel = st.selectbox('select the type of chart', chart)
    fig,ax = plt.subplots()
    if chart_sel == 'bar':
        sn.barplot(x='Source', y='Price', data=d)
    elif chart_sel == 'boxplot':
        sn.boxplot(x='Source', y='Price', data=d)
    elif chart_sel == 'volinplot':
        sn.violinplot(x='Source', y='Price', data=d)
    else:
        sn.histplot(x='Source', hue='Price', data=d)
st.pyplot(fig)'''



a=duckdb.query("select Price from d").df()
st.dataframe(a)


'''if st.button("prection of airline and price"):
    chart=['barplot','boxplot']
    select=st.selectbox("select type of graph",chart)
    fig,ax=plt.subplots()
    if select=='barplot':
        sn.barplot(x='Airline', y='Price', data=d)
        plt.xticks(rotation="vertical")
    elif select=='boxplot':
        ab = duckdb.query("select Airline,Price from data_train order by Price desc").df()
        sn.boxplot(x='Airline', y='Price', data=ab)
        plt.xticks(rotation="vertical")
st.pyplot(fig)'''

with st.container():
    st.title("Prices of Airline")
    ab = duckdb.query("select Airline,Price from d order by Price desc").df()

    chart = ('bar', 'hist', 'boxplot', 'volinplot')
    chart_sel = st.selectbox('select the type of chart', chart)
    fig, ax = plt.subplots()
    if chart_sel == 'bar':
        sn.barplot(x='Airline', y='Price', data=ab)
        plt.xticks(rotation="vertical")
    elif chart_sel == 'boxplot':
        sn.boxplot(x='Airline', y='Price', data=ab)
        plt.xticks(rotation="vertical")
    else :
        sn.violinplot(x='Airline', y='Price', data=ab)
        plt.xticks(rotation="vertical")

st.pyplot(fig)


st.markdown('----------------------------------------------------------------------')
with st.container():
                   st.header('price based on destination')

                  #c=duckdb.query("select Distinct Destination ,Price from d order by Price").df()

                   chart=['box','bar','scatter']
                   s=st.selectbox("select chart",chart)
                   fig1, ax = plt.subplots()
                   if s=='box':
                                sn.boxplot(x='Destination',y='Price',data=d)

                   elif s=='bar':

                       sn.barplot(x='Destination',y='Price',data=d)

                   else :
                       sn.scatterplot(x='Destination',y='Price',data=d)
st.pyplot(fig1)
st.markdown('-------------------------------')
'''with st.container():
     st.title("prices of flight based on Routes")
     chart=['bar','box','scatter']
     chart_sel=st.selectbox('select type of chart',chart)
     fig, ax = plt.subplots()
     if chart_sel=='bar':

         sn.barplot(x='Route',y='Price',data=d)
         plt.xticks(rotation="vertical")
     elif chart_sel=='box':
         sn.boxplot(x='Route',y='Price',data=d)
         plt.xticks(rotation="vertical")
     else:
         sn.scatterplot(x='Route',y='Price',data=d)
         plt.xticks(rotation="vertical")
st.pyplot(fig)'''


# data cleaning and extracting new featurs
d.dropna(inplace=True)

d['Date_of_Journey']=pd.to_datetime(d['Date_of_Journey'])
d['Arrival_Time']=pd.to_datetime(d['Arrival_Time'])
d['Dep_Time']=pd.to_datetime(d['Dep_Time'])
d['Journey_day']=d['Date_of_Journey'].dt.day
d['journey_month']=d['Date_of_Journey'].dt.month
d['journey_year']=d['Date_of_Journey'].dt.year
d['dep_time_hour']=d['Dep_Time'].dt.hour
d['dep_time_minute']=d['Dep_Time'].dt.minute
d['Arrival_Time_hour']=d['Arrival_Time'].dt.hour
d['Arrival_Time_minute']=d['Arrival_Time'].dt.minute
#d['Duration']=pd.to_datetime(d['Duration'])
#d['Durtion_hour']=d['Duration'].dt.hour
#d['Duration_minute']=d['Duration'].dt.minute


def flight_dep_time(x):
    '''
    This function takes the flight Departure time
    and convert into appropriate format.

    '''

    if (x > 4) and (x <= 8):
        return "Early Morning"

    elif (x > 8) and (x <= 12):
        return "Morning"

    elif (x > 12) and (x <= 16):
        return "Noon"

    elif (x > 16) and (x <= 20):
        return "Evening"

    elif (x > 20) and (x <= 24):
        return "Night"

    else:
        return "late night"




x=d['dep_time_hour'].apply(flight_dep_time).value_counts().plot(kind="bar" , color="g")


ch={'Banglore':0,'Kolkata':1,'Delhi':3,'Chennai':4,'Mumbai':5}
d['Source']=d['Source'].map(ch)
vh={'New Delhi':0, 'Banglore':1, 'Cochin':2, 'Kolkata':3, 'Delhi':4, 'Hyderabad':5}
d['Destination']=d['Destination'].map(vh)
x={'non-stop':0, '2 stops':1, '1 stop':2, '3 stops':3, '4 stops':4}
d['Total_Stops']=d['Total_Stops'].map(x)
u={'Trujet': 0,'SpiceJet': 1, 'Air Asia': 2, 'IndiGo': 3,'GoAir': 4,'Vistara': 5,'Vistara Premium economy': 6,'Air India': 7,
 'Multiple carriers': 8,
 'Multiple carriers Premium economy': 9,
 'Jet Airways': 10,
 'Jet Airways Business': 11}
d['Airline']=d['Airline'].map(u)

# feature selection for machine leraning

X = d.drop(['Price'], axis=1)
y = d['Price']





'''cat_col = [col for col in d.columns if d[col].dtype=="object"]
num_col = [col for col in d.columns if d[col].dtype!="object"]
cat_col
d['Source'].unique()



d['Source'].apply(lambda x: 1 if x=='Banglore' else 0)
for sub_category in d['Source'].unique():
    d['Source_'+sub_category] = d['Source'].apply(lambda x: 1 if x==sub_category else 0)
'''
d.drop(columns=['Date_of_Journey','Arrival_Time','Dep_Time','Additional_Info', 'Source', 'journey_year'], axis=1, inplace=True)
st.dataframe(d)

#ml part
#training data
X=d.drop(['Price'], axis=1)
y=d['Price']
from sklearn.model_selection import train_test_split
from sklearn.feature_selection import mutual_info_regression
imp = mutual_info_regression(X , y)



























