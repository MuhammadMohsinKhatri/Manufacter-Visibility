import React, { useState, useEffect } from 'react';
import { 
  Box, 
  Typography, 
  Paper, 
  Grid, 
  TextField, 
  Button, 
  MenuItem, 
  CircularProgress,
  Alert,
  Stepper,
  Step,
  StepLabel,
  Card,
  CardContent,
  CardHeader,
  List,
  ListItem,
  ListItemText,
  Divider,
  Chip,
  LinearProgress,
  IconButton
} from '@mui/material';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import { format, addDays } from 'date-fns';

// Icons
import AddIcon from '@mui/icons-material/Add';
import RemoveIcon from '@mui/icons-material/Remove';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import WarningIcon from '@mui/icons-material/Warning';
import ErrorIcon from '@mui/icons-material/Error';

// Services
import { orderService } from '../services';

// Notification context
import { useNotification } from '../context/NotificationContext';

export default function OrderFeasibility() {
  const [loading, setLoading] = useState(false);
  const [products, setProducts] = useState([]);
  const [orderItems, setOrderItems] = useState([{ productId: '', quantity: 1 }]);
  const [deliveryDate, setDeliveryDate] = useState(addDays(new Date(), 30));
  const [feasibilityResult, setFeasibilityResult] = useState(null);
  const [error, setError] = useState(null);
  const [activeStep, setActiveStep] = useState(0);
  
  const { showError } = useNotification();

  useEffect(() => {
    // In a real app, fetch products from API
    // For demo, use simulated data
    const simulatedProducts = [
      { id: 1, name: 'Industrial Controller', price: 1299.99 },
      { id: 2, name: 'Smart Thermostat', price: 249.99 },
      { id: 3, name: 'Power Management Unit', price: 3499.99 },
      { id: 4, name: 'Security Gateway', price: 1899.99 },
      { id: 5, name: 'Environmental Monitor', price: 899.99 }
    ];
    
    setProducts(simulatedProducts);
  }, []);

  const handleAddItem = () => {
    setOrderItems([...orderItems, { productId: '', quantity: 1 }]);
  };

  const handleRemoveItem = (index) => {
    const newItems = [...orderItems];
    newItems.splice(index, 1);
    setOrderItems(newItems);
  };

  const handleItemChange = (index, field, value) => {
    const newItems = [...orderItems];
    newItems[index][field] = value;
    setOrderItems(newItems);
  };

  const handleNext = () => {
    setActiveStep((prevStep) => prevStep + 1);
  };

  const handleBack = () => {
    setActiveStep((prevStep) => prevStep - 1);
  };

  const handleCheckFeasibility = async () => {
    // Validate form
    const invalidItems = orderItems.filter(item => !item.productId || item.quantity < 1);
    if (invalidItems.length > 0) {
      setError('Please select a product and quantity for all items');
      return;
    }
    
    try {
      setLoading(true);
      setError(null);
      
      // Move to loading step first
      handleNext();
      
      // Convert to the format expected by the API
      const checkData = {
        product_ids: orderItems.map(item => parseInt(item.productId)),
        quantities: orderItems.map(item => item.quantity),
        requested_delivery_date: deliveryDate.toISOString()
      };
      
      // Call the API for feasibility check
      const result = await orderService.checkFeasibility(checkData);
      
      console.log('Feasibility check result:', result);
      
      if (!result) {
        throw new Error('No result received from server');
      }
      
      setFeasibilityResult(result);
      // Move to results step
      handleNext();
    } catch (err) {
      console.error('Error checking feasibility:', err);
      setError('Failed to check order feasibility');
      showError('Failed to check order feasibility');
      // Go back to step 0 on error
      setActiveStep(0);
    } finally {
      setLoading(false);
    }
  };

  const steps = ['Select Products', 'Check Feasibility', 'Review Results'];

  const getStepContent = (step) => {
    switch (step) {
      case 0:
        return (
          <Box sx={{ mt: 2 }}>
            <Typography variant="h6" gutterBottom>
              Order Details
            </Typography>
            
            {orderItems.map((item, index) => (
              <Grid container spacing={2} key={index} sx={{ mb: 2 }}>
                <Grid item xs={12} sm={5}>
                  <TextField
                    select
                    label="Product"
                    value={item.productId}
                    onChange={(e) => handleItemChange(index, 'productId', e.target.value)}
                    fullWidth
                    required
                  >
                    <MenuItem value="">Select a product</MenuItem>
                    {products.map((product) => (
                      <MenuItem key={product.id} value={product.id}>
                        {product.name} (${product.price.toFixed(2)})
                      </MenuItem>
                    ))}
                  </TextField>
                </Grid>
                <Grid item xs={12} sm={5}>
                  <TextField
                    label="Quantity"
                    type="number"
                    value={item.quantity}
                    onChange={(e) => handleItemChange(index, 'quantity', parseInt(e.target.value) || 0)}
                    fullWidth
                    required
                    InputProps={{ inputProps: { min: 1 } }}
                  />
                </Grid>
                <Grid item xs={12} sm={2} sx={{ display: 'flex', alignItems: 'center' }}>
                  {index === 0 ? (
                    <IconButton color="primary" onClick={handleAddItem}>
                      <AddIcon />
                    </IconButton>
                  ) : (
                    <IconButton color="error" onClick={() => handleRemoveItem(index)}>
                      <RemoveIcon />
                    </IconButton>
                  )}
                </Grid>
              </Grid>
            ))}
            
            <LocalizationProvider dateAdapter={AdapterDateFns}>
              <DatePicker
                label="Requested Delivery Date"
                value={deliveryDate}
                onChange={(newValue) => setDeliveryDate(newValue)}
                minDate={addDays(new Date(), 7)}
                slotProps={{
                  textField: {
                    fullWidth: true,
                    sx: { mt: 2 }
                  }
                }}
              />
            </LocalizationProvider>
            
            <Box sx={{ mt: 4, display: 'flex', justifyContent: 'flex-end' }}>
              <Button
                variant="contained"
                onClick={handleCheckFeasibility}
                disabled={loading || orderItems.some(item => !item.productId)}
              >
                {loading ? <CircularProgress size={24} /> : 'Check Feasibility'}
              </Button>
            </Box>
          </Box>
        );
      case 1:
        return (
          <Box sx={{ mt: 2, display: 'flex', justifyContent: 'center', alignItems: 'center', height: '300px' }}>
            <CircularProgress />
          </Box>
        );
      case 2:
        return (
          <Box sx={{ mt: 2 }}>
            {feasibilityResult && (
              <Grid container spacing={3}>
                <Grid item xs={12}>
                  <Alert 
                    severity={feasibilityResult.feasible ? 'success' : 'warning'}
                    icon={feasibilityResult.feasible ? <CheckCircleIcon /> : <WarningIcon />}
                    sx={{ mb: 3 }}
                  >
                    <Typography variant="h6">
                      {feasibilityResult.feasible 
                        ? 'Order is feasible with the requested delivery date' 
                        : 'Order is not feasible with the requested delivery date'}
                    </Typography>
                    <Typography>
                      {feasibilityResult.feasible 
                        ? `We can deliver by ${format(new Date(deliveryDate), 'MMMM dd, yyyy')}` 
                        : `Earliest possible delivery date: ${format(new Date(feasibilityResult.earliest_possible_date), 'MMMM dd, yyyy')}`}
                    </Typography>
                  </Alert>
                </Grid>
                
                {/* AI Analysis Section */}
                {feasibilityResult.ai_analysis?.ai_enabled && (
                  <Grid item xs={12}>
                    <Card sx={{ bgcolor: '#f0f7ff', border: '2px solid #2196f3' }}>
                      <CardHeader 
                        title="🤖 AI-Powered Analysis" 
                        titleTypographyProps={{ variant: 'h6', color: 'primary' }}
                        subheader={`Model: ${feasibilityResult.ai_analysis.model_used || 'GPT-4'}`}
                      />
                      <CardContent>
                        {feasibilityResult.critical_bottleneck && (
                          <>
                            <Typography variant="subtitle1" gutterBottom sx={{ fontWeight: 'bold', color: 'error.main' }}>
                              Critical Bottleneck:
                            </Typography>
                            <Alert severity="error" sx={{ mb: 2 }}>
                              {feasibilityResult.critical_bottleneck}
                            </Alert>
                          </>
                        )}
                        
                        {feasibilityResult.actionable_recommendations?.length > 0 && (
                          <>
                            <Typography variant="subtitle1" gutterBottom sx={{ fontWeight: 'bold', mt: 2 }}>
                              ✅ Actionable Recommendations:
                            </Typography>
                            <List dense>
                              {feasibilityResult.actionable_recommendations.map((rec, idx) => (
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
                        
                        {feasibilityResult.alternative_strategies?.length > 0 && (
                          <>
                            <Divider sx={{ my: 2 }} />
                            <Typography variant="subtitle1" gutterBottom sx={{ fontWeight: 'bold' }}>
                              💡 Alternative Strategies:
                            </Typography>
                            <List dense>
                              {feasibilityResult.alternative_strategies.map((strategy, idx) => (
                                <ListItem key={idx}>
                                  <ListItemText 
                                    primary={`• ${strategy}`}
                                    primaryTypographyProps={{ variant: 'body2', color: 'text.secondary' }}
                                  />
                                </ListItem>
                              ))}
                            </List>
                          </>
                        )}
                        
                        {feasibilityResult.executive_summary && (
                          <>
                            <Divider sx={{ my: 2 }} />
                            <Typography variant="subtitle1" gutterBottom sx={{ fontWeight: 'bold' }}>
                              📊 Executive Summary:
                            </Typography>
                            <Alert severity="info" sx={{ mt: 1 }}>
                              {feasibilityResult.executive_summary}
                            </Alert>
                          </>
                        )}
                        
                        {feasibilityResult.ai_confidence_score && (
                          <Box sx={{ mt: 2 }}>
                            <Chip 
                              label={`AI Confidence: ${feasibilityResult.ai_confidence_score}%`}
                              color={feasibilityResult.ai_confidence_score > 70 ? 'success' : 'warning'}
                              size="small"
                            />
                          </Box>
                        )}
                      </CardContent>
                    </Card>
                  </Grid>
                )}
                
                {/* Show message if AI is not enabled */}
                {feasibilityResult.ai_analysis && !feasibilityResult.ai_analysis.ai_enabled && (
                  <Grid item xs={12}>
                    <Alert severity="info" sx={{ mb: 2 }}>
                      ℹ️ AI analysis is currently unavailable. Using rule-based analysis. 
                      Configure OPENAI_API_KEY in backend/.env to enable AI features.
                    </Alert>
                  </Grid>
                )}
                
                <Grid item xs={12} md={4}>
                  <Card>
                    <CardHeader 
                      title="Inventory Status" 
                      titleTypographyProps={{ variant: 'h6' }}
                      avatar={
                        feasibilityResult.inventory_constraints.length > 0 
                          ? <ErrorIcon color="error" /> 
                          : <CheckCircleIcon color="success" />
                      }
                    />
                    <CardContent>
                      {feasibilityResult.inventory_constraints.length > 0 ? (
                        <List dense>
                          {feasibilityResult.inventory_constraints.map((constraint, index) => (
                            <React.Fragment key={index}>
                              <ListItem>
                                <ListItemText primary={constraint} />
                              </ListItem>
                              {index < feasibilityResult.inventory_constraints.length - 1 && <Divider />}
                            </React.Fragment>
                          ))}
                        </List>
                      ) : (
                        <Typography variant="body2" color="text.secondary">
                          All required components are available in inventory
                        </Typography>
                      )}
                    </CardContent>
                  </Card>
                </Grid>
                
                <Grid item xs={12} md={4}>
                  <Card>
                    <CardHeader 
                      title="Production Capacity" 
                      titleTypographyProps={{ variant: 'h6' }}
                      avatar={
                        feasibilityResult.production_constraints.length > 0 
                          ? <ErrorIcon color="error" /> 
                          : <CheckCircleIcon color="success" />
                      }
                    />
                    <CardContent>
                      {feasibilityResult.production_constraints.length > 0 ? (
                        <List dense>
                          {feasibilityResult.production_constraints.map((constraint, index) => (
                            <React.Fragment key={index}>
                              <ListItem>
                                <ListItemText primary={constraint} />
                              </ListItem>
                              {index < feasibilityResult.production_constraints.length - 1 && <Divider />}
                            </React.Fragment>
                          ))}
                        </List>
                      ) : (
                        <Typography variant="body2" color="text.secondary">
                          Sufficient production capacity available
                        </Typography>
                      )}
                    </CardContent>
                  </Card>
                </Grid>
                
                <Grid item xs={12} md={4}>
                  <Card>
                    <CardHeader 
                      title="Supply Chain Risks" 
                      titleTypographyProps={{ variant: 'h6' }}
                      avatar={
                        feasibilityResult.risk_factors.length > 0 
                          ? <WarningIcon color="warning" /> 
                          : <CheckCircleIcon color="success" />
                      }
                    />
                    <CardContent>
                      {feasibilityResult.risk_factors.length > 0 ? (
                        <List dense>
                          {feasibilityResult.risk_factors.map((risk, index) => (
                            <React.Fragment key={index}>
                              <ListItem>
                                <ListItemText primary={risk} />
                              </ListItem>
                              {index < feasibilityResult.risk_factors.length - 1 && <Divider />}
                            </React.Fragment>
                          ))}
                        </List>
                      ) : (
                        <Typography variant="body2" color="text.secondary">
                          No significant supply chain risks detected
                        </Typography>
                      )}
                    </CardContent>
                  </Card>
                </Grid>
                
                <Grid item xs={12}>
                  <Box sx={{ mt: 2 }}>
                    <Typography variant="subtitle1" gutterBottom>
                      Confidence Score: {feasibilityResult.confidence_score}%
                    </Typography>
                    <LinearProgress 
                      variant="determinate" 
                      value={feasibilityResult.confidence_score} 
                      color={
                        feasibilityResult.confidence_score > 70 ? 'success' :
                        feasibilityResult.confidence_score > 40 ? 'warning' : 'error'
                      }
                      sx={{ height: 10, borderRadius: 5 }}
                    />
                    <Typography variant="caption" color="text.secondary" sx={{ mt: 1, display: 'block' }}>
                      {feasibilityResult.confidence_score > 70 
                        ? 'High confidence in this assessment'
                        : feasibilityResult.confidence_score > 40
                          ? 'Medium confidence in this assessment'
                          : 'Low confidence in this assessment - consider adjusting order parameters'
                      }
                    </Typography>
                  </Box>
                </Grid>
                
                <Grid item xs={12} sx={{ mt: 2 }}>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                    <Button onClick={handleBack}>
                      Back
                    </Button>
                    <Box>
                      <Button 
                        variant="outlined" 
                        sx={{ mr: 2 }}
                        onClick={() => {
                          setActiveStep(0);
                          setFeasibilityResult(null);
                        }}
                      >
                        Modify Order
                      </Button>
                      <Button 
                        variant="contained"
                        disabled={!feasibilityResult.feasible}
                      >
                        Proceed to Order
                      </Button>
                    </Box>
                  </Box>
                </Grid>
              </Grid>
            )}
          </Box>
        );
      default:
        return 'Unknown step';
    }
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Order Feasibility Check
      </Typography>
      
      <Paper sx={{ p: 3 }}>
        <Stepper activeStep={activeStep} sx={{ mb: 4 }}>
          {steps.map((label) => (
            <Step key={label}>
              <StepLabel>{label}</StepLabel>
            </Step>
          ))}
        </Stepper>
        
        {error && (
          <Alert severity="error" sx={{ mb: 2 }}>
            {error}
          </Alert>
        )}
        
        {getStepContent(activeStep)}
      </Paper>
    </Box>
  );
}