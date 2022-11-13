import streamlit as st
from src.decay import DADOS, DecaimentoRadioativo

st.set_page_config(
    page_title="Decaimento radioativo - PyMat 2022", page_icon="images/pymat.ico"
)

TEXTO = "pages/decaimento.md"

st.title("Exemplo - Decaimento radioativo")

st.markdown(
    r"""
Sabe-se que o isótopo fósforo-32 é radioativo, sofrendo decaimento beta de acordo
com a equação

$${_{15}^{32}P \rightarrow _{16}^{32}S^{+1} + e + \nu_e}$$

Vamos obter o tempo-meia deste isótopo a partir de dados experimentais e comparar com
o valor da literatura. No processo, entender um pouco mais sobre propagação de erros,
fit de curvas e linearização.
"""
)

teoria = st.expander("Clique para ler a teoria")

with open(TEXTO) as f:
    linhas = f.read()

with teoria:
    st.markdown("".join(linhas))


tempo = DADOS["dias"]
contagem = DADOS["contagem"]
incerteza = DADOS["incerteza"]

fosforo32 = DecaimentoRadioativo(
    tempo,
    contagem,
    incerteza,
    literatura_pre_exp=1000,
    literatura_meia_vida=14.29,
    literatura_numero_pontos=120,
)

backend_grafico = st.selectbox(
    "Escolha o backend gráfico", ("Matplotlib", "Plotly"), index=1
)

labels = ("Incerteza", "Literatura", "Fit", "Escala logarítmica", "Linearização")
colunas_checkboxes = st.columns(len(labels))

checkboxes = dict()

for label, coluna in zip(labels, colunas_checkboxes):
    with coluna:
        checkbox = st.checkbox(label)
        checkboxes[label] = checkbox

if checkboxes["Escala logarítmica"] and checkboxes["Linearização"]:
    st.warning("Linearização só funciona se desmarcar escala logarítmica", icon="⚠️")

if backend_grafico == "Matplotlib":
    fig, ax = fosforo32.plot(
        erro=checkboxes["Incerteza"],
        escala_log10=checkboxes["Escala logarítmica"],
        curva_literatura=checkboxes["Literatura"],
        linearizacao=checkboxes["Linearização"],
        fit=checkboxes["Fit"],
    )

    st.pyplot(fig)

else:
    fig = fosforo32.plot(
        backend="plotly",
        erro=checkboxes["Incerteza"],
        escala_log10=checkboxes["Escala logarítmica"],
        curva_literatura=checkboxes["Literatura"],
        linearizacao=checkboxes["Linearização"],
        fit=checkboxes["Fit"],
    )

    st.plotly_chart(fig, use_container_width=True)

st.latex(
    rf"""
\text{{Equação de fit}}: {fosforo32.fit_exponencial().valores_otimos.pre_exp:.1f} 
\exp(-{fosforo32.fit_exponencial().valores_otimos.taxa_decaimento:.4f}t) + 
{fosforo32.fit_exponencial().valores_otimos.constante:.2f}"""
)

st.latex(
    rf"t_{{1/2}} \text{{ literatura}}: {fosforo32.literatura_meia_vida} \text{{ dias}}"
)
st.latex(
    rf"t_{{1/2}} \text{{ calculado}}: {fosforo32.tempo_de_meia_vida} \text{{ dias}}"
)

dataframe = st.expander("Clique para ver os dados experimentais")

with dataframe:
    st.dataframe(DADOS.style.format(formatter={"dias": "{:.0f}"}))
