import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import calendar
import locale

df_gastos_consolidados = pd.read_csv("Archivos_Consolidados/df_gastos.csv", sep=",")
df_gastos_consolidados["Mes"] = pd.to_datetime(df_gastos_consolidados['Fecha']).dt.month
df_gastos_consolidados['Año'] = pd.to_datetime(df_gastos_consolidados['Fecha']).dt.year


st.title("Gasto en la Operación")
st.markdown('''**Esta sección detalla los gastos generados en la operación en cuanto a repuestos,
            mantenimientos y gastos de origen administrativo.**''')

## Tabla consolidada Gastos Operativos por tipo Equipo/Placa

if st.checkbox("Ver tabla resumen gasto ($) ACPM por tipo vehiculo"):
    # Establecer el separador de miles como el punto (.)
    locale.setlocale(locale.LC_ALL, '')
    meses = df_gastos_consolidados["Mes"].unique().tolist()
    años = df_gastos_consolidados["Año"].unique().tolist()
    # Componente multiselec para los meses
    selected_meses = st.multiselect("Selecciona los meses", meses, default=meses)
    # Componente select box para los años
    selected_año = st.selectbox("Selecciona el año", años)
    # Filtrar el DataFrame según los meses y el año seleccionados
    df_filtrado = df_gastos_consolidados[
        (df_gastos_consolidados["Mes"].isin(selected_meses)) & (df_gastos_consolidados["Año"] == selected_año)
    ]
    df_suma_por_vehiculo = df_filtrado.groupby('Equipo/Placa').sum()
    columnas = ["Valor"]
    df_suma_por_vehiculo = df_suma_por_vehiculo[columnas]
    # Formatear los números con el separador de miles como el punto (.)
    df_suma_por_vehiculo["Valor"] = df_suma_por_vehiculo["Valor"].apply(lambda x: locale.format_string("%d", x, grouping=True))
    st.dataframe(df_suma_por_vehiculo)


##Grafico Gastos por tipo (mantenimiento, repuestos, administrativos)

if st.checkbox("Ver Gastos operativos por su clasificación (En millones)"):
    # Obtener los valores únicos de Clasificacion_Gasto y Año
    clasificaciones = df_gastos_consolidados['Clasificacion_Gasto'].unique().tolist()
    años = df_gastos_consolidados['Año'].unique().tolist()
    meses = df_gastos_consolidados['Mes'].unique().tolist()

    # Agregar los filtros de Clasificacion_Gasto, Año y Mes
    clasificaciones_filtradas = st.multiselect("Seleccione la Clasificación de Gasto:", clasificaciones, default=clasificaciones)
    año_filtrado = st.multiselect("Seleccione el año:", años, default=años)
    meses_filtrados = st.multiselect("Seleccione el mes:", meses, default=meses)

    # Filtrar los datos por Clasificacion_Gasto, Año y Mes seleccionados
    df_filtrado = df_gastos_consolidados[
        (df_gastos_consolidados['Clasificacion_Gasto'].isin(clasificaciones_filtradas)) &
        (df_gastos_consolidados['Año'].isin(año_filtrado)) &
        (df_gastos_consolidados['Mes'].isin(meses_filtrados))
    ]

    # Agrupar y sumar los valores por clasificación de gasto
    df_agrupado = df_filtrado.groupby('Clasificacion_Gasto')['Valor'].sum()
    df_agrupado = df_agrupado/1000000

    # Crear la figura y el eje
    fig, ax = plt.subplots()

    # Crear el gráfico de barras
    barplot = df_agrupado.plot(kind='bar', color='#8B6914', ax=ax)

    # Configurar etiquetas y título
    ax.set_xlabel('Clasificación de Gasto')
    ax.set_ylabel('Total Gasto (Millones)')
    ax.set_title('Gastos de la Operación por Clasificación de Gasto')

    # Añadir etiquetas de los valores encima de cada barra
    for p in barplot.patches:
        barplot.annotate(f'{p.get_height():.2f}', (p.get_x() + p.get_width() / 2, p.get_height()), ha='center', va='bottom')

    # Mostrar el gráfico utilizando st.pyplot()
    st.pyplot(fig)



## GRAFICO GASTO POR MES
if st.checkbox("Ver gráfico gasto por mes (En millones)"):

    # Diccionario para mapear los nombres de los meses
    meses_dict = {
        1: "Enero",
        2: "Febrero",
        3: "Marzo",
        4: "Abril"
        # Agrega los demás meses aquí
    }

    # Obtener los valores únicos de Clasificacion_Gasto y Año
    clasificaciones = df_gastos_consolidados['Clasificacion_Gasto'].unique().tolist()
    años = df_gastos_consolidados['Año'].unique().tolist()

    # Agregar los filtros de Clasificacion_Gasto y Año
    clasificaciones_filtradas = st.multiselect("Seleccione la Clasificación de Gasto:", clasificaciones, default=clasificaciones)
    año_filtrado = st.multiselect("Seleccione el año:", años, default=años)

    # Filtrar los datos por Clasificacion_Gasto y Año seleccionados
    df_filtrado = df_gastos_consolidados[
        (df_gastos_consolidados['Clasificacion_Gasto'].isin(clasificaciones_filtradas)) &
        (df_gastos_consolidados['Año'].isin(año_filtrado))
    ]

    # Agrupar y sumar los valores por mes
    df_agrupado = df_filtrado.groupby('Mes')['Valor'].sum()
    df_agrupado = df_agrupado/1000000

    # Cambiar los valores numéricos de los meses por sus nombres
    df_agrupado.index = df_agrupado.index.map(meses_dict)

    # Crear la figura y el eje
    fig, ax = plt.subplots()

    # Crear el gráfico de barras
    barplot = df_agrupado.plot(kind='bar', color='#8B6914', ax=ax)

    # Configurar etiquetas y título
    ax.set_xlabel('Mes')
    ax.set_ylabel('Total Gasto')
    ax.set_title('Gastos de la Operación en millones')

    # Añadir etiquetas de los valores encima de cada barra
    for p in barplot.patches:
        barplot.annotate(f'{p.get_height():.2f}', (p.get_x() + p.get_width() / 2, p.get_height()), ha='center', va='bottom')

    # Mostrar el gráfico utilizando st.pyplot()
    st.pyplot(fig)

if st.checkbox("Ver todos los gastos registrados a la fecha"):
    st.dataframe(df_gastos_consolidados)