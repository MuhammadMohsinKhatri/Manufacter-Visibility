import React, { useState, useEffect } from 'react';
import { 
  Box, 
  Typography, 
  Paper, 
  Grid, 
  Card, 
  CardContent, 
  CardHeader, 
  Button, 
  CircularProgress,
  Alert,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  MenuItem,
  IconButton,
  Tooltip,
  Chip,
  Tabs,
  Tab
} from '@mui/material';
import { DataGrid } from '@mui/x-data-grid';
import { DateTimePicker } from '@mui/x-date-pickers/DateTimePicker';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import { format, addDays, differenceInHours } from 'date-fns';

// Icons
import AddIcon from '@mui/icons-material/Add';
import EditIcon from '@mui/icons-material/Edit';
import PlayArrowIcon from '@mui/icons-material/PlayArrow';
import StopIcon from '@mui/icons-material/Stop';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import EventBusyIcon from '@mui/icons-material/EventBusy';

// Services
import { productionService } from '../services';

// Notification context
import { useNotification } from '../context/NotificationContext';

// Tab panel component
function TabPanel(props) {
  const { children, value, index, ...other } = props;

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`production-tabpanel-${index}`}
      aria-labelledby={`production-tab-${index}`}
      {...other}
    >
      {value === index && (
        <Box sx={{ p: 3 }}>
          {children}
        </Box>
      )}
    </div>
  );
}

