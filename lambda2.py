import os
import csv
import boto3
import pymysql

s3 = boto3.client('s3')

def get_s3_object(bucket_name, key):
    try:
        response = s3.get_object(Bucket=bucket_name, Key=key)
        return response['Body'].read().decode('latin1')
    except Exception as e:
        print(f"Erro ao recuperar o objeto do S3: {str(e)}")
        raise


def process_csv_data(csv_data):
    metrics = []
    reader = csv.DictReader(csv_data.splitlines())
    for row in reader:
        vehicle = row.get('tipo_veiculo')
        deaths = int(row.get('mortos', 0))
        if vehicle in ['automovel', 'bicicleta', 'caminhao', 'moto', 'onibus'] and deaths > 0:
            metrics.append({
                'vehicle': vehicle,
                'number_deaths': deaths
            })
    return metrics


def save_to_db(metrics, road_name):
    try:
        connection = pymysql.connect(
            host=os.environ['DB_HOST'],
            user=os.environ['DB_USER'],
            password=os.environ['DB_PASSWORD'],
            database=os.environ['DB_NAME'],
        )
        with connection.cursor() as cursor:
            for metric in metrics:
                sql = """
                        INSERT INTO accident_metrics (created_at, road_name, vehicle, number_deaths)
                        VALUES (NOW(), %s, %s, %s)
                    """
                cursor.execute(sql, (road_name, metric['vehicle'], metric['number_deaths']))
            connection.commit()
    finally:
        pass


def handler(event, context):
    try:
        if 'road_name' not in event:
            raise KeyError("A chave 'road_name' não está presente no evento.")

        bucket_name = os.environ['BUCKET_NAME']
        road_name = event['road_name']
        s3_key = f"downloads/{road_name}.csv"

        csv_data = get_s3_object(bucket_name, s3_key)
        metrics = process_csv_data(csv_data)
        save_to_db(metrics, road_name)

        return {
            'statusCode': 200,
            'body': f"Processamento completo para a estrada: {road_name}"
        }
    except Exception as e:
        print(f"Erro ao processar a função Lambda: {str(e)}")
        raise