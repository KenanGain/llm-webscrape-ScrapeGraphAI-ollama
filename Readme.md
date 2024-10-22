Thanks for sharing the **repository structure** and the **GitHub link**: 

[llm-webscrape-ScrapeGraphAI-ollama](https://github.com/KenanGain/llm-webscrape-ScrapeGraphAI-ollama).

Below is an improved **README.md** tailored for your repository structure and files:

---

# **LLM Web Scrape – ScrapeGraphAI with Ollama**

This project leverages **ScrapeGraphAI**, **Ollama models**, and **Docker** to build a scalable web scraper. It provides:

1. **Local Execution**: Run the scraper on your local machine.
2. **Containerized Execution**: Use Docker for consistent containerized runs.
3. **AWS Lambda Function**: Serverless deployment with **API Gateway integration**.

---

## **Features**

- **Ollama Integration**: Uses `mistral` and `nomic-embed-text` models to process web content.
- **Python**: Main programming language.
- **Docker**: For containerization and local testing.
- **AWS Lambda**: Serverless function for on-demand API-based scraping.
- **API Gateway**: Exposes the Lambda function as an API.

---

## **Repository Structure**

```
LLM WEBSCRAPE/
│
├── lamdafunction/        # AWS Lambda function code
│   ├── app.py            # Lambda handler function
│   ├── Dockerfile.df     # Dockerfile for Lambda container deployment
│   └── Dockerfile        # Dockerfile for containerized run
│
├── llmscrape.py          # Script for local run
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation
```

---

## **Getting Started**

### **Prerequisites**

1. **Docker** installed locally.
2. **AWS CLI** configured with your credentials.
3. **ECR Repository** in your AWS account (for Lambda deployment).
4. **Python 3.11+** installed on your machine.

---

## **Installation**

### **1. Run Locally**

Clone the repository and install dependencies:

```bash
git clone https://github.com/KenanGain/llm-webscrape-ScrapeGraphAI-ollama.git
cd llm-webscrape-ScrapeGraphAI-ollama
pip install -r requirements.txt
```

Run the scraper locally:

```bash
python llmscrape.py
```

---

### **2. Run with Docker**

Build the Docker image:

```bash
docker build -t smart-scraper .
```

Run the Docker container:

```bash
docker run -it --rm smart-scraper
```

---

### **3. Deploy to AWS Lambda**

Navigate to the `lamdafunction` folder and use the **`Dockerfile.df`** for Lambda deployment.

#### Step 1: Build the Docker Image

```bash
cd lamdafunction
docker build -t smart-scraper-api -f Dockerfile.df .
```

#### Step 2: Push the Image to AWS ECR

```bash
aws ecr get-login-password --region <your-region> | docker login --username AWS --password-stdin <your-account-id>.dkr.ecr.<your-region>.amazonaws.com

docker tag smart-scraper-api:latest <your-account-id>.dkr.ecr.<your-region>.amazonaws.com/smart-scraper-api:latest
docker push <your-account-id>.dkr.ecr.<your-region>.amazonaws.com/smart-scraper-api:latest
```

#### Step 3: Create the Lambda Function

```bash
aws lambda create-function \
  --function-name SmartScraperAPI \
  --package-type Image \
  --code ImageUri=<your-account-id>.dkr.ecr.<your-region>.amazonaws.com/smart-scraper-api:latest \
  --role <your-lambda-execution-role-arn>
```

#### Step 4: Set up API Gateway

1. **Create an HTTP API Gateway**.
2. **Create a POST Route**: `/scrape`.
3. **Integrate with Lambda**: Connect the **SmartScraperAPI** Lambda function.
4. **Deploy the API** and copy the **endpoint URL**.

---

## **Usage**

### **API Request Example**

You can use **Postman** or **cURL** to test your Lambda API.

```bash
curl -X POST <API_ENDPOINT_URL>/scrape \
  -H "Content-Type: application/json" \
  -d '{"url": "https://dev.to/t/webdev", "prompt": "What is this about?"}'
```

### **Response Example**

```json
{
  "statusCode": 200,
  "body": {
    "scraped_data": "This article discusses various aspects of web development."
  }
}
```

---

## **Technology Stack**

- **Python 3.11**: Programming language.
- **Ollama Models**: Mistral and Nomic-Embed-Text for embedding.
- **Docker**: Containerized environment for consistent runs.
- **AWS Lambda**: Serverless function with API Gateway integration.
- **API Gateway**: Exposes the scraper as a REST API.

---

## **Contributing**

Feel free to **open issues** or **submit pull requests** if you'd like to contribute or have any suggestions.

---

## **License**

This project is licensed under the **MIT License**. See the `LICENSE` file for more details.

---

## **Acknowledgments**

- **Ollama** for providing AI models.
- **AWS Lambda** for serverless computing.
- **Docker** for containerization.

---
