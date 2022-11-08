import streamlit as st
from src.decay import DADOS

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

st.dataframe(DADOS.style.format(formatter={"dias": "{:.0f}"}))
