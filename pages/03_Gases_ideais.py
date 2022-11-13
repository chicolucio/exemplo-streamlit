from io import BytesIO
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
from src.gas_ideal import GasIdeal

st.set_page_config(
    page_title="Gases ideais - PyMat 2022", page_icon="images/pymat.ico", layout="wide"
)

st.title("Exemplo - Gases ideais")

st.markdown(
    r"""
    Para um gás ideal
    
    $$ P = f(n, V, T) \therefore PV = nRT $$
    
    Nos gráficos a seguir, $n = 1 \text{ mol}$
    """
)

gas_ideal = GasIdeal()
faixa_temperaturas = np.linspace(1, 400, 100)
faixa_volumes = np.linspace(1, 10, 100)

with st.sidebar:
    st.header("Variáveis:")

    ponto_temperatura = st.slider("Temperatura fixa / K", 50, 400, 300, 50)
    ponto_volume = st.slider("Volume fixo / V", 1.0, 10.0, 5.0, 1.0)

    ponto_pressao = (
        gas_ideal.mol * gas_ideal.CONSTANTE_GASES * ponto_temperatura / ponto_volume
    )

    mostrar_ponto_pressao = st.metric("Pressão fixa / atm", round(ponto_pressao, 2))

graficos_2d = st.expander("Gráficos 2D", expanded=True)

with graficos_2d:
    colunas_2d = st.columns(3)

    with colunas_2d[0]:
        fig, _ = gas_ideal.plot_2d(
            "PV",
            ponto_temperatura,
            faixa_abscissa=(min(faixa_volumes), max(faixa_volumes)),
        )
        st.pyplot(fig)
    with colunas_2d[1]:
        fig, _ = gas_ideal.plot_2d(
            "TV",
            ponto_pressao,
            faixa_abscissa=(min(faixa_temperaturas), max(faixa_temperaturas)),
        )
        st.pyplot(fig)
    with colunas_2d[2]:
        fig, _ = gas_ideal.plot_2d(
            "TP",
            ponto_volume,
            faixa_abscissa=(min(faixa_temperaturas), max(faixa_temperaturas)),
        )
        st.pyplot(fig)


grafico_3d = st.expander("Gráfico 3D", expanded=True)

with grafico_3d:
    with st.sidebar:
        st.header("Controle visão 3D:")

        mostrar_ponto = st.checkbox("Mostrar ponto", value=False)
        mostrar_curvas = st.checkbox("Mostrar curvas", value=False)

        elev = st.slider("Elevação", 0, 360, 30, 30)
        azim = st.slider("Azimutal", 0, 360, 330, 30)

    fig = plt.figure(tight_layout=True)
    ax = fig.add_subplot(111, projection="3d")
    gas_ideal.plot_3d(
        faixa_volumes,
        faixa_temperaturas,
        step=1,
        visao_inicial=(elev, azim),
        ponto_VT=(ponto_volume, ponto_temperatura),
        mostrar_ponto=mostrar_ponto,
        mostrar_curva_PT=mostrar_curvas,
        mostrar_curva_PV=mostrar_curvas,
        mostrar_curva_VT=mostrar_curvas,
    )

    buf = BytesIO()
    fig.savefig(buf, format="png")
    with st.sidebar:
        largura_imagem = st.number_input("Largura imagem", 1, 2000, 900, 50)
        usar_largura_coluna = st.checkbox("Usar largura da coluna")
    st.image(buf, width=largura_imagem, use_column_width=usar_largura_coluna)
