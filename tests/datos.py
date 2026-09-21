
REQ = ("Una plataforma de e-commerce necesita mejorar su sistema de recomendaciones "
       "de productos para aumentar la conversión de ventas.")


def _hu(i, titulo, prio, como, quiero, para, crit):
    return {"id": f"HU-{i:02d}", "titulo": titulo, "prioridad": prio, "como": como,
            "quiero": quiero, "para": para, "criterios_de_aceptacion": crit}


DOC = {
    "resumen": ("Se propone un motor de recomendaciones que personalice los productos mostrados en el home, "
                "la ficha de producto y el carrito, con el objetivo de aumentar la tasa de conversión y el ticket promedio."),
    "historias_de_usuario": [
        _hu(1, "Recomendaciones en el home", "Alta", "cliente registrado",
            "ver productos sugeridos según mi historial", "encontrar rápido lo que me interesa",
            ["Dado un cliente con al menos 3 compras, cuando entra al home, entonces ve 8 productos recomendados.",
             "Dado un cliente sin historial, cuando entra al home, entonces ve los productos más vendidos.",
             "Dado que el servicio de recomendaciones no responde en 2 s, cuando carga el home, entonces se muestran productos destacados sin error visible."]),
        _hu(2, "Productos relacionados en la ficha", "Alta", "visitante",
            "ver productos complementarios en la ficha de un producto", "comprar artículos que combinan",
            ["Dado un producto con stock, cuando abro su ficha, entonces veo hasta 6 productos relacionados.",
             "Dado un producto sin stock, cuando abro su ficha, entonces no se recomiendan otros sin stock.",
             "Dado un producto nuevo sin datos de compra, cuando abro su ficha, entonces se recomiendan productos de la misma categoría."]),
        _hu(3, "Sugerencias en el carrito", "Media", "cliente",
            "recibir sugerencias antes de pagar", "sumar accesorios sin buscarlos",
            ["Dado un carrito con 1 o más productos, cuando lo abro, entonces veo hasta 4 sugerencias.",
             "Dado que agrego una sugerencia, cuando se actualiza el carrito, entonces el total se recalcula al instante.",
             "Dado un producto ya presente en el carrito, cuando se generan sugerencias, entonces ese producto no aparece."]),
        _hu(4, "Control de privacidad", "Media", "cliente",
            "desactivar la personalización", "decidir cómo se usan mis datos",
            ["Dado un cliente con la personalización desactivada, cuando navega, entonces solo ve recomendaciones genéricas.",
             "Dado que desactivo la personalización, cuando confirmo, entonces mi historial deja de usarse en menos de 24 h.",
             "Dado un usuario de la UE, cuando entra por primera vez, entonces se le pide consentimiento explícito."]),
        _hu(5, "Panel de rendimiento", "Baja", "analista de negocio",
            "ver métricas de clics y conversión de las recomendaciones", "medir el impacto y ajustar el modelo",
            ["Dado un rango de fechas, cuando consulto el panel, entonces veo CTR y conversión por ubicación.",
             "Dado que hay un A/B test activo, cuando abro el panel, entonces veo los resultados por variante.",
             "Dado un período sin datos, cuando consulto el panel, entonces se muestra un aviso y no un error."]),
    ],
    "requisitos_no_funcionales": [
        "Las recomendaciones deben responder en menos de 300 ms (percentil 95).",
        "Cumplir con la normativa de protección de datos personales aplicable.",
        "El sistema debe soportar 500 solicitudes por segundo en horas pico.",
        "Disponibilidad mínima del 99,5 % mensual.",
    ],
    "solucion_tecnica": {
        "enfoque": "Modelo híbrido de filtrado colaborativo y basado en contenido, expuesto como un servicio interno vía API REST.",
        "componentes": ["API de recomendaciones", "Pipeline de datos de eventos", "Modelo de ranking", "Caché de resultados", "Panel de métricas"],
        "datos_necesarios": ["Historial de compras", "Eventos de navegación", "Catálogo con categorías y stock"],
    },
    "riesgos": [
        {"riesgo": "Arranque en frío para usuarios y productos nuevos", "mitigacion": "Usar populares y por categoría hasta juntar datos."},
        {"riesgo": "Sesgo hacia productos ya populares", "mitigacion": "Incluir un porcentaje de exploración y revisar la diversidad."},
        {"riesgo": "Incumplimiento de privacidad", "mitigacion": "Consentimiento explícito y anonimización de eventos."},
    ],
    "metricas_de_exito": [
        {"metrica": "Tasa de conversión", "objetivo": "+5 % en 3 meses"},
        {"metrica": "CTR de recomendaciones", "objetivo": "≥ 8 %"},
        {"metrica": "Ticket promedio", "objetivo": "+7 %"},
    ],
    "supuestos": ["Existe al menos 12 meses de historial de compras.", "El catálogo se actualiza a diario."],
    "fuera_de_alcance": ["Recomendaciones por correo electrónico", "Personalización de precios"],
    "preguntas_abiertas": ["¿Se dispone de datos de navegación de usuarios anónimos?", "¿Hay un presupuesto definido para infraestructura?"],
}
