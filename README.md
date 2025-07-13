# Airflow-youtube-etl-pipeline
A simple ETL pipeline that uses the **YouTube Data API** to fetch daily trending videos and stores them in a **PostgreSQL** database using **Apache Airflow**, all inside a **Docker** environment.
<img width="1920" height="1080" alt="EXTRACT" src="https://github.com/user-attachments/assets/cf623ca4-adec-4446-b49c-c2c03e670346" />

*  Created a DAG to automate a real-time ETL pipeline.
*  Used YouTube Data API to extract trending video metadata.
*  Used Python and Pandas for transformation and formatting.
*  Stored the clean data into a PostgreSQL database for analytics.
*  All tasks are orchestrated with Apache Airflow using DAG operators and sensors.
*  Dockerized the full setup for easy, consistent local or cloud deployment.
*  Validated the API data and ensured correct format before loading
---

## 🚀 Features

- Extracts top 10 trending YouTube videos using YouTube Data API.
- Loads data into PostgreSQL with views & likes.
- Uses Apache Airflow to orchestrate and schedule daily runs.
- Clean modular DAG and scalable design.

---

## 🔧 Stack

- Apache Airflow
- Python 3
- YouTube Data API v3
- PostgreSQL
- Docker
- Pandas

---
## DAG 
`create_table` → `check_youtube_api` → `extract_trending_videos` → `process_video_data` → `store_video_data`

---

## 🛠 Setup Instructions

### 1. Clone Repo
```bash
git clone https://github.com/sharmila0807/youtube-trending-etl.git
cd youtube-trending-etl
```
### 2. Install Requirements
```bash
pip install -r requirements.txt
```
### 3. Set Up Airflow Variables
In Airflow UI → Admin → Variables → create:
* Key: youtube_api_key 
* Value:	YOUR_YOUTUBE_API_KEY

### 4. Set Up Connection
Airflow UI → Admin → Connections → create:

* Conn ID: youtube_api
* Conn Type: HTTP
* Host: https://www.googleapis.com/youtube/v3

### 5. Set Up Postgres Connection:
Airflow UI → Admin → Connections → create:
* Conn ID:	postgres
* Conn Type:	Postgres
* Host: postgres
* Login: admin
* Password: admin
* Port:	5432

### Output Example
| Title             | Channel    | Published At           | Views     | Likes    |
|-------------------|------------|-------------------------|-----------|----------|
| Trending Video 1  | Channel A  | 2025-07-13T10:00:00Z    | 4,521,000 | 120,000  |
| Trending Video 2  | Channel B  | 2025-07-13T12:00:00Z    | 2,019,000 | 84,000   |

