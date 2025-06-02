
# 🤖 Agente de Sugerencias KMP para Documentos FM35

Este proyecto implementa un agente inteligente que sugiere documentos relevantes de un repositorio institucional mientras se redacta un documento FM35 (Solicitud de Atención de Requerimientos de Producto Software). Utiliza el algoritmo de búsqueda Knuth-Morris-Pratt (KMP) para encontrar coincidencias.

---

## 📁 Estructura del proyecto

```
watcher/
├── agente.py                 # Agente Flask con lógica de percepción y sugerencia
├── watcher.py                # Observador de archivos Markdown
├── requirements.txt          # Dependencias necesarias
├── fm35/
│   └── docs/                 # Archivos .md que editas (FM35)
└── static/
    └── docs_procesados/     # Archivos PDF, DOCX, etc. sugeridos por el agente
```

---

## 🚀 Requisitos previos

- Python 3.9 o superior
- pip (Python package manager)

---

## 🔧 Instalación

1. Clona este repositorio:

```bash
git clone https://github.com/tuusuario/agente-kmp-fm35.git
cd agente-kmp-fm35
```

2. Crea un entorno virtual (opcional pero recomendado):

```bash
python -m venv .venv
source .venv/bin/activate  # en Windows: .venv\Scripts\activate
```

3. Instala las dependencias:

```bash
pip install -r requirements.txt
```

Contenido de `requirements.txt`:
```text
flask
watchdog
requests
pyyaml 
```

---

## ▶️ Ejecución del Agente

1. Asegúrate de tener la carpeta `static/docs_procesados` con algunos archivos PDF/DOCX usados como sugerencias.

2. Inicia el agente:

```bash
python agente.py
```

- El servidor Flask quedará escuchando en: `http://localhost:5000`
- Puedes visitar el historial de sugerencias en tu navegador: [http://localhost:5000](http://localhost:5000)

---

## 👁️ Observación automática (`watcher.py`)

Este script detecta cambios en archivos `.md` dentro de `fm35/docs` y envía una percepción automática al agente.

```bash
python watcher.py
```

---

## 📝 Estructura esperada de tus archivos Markdown (`fm35/docs/*.md`)

Cada archivo debe tener un *frontmatter* como este:

```markdown
---
id: plan-contingencia
title: Plan de Contingencia
tags: [fm35, seccion:planificacion]
patron: incidentes
---
Contenido del documento...
```

---

## ✅ Prueba rápida

1. Edita o guarda un archivo `.md` dentro de `fm35/docs` con un patrón y sección.
2. El `watcher.py` lo detectará y enviará la percepción al agente.
3. Visita [http://localhost:5000](http://localhost:5000) para ver si el agente te sugiere documentos relevantes.

---

## 💬 Notas adicionales

- El agente sugiere documentos con coincidencias del patrón dentro de la sección especificada.
- Los enlaces a los documentos están activos y apuntan a `/static/docs_procesados/<archivo>`.
- Se utiliza el algoritmo **KMP** para mayor eficiencia en la búsqueda.

---

## 🛠️ Mantenimiento

Si agregas nuevos documentos al repositorio sugerido, colócalos en `static/docs_procesados/` y actualiza la lista `DOCUMENTOS_PROCESADOS` en `agente.py`.

---

## 📄 Licencia

MIT