export default function Production() {
  const [tabValue, setTabValue] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [productionLines, setProductionLines] = useState([]);
  const [productionSchedules, setProductionSchedules] = useState([]);
  const [openDialog, setOpenDialog] = useState(false);
  const [dialogType, setDialogType] = useState('line'); // 'line' or 'schedule'
  const [selectedItem, setSelectedItem] = useState(null);
  
  const { showSuccess, showError } = useNotification();

  useEffect(() => {
    fetchProductionData();
  }, []);

  const fetchProductionData = async () => {
    try {
      setLoading(true);
      
      // In a real app, these would be API calls
      // For the demo, we'll use simulated data
      
      // Fetch production lines and schedules
      // const linesData = await productionService.getProductionLines();
      // const schedulesData = await productionService.getProductionSchedules();
      
      // Simulated data
      const simulatedProductionLines = [
        { 
          id: 1, 
          name: 'Assembly Line A', 
          description: 'Main assembly line for large products',
          capacity_per_hour: 5,
          is_active: true
        },
        { 
          id: 2, 
          name: 'Assembly Line B', 
          description: 'Secondary assembly line for medium products',
          capacity_per_hour: 8,
          is_active: true
        },
        { 
          id: 3, 
          name: 'Electronics Line', 
          description: 'Specialized line for electronic components',
          capacity_per_hour: 12,
          is_active: true
        },
        { 
          id: 4, 
          name: 'Testing Line', 
          description: 'Quality control and testing',
          capacity_per_hour: 15,
          is_active: true
        },
        { 
          id: 5, 
          name: 'Packaging Line', 
          description: 'Final packaging and preparation',
          capacity_per_hour: 20,
          is_active: true
        }
      ];
      
      const now = new Date();
      
      const simulatedSchedules = [
        { 
          id: 1, 
          order_id: 1,
          production_line: simulatedProductionLines[0],
          production_line_id: 1,
          scheduled_start: new Date(now.getTime() - 10 * 24 * 60 * 60 * 1000).toISOString(),
          scheduled_end: new Date(now.getTime() - 5 * 24 * 60 * 60 * 1000).toISOString(),
          actual_start: new Date(now.getTime() - 10 * 24 * 60 * 60 * 1000).toISOString(),
          actual_end: new Date(now.getTime() - 6 * 24 * 60 * 60 * 1000).toISOString(),
          status: 'completed',
          notes: 'Completed ahead of schedule'
        },
        { 
          id: 2, 
          order_id: 2,
          production_line: simulatedProductionLines[2],
          production_line_id: 3,
          scheduled_start: new Date(now.getTime() - 5 * 24 * 60 * 60 * 1000).toISOString(),
          scheduled_end: new Date(now.getTime() - 1 * 24 * 60 * 60 * 1000).toISOString(),
          actual_start: new Date(now.getTime() - 5 * 24 * 60 * 60 * 1000).toISOString(),
          actual_end: new Date(now.getTime() - 1 * 24 * 60 * 60 * 1000).toISOString(),
          status: 'completed',
          notes: 'Completed on schedule'
        },
        { 
          id: 3, 
          order_id: 3,
          production_line: simulatedProductionLines[0],
          production_line_id: 1,
          scheduled_start: new Date(now.getTime() - 1 * 24 * 60 * 60 * 1000).toISOString(),
          scheduled_end: new Date(now.getTime() + 5 * 24 * 60 * 60 * 1000).toISOString(),
          actual_start: new Date(now.getTime() - 1 * 24 * 60 * 60 * 1000).toISOString(),
          actual_end: null,
          status: 'in_progress',
          notes: 'Production proceeding normally'
        },
        { 
          id: 4, 
          order_id: 4,
          production_line: simulatedProductionLines[1],
          production_line_id: 2,
          scheduled_start: new Date(now.getTime() + 5 * 24 * 60 * 60 * 1000).toISOString(),
          scheduled_end: new Date(now.getTime() + 10 * 24 * 60 * 60 * 1000).toISOString(),
          actual_start: null,
          actual_end: null,
          status: 'scheduled',
          notes: 'Awaiting start'
        },
        { 
          id: 5, 
          order_id: 5,
          production_line: simulatedProductionLines[3],
          production_line_id: 4,
          scheduled_start: new Date(now.getTime() + 7 * 24 * 60 * 60 * 1000).toISOString(),
          scheduled_end: new Date(now.getTime() + 12 * 24 * 60 * 60 * 1000).toISOString(),
          actual_start: null,
          actual_end: null,
          status: 'scheduled',
          notes: 'Materials on order'
        }
      ];
      
      setProductionLines(simulatedProductionLines);
      setProductionSchedules(simulatedSchedules);
    } catch (err) {
      console.error('Error fetching production data:', err);
      setError('Failed to load production data. Please try again later.');
      showError('Failed to load production data');
    } finally {
      setLoading(false);
    }
  };

  const handleTabChange = (event, newValue) => {
    setTabValue(newValue);
  };

  const handleOpenDialog = (type, item = null) => {
    setDialogType(type);
    setSelectedItem(item);
    setOpenDialog(true);
  };

  const handleCloseDialog = () => {
    setOpenDialog(false);
    setSelectedItem(null);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    const formData = new FormData(event.target);
    
    try {
      if (dialogType === 'line') {
        if (selectedItem) {
          // Update production line - not implemented in demo
          showSuccess('Production line updated successfully');
        } else {
          // Create new production line
          const lineData = {
            name: formData.get('name'),
            description: formData.get('description'),
            capacity_per_hour: parseInt(formData.get('capacity_per_hour')),
            is_active: true
          };
          
          // In a real app, call API
          // await productionService.createProductionLine(lineData);
          showSuccess('Production line created successfully');
        }
      } else {
        // Production schedule
        if (selectedItem) {
          // Update production schedule
          const scheduleData = {
            scheduled_start: formData.get('scheduled_start'),
            scheduled_end: formData.get('scheduled_end'),
            status: formData.get('status'),
            notes: formData.get('notes')
          };
          
          // Add actual times if provided
          if (formData.get('actual_start')) {
            scheduleData.actual_start = formData.get('actual_start');
          }
          
          if (formData.get('actual_end')) {
            scheduleData.actual_end = formData.get('actual_end');
          }
          
          // In a real app, call API
          // await productionService.updateProductionSchedule(selectedItem.id, scheduleData);
          showSuccess('Production schedule updated successfully');
        } else {
          // Create new production schedule
          const scheduleData = {
            order_id: parseInt(formData.get('order_id')),
            production_line_id: parseInt(formData.get('production_line_id')),
            scheduled_start: formData.get('scheduled_start'),
            scheduled_end: formData.get('scheduled_end'),
            status: 'scheduled',
            notes: formData.get('notes')
          };
          
          // In a real app, call API
          // await productionService.createProductionSchedule(scheduleData);
          showSuccess('Production schedule created successfully');
        }
      }
      
      handleCloseDialog();
      fetchProductionData();
    } catch (err) {
      console.error('Error saving data:', err);
      showError('Failed to save data');
    }
  };

  const handleStartProduction = (schedule) => {
    // In a real app, call API to update schedule
    showSuccess(`Production started for Order #${schedule.order_id}`);
    fetchProductionData();
  };

  const handleCompleteProduction = (schedule) => {
    // In a real app, call API to update schedule
    showSuccess(`Production completed for Order #${schedule.order_id}`);
    fetchProductionData();
  };

  // DataGrid columns for production lines
  const lineColumns = [
    { field: 'id', headerName: 'ID', width: 70 },
    { field: 'name', headerName: 'Name', width: 200 },
    { field: 'description', headerName: 'Description', width: 300 },
    { field: 'capacity_per_hour', headerName: 'Capacity (units/hr)', width: 150 },
    { 
      field: 'is_active', 
      headerName: 'Status', 
      width: 120,
      renderCell: (params) => (
        <Chip 
          label={params.value ? 'Active' : 'Inactive'} 
          color={params.value ? 'success' : 'default'} 
          size="small" 
        />
      )
    },
    {
      field: 'actions',
      headerName: 'Actions',
      width: 100,
      sortable: false,
      renderCell: (params) => (
        <Box>
          <Tooltip title="Edit">
            <IconButton 
              size="small" 
              onClick={() => handleOpenDialog('line', params.row)}
            >
              <EditIcon fontSize="small" />
            </IconButton>
          </Tooltip>
        </Box>
      )
    }
  ];

  // DataGrid columns for production schedules
  const scheduleColumns = [
    { field: 'id', headerName: 'ID', width: 70 },
    { 
      field: 'order_id', 
      headerName: 'Order ID', 
      width: 100 
    },
    { 
      field: 'production_line', 
      headerName: 'Production Line', 
      width: 180,
      valueGetter: (params) => params.row.production_line?.name || 'Unknown'
    },
    { 
      field: 'scheduled_start', 
      headerName: 'Scheduled Start', 
      width: 180,
      valueFormatter: (params) => format(new Date(params.value), 'MM/dd/yyyy HH:mm')
    },
    { 
      field: 'scheduled_end', 
      headerName: 'Scheduled End', 
      width: 180,
      valueFormatter: (params) => format(new Date(params.value), 'MM/dd/yyyy HH:mm')
    },
    { 
      field: 'status', 
      headerName: 'Status', 
      width: 130,
      renderCell: (params) => {
        const status = params.value;
        let color, icon;
        
        switch (status) {
          case 'scheduled':
            color = 'primary';
            icon = <EventBusyIcon />;
            break;
          case 'in_progress':
            color = 'warning';
            icon = <PlayArrowIcon />;
            break;
          case 'completed':
            color = 'success';
            icon = <CheckCircleIcon />;
            break;
          default:
            color = 'default';
            icon = null;
        }
        
        return (
          <Chip 
            label={status} 
            color={color} 
            size="small"
            icon={icon}
          />
        );
      }
    },
    {
      field: 'actions',
      headerName: 'Actions',
      width: 180,
      sortable: false,
      renderCell: (params) => (
        <Box>
          <Tooltip title="Edit">
            <IconButton 
              size="small" 
              onClick={() => handleOpenDialog('schedule', params.row)}
            >
              <EditIcon fontSize="small" />
            </IconButton>
          </Tooltip>
          
          {params.row.status === 'scheduled' && (
            <Tooltip title="Start Production">
              <IconButton 
                size="small" 
                color="primary"
                onClick={() => handleStartProduction(params.row)}
              >
                <PlayArrowIcon fontSize="small" />
              </IconButton>
            </Tooltip>
          )}
          
          {params.row.status === 'in_progress' && (
            <Tooltip title="Complete Production">
              <IconButton 
                size="small" 
                color="success"
                onClick={() => handleCompleteProduction(params.row)}
              >
                <StopIcon fontSize="small" />
              </IconButton>
            </Tooltip>
          )}
        </Box>
      )
    }
  ];

  // Calculate production metrics
  const activeLines = productionLines.filter(line => line.is_active).length;
  const inProgressSchedules = productionSchedules.filter(schedule => schedule.status === 'in_progress').length;
  const completedSchedules = productionSchedules.filter(schedule => schedule.status === 'completed').length;
  const upcomingSchedules = productionSchedules.filter(schedule => schedule.status === 'scheduled').length;

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '80vh' }}>
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Production Management
      </Typography>
      
      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}
      
      <Grid container spacing={3}>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardHeader 
              title="Active Lines" 
              titleTypographyProps={{ variant: 'h6' }}
            />
            <CardContent>
              <Typography variant="h3" align="center">
                {activeLines} / {productionLines.length}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardHeader 
              title="In Progress" 
              titleTypographyProps={{ variant: 'h6' }}
              avatar={inProgressSchedules > 0 ? <PlayArrowIcon color="warning" /> : null}
            />
            <CardContent>
              <Typography 
                variant="h3" 
                align="center"
                color={inProgressSchedules > 0 ? 'warning.main' : 'inherit'}
              >
                {inProgressSchedules}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardHeader 
              title="Completed" 
              titleTypographyProps={{ variant: 'h6' }}
              avatar={<CheckCircleIcon color="success" />}
            />
            <CardContent>
              <Typography variant="h3" align="center" color="success.main">
                {completedSchedules}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardHeader 
              title="Upcoming" 
              titleTypographyProps={{ variant: 'h6' }}
              avatar={<EventBusyIcon color="primary" />}
            />
            <CardContent>
              <Typography variant="h3" align="center" color="primary.main">
                {upcomingSchedules}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
      
      <Paper sx={{ mt: 3 }}>
        <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
          <Tabs value={tabValue} onChange={handleTabChange} aria-label="production tabs">
            <Tab label="Production Schedules" id="production-tab-0" />
            <Tab label="Production Lines" id="production-tab-1" />
          </Tabs>
        </Box>
        
        <TabPanel value={tabValue} index={0}>
          <Box sx={{ display: 'flex', justifyContent: 'flex-end', mb: 2 }}>
            <Button
              variant="contained"
              startIcon={<AddIcon />}
              onClick={() => handleOpenDialog('schedule')}
            >
              Add Production Schedule
            </Button>
          </Box>
          
          <div style={{ height: 500, width: '100%' }}>
            <DataGrid
              rows={productionSchedules}
              columns={scheduleColumns}
              pageSize={10}
              rowsPerPageOptions={[10, 25, 50]}
              disableSelectionOnClick
            />
          </div>
        </TabPanel>
        
        <TabPanel value={tabValue} index={1}>
          <Box sx={{ display: 'flex', justifyContent: 'flex-end', mb: 2 }}>
            <Button
              variant="contained"
              startIcon={<AddIcon />}
              onClick={() => handleOpenDialog('line')}
            >
              Add Production Line
            </Button>
          </Box>
          
          <div style={{ height: 500, width: '100%' }}>
            <DataGrid
              rows={productionLines}
              columns={lineColumns}
              pageSize={10}
              rowsPerPageOptions={[10, 25, 50]}
              disableSelectionOnClick
            />
          </div>
        </TabPanel>
      </Paper>
      
      {/* Dialog for adding/editing production lines or schedules */}
      <Dialog open={openDialog} onClose={handleCloseDialog} maxWidth="md" fullWidth>
        <DialogTitle>
          {selectedItem 
            ? `Edit ${dialogType === 'line' ? 'Production Line' : 'Production Schedule'}`
            : `Add New ${dialogType === 'line' ? 'Production Line' : 'Production Schedule'}`
          }
        </DialogTitle>
        <Box component="form" onSubmit={handleSubmit}>
          <DialogContent>
            {dialogType === 'line' ? (
              // Production Line form
              <Grid container spacing={2}>
                <Grid item xs={12}>
                  <TextField
                    name="name"
                    label="Line Name"
                    fullWidth
                    required
                    defaultValue={selectedItem?.name || ''}
                  />
                </Grid>
                <Grid item xs={12}>
                  <TextField
                    name="description"
                    label="Description"
                    fullWidth
                    multiline
                    rows={2}
                    defaultValue={selectedItem?.description || ''}
                  />
                </Grid>
                <Grid item xs={12}>
                  <TextField
                    name="capacity_per_hour"
                    label="Capacity (units/hour)"
                    type="number"
                    fullWidth
                    required
                    defaultValue={selectedItem?.capacity_per_hour || 1}
                    InputProps={{ inputProps: { min: 1 } }}
                  />
                </Grid>
              </Grid>
            ) : (
              // Production Schedule form
              <LocalizationProvider dateAdapter={AdapterDateFns}>
                <Grid container spacing={2}>
                  {!selectedItem && (
                    <>
                      <Grid item xs={12} sm={6}>
                        <TextField
                          select
                          name="order_id"
                          label="Order"
                          fullWidth
                          required
                          defaultValue={selectedItem?.order_id || ''}
                        >
                          <MenuItem value="1">Order #1 - Acme Corporation</MenuItem>
                          <MenuItem value="2">Order #2 - Globex Industries</MenuItem>
                          <MenuItem value="3">Order #3 - Initech Systems</MenuItem>
                          <MenuItem value="4">Order #4 - Umbrella Corporation</MenuItem>
                          <MenuItem value="5">Order #5 - Stark Industries</MenuItem>
                        </TextField>
                      </Grid>
                      <Grid item xs={12} sm={6}>
                        <TextField
                          select
                          name="production_line_id"
                          label="Production Line"
                          fullWidth
                          required
                          defaultValue={selectedItem?.production_line_id || ''}
                        >
                          {productionLines.map((line) => (
                            <MenuItem key={line.id} value={line.id}>
                              {line.name} ({line.capacity_per_hour} units/hour)
                            </MenuItem>
                          ))}
                        </TextField>
                      </Grid>
                    </>
                  )}
                  <Grid item xs={12} sm={6}>
                    <DateTimePicker
                      label="Scheduled Start"
                      name="scheduled_start"
                      value={selectedItem ? new Date(selectedItem.scheduled_start) : new Date()}
                      onChange={() => {}}
                      renderInput={(params) => <TextField {...params} fullWidth required />}
                    />
                  </Grid>
                  <Grid item xs={12} sm={6}>
                    <DateTimePicker
                      label="Scheduled End"
                      name="scheduled_end"
                      value={selectedItem ? new Date(selectedItem.scheduled_end) : addDays(new Date(), 5)}
                      onChange={() => {}}
                      renderInput={(params) => <TextField {...params} fullWidth required />}
                    />
                  </Grid>
                  {selectedItem && (
                    <>
                      <Grid item xs={12} sm={6}>
                        <DateTimePicker
                          label="Actual Start"
                          name="actual_start"
                          value={selectedItem.actual_start ? new Date(selectedItem.actual_start) : null}
                          onChange={() => {}}
                          renderInput={(params) => <TextField {...params} fullWidth />}
                        />
                      </Grid>
                      <Grid item xs={12} sm={6}>
                        <DateTimePicker
                          label="Actual End"
                          name="actual_end"
                          value={selectedItem.actual_end ? new Date(selectedItem.actual_end) : null}
                          onChange={() => {}}
                          renderInput={(params) => <TextField {...params} fullWidth />}
                        />
                      </Grid>
                      <Grid item xs={12}>
                        <TextField
                          select
                          name="status"
                          label="Status"
                          fullWidth
                          required
                          defaultValue={selectedItem?.status || 'scheduled'}
                        >
                          <MenuItem value="scheduled">Scheduled</MenuItem>
                          <MenuItem value="in_progress">In Progress</MenuItem>
                          <MenuItem value="completed">Completed</MenuItem>
                        </TextField>
                      </Grid>
                    </>
                  )}
                  <Grid item xs={12}>
                    <TextField
                      name="notes"
                      label="Notes"
                      fullWidth
                      multiline
                      rows={3}
                      defaultValue={selectedItem?.notes || ''}
                    />
                  </Grid>
                </Grid>
              </LocalizationProvider>
            )}
          </DialogContent>
          <DialogActions>
            <Button onClick={handleCloseDialog}>Cancel</Button>
            <Button type="submit" variant="contained">
              {selectedItem ? 'Update' : 'Create'}
            </Button>
          </DialogActions>
        </Box>
      </Dialog>
    </Box>
  );
}