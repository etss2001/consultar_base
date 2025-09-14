import streamlit as st
import pandas as pd
import requests
import plotly.express as px


st.set_page_config(layout="wide")

st.markdown("""
    <style>
    .block-container {
        padding-top: 1rem;
        padding-bottom: 0rem;
        padding-left: 5rem;
        padding-right: 5rem;
        max-width: 100%;
    }
    
    .centered-header {
        text-align: center;
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 10px;
        color: #FFC1C7;
    }
    </style>
    """, unsafe_allow_html=True)


API_URL = "https://9ls1vcbcof.execute-api.us-east-1.amazonaws.com/prueba1-apii/base"

def obtener_datos_cliente(documento):
    doc_api = f"{documento}_"
    params = {"documento": doc_api}
    try:
        response = requests.get(API_URL, params=params)
        response.raise_for_status()
        data = response.json()
        items = data.get("items", [])
        return pd.DataFrame(items)
    except Exception as e:
        st.error(f"Error al consultar la API: {e}")
        return pd.DataFrame()

# ========================
def mostrar_kpi(titulo, valor, color_base="#87CEEB"):
    color_interno = "#D0F0FF"
    color_borde = "#00BFFF"
    st.markdown(
        f"""
        <div style="
            background-color: {color_interno};
            border: 2px solid {color_borde};
            padding: 15px;
            border-radius: 12px;
            text-align: center;
            margin-bottom: 10px;
            box-shadow: 2px 2px 5px rgba(0,0,0,0.15);
            font-size: 18px;
            font-weight: bold;
            color: #000080;
        ">
            {titulo}<br><span style="font-size:22px;">{valor}</span>
        </div>
        """,
        unsafe_allow_html=True
    )

# interfaz streamlit
st.title("Consulta de Datos de Cliente")

doc_input = st.text_input("Ingrese el documento del cliente:", value="-2747430000000000000")

if st.button("Buscar"):
    if doc_input.strip() == "":
        st.warning("Ingrese un documento válido.")
    else:
        df = obtener_datos_cliente(doc_input)
        if df.empty:
            st.info("No se encontraron datos para este documento.")
        else:
            st.subheader(f"Datos del cliente {doc_input}")
            
            # Primera fila: tabla de datos y KPIs a la derecha
            col_tabla, col_kpis = st.columns([0.7, 0.3])
            
            with col_tabla:
                st.dataframe(df)
            
            with col_kpis:
                categoria_mayor_gasto = df.loc[df["mnt_trx_mm"].idxmax(), "categoria"]
                mostrar_kpi("Categoría con mayor gasto", categoria_mayor_gasto)

                categoria_mas_trx = df.loc[df["num_trx"].idxmax(), "categoria"]
                mostrar_kpi("Categoría con más transacciones", categoria_mas_trx)
            
            col_bar1, col_bar2 = st.columns(2)
            
            with col_bar1:
                st.markdown('<div class="centered-header">Monto por Categoría</div>', unsafe_allow_html=True)
                
                # monto por categora
                df_monto = df.sort_values("mnt_trx_mm", ascending=False)
                fig_monto = px.bar(
                    df_monto,
                    x="mnt_trx_mm",
                    y="categoria",
                    orientation="h",
                    text="mnt_trx_mm",
                    hover_data={
                        "categoria": True,
                        "mnt_trx_mm": True,
                        "num_trx": True,
                        "pct_mnt_tot": True,
                        "pct_num_trx_tot": True
                    },
                    labels={"mnt_trx_mm": "Monto", "num_trx": "Número de transacciones"},
                    text_auto=True
                )
                fig_monto.update_traces(textfont_color='darkblue', marker_color="#a1cbe7")
                fig_monto.update_layout(
                    height=500, 
                    margin=dict(l=50, r=50, t=20, b=50),
                    showlegend=False,
                    xaxis_title="Monto",
                    yaxis_title="Categoría"
                )
                st.plotly_chart(fig_monto, use_container_width=True)
            
            with col_bar2:
                st.markdown('<div class="centered-header">Número de Transacciones por Categoría</div>', unsafe_allow_html=True)
                
                # num de transacciones por categoria
                df_num = df.sort_values("num_trx", ascending=False)
                fig_num = px.bar(
                    df_num,
                    x="num_trx",
                    y="categoria",
                    orientation="h",
                    text="num_trx",
                    hover_data={
                        "categoria": True,
                        "mnt_trx_mm": True,
                        "num_trx": True,
                        "pct_mnt_tot": True,
                        "pct_num_trx_tot": True
                    },
                    labels={"num_trx": "Número de transacciones", "mnt_trx_mm": "Monto"},
                    text_auto=True
                )
                fig_num.update_traces(textfont_color='darkgreen', marker_color="#89ffa7")
                fig_num.update_layout(
                    height=500, 
                    margin=dict(l=50, r=50, t=20, b=50),
                    showlegend=False,
                    xaxis_title="Número de Transacciones",
                    yaxis_title="Categoría"
                )
                st.plotly_chart(fig_num, use_container_width=True)
            
            st.markdown('<div class="centered-header">Distribución de Monto por Categoría</div>', unsafe_allow_html=True)
            
            # graf circular
            fig_pie = px.pie(
                df,
                names="categoria",
                values="mnt_trx_mm",
                hover_data={
                    "num_trx": True,
                    "pct_mnt_tot": True,
                    "pct_num_trx_tot": True
                },
                labels={"mnt_trx_mm": "Monto", "num_trx": "Número de transacciones"},
                hole=0.3
            )
            fig_pie.update_layout(height=500, margin=dict(l=50, r=50, t=20, b=50))
            st.plotly_chart(fig_pie, use_container_width=True)