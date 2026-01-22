import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Paper,
  Grid,
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
  Divider,
  Autocomplete,
  TextField,
  Timeline,
  TimelineItem,
  TimelineSeparator,
  TimelineConnector,
  TimelineContent,
  TimelineDot,
  TimelineOppositeContent,
  LinearProgress,
  Stack
} from '@mui/material';
import LocalShippingIcon from '@mui/icons-material/LocalShipping';
import WarningIcon from '@mui/icons-material/Warning';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import CloudIcon from '@mui/icons-material/Cloud';
import AccessTimeIcon from '@mui/icons-material/AccessTime';
import LocationOnIcon from '@mui/icons-material/LocationOn';
import FlightIcon from '@mui/icons-material/Flight';
import DirectionsBoatIcon from '@mui/icons-material/DirectionsBoat';
import LocalShippingOutlinedIcon from '@mui/icons-material/LocalShippingOutlined';
import TrainIcon from '@mui/icons-material/Train';
import WbSunnyIcon from '@mui/icons-material/WbSunny';
import ThunderstormIcon from '@mui/icons-material/Thunderstorm';
import AirIcon from '@mui/icons-material/Air';

import { useNotification } from '../context/NotificationContext';
import shipmentService from '../services/shipmentService';

export default function ShipmentTracking() {
  const [shipments, setShipments] = useState([]);
  const [selectedShipment, setSelectedShipment] = useState(null);
  const [loading, setLoading] = useState(false);
  const [loadingShipments, setLoadingShipments] = useState(true);
  const [prediction, setPrediction] = useState(null);
  const [error, setError] = useState(null);
  const { showError, showSuccess } = useNotification();

  // Fetch shipments on component mount
  useEffect(() => {
    const fetchShipments = async () => {
      try {
        setLoadingShipments(true);
        const data = await shipmentService.getShipments();
        setShipments(data);
        if (data.length > 0 && !selectedShipment) {
          setSelectedShipment(data[0]);
        }
      } catch (err) {
        console.error('Error fetching shipments:', err);
        showError('Failed to load shipments');
      } finally {
        setLoadingShipments(false);
      }
    };

    fetchShipments();
  }, []);

  const handlePredict = async () => {
    if (!selectedShipment) {
      setError('Please select a shipment');
      return;
    }

    try {
      setLoading(true);
      setError(null);
      
      const response = await shipmentService.predictDelay(selectedShipment.id);
      setPrediction(response);
      showSuccess('Delay prediction completed');
    } catch (err) {
      console.error('Error predicting delay:', err);
      setError(err.response?.data?.detail || 'Failed to predict shipment delay');
      showError('Failed to predict shipment delay');
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (dateString) => {
    if (!dateString) return 'Not set';
    try {
      const date = new Date(dateString);
      return date.toLocaleString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      });
    } catch {
      return dateString;
    }
  };

  const getDaysUntilArrival = (dateString) => {
    if (!dateString) return null;
    try {
      const date = new Date(dateString);
      const now = new Date();
      const diffTime = date - now;
      const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
      return diffDays;
    } catch {
      return null;
    }
  };

  const getShippingMethodIcon = (method) => {
    if (!method) return <LocalShippingOutlinedIcon />;
    const methodLower = method.toLowerCase();
    if (methodLower.includes('air') || methodLower.includes('flight')) {
      return <FlightIcon />;
    } else if (methodLower.includes('sea') || methodLower.includes('ship') || methodLower.includes('ocean')) {
      return <DirectionsBoatIcon />;
    } else if (methodLower.includes('train') || methodLower.includes('rail')) {
      return <TrainIcon />;
    } else {
      return <LocalShippingOutlinedIcon />;
    }
  };

  const getStatusColor = (status) => {
    if (!status) return 'default';
    const statusLower = status.toLowerCase();
    if (statusLower.includes('delivered') || statusLower.includes('complete')) {
      return 'success';
    } else if (statusLower.includes('transit') || statusLower.includes('shipped')) {
      return 'info';
    } else if (statusLower.includes('pending') || statusLower.includes('processing')) {
      return 'warning';
    } else if (statusLower.includes('delayed') || statusLower.includes('error')) {
      return 'error';
    }
    return 'default';
  };

  const shipmentDetails = prediction?.shipment_details || selectedShipment;

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        🚚 AI Shipment Delay Prediction
      </Typography>
      <Typography variant="body2" color="text.secondary" gutterBottom sx={{ mb: 3 }}>
        Predict shipment delays using real-time weather data and AI-powered analysis
      </Typography>

      <Paper sx={{ p: 3, mb: 3 }}>
        <Grid container spacing={2} alignItems="center">
          <Grid item xs={12}>
            <Autocomplete
              options={shipments}
              getOptionLabel={(option) => option.display_name || `Shipment #${option.id}`}
              value={selectedShipment}
              onChange={(event, newValue) => {
                setSelectedShipment(newValue);
                setPrediction(null);
                setError(null);
              }}
              loading={loadingShipments}
              renderInput={(params) => (
                <TextField
                  {...params}
                  label="Select Shipment"
                  placeholder="Choose a shipment to analyze"
                  helperText={selectedShipment ? `Tracking: ${selectedShipment.tracking_number || 'N/A'}` : 'Select a shipment from the list'}
                  InputProps={{
                    ...params.InputProps,
                    endAdornment: (
                      <>
                        {loadingShipments ? <CircularProgress color="inherit" size={20} /> : null}
                        {params.InputProps.endAdornment}
                      </>
                    ),
                  }}
                />
              )}
              renderOption={(props, option) => (
                <Box component="li" {...props} key={option.id}>
                  <Box sx={{ display: 'flex', flexDirection: 'column', width: '100%' }}>
                    <Typography variant="body1">
                      {option.tracking_number || `SHIP-${option.id.toString().padStart(4, '0')}`}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      {option.supplier_name} • {option.shipping_method} • {option.status}
                    </Typography>
                    {option.expected_arrival && (
                      <Typography variant="caption" color="text.secondary">
                        Expected: {formatDate(option.expected_arrival)}
                      </Typography>
                    )}
                  </Box>
                </Box>
              )}
            />
          </Grid>
          <Grid item xs={12}>
            <Button
              variant="contained"
              onClick={handlePredict}
              disabled={loading || !selectedShipment}
              fullWidth
              size="large"
              startIcon={loading ? <CircularProgress size={20} color="inherit" /> : <LocalShippingIcon />}
              sx={{ mt: 1 }}
            >
              {loading ? 'Analyzing...' : 'Predict Delay & Analyze Weather'}
            </Button>
          </Grid>

          {error && (
            <Grid item xs={12}>
              <Alert severity="error" sx={{ mt: 2 }}>
                {error}
              </Alert>
            </Grid>
          )}
        </Grid>
      </Paper>

      {prediction && shipmentDetails && (
        <Grid container spacing={3}>
          {/* Shipment Details Card */}
          <Grid item xs={12}>
            <Card elevation={3}>
              <CardHeader
                title="Shipment Details"
                avatar={<LocalShippingIcon color="primary" />}
                action={
                  <Chip
                    label={shipmentDetails.status || 'Unknown'}
                    color={getStatusColor(shipmentDetails.status)}
                    size="small"
                  />
                }
              />
              <CardContent>
                <Grid container spacing={3}>
                  <Grid item xs={12} md={6}>
                    <Stack spacing={2}>
                      <Box>
                        <Typography variant="body2" color="text.secondary" gutterBottom>
                          Tracking Number
                        </Typography>
                        <Typography variant="h6" sx={{ fontWeight: 'bold' }}>
                          {shipmentDetails.tracking_number || `SHIP-${shipmentDetails.id.toString().padStart(4, '0')}`}
                        </Typography>
                      </Box>
                      <Box>
                        <Typography variant="body2" color="text.secondary" gutterBottom>
                          Supplier
                        </Typography>
                        <Typography variant="body1">
                          {shipmentDetails.supplier_name || 'Unknown Supplier'}
                        </Typography>
                        <Typography variant="body2" color="text.secondary" sx={{ mt: 0.5 }}>
                          <LocationOnIcon sx={{ fontSize: 14, verticalAlign: 'middle', mr: 0.5 }} />
                          {prediction.origin || shipmentDetails.supplier_address || 'Unknown Location'}
                        </Typography>
                      </Box>
                      <Box>
                        <Typography variant="body2" color="text.secondary" gutterBottom>
                          Shipping Method
                        </Typography>
                        <Chip
                          icon={getShippingMethodIcon(shipmentDetails.shipping_method)}
                          label={shipmentDetails.shipping_method || 'Unknown'}
                          variant="outlined"
                        />
                      </Box>
                    </Stack>
                  </Grid>
                  <Grid item xs={12} md={6}>
                    <Stack spacing={2}>
                      <Box>
                        <Typography variant="body2" color="text.secondary" gutterBottom>
                          <AccessTimeIcon sx={{ fontSize: 16, verticalAlign: 'middle', mr: 0.5 }} />
                          Expected Arrival
                        </Typography>
                        <Typography variant="body1" sx={{ fontWeight: 'bold' }}>
                          {formatDate(shipmentDetails.expected_arrival)}
                        </Typography>
                        {shipmentDetails.expected_arrival && (
                          <Typography variant="body2" color="text.secondary" sx={{ mt: 0.5 }}>
                            {(() => {
                              const days = getDaysUntilArrival(shipmentDetails.expected_arrival);
                              if (days === null) return '';
                              if (days < 0) return `${Math.abs(days)} days overdue`;
                              if (days === 0) return 'Arriving today';
                              return `${days} day${days !== 1 ? 's' : ''} until arrival`;
                            })()}
                          </Typography>
                        )}
                      </Box>
                      <Box>
                        <Typography variant="body2" color="text.secondary" gutterBottom>
                          Destination
                        </Typography>
                        <Typography variant="body1">
                          <LocationOnIcon sx={{ fontSize: 16, verticalAlign: 'middle', mr: 0.5 }} />
                          {prediction.destination || 'Company Warehouse'}
                        </Typography>
                      </Box>
                      {shipmentDetails.actual_arrival && (
                        <Box>
                          <Typography variant="body2" color="text.secondary" gutterBottom>
                            Actual Arrival
                          </Typography>
                          <Typography variant="body1" color="success.main">
                            {formatDate(shipmentDetails.actual_arrival)}
                          </Typography>
                        </Box>
                      )}
                    </Stack>
                  </Grid>
                </Grid>
              </CardContent>
            </Card>
          </Grid>

          {/* Delay Prediction Card */}
          <Grid item xs={12} md={6}>
            <Card 
              elevation={3}
              sx={{ 
                bgcolor: prediction.overall_delay_probability > 50 ? '#fff3e0' : '#e8f5e9',
                border: `2px solid ${prediction.overall_delay_probability > 50 ? '#ff9800' : '#4caf50'}`
              }}
            >
              <CardHeader
                title="Delay Prediction"
                avatar={
                  prediction.overall_delay_probability > 50 
                    ? <WarningIcon color="warning" /> 
                    : <CheckCircleIcon color="success" />
                }
              />
              <CardContent>
                <Box sx={{ textAlign: 'center', mb: 3 }}>
                  <Typography variant="h1" color={prediction.overall_delay_probability > 50 ? 'warning.main' : 'success.main'}>
                    {prediction.overall_delay_probability.toFixed(1)}%
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Delay Probability
                  </Typography>
                  <LinearProgress 
                    variant="determinate" 
                    value={prediction.overall_delay_probability} 
                    sx={{ mt: 2, height: 8, borderRadius: 4 }}
                    color={prediction.overall_delay_probability > 50 ? 'warning' : 'success'}
                  />
                </Box>
                
                {prediction.expected_delay_days > 0 ? (
                  <Alert severity="warning" icon={<WarningIcon />}>
                    <Typography variant="body1" sx={{ fontWeight: 'bold' }}>
                      Expected Delay: {prediction.expected_delay_days} day{prediction.expected_delay_days !== 1 ? 's' : ''}
                    </Typography>
                    {shipmentDetails.expected_arrival && (
                      <Typography variant="body2" sx={{ mt: 1 }}>
                        New estimated arrival: {formatDate(
                          new Date(new Date(shipmentDetails.expected_arrival).getTime() + prediction.expected_delay_days * 24 * 60 * 60 * 1000).toISOString()
                        )}
                      </Typography>
                    )}
                  </Alert>
                ) : (
                  <Alert severity="success" icon={<CheckCircleIcon />}>
                    <Typography variant="body1" sx={{ fontWeight: 'bold' }}>
                      On-time delivery expected
                    </Typography>
                  </Alert>
                )}
              </CardContent>
            </Card>
          </Grid>

          {/* Weather Assessment Card */}
          <Grid item xs={12} md={6}>
            <Card elevation={3}>
              <CardHeader
                title="Weather Conditions"
                avatar={<CloudIcon color="info" />}
              />
              <CardContent>
                {prediction.weather_assessment?.severe_weather_detected ? (
                  <>
                    <Alert severity="error" icon={<ThunderstormIcon />} sx={{ mb: 2 }}>
                      <Typography variant="body1" sx={{ fontWeight: 'bold' }}>
                        ⚠️ Severe Weather Detected
                      </Typography>
                    </Alert>
                    <Box sx={{ mb: 2 }}>
                      <Typography variant="body2" color="text.secondary" gutterBottom>
                        Combined Risk Score
                      </Typography>
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                        <LinearProgress 
                          variant="determinate" 
                          value={prediction.weather_assessment.combined_risk_score || 0} 
                          sx={{ flexGrow: 1, height: 8, borderRadius: 4 }}
                          color="error"
                        />
                        <Typography variant="body1" sx={{ fontWeight: 'bold', minWidth: 50 }}>
                          {prediction.weather_assessment.combined_risk_score || 0}/100
                        </Typography>
                      </Box>
                    </Box>
                    {prediction.weather_assessment.origin_weather && (
                      <Box sx={{ mb: 2 }}>
                        <Typography variant="body2" color="text.secondary" gutterBottom>
                          Origin Weather ({prediction.origin})
                        </Typography>
                        <Chip 
                          icon={prediction.weather_assessment.origin_weather.severe_weather ? <ThunderstormIcon /> : <WbSunnyIcon />}
                          label={prediction.weather_assessment.origin_weather.overall_condition || 'Unknown'}
                          color={prediction.weather_assessment.origin_weather.severe_weather ? 'error' : 'success'}
                          sx={{ mr: 1 }}
                        />
                        <Chip 
                          label={`Risk: ${prediction.weather_assessment.origin_weather.risk_score || 0}`}
                          size="small"
                          color={prediction.weather_assessment.origin_weather.severe_weather ? 'error' : 'default'}
                        />
                        {prediction.weather_assessment.origin_weather.weather_risks && 
                         prediction.weather_assessment.origin_weather.weather_risks.length > 0 && (
                          <Box sx={{ mt: 1 }}>
                            <Typography variant="caption" color="text.secondary">
                              Risks: {prediction.weather_assessment.origin_weather.weather_risks
                                .slice(0, 2)
                                .map(r => r.condition || r.description)
                                .join(', ')}
                            </Typography>
                          </Box>
                        )}
                      </Box>
                    )}
                    {prediction.weather_assessment.destination_weather && (
                      <Box>
                        <Typography variant="body2" color="text.secondary" gutterBottom>
                          Destination Weather ({prediction.destination})
                        </Typography>
                        <Chip 
                          icon={prediction.weather_assessment.destination_weather.severe_weather ? <ThunderstormIcon /> : <WbSunnyIcon />}
                          label={prediction.weather_assessment.destination_weather.overall_condition || 'Unknown'}
                          color={prediction.weather_assessment.destination_weather.severe_weather ? 'error' : 'success'}
                          sx={{ mr: 1 }}
                        />
                        <Chip 
                          label={`Risk: ${prediction.weather_assessment.destination_weather.risk_score || 0}`}
                          size="small"
                          color={prediction.weather_assessment.destination_weather.severe_weather ? 'error' : 'default'}
                        />
                        {prediction.weather_assessment.destination_weather.weather_risks && 
                         prediction.weather_assessment.destination_weather.weather_risks.length > 0 && (
                          <Box sx={{ mt: 1 }}>
                            <Typography variant="caption" color="text.secondary">
                              Risks: {prediction.weather_assessment.destination_weather.weather_risks
                                .slice(0, 2)
                                .map(r => r.condition || r.description)
                                .join(', ')}
                            </Typography>
                          </Box>
                        )}
                      </Box>
                    )}
                  </>
                ) : (
                  <Alert severity="success" icon={<WbSunnyIcon />}>
                    <Typography variant="body1" sx={{ fontWeight: 'bold' }}>
                      ✅ Normal weather conditions
                    </Typography>
                    <Typography variant="body2" sx={{ mt: 1 }}>
                      No severe weather detected along the route. Conditions are favorable for on-time delivery.
                    </Typography>
                  </Alert>
                )}
              </CardContent>
            </Card>
          </Grid>

          {/* AI Analysis Card */}
          {prediction.ai_prediction?.ai_enabled && (
            <Grid item xs={12}>
              <Card elevation={3} sx={{ bgcolor: '#f0f7ff', border: '2px solid #2196f3' }}>
                <CardHeader
                  title="🤖 AI-Powered Analysis"
                  subheader={`Model: ${prediction.ai_prediction.model_used || 'GPT-3.5'} • Confidence: ${prediction.ai_prediction.confidence || 'N/A'}%`}
                />
                <CardContent>
                  {prediction.ai_prediction.primary_risk_factors?.length > 0 && (
                    <>
                      <Typography variant="subtitle1" gutterBottom sx={{ fontWeight: 'bold' }}>
                        Primary Risk Factors:
                      </Typography>
                      <List dense>
                        {prediction.ai_prediction.primary_risk_factors.map((factor, idx) => (
                          <ListItem key={idx} sx={{ pl: 0 }}>
                            <ListItemText primary={`• ${factor}`} />
                          </ListItem>
                        ))}
                      </List>
                      <Divider sx={{ my: 2 }} />
                    </>
                  )}

                  {prediction.recommendations?.length > 0 && (
                    <>
                      <Typography variant="subtitle1" gutterBottom sx={{ fontWeight: 'bold' }}>
                        ✅ Recommended Actions:
                      </Typography>
                      <List>
                        {prediction.recommendations.map((rec, idx) => (
                          <ListItem key={idx} sx={{ pl: 0 }}>
                            <ListItemText 
                              primary={`${idx + 1}. ${rec}`}
                              primaryTypographyProps={{ variant: 'body1' }}
                            />
                          </ListItem>
                        ))}
                      </List>
                    </>
                  )}
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
