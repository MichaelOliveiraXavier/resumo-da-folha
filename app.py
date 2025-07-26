import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="Resumo da Folha", layout="wide")

st.title("📊 Resumo da Folha de Pagamento")

uploaded_file = st.file_uploader("📂 Envie a planilha `.xlsx` com os dados", type=["xlsx"])

if uploaded_file:
    try:
        # Leitura inicial para identificar linha do cabeçalho
        xls = pd.ExcelFile(uploaded_file)
        preview = xls.parse(xls.sheet_names[0])
        header_row_index = preview[preview.iloc[:, 2] == "FUNCIONÁRIO"].index[0]

        # Ler planilha com cabeçalhos corretos
        df = pd.read_excel(uploaded_file, sheet_name=xls.sheet_names[0], skiprows=header_row_index + 1)
        df.columns = ["ID", "Código", "Funcionário", "Cargo", "Premiação"]
        df = df.dropna(subset=["Funcionário"])

        # Filtro
        st.sidebar.header("🔍 Filtros")
        funcionarios = ["Todos"] + sorted(df["Funcionário"].unique())
        escolha = st.sidebar.selectbox("Selecionar Funcionário", funcionarios)

        if escolha != "Todos":
            df_filtrado = df[df["Funcionário"] == escolha]
        else:
            df_filtrado = df

        # Mostrar dados
        st.dataframe(df_filtrado, use_container_width=True)

        # Exportar dados filtrados
        def to_excel(data):
            output = BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                data.to_excel(writer, index=False, sheet_name='Resumo')
            output.seek(0)
            return output

        excel_data = to_excel(df_filtrado)
        st.download_button("⬇️ Baixar Excel com dados filtrados", data=excel_data,
                           file_name="resumo_folha.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    except Exception as e:
        st.error(f"Erro ao processar a planilha: {e}")
else:
    st.info("Envie uma planilha para visualizar os dados.")
