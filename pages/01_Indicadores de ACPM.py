import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import locale


df_acpm_consolidado = pd.read_csv(r"Archivos_Consolidados\df_acpm.csv", sep=",")
df_acpm_consolidado["Mes"] = pd.to_datetime(df_acpm_consolidado['Fecha']).dt.month
df_acpm_consolidado['Año'] = pd.to_datetime(df_acpm_consolidado['Fecha']).dt.year


st.title("Indicadores de Consumo ACPM")
st.markdown('''**En esta sección se encuentran los indicadores relacionados con el consumo de ACPM y los
            costos asociados por periodo, equipo/placa, tipo de vehiculo y estación de servicio**''')

## Tabla consolidada ACPM por tipo vehiculo

if st.checkbox("Ver tabla resumen gasto ($) ACPM por tipo vehiculo"):
    # Establecer el separador de miles como el punto (.)
    locale.setlocale(locale.LC_ALL, '')
    meses = df_acpm_consolidado["Mes"].unique().tolist()
    años = df_acpm_consolidado["Año"].unique().tolist()
    # Componente multiselec para los meses
    selected_meses = st.multiselect("Selecciona los meses", meses, default=meses)
    # Componente select box para los años
    selected_año = st.selectbox("Selecciona el año", años)
    # Filtrar el DataFrame según los meses y el año seleccionados
    df_filtrado = df_acpm_consolidado[
        (df_acpm_consolidado["Mes"].isin(selected_meses)) & (df_acpm_consolidado["Año"] == selected_año)
    ]
    df_suma_por_vehiculo = df_filtrado.groupby('Vehiculo').sum()
    columnas = ["Cantidad_Galones", "Costo_Total_ACPM"]
    df_suma_por_vehiculo = df_suma_por_vehiculo[columnas]
    # Formatear los números con el separador de miles como el punto (.)
    df_suma_por_vehiculo["Cantidad_Galones"] = df_suma_por_vehiculo["Cantidad_Galones"].apply(lambda x: locale.format_string("%d", x, grouping=True))
    df_suma_por_vehiculo["Costo_Total_ACPM"] = df_suma_por_vehiculo["Costo_Total_ACPM"].apply(lambda x: locale.format_string("%d", x, grouping=True))
    st.dataframe(df_suma_por_vehiculo)

    
#tabla consumo de acpm por Equipo/Placa

if st.checkbox("Ver tabla resumen gasto ($) ACPM por tipo Equipo/Placa"):
    
    # Establecer el separador de miles como el punto (.)
    locale.setlocale(locale.LC_ALL, '')

    meses = df_acpm_consolidado["Mes"].unique().tolist()
    años = df_acpm_consolidado["Año"].unique().tolist()
    # Componente multiselec para los meses
    selected_meses = st.multiselect("Selecciona los meses", meses, default=meses)
    # Componente select box para los años
    selected_año = st.selectbox("Selecciona el año", años)
    # Filtrar el DataFrame según los meses y el año seleccionados
    df_filtrado = df_acpm_consolidado[
        (df_acpm_consolidado["Mes"].isin(selected_meses)) & (df_acpm_consolidado["Año"] == selected_año)
    ]
    df_suma_por_vehiculo = df_filtrado.groupby('Equipo/Placa').sum()
    columnas = ["Cantidad_Galones", "Costo_Total_ACPM"]
    df_suma_por_vehiculo = df_suma_por_vehiculo[columnas]

    # Formatear los números con el separador de miles como el punto (.)
    df_suma_por_vehiculo["Cantidad_Galones"] = df_suma_por_vehiculo["Cantidad_Galones"].apply(lambda x: locale.format_string("%d", x, grouping=True))
    df_suma_por_vehiculo["Costo_Total_ACPM"] = df_suma_por_vehiculo["Costo_Total_ACPM"].apply(lambda x: locale.format_string("%d", x, grouping=True))

    st.dataframe(df_suma_por_vehiculo)


  
##Tabla por eds

import locale

if st.checkbox("Ver resumen de consumo por Estación de Servicio y Producto"):
    # Establecer el separador de miles como el punto (.)
    locale.setlocale(locale.LC_ALL, '')
    meses = df_acpm_consolidado["Mes"].unique().tolist()
    años = df_acpm_consolidado["Año"].unique().tolist()

    # Agregar los filtros de meses y años
    meses_filtrados = st.multiselect("Seleccione los meses:", meses, default=meses)
    año_filtrado = st.selectbox("Seleccione el año:", años)

    # Filtrar los datos por mes y año seleccionados
    df_filtrado = df_acpm_consolidado[(df_acpm_consolidado['Mes'].isin(meses_filtrados)) & (df_acpm_consolidado['Año'] == año_filtrado)]
    # Agrupar los datos por Estacion_de_Servicio y Producto y calcular la suma de Cantidad_Galones y Costo_Total_ACPM
    resumen_data = df_filtrado.groupby(['Estacion_de_Servicio', 'Producto']).agg({'Cantidad_Galones': 'sum', 'Costo_Total_ACPM': 'sum'}).reset_index()
    # Redondear la cantidad de galones y formatear los valores en las columnas Cantidad_Galones y Costo_Total_ACPM
    resumen_data['Cantidad_Galones'] = resumen_data['Cantidad_Galones'].apply(lambda x: round(x, 0))
    locale.setlocale(locale.LC_ALL, '')
    resumen_data['Cantidad_Galones'] = resumen_data['Cantidad_Galones'].apply(lambda x: locale.format_string("%d", x, grouping=True))
    resumen_data['Costo_Total_ACPM'] = resumen_data['Costo_Total_ACPM'].apply(lambda x: locale.format_string("$ %.0f", x, grouping=True))
    # Mostrar la tabla
    st.dataframe(resumen_data[['Estacion_de_Servicio', 'Producto', 'Cantidad_Galones', 'Costo_Total_ACPM']])


