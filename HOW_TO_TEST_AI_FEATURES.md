# How to Test AI Features - Complete Guide

## 🎯 Two Ways to Test AI Features

### Method 1: **Through the UI** (Easiest - Shows AI in frontend)
### Method 2: **Through API** (Direct testing with Postman/curl)

---

## 🔑 FIRST: Setup API Keys

### Step 1: Get OpenAI API Key (FREE $5 credit!)

1. Go to: https://platform.openai.com/signup
2. Sign up with your email
3. Verify your email
4. Go to: https://platform.openai.com/api-keys
5. Click **"Create new secret key"**
6. Copy the key (looks like: `sk-proj-xxxxxxxxxxxxxxxxxxxxxxx`)

### Step 2: Add API Key to Your Project

**Edit this file:** `backend/.env`

```env
# Replace with your actual OpenAI key
OPENAI_API_KEY=sk-proj-your-actual-key-here

# Weather API is optional (app uses simulated data as fallback)
OPENWEATHER_API_KEY=your_weather_key_here
```

**Important:** The `.env` file should be in the `backend` directory!

```
backend/
  ├── .env          ← Put your API keys HERE
  ├── app/
  ├── requirements.txt
  └── run.py
```

### Step 3: Verify Setup

```bash
cd backend
cat .env  # Linux/Mac
type .env  # Windows

# Should show:
# OPENAI_API_KEY=sk-proj-xxxxx...
```

---

## ✅ Method 1: Test Through UI (Recommended for Demo)

### Step 1: Start the Application

**Terminal 1 - Backend:**
```bash
cd backend
venv\Scripts\activate  # Windows
# OR: source venv/bin/activate  # Linux/Mac
python run.py
```

You should see:
```
INFO:     Started server process
INFO:     Uvicorn running on http://127.0.0.1:8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm start
```

Browser opens at: http://localhost:3000

### Step 2: Navigate to Order Feasibility

1. Open http://localhost:3000
2. Click **"Order Feasibility"** in the sidebar
3. You'll see a form to check order feasibility

### Step 3: Fill the Form

1. **Select Product:** Choose "Industrial Controller" (or any product)
2. **Quantity:** Enter `100` (high quantity to test constraints)
3. **Requested Delivery Date:** Choose a date ~30 days from now
4. Click **"Check Feasibility"**

### Step 4: See AI Analysis! 🎉

The response will show **AI-powered insights**:

#### What You'll See in the UI:

**Feasibility Result Card:**
- ✅ GO or ❌ NO-GO recommendation
- 📊 Confidence score with progress bar
- 📦 Inventory Status
- 🏭 Production Capacity Status
- ⚠️ Supply Chain Risks

**AI Insights (NEW!):**
Look for these sections in the response:
- **Critical Bottleneck** - AI identifies the main issue
- **Actionable Recommendations** - 3 specific suggestions
- **Alternative Strategies** - Ways to work around constraints
- **Executive Summary** - High-level decision guidance

#### Example Response in UI:

```
❌ Order is not feasible with the requested delivery date
Earliest possible delivery: March 15, 2026

Critical Bottleneck:
"Circuit Board inventory shortage - need 100 units, only 50 available"

Actionable Recommendations:
✓ Expedite Circuit Board procurement from secondary supplier in Taiwan
✓ Reallocate 20 units from Order #1234 which has flexible delivery date
✓ Consider partial fulfillment: deliver 50% now, 50% in 2 weeks

Alternative Strategies:
• Extend delivery timeline by 14 days to allow for component procurement
• Split order into two shipments based on component availability
• Use premium air freight for critical components (adds $2,500 cost)
```

**This is AI in action!** The system isn't just saying "not feasible" - it's telling you WHY and HOW to fix it.

---

## 🔬 Method 2: Test Through API Directly

### Option A: Using Browser (Swagger UI)

1. Go to: http://localhost:8000/docs
2. Find **"POST /orders/check-feasibility"**
3. Click **"Try it out"**
4. Enter this JSON:

```json
{
  "product_ids": [1, 2],
  "quantities": [50, 30],
  "requested_delivery_date": "2026-02-28T00:00:00Z"
}
```

5. Click **"Execute"**
6. Scroll down to see the **Response body**

### Option B: Using curl (Command Line)

```bash
curl -X POST "http://localhost:8000/orders/check-feasibility" \
  -H "Content-Type: application/json" \
  -d '{
    "product_ids": [1, 2],
    "quantities": [50, 30],
    "requested_delivery_date": "2026-02-28T00:00:00Z"
  }'
```

### Option C: Using Postman

1. Open Postman
2. Create a new **POST** request
3. URL: `http://localhost:8000/orders/check-feasibility`
4. Headers: `Content-Type: application/json`
5. Body (raw JSON):
```json
{
  "product_ids": [1, 2],
  "quantities": [50, 30],
  "requested_delivery_date": "2026-02-28T00:00:00Z"
}
```
6. Click **Send**

### What to Look For in API Response:

