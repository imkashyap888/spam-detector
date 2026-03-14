# Spam Detector API

A serverless spam detection API deployed on Vercel using a Naive Bayes + TF-IDF model.

## Endpoint

`POST /api/predict`

### Request Body
```json
{
  "text": "Congratulations! You've won a free prize. Click here now!"
}
```

### Response
```json
{
  "text": "Congratulations! You've won a free prize. Click here now!",
  "prediction": "spam",
  "is_spam": true,
  "confidence": {
    "ham": 0.0312,
    "spam": 0.9688
  }
}
```

## Deploy to Vercel

```bash
npm i -g vercel
vercel
```