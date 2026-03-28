from openai import OpenAI
client = OpenAI()

def analizar_requerimiento(texto):
    prompt = f"""
    Actúa como Analista Funcional.

    Requerimiento:
    {texto}

    Genera:
    1. Historia de usuario
    2. Criterios de aceptación
    3. Solución técnica
    4. Riesgos
    5. Métricas de éxito
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content


print(analizar_requerimiento("Un e-commerce quiere mejorar recomendaciones"))
