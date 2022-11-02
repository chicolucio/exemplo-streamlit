import streamlit as st

st.set_page_config(page_title="Streamlit - PyMat 2022",
                   page_icon="images/pymat.ico")

st.title("Streamlit - PyMat 2022")

columns = st.columns(2)

with columns[0]:
    st.image("images/streamlit_logo.png")
with columns[1]:
    st.image("images/pymat.ico")

st.markdown("""
Usualmente dedicamos muito tempo no desenvolvimento de códigos para resolver um
determinado problema. Mas como mostrar visualmente o resultado para as partes
interessadas, especialmente as que não lidam tanto com programação? E, mais, de uma forma
*fácil, interativa e com o mínimo de barreiras*? 

Durante muito tempo, especialmente em alguns nichos mais científicos, esse papel foi 
exercido pelo Jupyter Notebook. 
No entanto, cada vez mais há a necessidade de adotar meios de compartilhamento mais 
práticos e multiplataformas. Afinal, nada mais simples que clicar em um link para uma 
página web. Nesse contexto, o **Streamlit** tem se destacado. Nesta palestra, veremos 
exemplos de aplicativos e entenderemos a estrutura básica de um projeto Streamlit.
""")
