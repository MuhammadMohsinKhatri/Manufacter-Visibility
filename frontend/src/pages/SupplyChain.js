import React, { useState, useEffect } from 'react';
import { 
  Box, 
  Typography, 
  Button, 
  Paper, 
  CircularProgress,
  Alert,
  Chip,
  Card,
  CardContent,
  CardHeader,
  Grid,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Divider,
  TextField,
  MenuItem,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  LinearProgress,
  Stack,
  Tabs,
  Tab,
  Accordion,
  AccordionSummary,
  AccordionDetails
} from '@mui/material';
import { DataGrid } from '@mui/x-data-grid';
import { format } from 'date-fns';

// Icons
import WarningIcon from '@mui/icons-material/Warning';
import UpdateIcon from '@mui/icons-material/Update';
import AddIcon from '@mui/icons-material/Add';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import ErrorIcon from '@mui/icons-material/Error';
import InfoIcon from '@mui/icons-material/Info';
import CloudIcon from '@mui/icons-material/Cloud';
import LocalShippingIcon from '@mui/icons-material/LocalShipping';
import TrendingUpIcon from '@mui/icons-material/TrendingUp';
import AssessmentIcon from '@mui/icons-material/Assessment';
import AutoAwesomeIcon from '@mui/icons-material/AutoAwesome';

// Services
import supplyChainService from '../services/supplyChainService';

// Notification context
import { useNotification } from '../context/NotificationContext';

