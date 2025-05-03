# 🏗️ Medallion Architecture for Customer Data Processing (AWS)

This project implements a **medallion architecture** pipeline using **AWS S3, Lambda, SNS, and CloudWatch** to process customer data in stages — from raw ingestion to refined, country-specific datasets. It includes automated notifications and monitoring for reliability and transparency.

---

## 📁 S3 Buckets Overview

1. **customer-raw-data-landing**  
   - Initial landing zone for raw data (`customer_data_raw.jsonl`).

2. **customer-rejected-data-landing**  
   - Stores rejected data (e.g., inconsistent, invalid, or outlier entries).

3. **customer-cleaned-data-landing**  
   - Stores cleaned data after processing.

4. **customer-data-cleaned-active-users-landing**  
   - Stores only active users from the cleaned dataset.

5. **customer-data-india-specific-landing**  
   - Stores only Indian-specific customer records.

---

## ⚙️ Lambda Functions Flow

### 1. Processing_lambda
- **Triggered by:** `customer-raw-data-landing`
- **Function:** 
  - Cleans the data by removing inconsistent and outlier records.
  - Uploads cleaned data to `customer-cleaned-data-landing`.
  - Uploads rejected data to `customer-rejected-data-landing`.

### 2. Fail_File_Notification
- **Triggered by:** `customer-rejected-data-landing`
- **Function:** 
  - Sends an email alert via **Amazon SNS** when rejected data is uploaded.

### 3. Active_users_lambda
- **Triggered by:** `customer-cleaned-data-landing`
- **Function:** 
  - Filters for active users only.
  - Uploads data to `customer-data-cleaned-active-users-landing`.

### 4. India_specific_lambda
- **Triggered by:** `customer-data-cleaned-active-users-landing`
- **Function:** 
  - Extracts Indian-specific user data.
  - Uploads data to `customer-data-india-specific-landing`.

---

## 🔔 Alerts & Monitoring

- **SNS Email Notifications** for:
  - Any Lambda function failure
  - Upload of rejected records to `customer-rejected-data-landing`

- **CloudWatch Alarms & Dashboards** to:
  - Monitor Lambda invocations and errors
  - Track processing duration
  - Visualize pipeline health and performance

---

## 📊 Data Flow Diagram

```mermaid
graph TD
    A[Raw JSONL uploaded to<br>customer-raw-data-landing] --> B[Processing_lambda]
    B -->|Cleaned| C[customer-cleaned-data-landing]
    B -->|Rejected| D[customer-rejected-data-landing]
    D --> E[Fail_File_Notification → SNS Email]

    C --> F[Active_users_lambda]
    F --> G[customer-data-cleaned-active-users-landing]
    G --> H[India_specific_lambda]
    H --> I[customer-data-india-specific-landing]
