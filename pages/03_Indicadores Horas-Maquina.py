import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import calendar
import locale

df_Horas_consolidado = pd.read_csv("Archivos_Consolidados/df_Horas.csv", sep=",")
df_Horas_consolidado["Mes"] = pd.to_datetime(df_Horas_consolidado['Fecha']).dt.month
df_Horas_consolidado['Año'] = pd.to_datetime(df_Horas_consolidado['Fecha']).dt.year
df_Horas_consolidado["Costo-Hora"] = df_Horas_consolidado["Horas"] * 16000
df_Horas_consolidado["Costo-ACPM"] = df_Horas_consolidado["ACPM"] * 8250 #PROMEDIE EL COSTO DEL ACPM


st.title("Indicadores asociados a Horas-Máquina")
st.markdown('''**Esta sección detalla las Horas máquina por periodo y equipo, consumos de ACPM
         y costos asociados.**''')


## Tabla de Horas, Galones, Costos por Equipo

if st.checkbox("Ver tabla resumen Horas, Galones y costos por Equipo"):
    # Establecer el separador de miles como el punto (.)
    locale.setlocale(locale.LC_ALL, '')
    meses = df_Horas_consolidado["Mes"].unique().tolist()
    años = df_Horas_consolidado["Año"].unique().tolist()
    # Componente multiselec para los meses
    selected_meses = st.multiselect("Selecciona los meses", meses, default=meses)
    # Componente select box para los años
    selected_año = st.selectbox("Selecciona el año", años)
    # Filtrar el DataFrame según los meses y el año seleccionados
    df_filtrado = df_Horas_consolidado[
        (df_Horas_consolidado["Mes"].isin(selected_meses)) & (df_Horas_consolidado["Año"] == selected_año)
    ]
    df_suma_Equipo = df_filtrado.groupby('Equipo').sum()
    columnas = ["Horas","Costo-Hora","ACPM", "Costo-ACPM"]
    df_suma_Equipo= df_suma_Equipo[columnas]
    # Formatear los números con el separador de miles como el punto (.)
    df_suma_Equipo["Costo-Hora"] = df_suma_Equipo["Costo-Hora"].apply(lambda x: locale.format_string("%d", x, grouping=True))
    df_suma_Equipo["Horas"] = df_suma_Equipo["Horas"].apply(lambda x: locale.format_string("%d", x, grouping=True))
    df_suma_Equipo["ACPM"] = df_suma_Equipo["ACPM"].apply(lambda x: locale.format_string("%d", x, grouping=True))
    df_suma_Equipo["Costo-ACPM"] = df_suma_Equipo["Costo-ACPM"].apply(lambda x: locale.format_string("%d", x, grouping=True))
    st.dataframe(df_suma_Equipo)
    
    ## GRAFICO HORAS-MAQUINA POR MES

if st.checkbox("Ver Gráfico Horas-Máquina por mes"):
    # Diccionario para mapear los nombres de los meses
    meses_dict = {
        1: "Enero",
        2: "Febrero",
        3: "Marzo",
        4: "Abril"
        # Agrega los demás meses aquí
    }

    # Obtener los valores únicos de mes y Año- actividad
    meses = df_Horas_consolidado['Mes'].unique().tolist()
    años = df_Horas_consolidado['Año'].unique().tolist()
    actividades = df_Horas_consolidado["Actividad/Equipo"].unique().tolist()

    # Agregar los filtros de Clasificacion_Gasto y Año
    actividades_filtradas = st.multiselect("Seleccione la actividad:", actividades, default=actividades)
    meses_filtrados = st.multiselect("Seleccione el mes:", meses, default=meses)
    año_filtrado = st.multiselect("Seleccione el año:", años, default=años)

    # Filtrar los datos por mes y Año seleccionados
    df_filtrado = df_Horas_consolidado[
        (df_Horas_consolidado['Mes'].isin(meses_filtrados)) &
        (df_Horas_consolidado['Año'].isin(año_filtrado)) &
        (df_Horas_consolidado['Actividad/Equipo'].isin(actividades_filtradas))
    ]

    # Agrupar y sumar los valores por mes
    df_agrupado = df_filtrado.groupby('Mes')['Horas'].sum()
    
    # Cambiar los valores numéricos de los meses por sus nombres
    df_agrupado.index = df_agrupado.index.map(meses_dict)

    # Crear la figura y el eje
    fig, ax = plt.subplots()

    # Crear el gráfico de barras
    barplot = df_agrupado.plot(kind='bar', color='#8B6914', ax=ax)

    # Configurar etiquetas y título
    ax.set_xlabel('Mes')
    ax.set_ylabel('Horas-Máquina')
    ax.set_title('Horas-Máquina')

    # Añadir etiquetas de los valores encima de cada barra
    for p in barplot.patches:
        barplot.annotate(f'{p.get_height():.2f}', (p.get_x() + p.get_width() / 2, p.get_height()), ha='center', va='bottom')

    # Mostrar el gráfico utilizando st.pyplot()
    st.pyplot(fig)
    
    
    #Gráfico Costo - Operador (Costo de las horas)
    
if st.checkbox("Ver Gráfico Costo-Operadores por mes"):
    # Diccionario para mapear los nombres de los meses
    meses_dict = {
        1: "Enero",
        2: "Febrero",
        3: "Marzo",
        4: "Abril"
        # Agrega los demás meses aquí
    }
    # Obtener los valores únicos de mes y Año- actividad
    meses = df_Horas_consolidado['Mes'].unique().tolist()
    años = df_Horas_consolidado['Año'].unique().tolist()
    actividades = df_Horas_consolidado["Actividad/Equipo"].unique().tolist()
    df_Horas_consolidado["Costo-Hora"] = df_Horas_consolidado["Costo-Hora"]/1000000
    # Agregar los filtros de Clasificacion_Gasto y Año
    actividades_filtradas = st.multiselect("Seleccione la actividad:", actividades, default=actividades)
    meses_filtrados = st.multiselect("Seleccione el mes:", meses, default=meses)
    año_filtrado = st.multiselect("Seleccione el año:", años, default=años)
    # Filtrar los datos por mes y Año seleccionados
    df_filtrado = df_Horas_consolidado[
        (df_Horas_consolidado['Mes'].isin(meses_filtrados)) &
        (df_Horas_consolidado['Año'].isin(año_filtrado)) &
        (df_Horas_consolidado['Actividad/Equipo'].isin(actividades_filtradas))
    ]
    # Agrupar y sumar los valores por mes
    df_agrupado = df_filtrado.groupby('Mes')['Costo-Hora'].sum()
    
    # Cambiar los valores numéricos de los meses por sus nombres
    df_agrupado.index = df_agrupado.index.map(meses_dict)

    # Crear la figura y el eje
    fig, ax = plt.subplots()

    # Crear el gráfico de barras
    barplot = df_agrupado.plot(kind='bar', color='#8B6914', ax=ax)

    # Configurar etiquetas y título
    ax.set_xlabel('Mes')
    ax.set_ylabel('Costos $')
    ax.set_title('Costo por Operadores ($) en millones')

    # Añadir etiquetas de los valores encima de cada barra
    for p in barplot.patches:
        barplot.annotate(f'{p.get_height():.2f}', (p.get_x() + p.get_width() / 2, p.get_height()), ha='center', va='bottom')

    # Mostrar el gráfico utilizando st.pyplot()
    st.pyplot(fig)