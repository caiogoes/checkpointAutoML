#!pip install streamlit

import streamlit as st
import pandas as pd
import numpy as np
import pickle
from pycaret.classification import *
from sklearn.metrics import accuracy_score

def formatar_valores(df):
    df.ID = df.ID.astype("int64")
    df.Year_Birth = df.Year_Birth.astype("int64")
    df.Income = df.Income.astype("float64")
    df.Kidhome = df.Kidhome.astype("int64")
    df.Teenhome = df.Teenhome.astype("int64")
    df.Recency = df.Recency.astype("int64")
    df.MntWines = df.MntWines.astype("int64")
    df.MntFruits = df.MntFruits.astype("int64")
    df.MntMeatProducts = df.MntMeatProducts.astype("int64")
    df.MntFishProducts = df.MntFishProducts.astype("int64")
    df.MntSweetProducts = df.MntSweetProducts.astype("int64")
    df.MntGoldProds = df.MntGoldProds.astype("int64")
    df.NumDealsPurchases = df.NumDealsPurchases.astype("int64")
    df.NumWebPurchases = df.NumWebPurchases.astype("int64")
    df.NumCatalogPurchases = df.NumCatalogPurchases.astype("int64")
    df.NumStorePurchases = df.NumStorePurchases.astype("int64")
    df.NumWebVisitsMonth = df.NumWebVisitsMonth.astype("int64")
    df.AcceptedCmp3 = df.AcceptedCmp3.astype("int64")
    df.AcceptedCmp4 = df.AcceptedCmp4.astype("int64")
    df.AcceptedCmp5 = df.AcceptedCmp5.astype("int64")
    df.AcceptedCmp1 = df.AcceptedCmp1.astype("int64")
    df.AcceptedCmp2 = df.AcceptedCmp2.astype("int64")
    df.Complain = df.Complain.astype("int64")
    df.Z_CostContact = df.Z_CostContact.astype("int64")
    df.Z_Revenue = df.Z_Revenue.astype("int64")
    df.Response = df.Response.astype("int64")

    return df

st.set_page_config( page_title = 'CK - Auto ML',
                   page_icon = './logo_fiap.png',
                   layout = 'wide',
                   initial_sidebar_state = 'expanded')
 
st.title('Checkpoint 1 - Auto ML')
 
with st.sidebar:
   c1, c2 = st.columns(2)
   c1.image('./logo_fiap.png', width = 100)
   c2.write('')
   c2.subheader('Auto ML - Fiap [v2]')

   database = st.radio('Fonte dos dados de entrada (X):', ('CSV', 'Online'))

   if database == 'CSV':
       st.info('Upload do CSV')
       file = st.file_uploader('Selecione o arquivo CSV', type='csv')
 
if database == 'CSV':
   if file:
        #carregamento do CSV
        Xtest = pd.read_csv(file)

        #carregamento / instanciamento do modelo pkl
        mdl_lgbm = load_model('model')

        #predict do modelo
        ypred = predict_model(mdl_lgbm, data = Xtest, raw_score = True)

        with st.expander('Visualizar CSV carregado:', expanded = False):
            c1, _ = st.columns([2,4])
            qtd_linhas = c1.slider('Visualizar quantas linhas do CSV:', 
                                   min_value = 5, 
                                   max_value = Xtest.shape[0], 
                                   step = 10,
                                   value = 5)
            st.dataframe(Xtest.head(qtd_linhas))

        with st.expander('Visualizar Predições:', expanded = True):
            c1, _, c2, c3 = st.columns([2,.5,1,1])
            treshold = c1.slider('Treshold (ponto de corte para considerar predição como True)',
                               min_value = 0.0,
                               max_value = 1.0,
                               step = .1,
                               value = .5)
            qtd_true = ypred.loc[ypred['prediction_label'] > treshold].shape[0]

            c2.metric('Qtd clientes True', value = qtd_true)
            c3.metric('Qtd clientes False', value = len(ypred) - qtd_true)

            def color_pred(val):
                color = 'olive' if val > treshold else 'orangered'
                return f'background-color: {color}'

            tipo_view = st.radio('', ('Completo', 'Apenas predições'))
            if tipo_view == 'Completo':
                df_view = ypred.copy()
            else:
                df_view = ypred[['prediction_label']].copy()

            st.dataframe(df_view.style.applymap(color_pred, subset = ['prediction_label']))

            csv = df_view.to_csv(sep = ';', decimal = ',', index = True)
            st.markdown(f'Shape do CSV a ser baixado: {df_view.shape}')
            st.download_button(label = 'Download CSV',
                           data = csv,
                           file_name = 'Predicoes.csv',
                           mime = 'text/csv')

   else:
       st.warning('Arquivo CSV não foi carregado')
 
