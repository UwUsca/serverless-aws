import os

import boto3
import requests
import yaml

s3 = boto3.client('s3')

def get_links_from_file():
    try:
        with open('links.yml', 'r') as file:
            links = yaml.safe_load(file)
        return links
    except Exception as e:
        print(f"Erro ao ler o arquivo 'links.yml': {str(e)}")
        raise

def download_csv(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.content.decode('latin1')
    except Exception as e:
        print(f"Erro ao baixar CSV da URL '{url}': {str(e)}")
        raise

def save_to_s3(data, bucket_name, key):
    try:
        s3.put_object(Body=data, Bucket=bucket_name, Key=key)
        print(f"Arquivo salvo no S3: '{key}'")
        return key
    except Exception as e:
        print(f"Erro ao salvar o arquivo '{key}' no bucket '{bucket_name}': {str(e)}")
        raise



def handler(event, context):
    try:
        bucket_name = os.environ['BUCKET_NAME']

        print(f"Nome do bucket: {bucket_name}")

        links = get_links_from_file()

        for road_name, url in links.items():
            try:
                csv_data = download_csv(url)
                s3_key = f"downloads/{road_name}.csv"
                save_to_s3(csv_data, bucket_name, s3_key)

                print(f"Arquivo CSV '{road_name}.csv' salvo no bucket '{bucket_name}'")

            except Exception as e:
                print(f"Erro ao processar a estrada '{road_name}': {str(e)}")

        return {
            'statusCode': 200,
            'body': 'Processamento completo.'
        }
    except Exception as e:
        print(f"Erro geral na execução da função Lambda: {str(e)}")
        raise