export default function SupplyChain() {
  const [loading, setLoading] = useState(true);
  const [assessing, setAssessing] = useState(false);
  const [risks, setRisks] = useState([]);
  const [riskAssessment, setRiskAssessment] = useState(null);
  const [error, setError] = useState(null);
  const [openDialog, setOpenDialog] = useState(false);
  const [activeTab, setActiveTab] = useState(0);
  const [filters, setFilters] = useState({
    risk_type: '',
    region: ''
  });
  const [assessmentParams, setAssessmentParams] = useState({
    time_horizon_days: 30
  });
  const { showSuccess, showError } = useNotification();

  const fetchRisks = async () => {
    try {
      setLoading(true);
      const params = {};
      if (filters.risk_type) params.risk_type = filters.risk_type;
      if (filters.region) params.region = filters.region;
      
      const data = await supplyChainService.getExternalRisks(params);
      setRisks(Array.isArray(data) ? data : []);
    } catch (err) {
      console.error('Error fetching risks:', err);
      setError('Failed to load supply chain risks. Please try again later.');
      showError('Failed to load supply chain risks');
    } finally {
      setLoading(false);
    }
  };

  const handleAssessRisks = async () => {
    try {
      setAssessing(true);
      setError(null);
      const result = await supplyChainService.assessRisks(assessmentParams);
      setRiskAssessment(result);
      showSuccess('Risk assessment completed');
      setActiveTab(0); // Stay on Risk Assessment tab to show results
    } catch (err) {
      console.error('Error assessing risks:', err);
      setError(err.response?.data?.detail || 'Failed to assess supply chain risks');
      showError('Failed to assess supply chain risks');
    } finally {
      setAssessing(false);
    }
  };

  useEffect(() => {
    fetchRisks();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [filters.risk_type, filters.region]);

  const handleUpdateRisks = async () => {
    try {
      setLoading(true);
      await supplyChainService.updateExternalRisks();
      showSuccess('Supply chain risks updated successfully');
      fetchRisks();
    } catch (err) {
      console.error('Error updating risks:', err);
      showError('Failed to update supply chain risks');
    } finally {
      setLoading(false);
    }
  };

  const handleCreateRisk = () => {
    setOpenDialog(true);
  };

  const handleDialogClose = () => {
    setOpenDialog(false);
  };

  const handleRiskSubmit = async (event) => {
    event.preventDefault();
    const formData = new FormData(event.target);
    
    try {
      const riskData = {
        risk_type: formData.get('risk_type'),
        region: formData.get('region'),
        description: formData.get('description'),
        risk_level: formData.get('risk_level'),
        detected_date: new Date().toISOString()
      };
      
      await supplyChainService.createExternalRisk(riskData);
      showSuccess('Risk created successfully');
      handleDialogClose();
      fetchRisks();
    } catch (err) {
      console.error('Error creating risk:', err);
      showError('Failed to create risk');
    }
  };

  const handleFilterChange = (field, value) => {
    setFilters(prev => ({ ...prev, [field]: value }));
  };

  // Use actual risks or fallback to empty array
  const data = risks.length > 0 ? risks : [];

  const getRiskLevelColor = (level) => {
    switch (level?.toUpperCase()) {
      case 'LOW':
        return 'success';
      case 'MEDIUM':
        return 'warning';
      case 'HIGH':
        return 'error';
      case 'CRITICAL':
        return 'error';
      default:
        return 'default';
    }
  };

  const getRiskLevelIcon = (level) => {
    switch (level?.toUpperCase()) {
      case 'CRITICAL':
      case 'HIGH':
        return <ErrorIcon />;
      case 'MEDIUM':
        return <WarningIcon />;
      case 'LOW':
        return <CheckCircleIcon />;
      default:
        return <InfoIcon />;
    }
  };

  const riskLevelCounts = {
    CRITICAL: data.filter(r => r.risk_level?.toUpperCase() === 'CRITICAL').length,
    HIGH: data.filter(r => r.risk_level?.toUpperCase() === 'HIGH').length,
    MEDIUM: data.filter(r => r.risk_level?.toUpperCase() === 'MEDIUM').length,
    LOW: data.filter(r => r.risk_level?.toUpperCase() === 'LOW').length
  };

  const totalRisks = data.length;
  const overallRiskScore = riskAssessment?.overall_risk_score || 0;

  const columns = [
    { field: 'id', headerName: 'ID', width: 80 },
    { 
      field: 'risk_type', 
      headerName: 'Type', 
      width: 150,
      renderCell: (params) => {
        const type = params.value || 'Unknown';
        const icons = {
          weather: <CloudIcon />,
          logistics: <LocalShippingIcon />,
          market: <TrendingUpIcon />,
          labor: <InfoIcon />,
          regulatory: <WarningIcon />
        };
        return (
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            {icons[type.toLowerCase()] || <InfoIcon />}
            <Typography>{type.charAt(0).toUpperCase() + type.slice(1)}</Typography>
          </Box>
        );
      }
    },
    { field: 'region', headerName: 'Region', width: 200 },
    { 
      field: 'description', 
      headerName: 'Description', 
      width: 400,
      flex: 1
    },
    { 
      field: 'risk_level', 
      headerName: 'Risk Level', 
      width: 150,
      renderCell: (params) => (
        <Chip 
          icon={getRiskLevelIcon(params.value)}
          label={params.value || 'Unknown'} 
          color={getRiskLevelColor(params.value)} 
          size="small" 
        />
      )
    },
    { 
      field: 'start_date', 
      headerName: 'Detected', 
      width: 180,
      valueFormatter: (params) => params.value ? format(new Date(params.value), 'MM/dd/yyyy') : 'N/A'
    }
  ];

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3, flexWrap: 'wrap', gap: 2 }}>
        <Typography variant="h4">
          Supply Chain Risk Management
        </Typography>
        <Box sx={{ display: 'flex', gap: 2 }}>
          <Button
            variant="outlined"
            startIcon={<UpdateIcon />}
            onClick={handleUpdateRisks}
            disabled={loading}
          >
            Refresh Risks
          </Button>
          <Button
            variant="contained"
            startIcon={<AddIcon />}
            onClick={handleCreateRisk}
          >
            Add Risk
          </Button>
        </Box>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError(null)}>
          {error}
        </Alert>
      )}

      {/* Summary Cards */}
      <Grid container spacing={3} sx={{ mb: 3 }}>
        <Grid item xs={12} sm={6} md={3}>
          <Card sx={{ borderLeft: '4px solid', borderColor: 'error.main' }}>
            <CardHeader 
              title="Critical Risks" 
              avatar={<ErrorIcon color="error" />}
            />
            <CardContent>
              <Typography variant="h3" color="error">
                {riskLevelCounts.CRITICAL}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Immediate action required
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card sx={{ borderLeft: '4px solid', borderColor: 'error.main' }}>
            <CardHeader 
              title="High Risks" 
              avatar={<WarningIcon color="error" />}
            />
            <CardContent>
              <Typography variant="h3" color="error">
                {riskLevelCounts.HIGH}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Monitor closely
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card sx={{ borderLeft: '4px solid', borderColor: 'warning.main' }}>
            <CardHeader 
              title="Medium Risks" 
              avatar={<WarningIcon color="warning" />}
            />
            <CardContent>
              <Typography variant="h3" color="warning.main">
                {riskLevelCounts.MEDIUM}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Standard monitoring
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card sx={{ borderLeft: '4px solid', borderColor: 'success.main' }}>
            <CardHeader 
              title="Total Risks" 
              avatar={<AssessmentIcon color="primary" />}
            />
            <CardContent>
              <Typography variant="h3">
                {totalRisks}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Active risk factors
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Tabs for different views */}
      <Paper sx={{ mb: 3 }}>
        <Tabs 
          value={activeTab} 
          onChange={(e, newValue) => {
            setActiveTab(newValue);
            // Clear error when switching tabs
            setError(null);
          }}
          indicatorColor="primary"
          textColor="primary"
          variant="fullWidth"
        >
          <Tab 
            label="Risk Assessment" 
            icon={<AutoAwesomeIcon />} 
            iconPosition="start"
            sx={{ textTransform: 'none', fontSize: '1rem', fontWeight: activeTab === 0 ? 'bold' : 'normal' }}
          />
          <Tab 
            label="Risk Registry" 
            icon={<AssessmentIcon />} 
            iconPosition="start"
            sx={{ textTransform: 'none', fontSize: '1rem', fontWeight: activeTab === 1 ? 'bold' : 'normal' }}
          />
        </Tabs>
      </Paper>

      {/* Risk Assessment Tab */}
      {activeTab === 0 && (
        <Box>
          <Paper sx={{ p: 3, mb: 3 }}>
            <Typography variant="h6" gutterBottom>
              AI-Powered Risk Assessment
            </Typography>
            <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
              Get comprehensive risk analysis with AI-generated mitigation strategies
            </Typography>
            
            <Grid container spacing={2} sx={{ mb: 3 }}>
              <Grid item xs={12} sm={6} md={4}>
                <TextField
                  label="Time Horizon (Days)"
                  type="number"
                  fullWidth
                  value={assessmentParams.time_horizon_days}
                  onChange={(e) => setAssessmentParams({
                    ...assessmentParams,
                    time_horizon_days: parseInt(e.target.value) || 30
                  })}
                  helperText="Assess risks for the next N days"
                />
              </Grid>
              <Grid item xs={12} sm={6} md={8} sx={{ display: 'flex', alignItems: 'center' }}>
                <Button
                  variant="contained"
                  size="large"
                  startIcon={assessing ? <CircularProgress size={20} color="inherit" /> : <AutoAwesomeIcon />}
                  onClick={handleAssessRisks}
                  disabled={assessing}
                  fullWidth
                >
                  {assessing ? 'Assessing Risks...' : 'Run AI Risk Assessment'}
                </Button>
              </Grid>
            </Grid>

            {riskAssessment && (
              <Box>
                <Divider sx={{ my: 3 }} />
                
                {/* Assessment Results Header */}
                <Box sx={{ mb: 3, textAlign: 'center' }}>
                  <Typography variant="h5" gutterBottom sx={{ fontWeight: 'bold' }}>
                    Assessment Results
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Analysis completed for {assessmentParams.time_horizon_days} day horizon
                  </Typography>
                </Box>
                
                {/* Overall Risk Score - Enhanced */}
                <Card 
                  elevation={4}
                  sx={{ 
                    mb: 3, 
                    background: overallRiskScore > 70 
                      ? 'linear-gradient(135deg, #ffebee 0%, #ffcdd2 100%)' 
                      : overallRiskScore > 40 
                        ? 'linear-gradient(135deg, #fff3e0 0%, #ffe0b2 100%)' 
                        : 'linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%)',
                    border: `3px solid ${overallRiskScore > 70 ? '#f44336' : overallRiskScore > 40 ? '#ff9800' : '#4caf50'}`
                  }}
                >
                  <CardHeader
                    title="Overall Risk Score"
                    avatar={<AssessmentIcon sx={{ fontSize: 40 }} />}
                    titleTypographyProps={{ variant: 'h5', fontWeight: 'bold' }}
                  />
                  <CardContent>
                    <Box sx={{ mb: 2 }}>
                      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                        <Box>
                          <Typography variant="h1" color={overallRiskScore > 70 ? 'error.main' : overallRiskScore > 40 ? 'warning.main' : 'success.main'} sx={{ fontWeight: 'bold' }}>
                            {overallRiskScore.toFixed(1)}%
                          </Typography>
                          <Typography variant="body2" color="text.secondary">
                            Risk Level
                          </Typography>
                        </Box>
                        <Chip 
                          icon={overallRiskScore > 70 ? <ErrorIcon /> : overallRiskScore > 40 ? <WarningIcon /> : <CheckCircleIcon />}
                          label={overallRiskScore > 70 ? 'High Risk' : overallRiskScore > 40 ? 'Medium Risk' : 'Low Risk'}
                          color={overallRiskScore > 70 ? 'error' : overallRiskScore > 40 ? 'warning' : 'success'}
                          size="large"
                          sx={{ fontSize: '1rem', padding: '8px 16px' }}
                        />
                      </Box>
                      <LinearProgress 
                        variant="determinate" 
                        value={overallRiskScore} 
                        sx={{ height: 12, borderRadius: 6 }}
                        color={overallRiskScore > 70 ? 'error' : overallRiskScore > 40 ? 'warning' : 'success'}
                      />
                    </Box>
                    <Alert 
                      severity={overallRiskScore > 70 ? 'error' : overallRiskScore > 40 ? 'warning' : 'success'}
                      icon={overallRiskScore > 70 ? <ErrorIcon /> : overallRiskScore > 40 ? <WarningIcon /> : <CheckCircleIcon />}
                    >
                      <Typography variant="body1">
                        {riskAssessment.summary || 
                         (overallRiskScore > 70 
                           ? 'High risk detected. Immediate action required to mitigate supply chain disruptions.'
                           : overallRiskScore > 40 
                             ? 'Moderate risk level. Monitor closely and implement preventive measures.'
                             : 'Low risk level. Supply chain conditions are stable.')}
                      </Typography>
                    </Alert>
                  </CardContent>
                </Card>

                {/* Quick Stats */}
                <Grid container spacing={2} sx={{ mb: 3 }}>
                  <Grid item xs={12} sm={6} md={3}>
                    <Card elevation={3} sx={{ textAlign: 'center', p: 2 }}>
                      <Typography variant="h3" color="primary">
                        {riskAssessment.risks?.length || 0}
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        Active Risks
                      </Typography>
                    </Card>
                  </Grid>
                  <Grid item xs={12} sm={6} md={3}>
                    <Card elevation={3} sx={{ textAlign: 'center', p: 2 }}>
                      <Typography variant="h3" color="warning.main">
                        {riskAssessment.affected_components?.length || 0}
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        Affected Components
                      </Typography>
                    </Card>
                  </Grid>
                  <Grid item xs={12} sm={6} md={3}>
                    <Card elevation={3} sx={{ textAlign: 'center', p: 2 }}>
                      <Typography variant="h3" color="error.main">
                        {riskAssessment.affected_suppliers?.length || 0}
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        Affected Suppliers
                      </Typography>
                    </Card>
                  </Grid>
                  <Grid item xs={12} sm={6} md={3}>
                    <Card elevation={3} sx={{ textAlign: 'center', p: 2 }}>
                      <Typography variant="h3" color="info.main">
                        {riskAssessment.risks?.filter(r => r.risk_level === 'CRITICAL' || r.risk_level === 'HIGH').length || 0}
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        High Priority Risks
                      </Typography>
                    </Card>
                  </Grid>
                </Grid>

                {/* Identified Risks - Enhanced */}
                {riskAssessment.risks && riskAssessment.risks.length > 0 && (
                  <Card elevation={3} sx={{ mb: 3 }}>
                    <CardHeader
                      title="Identified Risks"
                      subheader={`${riskAssessment.risks.length} risk factors detected in your supply chain`}
                      avatar={<WarningIcon color="warning" />}
                      titleTypographyProps={{ variant: 'h6', fontWeight: 'bold' }}
                    />
                    <CardContent>
                      <Grid container spacing={2}>
                        {riskAssessment.risks.map((risk, idx) => (
                          <Grid item xs={12} key={idx}>
                            <Accordion elevation={2}>
                              <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                                <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, width: '100%' }}>
                                  <Box sx={{ 
                                    p: 1, 
                                    borderRadius: 1, 
                                    bgcolor: getRiskLevelColor(risk.risk_level) === 'error' ? '#ffebee' : 
                                             getRiskLevelColor(risk.risk_level) === 'warning' ? '#fff3e0' : '#e8f5e9'
                                  }}>
                                    {getRiskLevelIcon(risk.risk_level)}
                                  </Box>
                                  <Box sx={{ flexGrow: 1 }}>
                                    <Typography variant="subtitle1" sx={{ fontWeight: 'bold' }}>
                                      {risk.risk_type ? risk.risk_type.charAt(0).toUpperCase() + risk.risk_type.slice(1) : 'Unknown Risk'}
                                    </Typography>
                                    <Typography variant="body2" color="text.secondary">
                                      {risk.region || 'Unknown Region'}
                                    </Typography>
                                  </Box>
                                  <Chip 
                                    icon={getRiskLevelIcon(risk.risk_level)}
                                    label={risk.risk_level || 'Unknown'} 
                                    color={getRiskLevelColor(risk.risk_level)}
                                    size="medium"
                                  />
                                </Box>
                              </AccordionSummary>
                              <AccordionDetails>
                                <Typography variant="body1" paragraph sx={{ fontWeight: 'medium' }}>
                                  {risk.description || 'No description available'}
                                </Typography>
                                {risk.start_date && (
                                  <Box sx={{ mt: 2, display: 'flex', gap: 2, flexWrap: 'wrap' }}>
                                    <Chip 
                                      label={`Start: ${format(new Date(risk.start_date), 'MMM dd, yyyy')}`}
                                      size="small"
                                      variant="outlined"
                                    />
                                    {risk.end_date && (
                                      <Chip 
                                        label={`End: ${format(new Date(risk.end_date), 'MMM dd, yyyy')}`}
                                        size="small"
                                        variant="outlined"
                                      />
                                    )}
                                  </Box>
                                )}
                                {risk.data && Object.keys(risk.data).length > 0 && (
                                  <Alert severity="info" sx={{ mt: 2 }}>
                                    <Typography variant="subtitle2" gutterBottom>
                                      Additional Details:
                                    </Typography>
                                    {Object.entries(risk.data).slice(0, 3).map(([key, value]) => (
                                      <Typography key={key} variant="body2">
                                        <strong>{key.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}:</strong> {String(value)}
                                      </Typography>
                                    ))}
                                  </Alert>
                                )}
                              </AccordionDetails>
                            </Accordion>
                          </Grid>
                        ))}
                      </Grid>
                    </CardContent>
                  </Card>
                )}

                {/* Affected Components & Suppliers */}
                <Grid container spacing={3} sx={{ mb: 3 }}>
                  {riskAssessment.affected_components && riskAssessment.affected_components.length > 0 && (
                    <Grid item xs={12} md={6}>
                      <Card elevation={3}>
                        <CardHeader
                          title="Affected Components"
                          subheader={`${riskAssessment.affected_components.length} components at risk`}
                          avatar={<WarningIcon color="warning" />}
                        />
                        <CardContent>
                          <List>
                            {riskAssessment.affected_components.map((comp, idx) => (
                              <ListItem key={idx} sx={{ borderLeft: '3px solid', borderColor: 'warning.main', mb: 1, bgcolor: '#fff3e0' }}>
                                <ListItemIcon>
                                  <ErrorIcon color="warning" />
                                </ListItemIcon>
                                <ListItemText 
                                  primary={comp.component_name || `Component #${comp.component_id}`}
                                  secondary={`${comp.risks?.length || 0} risk(s) affecting this component`}
                                />
                              </ListItem>
                            ))}
                          </List>
                        </CardContent>
                      </Card>
                    </Grid>
                  )}
                  
                  {riskAssessment.affected_suppliers && riskAssessment.affected_suppliers.length > 0 && (
                    <Grid item xs={12} md={6}>
                      <Card elevation={3}>
                        <CardHeader
                          title="Affected Suppliers"
                          subheader={`${riskAssessment.affected_suppliers.length} suppliers impacted`}
                          avatar={<LocalShippingIcon color="error" />}
                        />
                        <CardContent>
                          <List>
                            {riskAssessment.affected_suppliers.map((supplier, idx) => (
                              <ListItem key={idx} sx={{ borderLeft: '3px solid', borderColor: 'error.main', mb: 1, bgcolor: '#ffebee' }}>
                                <ListItemIcon>
                                  <ErrorIcon color="error" />
                                </ListItemIcon>
                                <ListItemText 
                                  primary={supplier.supplier_name || `Supplier #${supplier.supplier_id}`}
                                  secondary={
                                    <Box>
                                      <Typography variant="body2">
                                        Reliability: {supplier.reliability || 'Unknown'}
                                      </Typography>
                                      <Typography variant="caption" color="text.secondary">
                                        {supplier.risks?.length || 0} risk(s) affecting this supplier
                                      </Typography>
                                    </Box>
                                  }
                                />
                              </ListItem>
                            ))}
                          </List>
                        </CardContent>
                      </Card>
                    </Grid>
                  )}
                </Grid>

                {/* AI Mitigation Strategies */}
                {riskAssessment.ai_mitigation && riskAssessment.ai_mitigation.priority_actions && (
                  <Card sx={{ bgcolor: '#f0f7ff', border: '2px solid #2196f3' }}>
                    <CardHeader
                      title="🤖 AI-Generated Mitigation Strategies"
                      subheader="Recommended actions to reduce risk exposure"
                      avatar={<AutoAwesomeIcon color="primary" />}
                    />
                    <CardContent>
                      {riskAssessment.ai_mitigation.priority_actions.length > 0 ? (
                        <List>
                          {riskAssessment.ai_mitigation.priority_actions.map((action, idx) => (
                            <ListItem key={idx} sx={{ pl: 0 }}>
                              <ListItemIcon>
                                <CheckCircleIcon color="primary" />
                              </ListItemIcon>
                              <ListItemText 
                                primary={action}
                                primaryTypographyProps={{ variant: 'body1' }}
                              />
                            </ListItem>
                          ))}
                        </List>
                      ) : (
                        <Typography variant="body2" color="text.secondary">
                          No specific mitigation strategies available
                        </Typography>
                      )}
                      {riskAssessment.ai_mitigation.contingency_plan && (
                        <>
                          <Divider sx={{ my: 2 }} />
                          <Typography variant="subtitle2" gutterBottom sx={{ fontWeight: 'bold' }}>
                            Contingency Plan:
                          </Typography>
                          <Typography variant="body2" color="text.secondary">
                            {riskAssessment.ai_mitigation.contingency_plan}
                          </Typography>
                        </>
                      )}
                    </CardContent>
                  </Card>
                )}

                {/* Risk Breakdown by Type */}
                {riskAssessment.risks && riskAssessment.risks.length > 0 && (
                  <Card elevation={3} sx={{ mb: 3 }}>
                    <CardHeader 
                      title="Risk Breakdown by Type"
                      avatar={<AssessmentIcon />}
                    />
                    <CardContent>
                      <Grid container spacing={2}>
                        {(() => {
                          const breakdown = {};
                          riskAssessment.risks.forEach(risk => {
                            const type = risk.risk_type || 'unknown';
                            breakdown[type] = (breakdown[type] || 0) + 1;
                          });
                          return Object.entries(breakdown).map(([type, count]) => {
                            const icons = {
                              weather: <CloudIcon />,
                              logistics: <LocalShippingIcon />,
                              market: <TrendingUpIcon />,
                              labor: <InfoIcon />,
                              regulatory: <WarningIcon />,
                              geopolitical: <WarningIcon />
                            };
                            return (
                              <Grid item xs={6} sm={4} md={3} key={type}>
                                <Paper 
                                  elevation={2}
                                  sx={{ 
                                    p: 2, 
                                    textAlign: 'center',
                                    border: '2px solid',
                                    borderColor: 'primary.light',
                                    '&:hover': { bgcolor: 'action.hover' }
                                  }}
                                >
                                  <Box sx={{ mb: 1 }}>
                                    {icons[type.toLowerCase()] || <InfoIcon />}
                                  </Box>
                                  <Typography variant="h4" color="primary">
                                    {count}
                                  </Typography>
                                  <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
                                    {type.charAt(0).toUpperCase() + type.slice(1)} Risks
                                  </Typography>
                                </Paper>
                              </Grid>
                            );
                          });
                        })()}
                      </Grid>
                    </CardContent>
                  </Card>
                )}
              </Box>
            )}

            {!riskAssessment && (
              <Alert severity="info" icon={<InfoIcon />}>
                Click "Run AI Risk Assessment" to analyze your supply chain risks and get AI-powered mitigation strategies.
              </Alert>
            )}
          </Paper>
        </Box>
      )}

      {/* Risk Registry Tab */}
      {activeTab === 1 && (
        <Box>
          {/* Filters */}
          <Paper sx={{ p: 2, mb: 3 }}>
            <Typography variant="subtitle1" gutterBottom>
              Filter Risks
            </Typography>
            <Grid container spacing={2}>
              <Grid item xs={12} sm={6} md={3}>
                <TextField
                  select
                  label="Risk Type"
                  fullWidth
                  value={filters.risk_type}
                  onChange={(e) => handleFilterChange('risk_type', e.target.value)}
                >
                  <MenuItem value="">All Types</MenuItem>
                  <MenuItem value="weather">Weather</MenuItem>
                  <MenuItem value="logistics">Logistics</MenuItem>
                  <MenuItem value="market">Market</MenuItem>
                  <MenuItem value="labor">Labor</MenuItem>
                  <MenuItem value="regulatory">Regulatory</MenuItem>
                </TextField>
              </Grid>
              <Grid item xs={12} sm={6} md={3}>
                <TextField
                  select
                  label="Region"
                  fullWidth
                  value={filters.region}
                  onChange={(e) => handleFilterChange('region', e.target.value)}
                >
                  <MenuItem value="">All Regions</MenuItem>
                  <MenuItem value="Global">Global</MenuItem>
                  <MenuItem value="Asia Pacific">Asia Pacific</MenuItem>
                  <MenuItem value="Southeast Asia">Southeast Asia</MenuItem>
                  <MenuItem value="North America">North America</MenuItem>
                  <MenuItem value="Europe">Europe</MenuItem>
                </TextField>
              </Grid>
            </Grid>
          </Paper>

          {/* Risks Table */}
          <Paper sx={{ height: 500, width: '100%' }}>
            {loading ? (
              <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100%' }}>
                <CircularProgress />
              </Box>
            ) : data.length === 0 ? (
              <Box sx={{ display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center', height: '100%', p: 3 }}>
                <InfoIcon sx={{ fontSize: 48, color: 'text.secondary', mb: 2 }} />
                <Typography variant="h6" color="text.secondary">
                  No risks found
                </Typography>
                <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
                  {filters.risk_type || filters.region 
                    ? 'Try adjusting your filters or add a new risk'
                    : 'Click "Add Risk" to create a new risk entry'}
                </Typography>
              </Box>
            ) : (
              <DataGrid
                rows={data}
                columns={columns}
                pageSize={10}
                rowsPerPageOptions={[10, 25, 50]}
                checkboxSelection
                disableSelectionOnClick
              />
            )}
          </Paper>
        </Box>
      )}

      {/* Create Risk Dialog */}
      <Dialog open={openDialog} onClose={handleDialogClose} maxWidth="md" fullWidth>
        <DialogTitle>Add New Risk</DialogTitle>
        <Box component="form" onSubmit={handleRiskSubmit}>
          <DialogContent>
            <Grid container spacing={2}>
              <Grid item xs={12} sm={6}>
                <TextField
                  select
                  name="risk_type"
                  label="Risk Type"
                  fullWidth
                  required
                  defaultValue=""
                >
                  <MenuItem value="weather">Weather</MenuItem>
                  <MenuItem value="logistics">Logistics</MenuItem>
                  <MenuItem value="market">Market</MenuItem>
                  <MenuItem value="labor">Labor</MenuItem>
                  <MenuItem value="regulatory">Regulatory</MenuItem>
                </TextField>
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  select
                  name="risk_level"
                  label="Risk Level"
                  fullWidth
                  required
                  defaultValue="MEDIUM"
                >
                  <MenuItem value="LOW">Low</MenuItem>
                  <MenuItem value="MEDIUM">Medium</MenuItem>
                  <MenuItem value="HIGH">High</MenuItem>
                  <MenuItem value="CRITICAL">Critical</MenuItem>
                </TextField>
              </Grid>
              <Grid item xs={12}>
                <TextField
                  name="region"
                  label="Region"
                  fullWidth
                  required
                  placeholder="e.g., Asia Pacific, North America"
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  name="description"
                  label="Description"
                  fullWidth
                  required
                  multiline
                  rows={4}
                  placeholder="Describe the risk factor..."
                />
              </Grid>
            </Grid>
          </DialogContent>
          <DialogActions>
            <Button onClick={handleDialogClose}>Cancel</Button>
            <Button type="submit" variant="contained">
              Create
            </Button>
          </DialogActions>
        </Box>
      </Dialog>
    </Box>
  );
}
