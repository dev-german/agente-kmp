from flask import Flask, request, render_template_string
from datetime import datetime

app = Flask(__name__)

DOCUMENTOS_PROCESADOS = [
    {
        "nombre": "Normativa de Seguridad",
        "contenido": "La Intendencia de Seguridad es responsable del cumplimiento normativo.",
        "seccion": "normativa",
        "archivo": "normativa_seguridad.pdf",
        "relevancia": 9
    },
    {
        "nombre": "Plan de Contingencia",
        "contenido": "Se deben definir escenarios posibles de incidentes.",
        "seccion": "planificacion",
        "archivo": "plan_contingencia.docx",
        "relevancia": 7
    },
    {
        "nombre": "Acta de Comité de Seguridad",
        "contenido": "Se discutieron políticas de respaldo y recuperación ante desastres.",
        "seccion": "actas",
        "archivo": "acta_comite_seguridad.pdf",
        "relevancia": 6
    },
    {
        "nombre": "Informe de Brechas",
        "contenido": "Se detectaron brechas en la autenticación de usuarios.",
        "seccion": "evaluacion",
        "archivo": "informe_brechas.xlsx",
        "relevancia": 8
    },
    {
        "nombre": "Matriz de Riesgos",
        "contenido": "Los riesgos se clasifican según probabilidad e impacto.",
        "seccion": "riesgos",
        "archivo": "matriz_riesgos.xlsx",
        "relevancia": 7
    },
    {
        "nombre": "Política de Seguridad de la Información",
        "contenido": "Todo el personal debe firmar el compromiso de confidencialidad.",
        "seccion": "politicas",
        "archivo": "politica_seguridad.pdf",
        "relevancia": 9
    },
    {
        "nombre": "Reglamento Interno",
        "contenido": "Define los horarios, responsabilidades y sanciones del personal.",
        "seccion": "normativa",
        "archivo": "reglamento_interno.pdf",
        "relevancia": 6
    },
    {
        "nombre": "Procedimiento de Gestión de Incidentes",
        "contenido": "Todo incidente debe ser reportado dentro de las 24 horas.",
        "seccion": "procedimientos",
        "archivo": "gestion_incidentes.docx",
        "relevancia": 8
    },
    {
        "nombre": "Manual del Usuario SGSI",
        "contenido": "El sistema de gestión requiere credenciales únicas por usuario, existen unas credenciales secundarias.",
        "seccion": "manuales",
        "archivo": "manual_usuario_sgsi.pdf",
        "relevancia": 7
    },
    {
        "nombre": "Evaluación de Impacto",
        "contenido": "Evaluación de impacto en la protección de datos personales autenticación. la autenticación se realiza con",
        "seccion": "evaluacion",
        "archivo": "evaluacion_impacto.pdf",
        "relevancia": 6
    }
]

historial_sugerencias = []

# Algoritmo KMP
def construir_tabla_kmp(patron):
    m = len(patron)
    lps = [0] * m
    length = 0
    i = 1
    while i < m:
        if patron[i] == patron[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length > 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1
    return lps

def busqueda_kmp(text, patron):
    if not patron:
        return 0
    n, m = len(text), len(patron)
    lps = construir_tabla_kmp(patron)
    i = j = count = 0
    while i < n:
        if text[i] == patron[j]:
            i += 1
            j += 1
            if j == m:
                count += 1
                j = lps[j - 1]
        else:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    return count

@app.route("/percepcion", methods=["POST"])
def recibir_percepcion():
    data = request.json
    seccion = data.get("seccion", "")
    patron = data.get("patron", "")
    timestamp = datetime.now()

    print(f"Percepción recibida: sección = {seccion}, patrón = {patron}")

    sugerencias = []
    for doc in DOCUMENTOS_PROCESADOS:
        if doc["seccion"] == seccion:
            ocurrencias = busqueda_kmp(doc["contenido"], patron)
            if ocurrencias > 0:
                sugerencias.append({
                    "titulo": doc["nombre"],
                    "coindicencias": ocurrencias,
                    "relevancia": doc["relevancia"],                    
                    "contenido": doc["contenido"],
                    "archivo": doc["archivo"],
                    "link": f"/static/docs_procesados/{doc['archivo']}",
                    "fecha": timestamp.strftime("%Y-%m-%d %H:%M:%S")
                })

    sugerencias.sort(key=lambda d: (d.get("coincidencias", 0), d.get("relevancia", 0)), reverse=True)

    historial_sugerencias.append({
        "seccion": seccion,
        "hora": timestamp,
        "patron": patron,
        "sugerencias": sugerencias
    })

    return {"status": "ok", "sugerencias": sugerencias}, 200

@app.route("/")
def interfaz():
    html = """
    <html>
    <head>
        <meta charset="utf-8">
        <meta http-equiv="refresh" content="10">
        <title>Historial de Sugerencias del Agente</title>
        <style>
            body { font-family: Arial, sans-serif; background: #f4f4f4; padding: 2rem; }
            h2 { color: #003366; }
            .bloque {
                background: #fff; border: 1px solid #ccc; margin-bottom: 1.5rem;
                padding: 1rem; border-radius: 8px; box-shadow: 1px 1px 5px rgba(0,0,0,0.05);
            }
            .hora { font-size: 0.85rem; color: #666; margin-bottom: 0.5rem; }
            ul { padding-left: 1.2rem; }
            li { margin-bottom: 0.6rem; }
            .relevancia { font-size: 0.85rem; color: #555; }
        </style>
    </head>
    <body>
        <h2>Historial de Sugerencias del Agente (KMP)</h2>

        {% if historial %}
            {% for entrada in historial|reverse %}
    <div class="bloque">
        <div class="hora">
            <strong>Sección:</strong> {{ entrada.seccion }}<br>
            <strong>Patrón:</strong> "{{ entrada.patron }}"<br>
            <strong>Hora:</strong> {{ entrada.hora.strftime('%Y-%m-%d %H:%M:%S') }}
        </div>

        {% if entrada.sugerencias %}
            <ul>
                {% for doc in entrada.sugerencias %}
                    <li>
                        <strong>{{ doc.titulo }}</strong> – {{ doc.coindicencias }} coincidencias<br>
                        <a href="{{ doc.link }}" target="_blank">🔗 Ver documento</a><br>
                        <span class="relevancia">Archivo: {{ doc.archivo }}<br>Fecha: {{ doc.fecha }}</span>
                    </li>
                {% endfor %}
            </ul>
        {% else %}
            <p style="color: #b00;">⚠️ No se encontraron sugerencias para esta percepción.</p>
        {% endif %}
    </div>
{% endfor %}

        {% else %}
            <p>No hay sugerencias todavía. Edita una sección del FM35 y proporciona un patrón para comenzar.</p>
        {% endif %}
    </body>
    </html>
    """
    return render_template_string(html, historial=historial_sugerencias)

if __name__ == "__main__":
    app.run(port=5000)
