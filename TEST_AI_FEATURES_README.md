# AI Features Test Script

This test script comprehensively tests all AI-powered features in the Manufacturing Visibility System.

## 🤖 Features Tested

1. **Order Feasibility Check** (GPT-4)
   - Endpoint: `POST /orders/check-feasibility`
   - Tests multiple order scenarios
   - Validates AI analysis, recommendations, and executive summaries

2. **Shipment Delay Prediction** (GPT-3.5 + Weather API)
   - Endpoint: `POST /shipment-tracking/predict-delay`
   - Tests delay prediction with weather data
   - Validates AI recommendations and risk assessments

3. **Supply Chain Risk Assessment** (GPT-3.5)
   - Endpoint: `POST /supply-chain/assess-risks`
   - Tests various risk assessment scenarios
   - Validates AI mitigation strategies and contingency plans

## 🚀 Quick Start

### Prerequisites

1. **Backend server running** on `http://localhost:8000`
   ```bash
   cd backend
   python run.py
   ```

2. **Python 3.7+** installed

3. **Required Python packages** (usually pre-installed):
   ```bash
   pip install requests
   ```

### Run the Tests

```bash
# From project root
python test_ai_features.py
```

## 📊 What the Script Tests

### Input Validation
- ✅ Correct request payloads
- ✅ Required fields presence
- ✅ Data type validation

### Output Validation
- ✅ Response status codes
- ✅ Required response fields
- ✅ AI features presence (`ai_analysis`, `ai_prediction`, `ai_mitigation`)
- ✅ AI enabled/disabled detection

### AI Features Detection
- ✅ Checks if AI is enabled (`ai_enabled: true`)
- ✅ Validates AI-specific fields (recommendations, summaries, etc.)
- ✅ Warns if AI is in fallback mode (missing API key)

## 📋 Test Cases

### Order Feasibility
- Standard order (2 products, small quantities)
- Large order (1 product, 100 units)
- Multiple products (4 products, varying quantities)

### Shipment Delay Prediction
- Tests with available shipment IDs from database
- Validates weather assessment integration
- Checks AI delay probability calculations

### Risk Assessment
- General 30-day risk assessment
- Regional risk assessment (Southeast Asia)
- Component-specific risk assessment

## 📈 Output Example

```
======================================================================
                    AI Features Test Suite                    
======================================================================

🧪 Testing: Order Feasibility Check (AI-Enhanced)

  Testing: Standard Order
  ✅ AI Analysis: ENABLED (GPT-4)
  ℹ️  Recommendation: NO-GO
  ℹ️  Critical Bottleneck: Circuit Board inventory shortage...
  ℹ️  Feasible: False
  ℹ️  Confidence Score: 67.50%

======================================================================
                          TEST SUMMARY                          
======================================================================

Overall Results:
  Total Tests: 9
  Passed: 9
  Failed: 0
  Success Rate: 100.0%

Feature Breakdown:

  Order Feasibility:
    Passed: 3
    Failed: 0
    AI-Enabled: 3/3

  Shipment Delay:
    Passed: 3
    Failed: 0
    AI-Enabled: 2/3

  Risk Assessment:
    Passed: 3
    Failed: 0
    AI-Enabled: 3/3

✅ All tests passed! 🎉
```

## 🔧 Configuration

You can modify these variables at the top of `test_ai_features.py`:

```python
BASE_URL = "http://localhost:8000"  # Change if backend runs on different port
TIMEOUT = 60  # Timeout in seconds for AI API calls
```

## ⚠️ Troubleshooting

### API Not Accessible
```
❌ API is not accessible. Make sure backend server is running on http://localhost:8000
```
**Solution:** Start the backend server before running tests.

### AI Features Disabled
```
⚠️  AI Analysis: DISABLED (Fallback mode - check OPENAI_API_KEY)
```
**Solution:** 
- Add `OPENAI_API_KEY` to `backend/.env` file
- Restart backend server
- Tests will still pass but show fallback behavior

### Missing Shipments
```
⚠️  Shipment 1 not found (skipping)
```
**Solution:** This is normal if database doesn't have test shipments. The test will skip missing shipments.

### Timeout Errors
```
❌ Request failed: Connection timeout
```
**Solution:** 
- Check OpenAI API key is valid
- Check internet connection
- Increase `TIMEOUT` value in script

## 📝 Notes

- Tests run with **60-second timeout** to allow for AI API calls
- Script automatically detects available shipments from database
- All tests include validation of both required fields and AI features
- Tests show clear warnings if AI is disabled (fallback mode)

## 🎯 Exit Codes

- `0`: All tests passed
- `1`: One or more tests failed or API unavailable

## 📚 Related Documentation

- `AI_FEATURES.md` - Detailed AI features documentation
- `SETUP_AI_FEATURES.md` - Setup guide for AI features
- `HOW_TO_TEST_AI_FEATURES.md` - Manual testing guide