#Gráficos
if st.checkbox("Ver Gráfico de consumo en galones"):
    # Diccionario para mapear los nombres de los meses
    meses_dict = {
        1: "Enero",
        2: "Febrero",
        3: "Marzo",
        4: "Abril"
        # Agrega los demás meses aquí
    }

    # Obtener los valores únicos de Clasificacion_Gasto y Año
    meses = df_acpm_consolidado['Mes'].unique().tolist()
    años = df_acpm_consolidado['Año'].unique().tolist()

    # Agregar los filtros de Clasificacion_Gasto y Año
    meses_filtrados = st.multiselect("Seleccione el mes:", meses, default=meses)
    año_filtrado = st.multiselect("Seleccione el año:", años, default=años)

    # Filtrar los datos por Clasificacion_Gasto y Año seleccionados
    df_filtrado = df_acpm_consolidado[
        (df_acpm_consolidado['Mes'].isin(meses_filtrados)) &
        (df_acpm_consolidado['Año'].isin(año_filtrado))
    ]

    # Agrupar y sumar los valores por mes
    df_agrupado = df_filtrado.groupby('Mes')['Cantidad_Galones'].sum()
    
    # Cambiar los valores numéricos de los meses por sus nombres
    df_agrupado.index = df_agrupado.index.map(meses_dict)

    # Crear la figura y el eje
    fig, ax = plt.subplots()

    # Crear el gráfico de barras
    barplot = df_agrupado.plot(kind='bar', color='#8B6914', ax=ax)

    # Configurar etiquetas y título
    ax.set_xlabel('Mes')
    ax.set_ylabel('Cantidad de Galones Consumidos')
    ax.set_title('Cantidad de Galones de combustible Consumidos por periodo')

    # Añadir etiquetas de los valores encima de cada barra
    for p in barplot.patches:
        barplot.annotate(f'{p.get_height():.2f}', (p.get_x() + p.get_width() / 2, p.get_height()), ha='center', va='bottom')

    # Mostrar el gráfico utilizando st.pyplot()
    st.pyplot(fig)



    #Grafico de costo ACPM
if st.checkbox("Ver Gráfico Costo ($) en galones por periodo (En millones)"):
    # Diccionario para mapear los nombres de los meses
    meses_dict = {
        1: "Enero",
        2: "Febrero",
        3: "Marzo",
        4: "Abril"
        # Agrega los demás meses aquí
    }

    # Obtener los valores únicos de Clasificacion_Gasto y Año
    meses = df_acpm_consolidado['Mes'].unique().tolist()
    años = df_acpm_consolidado['Año'].unique().tolist()

    # Agregar los filtros de Clasificacion_Gasto y Año
    meses_filtrados = st.multiselect("Seleccione el mes:", meses, default=meses)
    año_filtrado = st.multiselect("Seleccione el año:", años, default=años)

    # Filtrar los datos por Clasificacion_Gasto y Año seleccionados
    df_filtrado = df_acpm_consolidado[
        (df_acpm_consolidado['Mes'].isin(meses_filtrados)) &
        (df_acpm_consolidado['Año'].isin(año_filtrado))
    ]

    # Agrupar y sumar los valores por mes
    df_agrupado = df_filtrado.groupby('Mes')['Costo_Total_ACPM'].sum()
    df_agrupado = df_agrupado/1000000
    
    # Cambiar los valores numéricos de los meses por sus nombres
    df_agrupado.index = df_agrupado.index.map(meses_dict)

    # Crear la figura y el eje
    fig, ax = plt.subplots()

    # Crear el gráfico de barras
    barplot = df_agrupado.plot(kind='bar', color='#8B6914', ax=ax)

    # Configurar etiquetas y título
    ax.set_xlabel('Mes')
    ax.set_ylabel('Costo por Galones Consumidos')
    ax.set_title('Costo total por Galones  Consumidos en millones')

    # Añadir etiquetas de los valores encima de cada barra
    for p in barplot.patches:
        barplot.annotate(f'{p.get_height():.2f}', (p.get_x() + p.get_width() / 2, p.get_height()), ha='center', va='bottom')

    # Mostrar el gráfico utilizando st.pyplot()
    st.pyplot(fig)
    
    
if st.checkbox("Ver todos los registros"):
    st.dataframe(df_acpm_consolidado)