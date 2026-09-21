
import json
import logging
import os
from typing import Type, TypeVar

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel, ValidationError

from modelos import Documento, Revision

load_dotenv()
log = logging.getLogger("agente")

MODELO = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
T = TypeVar("T", bound=BaseModel)


def llamar_llm(system: str, user: str) -> str:
    """Llamada cruda al modelo; devuelve texto JSON. (Se mockea en los tests.)"""
    client = OpenAI()  
    resp = client.chat.completions.create(
        model=MODELO,
        temperature=0.3,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
    )
    log.info("tokens usados: %s", resp.usage.total_tokens if resp.usage else "?")
    return resp.choices[0].message.content


def llamar_validado(modelo: Type[T], system: str, user: str, reintentos: int = 2) -> T:
    
    error = None
    for intento in range(reintentos + 1):
        prompt = user
        if error:
            prompt += (
                f"\n\nTu respuesta anterior NO era válida: {error}\n"
                "Corregila y devolvé solo el JSON completo."
            )
        raw = llamar_llm(system, prompt)
        try:
            return modelo.model_validate_json(raw)
        except (ValidationError, json.JSONDecodeError) as e:
            error = str(e)[:600]
            log.warning("salida inválida (intento %d/%d): %s", intento + 1, reintentos + 1, error)
    raise ValueError(f"El modelo no devolvió un JSON válido tras {reintentos + 1} intentos.")


def _esquema(modelo: Type[BaseModel]) -> str:
    return json.dumps(modelo.model_json_schema(), ensure_ascii=False)


GUIA_ANALISTA = (
    "Generá documentación funcional completa y detallada:\n"
    "- Entre 5 y 8 historias de usuario, cada una con id (HU-01...), título y prioridad.\n"
    "- De 3 a 5 criterios de aceptación POR historia, en formato Dado/Cuando/Entonces, "
    "medibles e incluyendo casos borde y de error.\n"
    "- Requisitos no funcionales (rendimiento, seguridad, privacidad, disponibilidad).\n"
    "- Solución técnica con enfoque, componentes y datos necesarios.\n"
    "- Al menos 3 riesgos (técnicos y de negocio) con su mitigación.\n"
    "- Al menos 3 métricas de éxito con objetivos numéricos.\n"
    "- Supuestos, fuera de alcance y preguntas abiertas para el negocio.\n"
    "Escribí en español, sé concreto y evitá generalidades."
)


def agente_analista(requerimiento: str) -> Documento:
    system = (
        "Sos un Analista Funcional senior. Respondé SOLO con JSON válido que "
        f"cumpla este JSON Schema:\n{_esquema(Documento)}\n\n{GUIA_ANALISTA}"
    )
    return llamar_validado(Documento, system, f"Requerimiento de negocio:\n{requerimiento}")


def agente_revisor(requerimiento: str, borrador: Documento) -> Revision:
    system = (
        "Sos un revisor crítico de documentación funcional. Buscá criterios no "
        "medibles, historias sin casos borde, riesgos omitidos, métricas sin objetivo "
        "numérico y supuestos no declarados. Aprobá solo si está a nivel de entrega a cliente. "
        f"Respondé SOLO con JSON que cumpla este JSON Schema:\n{_esquema(Revision)}"
    )
    user = f"Requerimiento:\n{requerimiento}\n\nBorrador:\n{borrador.model_dump_json()}"
    return llamar_validado(Revision, system, user)


def agente_refinador(requerimiento: str, borrador: Documento, observaciones: list[str]) -> Documento:
    system = (
        "Sos un Analista Funcional senior. Corregí el borrador aplicando las "
        f"observaciones. Respondé SOLO con JSON que cumpla este JSON Schema:\n{_esquema(Documento)}"
    )
    user = (
        f"Requerimiento:\n{requerimiento}\n\nBorrador:\n{borrador.model_dump_json()}\n\n"
        f"Observaciones a corregir:\n{json.dumps(observaciones, ensure_ascii=False)}"
    )
    return llamar_validado(Documento, system, user)


def analizar_requerimiento(requerimiento: str, on_paso=None) -> tuple[Documento, Revision]:
    """Ejecuta el flujo completo. `on_paso(texto)` permite mostrar progreso (CLI/UI)."""
    avisar = on_paso or (lambda _: None)

    avisar("1/3 Analista: generando borrador...")
    borrador = agente_analista(requerimiento)

    avisar("2/3 Revisor: evaluando calidad...")
    revision = agente_revisor(requerimiento, borrador)
    if revision.aprobado:
        avisar("Borrador aprobado sin cambios.")
        return borrador, revision

    avisar(f"3/3 Refinador: aplicando {len(revision.observaciones)} observaciones...")
    return agente_refinador(requerimiento, borrador, revision.observaciones), revision
