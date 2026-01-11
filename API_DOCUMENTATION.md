# 📡 API Documentation

The Business Discovery System provides a RESTful API for programmatic access to discovered businesses.

## Base URL

```
http://localhost:8000
```

## Authentication

The API uses HTTP Basic Authentication.

**Default Credentials:**
- Username: `admin`
- Password: `changeme123`

**Example:**
```bash
curl -u admin:changeme123 http://localhost:8000/api/businesses
```

---

## Endpoints

### 1. Get Businesses

Retrieve discovered businesses with optional filters.

**Endpoint:** `GET /api/businesses`

**Query Parameters:**
- `limit` (integer, optional): Number of results (1-500, default: 50)
- `platform` (string, optional): Filter by platform (`Facebook` or `LinkedIn`)
- `category` (string, optional): Filter by category

**Example Request:**
```bash
curl -u admin:changeme123 \
  "http://localhost:8000/api/businesses?limit=10&platform=Facebook"
```

**Example Response:**
```json
{
  "success": true,
  "count": 10,
  "data": [
    {
      "id": 1,
      "business_name": "Tech Startup Lagos",
      "platform": "Facebook",
      "page_url": "https://facebook.com/techstartuplagos",
      "category": "startups",
      "location": "Lagos, Nigeria",
      "phone": "+234 803 123 4567",
      "email": "info@techstartup.com",
      "description": "Innovative tech solutions...",
      "confidence_score": 85,
      "priority": "high",
      "discovered_date": "2024-01-10T14:30:00",
      "alerted": 1
    }
  ]
}
```

---

### 2. Get Statistics

Get system statistics and analytics.

**Endpoint:** `GET /api/statistics`

**Example Request:**
```bash
curl -u admin:changeme123 http://localhost:8000/api/statistics
```

**Example Response:**
```json
{
  "success": true,
  "data": {
    "total": 150,
    "by_platform": {
      "Facebook": 90,
      "LinkedIn": 60
    },
    "by_category": {
      "startups": 45,
      "hotels": 30,
      "real_estate": 25
    },
    "recent_24h": 12
  }
}
```

---

### 3. Get Categories

Get list of configured business categories.

**Endpoint:** `GET /api/categories`

**Example Request:**
```bash
curl -u admin:changeme123 http://localhost:8000/api/categories
```

**Example Response:**
```json
{
  "success": true,
  "data": [
    {
      "name": "startups",
      "keywords": ["startup", "tech startup", "innovation hub"],
      "priority": "high"
    },
    {
      "name": "hotels",
      "keywords": ["hotel", "resort", "lodge"],
      "priority": "high"
    }
  ]
}
```

---

### 4. Export to CSV

Export all businesses to CSV file.

**Endpoint:** `GET /api/export/csv`

**Example Request:**
```bash
curl -u admin:changeme123 \
  http://localhost:8000/api/export/csv \
  -o businesses.csv
```

**Response:** CSV file download

---

### 5. Health Check

Check if the API is running.

**Endpoint:** `GET /api/health`

**Authentication:** Not required

**Example Request:**
```bash
curl http://localhost:8000/api/health
```

**Example Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-10T14:30:00"
}
```

---

### 6. Trigger Facebook Discovery

Manually trigger Facebook page discovery.

**Endpoint:** `POST /api/trigger/facebook`

**Example Request:**
```bash
curl -X POST -u admin:changeme123 \
  http://localhost:8000/api/trigger/facebook
```

**Example Response:**
```json
{
  "success": true,
  "message": "Facebook discovery completed",
  "discovered": 5
}
```

---

### 7. Trigger LinkedIn Discovery

Manually trigger LinkedIn company discovery.

**Endpoint:** `POST /api/trigger/linkedin`

**Example Request:**
```bash
curl -X POST -u admin:changeme123 \
  http://localhost:8000/api/trigger/linkedin
```

---

### 8. Trigger Google Discovery

Manually trigger Google search discovery.

**Endpoint:** `POST /api/trigger/google`

**Example Request:**
```bash
curl -X POST -u admin:changeme123 \
  http://localhost:8000/api/trigger/google
```

---

## Python Client Example

```python
import requests
from requests.auth import HTTPBasicAuth

# Configuration
BASE_URL = "http://localhost:8000"
USERNAME = "admin"
PASSWORD = "changeme123"

# Create session with authentication
session = requests.Session()
session.auth = HTTPBasicAuth(USERNAME, PASSWORD)

# Get businesses
response = session.get(f"{BASE_URL}/api/businesses", params={
    "limit": 20,
    "platform": "Facebook",
    "category": "startups"
})

if response.status_code == 200:
    data = response.json()
    businesses = data['data']
    
    for business in businesses:
        print(f"Name: {business['business_name']}")
        print(f"Platform: {business['platform']}")
        print(f"Score: {business['confidence_score']}/100")
        print(f"URL: {business['page_url']}")
        print("-" * 50)

# Get statistics
stats_response = session.get(f"{BASE_URL}/api/statistics")
stats = stats_response.json()['data']
print(f"Total businesses: {stats['total']}")
print(f"Discovered today: {stats['recent_24h']}")

# Trigger manual discovery
trigger_response = session.post(f"{BASE_URL}/api/trigger/google")
result = trigger_response.json()
print(f"Discovery completed: {result['discovered']} new businesses")
```

---

## JavaScript/Node.js Client Example

```javascript
const axios = require('axios');

const BASE_URL = 'http://localhost:8000';
const USERNAME = 'admin';
const PASSWORD = 'changeme123';

// Create axios instance with authentication
const api = axios.create({
  baseURL: BASE_URL,
  auth: {
    username: USERNAME,
    password: PASSWORD
  }
});

// Get businesses
async function getBusinesses() {
  try {
    const response = await api.get('/api/businesses', {
      params: {
        limit: 20,
        platform: 'Facebook'
      }
    });
    
    const businesses = response.data.data;
    businesses.forEach(business => {
      console.log(`Name: ${business.business_name}`);
      console.log(`Platform: ${business.platform}`);
      console.log(`Score: ${business.confidence_score}/100`);
      console.log('-'.repeat(50));
    });
  } catch (error) {
    console.error('Error:', error.message);
  }
}

// Get statistics
async function getStatistics() {
  const response = await api.get('/api/statistics');
  const stats = response.data.data;
  console.log(`Total: ${stats.total}`);
  console.log(`Recent: ${stats.recent_24h}`);
}

// Run
getBusinesses();
getStatistics();
```

---

## Error Responses

**401 Unauthorized:**
```json
{
  "detail": "Incorrect credentials"
}
```

**500 Internal Server Error:**
```json
{
  "detail": "Error message here"
}
```

---

## Rate Limiting

Currently, there are no rate limits on the API. However, be mindful of:
- Database performance with large queries
- Triggering manual discoveries too frequently

---

## Webhooks (Future Feature)

Webhook support for real-time notifications is planned for future releases.

