
import streamlit as st

from agente import analizar_requerimiento
from exportar import a_docx, a_markdown, a_pdf

st.set_page_config(page_title="Analizador de Requerimientos", page_icon="📝", layout="centered")
st.title("📝 Analizador de Requerimientos")
st.caption("Transformá un requerimiento de negocio en documentación funcional lista para enviar. "
           "Flujo de 3 agentes: Analista → Revisor → Refinador.")

EJEMPLO = "Una plataforma de e-commerce necesita mejorar su sistema de recomendaciones de productos para aumentar la conversión de ventas."
requerimiento = st.text_area("Requerimiento de negocio", value=EJEMPLO, height=130)

if st.button("Generar documentación", type="primary", disabled=not requerimiento.strip()):
    try:
        with st.status("Ejecutando agentes...", expanded=True) as estado:
            doc, revision = analizar_requerimiento(requerimiento, on_paso=st.write)
            estado.update(label="Listo", state="complete")
        st.session_state["resultado"] = (doc, revision, requerimiento)
    except Exception as e:
        st.error(f"No se pudo generar el documento: {e}")

if "resultado" in st.session_state:
    doc, revision, req = st.session_state["resultado"]

    st.subheader("Descargar")
    c1, c2, c3 = st.columns(3)
    c1.download_button("⬇️ Word (.docx)", a_docx(doc, req), "requerimiento.docx",
                       "application/vnd.openxmlformats-officedocument.wordprocessingml.document")
    c2.download_button("⬇️ PDF", a_pdf(doc, req), "requerimiento.pdf", "application/pdf")
    c3.download_button("⬇️ Markdown", a_markdown(doc, req), "requerimiento.md", "text/markdown")

    tab_doc, tab_rev, tab_json = st.tabs(["Documento", "Revisión del agente", "JSON"])
    with tab_doc:
        st.markdown(a_markdown(doc, req))
    with tab_rev:
        if revision.aprobado:
            st.success("El revisor aprobó el borrador sin cambios.")
        else:
            st.warning("El revisor pidió correcciones, que el refinador aplicó:")
            for o in revision.observaciones:
                st.markdown(f"- {o}")
    with tab_json:
        st.json(doc.model_dump())
