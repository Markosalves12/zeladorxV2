import pandas as pd
import matplotlib.pyplot as plt
from shapely import wkt
from shapely.geometry import Polygon
from openpyxl import Workbook
from django.http import HttpResponse
from django.core.files.storage import default_storage
from io import BytesIO
from openpyxl.drawing.image import Image
from medidor.models import DocsFromProcess

def processar_poligonos(request, id_random):
    objeto = DocsFromProcess.objects.get(id_random=id_random)

    with default_storage.open(objeto.document.name, 'rb') as file:
        df = pd.read_csv(file) if objeto.document.name.endswith('.csv') else pd.read_excel(file)

    if 'WKT' not in df.columns:
        raise ValueError("O arquivo deve conter uma coluna 'WKT'.")

    df['Área estimada'] = df['WKT'].apply(
        lambda w: wkt.loads(w).area * 111319.9**2 if isinstance(wkt.loads(w), Polygon) else None)

    wb = Workbook()
    ws = wb.active
    ws.title = "Dimensionamento"
    ws.append(list(df.columns))
    for row in df.itertuples(index=False):
        ws.append(row)

    for coluna in df.drop(columns=['WKT', 'nome', 'descrição'], errors='ignore').columns:
        df[coluna] = df[coluna].astype(str).str.strip().str.capitalize()
        valores_unicos = sorted(df[coluna].dropna().unique())

        if len(valores_unicos) <= 30:
            plt.figure(figsize=(10, 8))  # Aumentado o tamanho
            cores = plt.cm.get_cmap('tab20', len(valores_unicos))
            for valor, cor in zip(valores_unicos, cores.colors):
                subset = df[df[coluna] == valor]
                for wkt_str, nome in zip(subset['WKT'], subset.get('nome', ['']*len(subset))):
                    polygon = wkt.loads(wkt_str)
                    if isinstance(polygon, Polygon):
                        x, y = polygon.exterior.xy
                        plt.fill(x, y, color=cor, alpha=0.5)
                        centroid = polygon.centroid
                        plt.text(centroid.x, centroid.y, nome, fontsize=5, ha='center')  # Fonte reduzida
                plt.plot([], [], color=cor, label=f"{valor}")

            plt.legend(title=coluna)
            plt.title(f"Polígonos por {coluna}")
            plt.xlabel("Longitude")
            plt.ylabel("Latitude")

            img_bytes = BytesIO()
            plt.savefig(img_bytes, format='png')
            plt.close()

            ws_img = wb.create_sheet(title=coluna)
            img_bytes.seek(0)
            ws_img.add_image(Image(img_bytes), 'A1')

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="poligonos_processados_{id_random}.xlsx"'
    wb.save(response)
    return response