else:
    with st.expander('Campos:', expanded = True):
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            ID = st.text_input('ID', value = "0")
 
        with col2:
            Year_Birth = st.text_input('Year_Birth', value = "0")
 
        with col3:
            Education = st.selectbox('Education', ('2n Cycle', 'Basic', 'Graduation', 'Master', 'PhD'))
 
        with col4:
            Marital_Status = st.selectbox('Marital_Status', ('Absurd', 'Alone', 'Divorced', 'Married', 'Single', 'Together', 'Widow', 'YOLO'))
 
        with col5:
            Income = st.text_input('Income', value = "0")
 
        col6, col7, col8, col9, col10 = st.columns(5)
        with col6:
            Kidhome = st.text_input('Kidhome', value = "0")
 
        with col7:
            Teenhome = st.text_input('Teenhome', value = "0")
 
        with col8:
            Dt_Customer = st.date_input('Dt_Customer')
 
        with col9:
            Recency = st.text_input('Recency', value = "0")
 
        with col10:
            MntWines = st.text_input('MntWines', value = "0")
 
        col11, col12, col13, col14, col15 = st.columns(5)
        with col11:
            MntFruits = st.text_input('MntFruits', value = "0")
 
        with col12:
            MntMeatProducts = st.text_input('MntMeatProducts', value = "0")
 
        with col13:
            MntFishProducts = st.text_input('MntFishProducts', value = "0")
 
        with col14:
            MntSweetProducts = st.text_input('MntSweetProducts', value = "0")
 
        with col15:
            MntGoldProds = st.text_input('MntGoldProds', value = "0")
 
        col16, col17, col18, col19, col20 = st.columns(5)
        with col16:
            NumDealsPurchases = st.text_input('NumDealsPurchases', value = "0")
 
        with col17:
            NumWebPurchases = st.text_input('NumWebPurchases', value = "0")
 
        with col18:
            NumCatalogPurchases = st.text_input('NumCatalogPurchases', value = "0")
 
        with col19:
            NumStorePurchases = st.text_input('NumStorePurchases', value = "0")
 
        with col20:
            NumWebVisitsMonth = st.text_input('NumWebVisitsMonth', value = "0")
 
        col21, col22, col23, col24, col25 = st.columns(5)
        with col21:
            AcceptedCmp3 = st.text_input('AcceptedCmp3', value = "0")
 
        with col22:
            AcceptedCmp4 = st.text_input('AcceptedCmp4', value = "0")
 
        with col23:
            AcceptedCmp5 = st.text_input('AcceptedCmp5', value = "0")
 
        with col24:
            AcceptedCmp1 = st.text_input('AcceptedCmp1', value = "0")
 
        with col25:
            AcceptedCmp2 = st.text_input('AcceptedCmp2', value = "0")
 
        col26, col27, col28, col29 = st.columns(4)
        with col26:
            Complain = st.text_input('Complain', value = "0")
 
        with col27:
            Z_CostContact = st.text_input('Z_CostContact', value = "0")
 
        with col28:
            Z_Revenue = st.text_input('Z_Revenue', value = "0")
 
        with col29:
            Response = st.text_input('Response', value = "0")
 
        data = {
       "ID": [ID],
       "Year_Birth": [Year_Birth],
       "Education": [Education],
       "Marital_Status": [Marital_Status],
       "Income": [Income],
       "Kidhome": [Kidhome],
       "Teenhome": [Teenhome],
       "Dt_Customer": [Dt_Customer],
       "Recency": [Recency],
       "MntWines": [MntWines],
       "MntFruits": [MntFruits],
       "MntMeatProducts": [MntMeatProducts],
       "MntFishProducts": [MntFishProducts],
       "MntSweetProducts": [MntSweetProducts],
       "MntGoldProds": [MntGoldProds],
       "NumDealsPurchases": [NumDealsPurchases],
       "NumWebPurchases": [NumWebPurchases],
       "NumCatalogPurchases": [NumCatalogPurchases],
       "NumStorePurchases": [NumStorePurchases],
       "NumWebVisitsMonth": [NumWebVisitsMonth],
       "AcceptedCmp3": [AcceptedCmp3],
       "AcceptedCmp4": [AcceptedCmp4],
       "AcceptedCmp5": [AcceptedCmp5],
       "AcceptedCmp1": [AcceptedCmp1],
       "AcceptedCmp2": [AcceptedCmp2],
       "Complain": [Complain],
       "Z_CostContact": [Z_CostContact],
       "Z_Revenue": [Z_Revenue],
       "Response": [Response]
        }
 
        df = pd.DataFrame(data)
 
        df = formatar_valores(df)
 
        model = load_model('model')
 
        predictions = predict_model(model, data = df, raw_score = True)
 
    with st.expander('Visualizar dados:', expanded = False):
        st.dataframe(df.head())
 
    with st.expander('Visualizar Predições:', expanded = False):
 
            c1, _, c2, c3 = st.columns([2,.5,1,1])
 
            score = accuracy_score(y_pred = predictions["prediction_label"], y_true = predictions["Response"])
 
            treshold = c1.slider('Treshold (ponto de corte para considerar predição como True)',
                 min_value = 0.0,
                 max_value = 1.0,
                 step = .1,
                 value = .5)
         
            qtd_true = predictions.loc[predictions['Response'] > treshold].shape[0]
 
            c2.metric('Qtd clientes True', value = qtd_true)
            c3.metric('Qtd clientes False', value = len(predictions) - qtd_true)
 
            if st.button('Score'):
                if score > .80:
                    st.success(f"Score: {score}")
                elif .50 < score < .80:
                    st.warning(f"Score: {score}")
                else:
                    st.error(f"Score: {score}")
                 
            st.header("Dataframe with predictions")
            #st.dataframe(predictions)
 
            def color_pred(val):
                color = 'olive' if val > treshold else 'orangered'
                return f'background-color: {color}'
 
            st.dataframe(predictions.style.applymap(color_pred, subset = ['prediction_label']))
         
            csv = predictions.to_csv(sep = ';', decimal = ',', index = True)
            st.download_button(label = 'Download', data = csv, file_name = 'predictions.csv', mime = 'text/csv')
