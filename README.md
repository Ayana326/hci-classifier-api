# HCI Classifier
This repository implements a REST API exposing the human-centric issue classifier tool implemented by Khalajzadeh et al. (2022), using Flask.

## Development Environment Setup

The server will run on port 5000 inside the container. On macOS, port 5000 is often used by AirPlay Receiver, so we recommend using port 8000 on the host. The API can be accessed at http://localhost:8000.

### Build Docker Image (Important)

**For Apple Silicon, you must specify the platform:**

```bash
docker build --platform=linux/amd64 -t hci-classifier-api .
```

⚠️ **Note:** This will take some time, as xgboost 0.90 will be built for Linux (amd64).

### Update Existing Docker Image

If you've updated `requirements.txt` or other files, you need to rebuild the Docker image:

1. **Stop and remove existing containers:**
   ```bash
   docker ps -a | grep hci-classifier-api
   docker stop <container_id>  # if container is running
   docker rm <container_id>    # remove the container
   ```

2. **Remove the old image (optional, but recommended):**
   ```bash
   docker rmi hci-classifier-api
   ```

3. **Rebuild the image:**
   ```bash
   docker build --platform=linux/amd64 -t hci-classifier-api .
   ```

### Run the Container

**Recommended (for macOS):**
```bash
docker run --platform=linux/amd64 -p 8000:5000 hci-classifier-api
```
Access the API at: http://localhost:8000

**Alternative (if port 5000 is available):**
```bash
docker run --platform=linux/amd64 -p 5000:5000 hci-classifier-api
```
Access the API at: http://localhost:5000

**Note:** On macOS, port 5000 is often used by AirPlay Receiver. If you get a "port already in use" error, use port 8000 instead. To use port 5000, you can disable AirPlay Receiver in System Settings > General > AirDrop & Handoff.

## API Usage

### Health Check

```bash
curl http://localhost:8000/health
```

### Classify Text(s)

The `/classify` endpoint accepts a JSON object where keys are text IDs and values are text content.

**Single text:**
```bash
curl -X POST http://localhost:8000/classify \
  -H "Content-Type: application/json" \
  -d '{"issue_1": "The app crashes when I try to upload a photo."}'
```

**Multiple texts:**
```bash
curl -X POST http://localhost:8000/classify \
  -H "Content-Type: application/json" \
  -d '{
    "issue_1": "The app crashes when I try to upload a photo.",
    "issue_2": "The color scheme is not accessible for colorblind users.",
    "issue_3": "Users are complaining about the slow loading time."
  }'
```

**Response format:**
```json
{
  "issue_1": {
    "content": "The app crashes when I try to upload a photo.",
    "predictions": {
      "app-usage": true,
      "inclusiveness": false,
      "user-reaction": true,
      "non-human-centric": false
    }
  },
  "issue_2": {
    "content": "The color scheme is not accessible for colorblind users.",
    "predictions": {
      "app-usage": false,
      "inclusiveness": true,
      "user-reaction": false,
      "non-human-centric": false
    }
  }
}
```

### Bulk Classify

The `/bulk-classify` endpoint accepts a list of dictionaries:

```bash
curl -X POST http://localhost:8000/bulk-classify \
  -H "Content-Type: application/json" \
  -d '[
    {"issue_1": "The app is difficult to use for elderly users."},
    {"issue_2": "The UI is not responsive on small screens."}
  ]'
```

## References
Khalajzadeh, H., Shahin, M., Obie, H. O., Agrawal, P., & Grundy, J. (2022). Supporting developers in addressing human-centric issues in mobile apps. IEEE Transactions on Software Engineering, 49(4), 2149-2168.