```json
{
  "feasible": false,
  "confidence_score": 67.5,
  "earliest_possible_date": "2026-03-15T00:00:00Z",
  "inventory_constraints": [
    "Insufficient Circuit Board: need 100, have 50"
  ],
  "production_constraints": [
    "Insufficient production capacity: need 200 hours, have 150 hours"
  ],
  "risk_factors": [
    "Weather risk in Southeast Asia: Tropical storm"
  ],
  
  "ai_analysis": {
    "ai_enabled": true,
    "recommendation": "NO-GO",
    "confidence": 75,
    "critical_bottleneck": "Circuit Board inventory shortage",
    "actionable_recommendations": [
      "Expedite Circuit Board procurement from Taiwan supplier",
      "Reallocate from flexible orders",
      "Consider partial fulfillment strategy"
    ],
    "alternative_strategies": [
      "Extend delivery timeline by 14 days",
      "Split order into two shipments",
      "Use premium air freight (+$2,500)"
    ],
    "executive_summary": "Order cannot be fulfilled by requested date due to Circuit Board shortage. Recommend discussing delivery extension with customer or implementing partial fulfillment strategy.",
    "model_used": "gpt-4-turbo-preview"
  },
  
  "ai_recommendation": "NO-GO",
  "ai_confidence_score": 75
}
```

**Key Fields Added by AI:**
- `ai_analysis` - Complete AI analysis object
- `ai_recommendation` - GO/NO-GO from AI
- `ai_confidence_score` - AI's confidence level
- `actionable_recommendations` - Specific actions to take
- `alternative_strategies` - Ways to work around issues
- `executive_summary` - Decision-maker summary
- `model_used` - Shows which AI model was used

---

## 🌤️ Test Weather-Based Shipment Tracking

### Through API (No UI for this yet):

```bash
curl -X POST "http://localhost:8000/shipment-tracking/predict-delay" \
  -H "Content-Type: application/json" \
  -d '{"shipment_id": 1}'
```

**Response will show:**
```json
{
  "shipment_id": 1,
  "origin": "Shanghai, China",
  "destination": "Los Angeles, USA",
  
  "weather_assessment": {
    "severe_weather": true,
    "origin_weather": {
      "condition": "Tropical Storm",
      "risk_score": 75
    },
    "delay_probability": 78
  },
  
  "ai_prediction": {
    "ai_enabled": true,
    "delay_probability": 82,
    "expected_delay_days": 5,
    "primary_risk_factors": [
      "Tropical storm at origin port",
      "Port operations likely suspended"
    ],
    "recommended_actions": [
      "Notify customer of potential 5-day delay",
      "Investigate air freight alternative",
      "Monitor storm path"
    ]
  },
  
  "overall_delay_probability": 78,
  "expected_delay_days": 5,
  "recommendations": [...]
}
```

---

## 🔍 How to Verify AI is Working

### ✅ AI is Working When You See:

1. **In Response JSON:**
   - `"ai_enabled": true`
   - `"model_used": "gpt-4-turbo-preview"` or `"gpt-3.5-turbo"`
   - Rich, contextual recommendations (not generic)
   - Executive summaries with specific details

2. **In Backend Logs:**
```
INFO: Processing order feasibility check with AI
INFO: OpenAI API call successful
INFO: AI analysis completed in 2.3 seconds
```

3. **Response Time:**
   - With AI: 2-4 seconds (calling OpenAI)
   - Without AI: <1 second (rule-based fallback)

### ❌ AI is NOT Working (Fallback Mode) When You See:

1. **In Response JSON:**
   - `"ai_enabled": false`
   - `"model_used": "rule-based-fallback"`
   - Generic recommendations like "Review inventory"

2. **In Backend Logs:**
```
WARNING: OpenAI API key not configured
INFO: Using rule-based fallback
```

**This means:** Check your `.env` file and API key!

---

## 🎨 UI Enhancement (Optional - To Show AI Prominently)

The current UI shows AI results, but to make it MORE obvious, you could enhance `OrderFeasibility.js`:

### Quick Enhancement:

Add an "AI Insights" section in the results:

```javascript
// In OrderFeasibility.js, add after the Confidence Score section:

{feasibilityResult.ai_analysis?.ai_enabled && (
  <Grid item xs={12}>
    <Card sx={{ bgcolor: '#f0f7ff', border: '2px solid #2196f3' }}>
      <CardHeader 
        title="🤖 AI Analysis" 
        titleTypographyProps={{ variant: 'h6' }}
        avatar={<SmartToyIcon color="primary" />}
      />
      <CardContent>
        <Typography variant="subtitle1" gutterBottom>
          <strong>Critical Bottleneck:</strong>
        </Typography>
        <Typography paragraph>
          {feasibilityResult.critical_bottleneck}
        </Typography>
        
        <Typography variant="subtitle1" gutterBottom>
          <strong>Actionable Recommendations:</strong>
        </Typography>
        <List>
          {feasibilityResult.actionable_recommendations?.map((rec, idx) => (
            <ListItem key={idx}>
              <ListItemIcon><CheckCircleIcon color="success" /></ListItemIcon>
              <ListItemText primary={rec} />
            </ListItem>
          ))}
        </List>
        
        <Divider sx={{ my: 2 }} />
        
        <Typography variant="subtitle1" gutterBottom>
          <strong>Executive Summary:</strong>
        </Typography>
        <Alert severity="info">
          {feasibilityResult.executive_summary}
        </Alert>
        
        <Chip 
          label={`AI Model: ${feasibilityResult.ai_analysis.model_used}`}
          size="small"
          sx={{ mt: 2 }}
        />
      </CardContent>
    </Card>
  </Grid>
)}
```

