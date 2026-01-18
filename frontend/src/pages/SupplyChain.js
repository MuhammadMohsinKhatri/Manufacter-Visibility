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
  Divider,
  TextField,
  MenuItem,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions
} from '@mui/material';
import { DataGrid } from '@mui/x-data-grid';
import { format } from 'date-fns';

// Icons
import WarningIcon from '@mui/icons-material/Warning';
import UpdateIcon from '@mui/icons-material/Update';
import AddIcon from '@mui/icons-material/Add';

// Services
import { supplyChainService } from '../services';

// Notification context
import { useNotification } from '../context/NotificationContext';

export default function SupplyChain() {
  const [loading, setLoading] = useState(true);
  const [risks, setRisks] = useState([]);
  const [error, setError] = useState(null);
  const [openDialog, setOpenDialog] = useState(false);
  const [filters, setFilters] = useState({
    risk_type: '',
    region: ''
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

  // For demo purposes, we'll use simulated data
  const simulatedRisks = [
    { 
      id: 1, 
      risk_type: 'weather', 
      region: 'Southeast Asia', 
      description: 'Tropical storm approaching manufacturing hubs',
      risk_level: 'HIGH',
      detected_date: '2026-01-15T08:00:00Z',
      source: 'weather_api'
    },
    { 
      id: 2, 
      risk_type: 'logistics', 
      region: 'Asia Pacific', 
      description: 'Port congestion at Shanghai port',
      risk_level: 'MEDIUM',
      detected_date: '2026-01-14T10:00:00Z',
      source: 'logistics_api'
    },
    { 
      id: 3, 
      risk_type: 'market', 
      region: 'Global', 
      description: 'Semiconductor shortage affecting electronics supply',
      risk_level: 'CRITICAL',
      detected_date: '2026-01-10T12:00:00Z',
      source: 'market_api'
    },
    { 
      id: 4, 
      risk_type: 'labor', 
      region: 'North America', 
      description: 'Potential strike at major supplier facility',
      risk_level: 'MEDIUM',
      detected_date: '2026-01-16T09:00:00Z',
      source: 'labor_api'
    }
  ];

  // Use simulated data for the demo
  const data = risks.length > 0 ? risks : simulatedRisks;

  const getRiskLevelColor = (level) => {
    switch (level) {
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

  const riskLevelCounts = {
    CRITICAL: data.filter(r => r.risk_level === 'CRITICAL').length,
    HIGH: data.filter(r => r.risk_level === 'HIGH').length,
    MEDIUM: data.filter(r => r.risk_level === 'MEDIUM').length,
    LOW: data.filter(r => r.risk_level === 'LOW').length
  };

  const columns = [
    { field: 'id', headerName: 'ID', width: 80 },
    { 
      field: 'risk_type', 
      headerName: 'Type', 
      width: 150,
      valueFormatter: (params) => params.value?.charAt(0).toUpperCase() + params.value?.slice(1) || 'N/A'
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
          label={params.value} 
          color={getRiskLevelColor(params.value)} 
          size="small" 
        />
      )
    },
    { 
      field: 'detected_date', 
      headerName: 'Detected', 
      width: 180,
      valueFormatter: (params) => params.value ? format(new Date(params.value), 'MM/dd/yyyy HH:mm') : 'N/A'
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
            Update Risks
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
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      {/* Summary Cards */}
      <Grid container spacing={3} sx={{ mb: 3 }}>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardHeader 
              title="Critical" 
              titleTypographyProps={{ color: 'error' }}
              avatar={<WarningIcon color="error" />}
            />
            <CardContent>
              <Typography variant="h3" align="center" color="error">
                {riskLevelCounts.CRITICAL}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardHeader 
              title="High" 
              titleTypographyProps={{ color: 'error' }}
              avatar={<WarningIcon color="error" />}
            />
            <CardContent>
              <Typography variant="h3" align="center" color="error">
                {riskLevelCounts.HIGH}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardHeader 
              title="Medium" 
              titleTypographyProps={{ color: 'warning.main' }}
            />
            <CardContent>
              <Typography variant="h3" align="center" color="warning.main">
                {riskLevelCounts.MEDIUM}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardHeader title="Low" />
            <CardContent>
              <Typography variant="h3" align="center">
                {riskLevelCounts.LOW}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Filters */}
      <Paper sx={{ p: 2, mb: 3 }}>
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

