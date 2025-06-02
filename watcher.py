from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import requests
import os
import yaml

# Guarda los últimos tiempos en que cada archivo fue procesado
ultimos_eventos = {}
INTERVALO_MINIMO = 3  # segundos

CARPETA_DOCUMENTOS = "fm35/docs"
AGENTE_URL = "http://localhost:5000/percepcion"

class ManejadorDeCambios(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith(".md") and os.path.isfile(event.src_path):
            ahora = time.time()
            archivo = event.src_path

            # Ignorar eventos duplicados
            ultimo = ultimos_eventos.get(archivo, 0)
            if ahora - ultimo < INTERVALO_MINIMO:
                print(f"Evento ignorado: {archivo}")
                return
            ultimos_eventos[archivo] = ahora

            # Procesar el archivo
            try:
                with open(archivo, 'r', encoding='utf-8') as f:
                    contenido = f.read()

                if contenido.startswith('---'):
                    partes = contenido.split('---')
                    if len(partes) >= 3:
                        try:
                            metadata = yaml.safe_load(partes[1])
                            tags = metadata.get('tags', [])
                            patron_raw = metadata.get('patron', '')
                            patron = patron_raw.strip() if isinstance(patron_raw, str) else ''
                            seccion = next((t.split(":")[1] for t in tags if isinstance(t, str) and t.startswith("seccion:")), None)


                            if seccion and patron:
                                payload = {
                                    "archivo": os.path.basename(archivo),
                                    "seccion": seccion,
                                    "patron": patron,
                                    "timestamp": time.time()
                                }
                                print(f"[✓] Sección: {seccion}, Patrón: '{patron}' → Enviando al agente")
                                requests.post(AGENTE_URL, json=payload)
                            else:
                                print(f"Faltan 'seccion' o 'patron' en {archivo}. No se enviará.")
                        except yaml.YAMLError as ye:
                            print(f"[✗] YAML inválido en {archivo}: {ye}")
                    else:
                        print(f"Frontmatter mal formado en {archivo}")
                else:
                    print(f"Archivo sin frontmatter válido: {archivo}")

            except Exception as e:
                print(f"[✗] Error procesando {archivo}: {e}")

# Iniciar watcher
if __name__ == "__main__":
    event_handler = ManejadorDeCambios()
    observer = Observer()
    observer.schedule(event_handler, path=CARPETA_DOCUMENTOS, recursive=False)
    observer.start()
    print(f"👀 Observando cambios en: {CARPETA_DOCUMENTOS}")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