But **you don't need to do this now** - the API already returns all AI data!

---

## 📋 Testing Checklist

### Before Testing:
- [ ] OpenAI API key added to `backend/.env`
- [ ] Dependencies installed: `pip install -r requirements.txt`
- [ ] Backend running: `python run.py`
- [ ] Frontend running: `npm start` (if testing UI)

### Test AI Order Feasibility:
- [ ] Through UI: Navigate to Order Feasibility page
- [ ] Fill form with product and quantity
- [ ] Click "Check Feasibility"
- [ ] Verify response shows `ai_analysis` object
- [ ] Check for actionable recommendations
- [ ] Look for executive summary

### Test AI Shipment Tracking:
- [ ] Use curl or Postman
- [ ] POST to `/shipment-tracking/predict-delay`
- [ ] Verify weather data in response
- [ ] Verify AI prediction with delay probability
- [ ] Check for recommended actions

### Verify AI is Active:
- [ ] Response contains `"ai_enabled": true`
- [ ] Response contains `"model_used": "gpt-4-turbo-preview"`
- [ ] Recommendations are specific (not generic)
- [ ] Response time is 2-4 seconds (AI processing)

---

## 🐛 Troubleshooting

### Problem: "ai_enabled": false in response

**Solution:**
1. Check `backend/.env` exists and has your API key
2. Restart the backend: `python run.py`
3. Verify key format: starts with `sk-proj-`

### Problem: "Invalid API key" error

**Solution:**
1. Copy key again from OpenAI dashboard
2. Make sure you copied the FULL key
3. Check for extra spaces in `.env` file
4. Format should be: `OPENAI_API_KEY=sk-proj-xxxxx` (no quotes, no spaces)

### Problem: No response or timeout

**Solution:**
1. Check internet connection (OpenAI API needs internet)
2. OpenAI API might be down (check status.openai.com)
3. You might have hit rate limit (wait a few minutes)
4. Free tier might be exhausted (add payment method)

### Problem: Can't see AI features in UI

**Solution:**
1. Frontend is calling the API correctly (already fixed!)
2. Check browser console (F12) for errors
3. Verify backend is returning `ai_analysis` in response
4. Response might be there but UI not displaying it prominently
   - Open browser Dev Tools (F12)
   - Go to Network tab
   - Check the API response - `ai_analysis` should be there

---

## 💡 Quick Demo Script (For Interview)

### 1. Show API Setup (30 seconds)
"I've configured OpenAI API for AI-powered analysis. Let me show you the `.env` configuration..."
```bash
cat backend/.env  # Show API key is configured
```

### 2. Test Through UI (2 minutes)
"Let me demonstrate the AI features through the user interface..."
1. Navigate to Order Feasibility
2. Enter large order (100 units)
3. Show the AI analysis results
4. Point out: "Notice it's not just 'not feasible' - the AI identifies the bottleneck, suggests alternatives, and provides an executive summary"

### 3. Test Through API (2 minutes)
"Let me show you the raw API response to demonstrate the AI integration..."
1. Open Swagger UI: http://localhost:8000/docs
2. Test `/orders/check-feasibility` endpoint
3. Show the response JSON
4. Point out: `"model_used": "gpt-4-turbo-preview"` - "This is real AI, not rules"

### 4. Show the Code (1 minute)
"Here's the AI service implementation..."
1. Open `backend/app/services/ai_service.py`
2. Show the OpenAI API call
3. Explain prompt engineering
4. Point out: "This is production-ready with fallback logic"

---

## ✅ Success Criteria

You'll know AI is working when:
- ✅ Response time is 2-4 seconds (AI processing)
- ✅ `ai_enabled` is `true` in response
- ✅ Recommendations are specific and contextual
- ✅ Executive summaries mention specific details
- ✅ Backend logs show "OpenAI API call successful"

---

## 🎯 Summary

### Where API Keys Go:
```
backend/.env file with:
OPENAI_API_KEY=sk-proj-your-key-here
```

### How to Test:
1. **UI Method**: Order Feasibility page → Fill form → See AI insights
2. **API Method**: Swagger UI or curl → Test endpoint → See JSON response

### What to Look For:
- `ai_analysis` object in response
- `ai_enabled: true`
- Specific, contextual recommendations
- Executive summaries

**Your AI features are ready to demonstrate!** 🚀

