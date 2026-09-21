import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import agente
from exportar import a_docx, a_markdown, a_pdf
from modelos import Documento
from datos import DOC, REQ

def test_exportadores_generan_archivos_validos():
    doc = Documento(**DOC)
    assert a_docx(doc, REQ)[:2] == b"PK"        # .docx es un zip
    assert a_pdf(doc, REQ)[:4] == b"%PDF"
    assert "Tasa de conversión" in a_markdown(doc, REQ)


def test_reintenta_cuando_el_json_es_invalido(monkeypatch):
    respuestas = iter(['{"resumen": "incompleto"}', json.dumps(DOC)])
    monkeypatch.setattr(agente, "llamar_llm", lambda s, u: next(respuestas))
    doc = agente.llamar_validado(Documento, "sys", "user")
    assert doc.resumen.startswith("Se propone")


def test_flujo_completo_con_refinador(monkeypatch):
    revision = json.dumps({"aprobado": False, "observaciones": ["Métricas vagas"]})
    respuestas = iter([json.dumps(DOC), revision, json.dumps(DOC)])
    monkeypatch.setattr(agente, "llamar_llm", lambda s, u: next(respuestas))
    doc, rev = agente.analizar_requerimiento("req")
    assert not rev.aprobado and doc.riesgos


def test_rechaza_documento_demasiado_pobre():
    import pytest
    from pydantic import ValidationError
    pobre = dict(DOC, historias_de_usuario=DOC["historias_de_usuario"][:1])
    with pytest.raises(ValidationError):
        Documento(**pobre)
