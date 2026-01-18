# Quick Setup Guide for AI Features

## 🚀 5-Minute Setup

### Step 1: Install AI Dependencies

```bash
cd backend
pip install openai scikit-learn pandas numpy
```

Or simply:
```bash
pip install -r requirements.txt
```

### Step 2: Get API Keys (Free!)

#### OpenAI API Key (REQUIRED for AI features)
1. Go to: https://platform.openai.com/signup
2. Sign up (you get $5 free credit)
3. Go to: https://platform.openai.com/api-keys
4. Click "Create new secret key"
5. Copy the key (starts with `sk-proj-...`)

#### OpenWeatherMap API Key (OPTIONAL - for real weather data)
1. Go to: https://openweathermap.org/appid
2. Sign up (free tier: 1000 calls/day)
3. Get your API key
4. Copy the key

### Step 3: Configure Environment

Create a `.env` file in the `backend` directory:

```bash
cd backend
echo OPENAI_API_KEY=sk-proj-your-key-here > .env
echo OPENWEATHER_API_KEY=your-weather-key-here >> .env
```

Or manually create `backend/.env`:
```env
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxx
OPENWEATHER_API_KEY=xxxxxxxxxxxxx
```

### Step 4: Test AI Features

```bash
# Start the backend
cd backend
python run.py

# In another terminal, test the AI endpoint
curl -X POST "http://localhost:8000/orders/check-feasibility" \
  -H "Content-Type: application/json" \
  -d '{
    "product_ids": [1, 2],
    "quantities": [10, 5],
    "requested_delivery_date": "2026-02-15T00:00:00Z"
  }'
```

You should see AI analysis in the response!

---

## 🎯 What Works Without API Keys?

### With API Keys (Full AI):
✅ GPT-4 powered order analysis
✅ Real-time weather data
✅ AI-generated recommendations
✅ Intelligent risk mitigation

### Without API Keys (Fallback):
✅ Rule-based feasibility checking
✅ Simulated weather data
✅ Basic recommendations
✅ System still works!

**The app is production-ready with graceful degradation.**

---

## 🧪 Testing AI Features

### Test 1: Order Feasibility with AI

```bash
curl -X POST "http://localhost:8000/orders/check-feasibility" \
  -H "Content-Type: application/json" \
  -d '{
    "product_ids": [1],
    "quantities": [100],
    "requested_delivery_date": "2026-02-01T00:00:00Z"
  }'
```

**Look for in response:**
- `ai_analysis` object
- `ai_recommendation`: "GO" or "NO-GO"
- `actionable_recommendations`: Array of suggestions
- `executive_summary`: AI-generated summary

### Test 2: Shipment Delay Prediction

```bash
curl -X POST "http://localhost:8000/shipment-tracking/predict-delay" \
  -H "Content-Type: application/json" \
  -d '{"shipment_id": 1}'
```

**Look for in response:**
- `weather_assessment`: Weather data
- `ai_prediction`: AI analysis
- `overall_delay_probability`: Combined score
- `recommendations`: Actionable steps

### Test 3: Risk Mitigation with AI

```bash
curl -X POST "http://localhost:8000/supply-chain/assess-risks" \
  -H "Content-Type: application/json" \
  -d '{
    "time_horizon_days": 30
  }'
```

**Look for in response:**
- `ai_mitigation`: AI-generated strategies
- `priority_actions`: Top recommendations
- `contingency_plans`: Backup strategies

---

## 🐛 Troubleshooting

### Error: "OpenAI API key not found"
**Solution:** Check your `.env` file exists in `backend/` directory

### Error: "Invalid API key"
**Solution:** Make sure you copied the full key including `sk-proj-` prefix

### Error: "Rate limit exceeded"
**Solution:** You've used your free credit. Either:
- Add payment method to OpenAI account
- Wait for rate limit reset
- App will use fallback logic

### AI features not working but no error
**Solution:** Check if `.env` file is in the correct location:
```bash
ls backend/.env  # Should exist
```

---

## 💰 Cost Estimate

### OpenAI API Costs:
- Order Feasibility (GPT-4): ~$0.02 per request
- Shipment Prediction (GPT-3.5): ~$0.001 per request
- Risk Mitigation (GPT-3.5): ~$0.002 per request

### Example Monthly Cost:
- 1000 orders checked: $20
- 500 shipments tracked: $0.50
- 200 risk assessments: $0.40
- **Total: ~$21/month**

### Free Tier:
- OpenAI: $5 credit (lasts for ~250 order checks)
- OpenWeatherMap: 1000 calls/day (more than enough)

**Perfect for demo and interview!**

---

## 📚 Quick Reference

### Environment Variables:
```env
OPENAI_API_KEY=sk-proj-...        # Required for AI
OPENWEATHER_API_KEY=...           # Optional for real weather
```

### AI Endpoints:
- `POST /orders/check-feasibility` - AI order analysis
- `POST /shipment-tracking/predict-delay` - AI delay prediction
- `POST /supply-chain/assess-risks` - AI risk mitigation

### Documentation:
- API Docs: http://localhost:8000/docs
- AI Features: [AI_FEATURES.md](AI_FEATURES.md)
- Presentation Guide: [INTERVIEW_PRESENTATION_GUIDE.md](INTERVIEW_PRESENTATION_GUIDE.md)

---

## ✅ Verification Checklist

After setup, verify:
- [ ] `pip list` shows `openai`, `scikit-learn`, `pandas`, `numpy`
- [ ] `.env` file exists in `backend/` directory
- [ ] Backend starts without errors
- [ ] Can access http://localhost:8000/docs
- [ ] Test order feasibility returns `ai_analysis` object
- [ ] Test shipment tracking returns `ai_prediction` object

---

## 🎯 For the Interview

**If you have API keys:**
- Show real AI responses
- Demonstrate GPT-4 analysis
- Explain prompt engineering

**If you DON'T have API keys:**
- Explain the architecture
- Show the code (ai_service.py)
- Explain fallback logic
- Mention you can add keys live if needed

**Either way, you're demonstrating AI engineering skills!** 🚀

---

## 🆘 Need Help?

1. Check backend logs for errors
2. Verify `.env` file location and format
3. Test API key separately:
   ```python
   from openai import OpenAI
   client = OpenAI(api_key="your-key")
   response = client.chat.completions.create(
       model="gpt-3.5-turbo",
       messages=[{"role": "user", "content": "test"}]
   )
   print(response)
   ```

4. Use fallback mode (no API keys) - system still works!

