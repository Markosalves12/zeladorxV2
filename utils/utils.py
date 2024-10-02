from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
import random
import string
from PIL import Image
import os
from io import BytesIO
from django.core.files.base import ContentFile
from django.shortcuts import reverse
from django.db.models.base import ModelBase
from django.db.models.query import QuerySet


def generate_id_random(length=12):
    characters = string.ascii_letters + string.digits
    random_id = ''.join(random.choices(characters, k=length))
    return random_id


def paginate(request, data_objects, per_page=10):
    paginator = Paginator(data_objects, per_page=per_page)
    page_number = request.GET.get('page')

    try:
        elementos_paginados = paginator.page(page_number)
    except PageNotAnInteger:
        # Se o número da página não for um número inteiro, retorne a primeira página
        elementos_paginados = paginator.page(1)
    except EmptyPage:
        # Se a página estiver fora do intervalo (por exemplo, 9999), retorne a última página de resultados
        elementos_paginados = paginator.page(paginator.num_pages)

    return elementos_paginados


def resize_image(image, max_width=620):
    # Dicionário de mapeamento de extensões para formatos Pillow
    EXTENSION_TO_FORMAT = {
        '.jpg': 'JPEG',
        '.jpeg': 'JPEG',
        '.png': 'PNG',
        '.gif': 'GIF',
        '.bmp': 'BMP',
        '.tiff': 'TIFF',
        '.webp': 'WEBP'
    }

    # Abre a imagem usando Pillow
    img = Image.open(image)

    # Verifica a extensão do arquivo
    ext = os.path.splitext(image.name)[1].lower()
    if ext not in EXTENSION_TO_FORMAT:
        raise ValueError(f"Unsupported file extension: {ext}")

    # Calcula a nova dimensão se a largura for maior que max_width
    if img.width > max_width:
        aspect_ratio = img.height / img.width
        new_width = max_width
        new_height = int(new_width * aspect_ratio)
        img = img.resize((new_width, new_height), Image.LANCZOS)

    # Salva a imagem redimensionada no formato correto
    img_io = BytesIO()
    img_format = EXTENSION_TO_FORMAT[ext]
    img.save(img_io, format=img_format)
    return ContentFile(img_io.getvalue(), image.name)

def aplicar_filtros_dinamicos(queryset, get_data, filtro_mapeamento):
    # Itera sobre os dados enviados no GET
    for field, value in get_data.items():
        if value:  # Apenas aplica o filtro se houver um valor válido
            # Verifica se o campo está no mapeamento de filtros personalizados
            print(type(value))
            if field in filtro_mapeamento:
                filtro_especifico = filtro_mapeamento[field]

                # Verifica se o campo é 'DataDeInicio' para aplicar o filtro >=
                if field == 'DataDeInicio':
                    queryset = queryset.filter(**{f"{filtro_especifico}__gte": value})

                # Verifica se o campo é 'DataDeConclusao' para aplicar o filtro <=
                elif field == 'DataDeConclusao':
                    queryset = queryset.filter(**{f"{filtro_especifico}__lte": value})

                # Suporte para múltiplos valores (caso seja uma lista)
                elif isinstance(value, list):
                    queryset = queryset.filter(**{f"{filtro_especifico}__in": value})

                else:
                    # Aplica o filtro padrão para outros campos
                    queryset = queryset.filter(**{filtro_especifico: value})

            else:
                # Log de campos ignorados que não têm mapeamento
                print(f"Aviso: Campo '{field}' não encontrado no mapeamento de filtros.")

    return queryset


class DataTableAndForms:
    def __init__(self, request, model, modelforms, per_page, columns, edition_rout, filtro_mapeamento, history_rout=False, userid=False):
        self.request = request
        self.model = model
        self.modelforms = modelforms
        self.per_page = per_page
        self.columns = columns
        self.edition_rout = edition_rout
        self.filtro_mapeamento = filtro_mapeamento
        self.history_rout = history_rout
        self.userid = userid

    def get_data_and_forms(self):
        # Verifica o tipo de modelo
        if isinstance(self.model, ModelBase):
            queryset = self.model.objects.all()
        elif isinstance(self.model, QuerySet):
            queryset = self.model
        else:
            raise ValueError("model deve ser uma instância de ModelBase ou QuerySet")

        # Aplica os filtros, se houver dados na requisição
        if self.request.method == 'GET':
            get_data = self.request.GET.dict()
            get_multiple_data = self.request.GET
            print(get_multiple_data)
            print(get_multiple_data.getlist('ServicosEscalados'))
            print(get_multiple_data.getlist('ColaboradoresEscalados'))
            queryset = aplicar_filtros_dinamicos(queryset, get_data, self.filtro_mapeamento)


        # Cria os formulários
        if self.userid:
            forms = self.modelforms(request=self.request, userid=self.userid)
        else:
            forms = self.modelforms()

        # Formata os dados para visualização
        formatted_events = [self.format_event(dado) for dado in queryset]
        # Pagina os dados formatados
        dados_paginados = paginate(
            request=self.request,
            data_objects=formatted_events,
            per_page=self.per_page
        )
        return forms, dados_paginados

    def format_event(self, dado):
        formatted_event = {coluna['nome']: getattr(dado, coluna['nome'], None) for coluna in self.columns}
        formatted_event['id_random'] = dado.id_random
        formatted_event['editar_url'] = reverse(f'{self.edition_rout}',
                                                kwargs={'userid': self.request.session.get('userid', ''),
                                                        'id_random': dado.id_random})
        if self.history_rout:
            formatted_event['history_rout'] = reverse(f'{self.history_rout}',
                                                          kwargs={
                                                              'userid': self.userid,
                                                              'id_random': dado.id_random
                                                          }
                                                      )

        return formatted_event



def formatar_atributos(queryset, atributo):
    """
    Converte uma queryset em uma string de valores de um atributo específico, separados por vírgulas.

    :param queryset: Queryset de objetos de um modelo Django.
    :param atributo: O nome do atributo do modelo que deve ser extraído.
    :return: Uma string com os valores do atributo separados por vírgulas.
    """
    # Cria uma lista de valores do atributo especificado
    valores = [getattr(obj, atributo) for obj in queryset]

    # Junta os valores em uma única string, separada por vírgulas
    valores_texto = ", ".join(str(valor) for valor in valores)

    return valores_texto