import argparse
import logging
import sys
from datetime import datetime
from pathlib import Path

from agente import analizar_requerimiento
from exportar import a_docx, a_markdown, a_pdf

EXPORTADORES = {
    "md": lambda d, r: a_markdown(d, r).encode("utf-8"),
    "docx": a_docx,
    "pdf": a_pdf,
    "json": lambda d, r: d.model_dump_json(indent=2).encode("utf-8"),
}


def main():
    parser = argparse.ArgumentParser(description="Agente analizador de requerimientos")
    parser.add_argument("texto", nargs="?", help="Requerimiento en texto")
    parser.add_argument("--archivo", help="Ruta a un .txt con el requerimiento")
    parser.add_argument("--formato", nargs="+", default=["md"], choices=EXPORTADORES,
                        help="Formatos de salida (default: md)")
    parser.add_argument("--salida", default="salida", help="Carpeta de salida")
    args = parser.parse_args()

    if args.archivo:
        requerimiento = Path(args.archivo).read_text(encoding="utf-8").strip()
    elif args.texto:
        requerimiento = args.texto
    else:
        parser.error("Pasá un texto o --archivo")

    logging.basicConfig(level=logging.WARNING)
    try:
        doc, _ = analizar_requerimiento(requerimiento, on_paso=lambda m: print(f"-> {m}"))
    except Exception as e:
        sys.exit(f"Error: {e}")

    carpeta = Path(args.salida)
    carpeta.mkdir(exist_ok=True)
    sello = datetime.now().strftime("%Y%m%d_%H%M%S")
    for fmt in args.formato:
        ruta = carpeta / f"requerimiento_{sello}.{fmt}"
        ruta.write_bytes(EXPORTADORES[fmt](doc, requerimiento))
        print(f"Generado: {ruta}")


if __name__ == "__main__":
    main()
