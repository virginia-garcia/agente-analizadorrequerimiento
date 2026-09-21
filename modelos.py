"""Modelos Pydantic: definen y validan la estructura del documento funcional.
Los `min_length` fuerzan una profundidad mínima: si el modelo devuelve menos,
la validación falla y el agente reintenta."""
from typing import Literal

from pydantic import BaseModel, Field


class HistoriaUsuario(BaseModel):
    id: str = Field(description="Identificador, ej: HU-01")
    titulo: str
    prioridad: Literal["Alta", "Media", "Baja"]
    como: str
    quiero: str
    para: str
    criterios_de_aceptacion: list[str] = Field(min_length=3)


class SolucionTecnica(BaseModel):
    enfoque: str
    componentes: list[str] = Field(min_length=2)
    datos_necesarios: list[str] = Field(default_factory=list)


class Riesgo(BaseModel):
    riesgo: str
    mitigacion: str


class Metrica(BaseModel):
    metrica: str
    objetivo: str


class Documento(BaseModel):
    resumen: str
    historias_de_usuario: list[HistoriaUsuario] = Field(min_length=4)
    requisitos_no_funcionales: list[str] = Field(min_length=3)
    solucion_tecnica: SolucionTecnica
    riesgos: list[Riesgo] = Field(min_length=3)
    metricas_de_exito: list[Metrica] = Field(min_length=3)
    supuestos: list[str] = Field(default_factory=list)
    fuera_de_alcance: list[str] = Field(default_factory=list)
    preguntas_abiertas: list[str] = Field(default_factory=list)


class Revision(BaseModel):
    aprobado: bool
    observaciones: list[str] = Field(default_factory=list)
