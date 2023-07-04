from __future__ import annotations

from typing import Optional
from datetime import datetime
from typing_extensions import TypedDict

csv_encodings = ['utf-8', 'cp1252']
csv_separators = [';', '\t']

dataset_source_url = 'https://dados.mj.gov.br/dataset/atendimentos-de-consumidores-nos-procons-sindec'
dataset_folder_name = 'csv_files'
dataset_ignore_list = ['fornecedor']
dataset_years = [2019, 2020, 2021, 2022, 2023]

# key: column name
# value: tuple(data type, slice size)


class DatasetDictionaryTypedDict(TypedDict):
    AnoAtendimento: Optional[int]
    TrimestreAtendimento: Optional[int]
    MesAtendimento: Optional[int]
    DataAtendimento: Optional[datetime]
    CodigoRegiao: Optional[int]
    Regiao: Optional[str]
    UF: Optional[str]
    CodigoTipoAtendimento: Optional[int]
    DescricaoTipoAtendimento: Optional[str]
    CodigoAssunto: Optional[int]
    DescricaoAssunto: Optional[str]
    GrupoAssunto: Optional[str]
    CodigoProblema: Optional[int]
    DescricaoProblema: Optional[str]
    GrupoProblema: Optional[str]
    SexoConsumidor: Optional[str]
    FaixaEtariaConsumidor: Optional[str]
    CEPConsumidor: Optional[str]

#--------------
# Validations
#--------------
def is_valid(data: DatasetDictionaryTypedDict) -> bool:
    if data['DataAtendimento'] is not None and data['DataAtendimento'].year != data['AnoAtendimento']:
        return False

    if data['CodigoRegiao'] is not None and (data['CodigoRegiao'] < 1 or data['CodigoRegiao'] > 5):
        return False

    if data['Regiao'] is not None and len(data['Regiao']) > 15:
        return False

    if data['UF'] is not None and len(data['UF']) != 2:
        return False

    if data['DescricaoTipoAtendimento'] is not None and len(data['DescricaoTipoAtendimento']) > 50:
        return False

    if data['DescricaoAssunto'] is not None and len(data['DescricaoAssunto']) > 160:
        return False

    if data['GrupoAssunto'] is not None and len(data['GrupoAssunto']) > 160:
        return False

    if data['DescricaoProblema'] is not None and len(data['DescricaoProblema']) > 160:
        return False

    if data['GrupoProblema'] is not None and len(data['GrupoProblema']) > 160:
        return False

    if data['SexoConsumidor'] is not None and len(data['SexoConsumidor']) != 1:
        return False

    if data['FaixaEtariaConsumidor'] is not None and len(data['FaixaEtariaConsumidor']) > 20:
        return False

    if data['CEPConsumidor'] is not None and len(data['CEPConsumidor']) != 8:
        return False

    return True
