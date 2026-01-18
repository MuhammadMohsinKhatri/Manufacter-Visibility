import React, { useState } from 'react';
import {
  Box,
  Typography,
  Paper,
  Grid,
  TextField,
  Button,
  Card,
  CardContent,
  CardHeader,
  Alert,
  CircularProgress,
  Chip,
  List,
  ListItem,
  ListItemText,
  Divider
} from '@mui/material';
import LocalShippingIcon from '@mui/icons-material/LocalShipping';
import WarningIcon from '@mui/icons-material/Warning';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import CloudIcon from '@mui/icons-material/Cloud';

import { useNotification } from '../context/NotificationContext';
import api from '../services/api';

export default function ShipmentTracking() {
  const [shipmentId, setShipmentId] = useState('1');
  const [loading, setLoading] = useState(false);
  const [prediction, setPrediction] = useState(null);
  const [error, setError] = useState(null);
  const { showError, showSuccess } = useNotification();

  const handlePredict = async () => {
    if (!shipmentId) {
      setError('Please enter a shipment ID');
      return;
    }

    try {
      setLoading(true);
      setError(null);
      
      const response = await api.post('/shipment-tracking/predict-delay', {
        shipment_id: parseInt(shipmentId)
      });
      
      setPrediction(response.data);
      showSuccess('Delay prediction completed');
    } catch (err) {
      console.error('Error predicting delay:', err);
      setError(err.response?.data?.detail || 'Failed to predict shipment delay');
      showError('Failed to predict shipment delay');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        🚚 AI Shipment Delay Prediction
      </Typography>
      <Typography variant="body2" color="text.secondary" gutterBottom sx={{ mb: 3 }}>
        Uses Weather API + AI to predict shipment delays
      </Typography>

      <Paper sx={{ p: 3, mb: 3 }}>
        <Grid container spacing={2} alignItems="center">
          <Grid item xs={12} sm={8}>
            <TextField
              label="Shipment ID"
              value={shipmentId}
              onChange={(e) => setShipmentId(e.target.value)}
              fullWidth
              type="number"
              helperText="Enter shipment ID (e.g., 1, 2, 3)"
            />
          </Grid>
          <Grid item xs={12} sm={4}>
            <Button
              variant="contained"
              onClick={handlePredict}
              disabled={loading}
              fullWidth
              startIcon={loading ? <CircularProgress size={20} /> : <LocalShippingIcon />}
            >
              {loading ? 'Analyzing...' : 'Predict Delay'}
            </Button>
          </Grid>
        </Grid>

        {error && (
          <Alert severity="error" sx={{ mt: 2 }}>
            {error}
          </Alert>
        )}
      </Paper>

      {prediction && (
        <Grid container spacing={3}>
          {/* Shipment Info */}
          <Grid item xs={12}>
            <Card>
              <CardHeader
                title="Shipment Information"
                avatar={<LocalShippingIcon color="primary" />}
              />
              <CardContent>
                <Grid container spacing={2}>
                  <Grid item xs={12} sm={6}>
                    <Typography variant="body2" color="text.secondary">Origin</Typography>
                    <Typography variant="body1">{prediction.origin}</Typography>
                  </Grid>
                  <Grid item xs={12} sm={6}>
                    <Typography variant="body2" color="text.secondary">Destination</Typography>
                    <Typography variant="body1">{prediction.destination}</Typography>
                  </Grid>
                </Grid>
              </CardContent>
            </Card>
          </Grid>

          {/* Delay Prediction */}
          <Grid item xs={12} md={6}>
            <Card sx={{ bgcolor: prediction.overall_delay_probability > 50 ? '#fff3e0' : '#e8f5e9' }}>
              <CardHeader
                title="Delay Prediction"
                avatar={
                  prediction.overall_delay_probability > 50 
                    ? <WarningIcon color="warning" /> 
                    : <CheckCircleIcon color="success" />
                }
              />
              <CardContent>
                <Box sx={{ textAlign: 'center', mb: 2 }}>
                  <Typography variant="h2" color={prediction.overall_delay_probability > 50 ? 'warning.main' : 'success.main'}>
                    {prediction.overall_delay_probability}%
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Delay Probability
                  </Typography>
                </Box>
                
                {prediction.expected_delay_days > 0 && (
                  <Alert severity="warning" sx={{ mt: 2 }}>
                    Expected Delay: <strong>{prediction.expected_delay_days} days</strong>
                  </Alert>
                )}
                
                {prediction.expected_delay_days === 0 && (
                  <Alert severity="success" sx={{ mt: 2 }}>
                    On-time delivery expected
                  </Alert>
                )}
              </CardContent>
            </Card>
          </Grid>

          {/* Weather Assessment */}
          <Grid item xs={12} md={6}>
            <Card>
              <CardHeader
                title="Weather Conditions"
                avatar={<CloudIcon color="info" />}
              />
              <CardContent>
                {prediction.weather_assessment?.severe_weather ? (
                  <>
                    <Alert severity="error" sx={{ mb: 2 }}>
                      ⚠️ Severe Weather Detected
                    </Alert>
                    <Typography variant="body2" gutterBottom>
                      <strong>Risk Score:</strong> {prediction.weather_assessment.combined_risk_score}/100
                    </Typography>
                    {prediction.weather_assessment.origin_weather && (
                      <Box sx={{ mt: 2 }}>
                        <Typography variant="body2" color="text.secondary">Origin Weather:</Typography>
                        <Chip 
                          label={prediction.weather_assessment.origin_weather.condition || 'Unknown'}
                          color="error"
                          size="small"
                          sx={{ mt: 1 }}
                        />
                      </Box>
                    )}
                  </>
                ) : (
                  <Alert severity="success">
                    ✅ Normal weather conditions
                  </Alert>
                )}
              </CardContent>
            </Card>
          </Grid>

          {/* AI Analysis */}
          {prediction.ai_prediction?.ai_enabled && (
            <Grid item xs={12}>
              <Card sx={{ bgcolor: '#f0f7ff', border: '2px solid #2196f3' }}>
                <CardHeader
                  title="🤖 AI-Powered Analysis"
                  subheader={`Model: ${prediction.ai_prediction.model_used || 'GPT-3.5'}`}
                />
                <CardContent>
                  {prediction.ai_prediction.primary_risk_factors?.length > 0 && (
                    <>
                      <Typography variant="subtitle1" gutterBottom sx={{ fontWeight: 'bold' }}>
                        Primary Risk Factors:
                      </Typography>
                      <List dense>
                        {prediction.ai_prediction.primary_risk_factors.map((factor, idx) => (
                          <ListItem key={idx}>
                            <ListItemText primary={`• ${factor}`} />
                          </ListItem>
                        ))}
                      </List>
                    </>
                  )}

                  {prediction.recommendations?.length > 0 && (
                    <>
                      <Divider sx={{ my: 2 }} />
                      <Typography variant="subtitle1" gutterBottom sx={{ fontWeight: 'bold' }}>
                        ✅ Recommended Actions:
                      </Typography>
                      <List dense>
                        {prediction.recommendations.map((rec, idx) => (
                          <ListItem key={idx}>
                            <ListItemText 
                              primary={`${idx + 1}. ${rec}`}
                              primaryTypographyProps={{ variant: 'body2' }}
                            />
                          </ListItem>
                        ))}
                      </List>
                    </>
                  )}

                  <Box sx={{ mt: 2 }}>
                    <Chip 
                      label={`AI Confidence: ${prediction.ai_prediction.confidence || 'N/A'}%`}
                      color="primary"
                      size="small"
                    />
                  </Box>
                </CardContent>
              </Card>
            </Grid>
          )}

          {/* No AI warning */}
          {prediction.ai_prediction && !prediction.ai_prediction.ai_enabled && (
            <Grid item xs={12}>
              <Alert severity="info">
                ℹ️ AI analysis is currently unavailable. Using rule-based prediction. 
                Configure OPENAI_API_KEY in backend/.env to enable AI features.
              </Alert>
            </Grid>
          )}
        </Grid>
      )}
    </Box>
  );
}

