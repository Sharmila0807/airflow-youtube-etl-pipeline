from airflow.providers.http.sensors.http import HttpSensor
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.models import Variable
from airflow import DAG

from datetime import datetime
import json
import pandas as pd

API_KEY = Variable.get("youtube_api_key")

def _process_videos(ti):
    response = ti.xcom_pull(task_ids='extract_trending_videos')
    videos = response['items']
    rows = []
    for video in videos:
        snippet = video['snippet']
        stats = video['statistics']
        rows.append({
            'title': snippet['title'],
            'channel': snippet['channelTitle'],
            'publish_time': snippet['publishedAt'],
            'views': stats.get('viewCount', 0),
            'likes': stats.get('likeCount', 0),
        })

    df = pd.DataFrame(rows)
    df.to_csv('/tmp/trending_videos.csv', index=False, header=False)

def _store_videos():
    hook = PostgresHook(postgres_conn_id='postgres')
    hook.copy_expert(
        sql="COPY trending_videos(title, channel, publish_time, views, likes) FROM stdin WITH CSV",
        filename='/tmp/trending_videos.csv'
    )

with DAG(
    dag_id='youtube_trending_etl',
    start_date=datetime(2023, 1, 1),
    schedule_interval='@daily',
    catchup=False
) as dag:

    create_table = PostgresOperator(
        task_id='create_table',
        postgres_conn_id='postgres',
        sql='''
            CREATE TABLE IF NOT EXISTS trending_videos (
                title TEXT,
                channel TEXT,
                publish_time TIMESTAMP,
                views BIGINT,
                likes BIGINT
            );
        '''
    )

    check_youtube_api = HttpSensor(
        task_id='check_youtube_api',
        http_conn_id='youtube_api',
        endpoint='videos',
        request_params={
            'part': 'snippet',
            'chart': 'mostPopular',
            'regionCode': 'IN',
            'key': API_KEY
        },
        response_check=lambda response: "items" in response.text,
        poke_interval=5,
        timeout=20
    )

    extract_trending_videos = SimpleHttpOperator(
        task_id='extract_trending_videos',
        http_conn_id='youtube_api',
        endpoint='videos',
        method='GET',
        data={
            'part': 'snippet,statistics',
            'chart': 'mostPopular',
            'regionCode': 'IN',
            'maxResults': 10,
            'key': API_KEY
        },
        response_filter=lambda response: json.loads(response.text),
        log_response=True
    )

    process_video_data = PythonOperator(
        task_id='process_video_data',
        python_callable=_process_videos
    )

    store_video_data = PythonOperator(
        task_id='store_video_data',
        python_callable=_store_videos
    )

    create_table >> check_youtube_api >> extract_trending_videos >> process_video_data >> store_video_data
