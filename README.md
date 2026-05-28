# 🚕 Enhancing Urban Transportation Resilience Through Big Data Analytics

> An end-to-end big data pipeline that integrates NYC taxi trip data with historical and real-time weather data to analyze weather's impact on urban transportation and predict ride fares using machine learning.

---

## 📌 Project Overview

Urban transportation generates massive volumes of data that, when combined with weather information, reveal powerful insights into fare dynamics and demand patterns. This project harnesses **PySpark**, **Amazon S3**, **Apache Kafka**, and **Azure Databricks** to build a scalable data pipeline — from raw data ingestion to real-time fare prediction.

The best-performing model, **Gradient Boosted Tree (GBT) Regression**, achieved:
- **R² Score:** 0.91
- **RMSE:** 4.027

---

## 🏗️ Architecture & Workflow

```
Data Sources                  ETL (Azure Databricks)         ML Models
─────────────                 ──────────────────────         ─────────────────
NYC TLC Yellow Taxi  ──┐      Data Preprocessing             Linear Regression
NYC TLC Green Taxi   ──┼──→  Amazon S3 (Data Lake) ──→     Random Forest
Historical Weather   ──┘      Data Exploration        ──→   GBT Regression ✅ Best
                              Data Transformation
                                     │
                              Real-Time Streaming
                              ─────────────────────
Weather API ──→ Apache Kafka (EC2) ──→ Stream Processor ──→ ML Prediction ──→ S3
```

---

## 🛠️ Tech Stack

| Category | Tools |
|----------|-------|
| **Data Processing** | PySpark, Azure Databricks |
| **Data Storage** | Amazon S3 (Data Lake) |
| **Real-Time Streaming** | Apache Kafka on AWS EC2 |
| **Machine Learning** | Linear Regression, Random Forest, GBT Regression |
| **Weather Data** | Visual Crossing API |
| **Cloud Infrastructure** | AWS (S3, EC2), Google Cloud, Azure |
| **Version Control** | Git, GitHub |
| **Project Management** | Trello (Agile/Scrum) |

---

## 📂 Dataset

### NYC Taxi Data
- **Source:** [NYC TLC Trip Record Data](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page)
- **Coverage:** Yellow and Green taxi trips, 2021–2022
- **Volume:** ~72 million rows
- **Format:** Parquet
- **Note:** For-hire vehicles (Uber, Lyft) excluded as they don't provide trip prices

