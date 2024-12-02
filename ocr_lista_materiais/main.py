import json
#from pahtlib import Path
import pathlib
from typing import Dict, List, Tuple
from mypy_boto3_textract.type_defs import BlockTypeDef
import boto3


def get_document_data( file_name: str) -> bytearray:
    with open(file_name, "rb") as file:
        img = file.read()
        doc_bytes = bytearray(img)

    return doc_bytes

def textract_analyze_document(file_path: str):
    client = boto3.client("textract")

    #file_path = str(pathlib.Path(__file__).parent / "images" / "lista_escolar.png")
    #print(f'file_path: {file_path}')

    doc_bytes = get_document_data(file_path)
    response = client.analyze_document(
        Document={"Bytes": doc_bytes},
        FeatureTypes=["LAYOUT"]             # valores validos: TABLES | FORMS | QUERIES | SIGNATURES | LAYOUT
    )
    with open("response.json", "w") as response_file:
        response_file.write(json.dumps(response))
        return json.dumps(response)


def get_text_list(file_path: str):

    blocks: List[BlockTypeDef] = {}

    try:
        with open("response.json", "r") as file:
            blocks = json.loads(file.read())["Blocks"]
    except IOError:
        blocks = json.loads(textract_analyze_document(file_path))["Blocks"]

    for block in blocks:
        block_id = block["Id"]
        if block["BlockType"] == "LINE":
            print(str(block["Text"]))



if __name__ == "__main__":

    file_path = str(pathlib.Path(__file__).parent / "images" / "lista_escolar.png")
    print(f'file_path: {file_path}')

    get_text_list(file_path)