### Weather Data
- **Source:** [Visual Crossing](https://www.visualcrossing.com/)
- **Format:** CSV with hourly records
- **Features:** Date, time, precipitation, humidity, temperature, perceived conditions

---

## 🔧 Data Preprocessing

### Cleaning & Handling Missing Values
- Null values in `passenger_count` → imputed with **median**
- Null values in `payment_type` → imputed with **mode**
- Standardized column names between yellow and green taxi datasets

### Outlier Filtering

| Field | Filter Applied |
|-------|---------------|
| Passenger Count | 0 < count < 7 |
| Trip Distance | 0.25 to 70 miles |
| Trip Duration | 1 minute to 5 hours |
| Fare Amount | $0 to $500 |

### Feature Engineering
New features extracted from existing data:
- `trip_duration` — time delta between pickup and drop-off
- `year`, `month`, `date`, `hour`, `weekend` — temporal attributes
- `total_fare_amount` — total amount minus tip

### Dimensionality Reduction
- Taxi data: retained key features from 20 available
- Weather data: retained key features from 24 available

### Data Integration
Taxi and weather datasets merged on shared timestamps (pickup time ↔ weather recording time).

---

## 🤖 Machine Learning Models

All models use an **80/20 train-test split** with a fixed seed of 42 for reproducibility. Features are assembled using `VectorAssembler`; target variable is `total_amount`.

| Model | R² Score | RMSE | Training Time |
|-------|----------|------|---------------|
| Random Forest Regression | 0.8909 | 4.5991 | ~22 min |
| Linear Regression | 0.9103 | 4.17 | ~9 min |
| **GBT Regression** | **0.9165** | **4.027** | ~100 min |

✅ **GBT Regression** selected as the best model — highest R² and lowest RMSE.

Trained models are persisted in S3 for real-time inference.

---

## ⚡ Real-Time Streaming Pipeline

1. **Kafka Cluster** deployed on AWS EC2
2. Topic `taxi-trips-topic` created for streaming raw taxi data from S3
3. **Consumer** processes stream:
   - Extracts and parses temporal information
   - Calls Weather API for concurrent weather conditions
   - Applies feature engineering
   - Feeds processed data into the saved GBT model for price prediction
4. **Predictions + processed data** stored back in S3 Data Lake for auditing and historical analysis

---

## 📊 Key Analysis Findings

- **Monthly Revenue:** Gradual increase mid-year (office commute season); dip at year-end (holiday season — shift to other transport)
- **Yearly Passenger Count:** Growth from 2021 to 2022 attributed to easing of pandemic travel restrictions
- **Top Pickup Locations:** Upper East Side South & North (~3.28M, ~2.97M), JFK and LaGuardia airports
- **Top Drop-off Locations:** Upper East Side North (>3M), Murray Hill, Lenox Hill West (commercial zones)

---

## 📁 Repository Structure

```
nyc-taxi-ml-streaming/
├── sourcecode/
│   ├── etl-script (taxi+weather).ipynb   # ETL pipeline using PySpark
│   ├── build-ml-models.ipynb             # Model training and evaluation
│   ├── producer-script.ipynb             # Kafka producer
│   ├── consumer-script.ipynb             # Kafka consumer + real-time prediction
│   └── download.py                       # Data download utility
└── README.md
```

---

## ⚙️ Setup & Installation

### Prerequisites
- Python 3.x
- Apache Spark / PySpark
- Apache Kafka
- AWS Account (S3, EC2)
- Azure Databricks workspace
- Visual Crossing API key

### Install Dependencies

```bash
pip install pyspark
pip install kafka-python
pip install boto3
pip install pandas
pip install requests
```

### Environment Configuration

```python
# S3 Configuration
S3_BUCKET = "<your-s3-bucket-name>"

# Kafka Configuration
KAFKA_BROKER = "<your-ec2-public-ip>:9092"
KAFKA_TOPIC  = "taxi-trips-topic"

# Weather API
WEATHER_API_KEY = "<your-visual-crossing-api-key>"
```

> ⚠️ Never hardcode credentials. Use environment variables or AWS IAM roles.

---

## ▶️ How to Run

1. **Set up S3** — create a bucket and upload raw taxi parquet files and weather CSV files
2. **Run ETL** — execute `etl-script (taxi+weather).ipynb` on Azure Databricks to preprocess and merge datasets
3. **Train Models** — run `build-ml-models.ipynb` to train and save all three ML models to S3
4. **Start Kafka** — launch your Kafka cluster on EC2 and create the topic `taxi-trips-topic`
5. **Start Producer** — run `producer-script.ipynb` to stream raw taxi data to the Kafka topic
6. **Start Consumer** — run `consumer-script.ipynb` to consume, process, predict, and store results

---

## ⚠️ Challenges

- **Long model training times** — GBT took ~100 minutes due to data volume; mitigated through model optimization
- **Version compatibility** — Hadoop, Spark, and Kafka have strict inter-dependencies; required careful alignment of library and JAR file versions across components

---

## 🔮 Future Scope

- **Expand datasets** — incorporate public events data and sentiment analysis for richer fare prediction
- **Feedback loops** — enable models to self-adjust when actual vs. predicted demand diverges
- **Global scalability** — extend the pipeline to support cities beyond NYC
- **Transportation provider insights** — analyze operational efficiency metrics such as driver profit and customer satisfaction

---

## 📚 References

1. [Apache Kafka](https://kafka.apache.org/)
2. [Azure Databricks](https://azure.microsoft.com/en-us/products/databricks/)
3. [Google Cloud Storage](https://cloud.google.com/storage)
4. [NOAA Climate Data — NYC Central Park](https://www.ncdc.noaa.gov/cdo-web/datasets/GHCND/stations/GHCND:USW00094728/detail)
5. [FHWA Road Weather Management](https://ops.fhwa.dot.gov/weather/q1_roadimpact.htm)
6. [NYC Taxi & Ridehailing Stats Dashboard](https://toddwschneider.com/dashboards/nyc-taxi-ridehailing-uber-lyft-data/)
7. [Amazon S3](https://aws.amazon.com/s3/)
8. [PySpark Documentation](https://spark.apache.org/docs/latest/api/python/index.html)
9. [NYC TLC Trip Record Data](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page)
10. [Visual Crossing Weather API](https://www.visualcrossing.com/)
11. Abdel-Aty & Pemmanaboina — *Calibrating a real-time traffic crash-prediction model using archived weather and ITS traffic data*, IEEE Trans. Intelligent Transportation Systems, 2006
12. Brodeur & Nield — *An empirical analysis of taxi, lyft and uber rides: Evidence from weather shocks in NYC*, Journal of Economic Behavior & Organization, 2018
13. Kaplunovich & Yesha — *Consolidating billions of taxi rides with AWS EMR and Spark in the cloud*, IEEE Big Data, 2018
14. Koncar & Bayram — *A probabilistic methodology to quantify the impacts of cold weather on EV demand*, IEEE Access, 2021
15. Yu et al. — *Utilizing microscopic traffic and weather data to analyze real-time crash patterns*, IEEE Trans. Intelligent Transportation Systems, 2013
