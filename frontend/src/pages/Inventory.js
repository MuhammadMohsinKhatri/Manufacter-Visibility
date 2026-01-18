import React, { useState, useEffect } from 'react';
import { 
  Box, 
  Typography, 
  Paper, 
  Tabs, 
  Tab, 
  Button, 
  CircularProgress,
  Alert,
  Grid,
  Card,
  CardContent,
  CardHeader,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  MenuItem,
  IconButton,
  Tooltip,
  Chip
} from '@mui/material';
import { DataGrid } from '@mui/x-data-grid';

// Icons
import AddIcon from '@mui/icons-material/Add';
import EditIcon from '@mui/icons-material/Edit';
import WarningIcon from '@mui/icons-material/Warning';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import LocalShippingIcon from '@mui/icons-material/LocalShipping';

// Services
import { inventoryService } from '../services';

// Notification context
import { useNotification } from '../context/NotificationContext';

// Tab panel component
function TabPanel(props) {
  const { children, value, index, ...other } = props;

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`inventory-tabpanel-${index}`}
      aria-labelledby={`inventory-tab-${index}`}
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

export default function Inventory() {
  const [tabValue, setTabValue] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [inventoryItems, setInventoryItems] = useState([]);
  const [components, setComponents] = useState([]);
  const [lowStockItems, setLowStockItems] = useState([]);
  const [openDialog, setOpenDialog] = useState(false);
  const [dialogType, setDialogType] = useState('component'); // 'component' or 'inventory'
  const [selectedItem, setSelectedItem] = useState(null);
  
  const { showSuccess, showError } = useNotification();

  useEffect(() => {
    fetchInventoryData();
  }, []);

  const fetchInventoryData = async () => {
    try {
      setLoading(true);
      
      // In a real app, these would be API calls
      // For the demo, we'll use simulated data
      
      // Fetch inventory items
      // const inventoryData = await inventoryService.getInventoryItems();
      // const componentsData = await inventoryService.getComponents();
      // const lowStockData = await inventoryService.getLowStockItems();
      
      // Simulated data
      const simulatedInventoryItems = [
        { 
          id: 1, 
          component: { id: 1, name: 'Steel Frame', sku: 'SF-001' },
          quantity_available: 50, 
          quantity_allocated: 20, 
          reorder_threshold: 30,
          location: 'Warehouse A, Aisle 3, Shelf 12'
        },
        { 
          id: 2, 
          component: { id: 2, name: 'Rubber Gasket', sku: 'RG-002' },
          quantity_available: 120, 
          quantity_allocated: 30, 
          reorder_threshold: 50,
          location: 'Warehouse A, Aisle 5, Shelf 8'
        },
        { 
          id: 3, 
          component: { id: 3, name: 'Circuit Board', sku: 'CB-003' },
          quantity_available: 5, 
          quantity_allocated: 10, 
          reorder_threshold: 20,
          location: 'Warehouse B, Aisle 1, Shelf 3'
        },
        { 
          id: 4, 
          component: { id: 4, name: 'Power Supply', sku: 'PS-004' },
          quantity_available: 8, 
          quantity_allocated: 5, 
          reorder_threshold: 15,
          location: 'Warehouse B, Aisle 1, Shelf 5'
        },
        { 
          id: 5, 
          component: { id: 5, name: 'LCD Display', sku: 'LCD-005' },
          quantity_available: 3, 
          quantity_allocated: 2, 
          reorder_threshold: 10,
          location: 'Warehouse B, Aisle 2, Shelf 1'
        },
        { 
          id: 6, 
          component: { id: 6, name: 'Aluminum Housing', sku: 'AH-006' },
          quantity_available: 25, 
          quantity_allocated: 15, 
          reorder_threshold: 20,
          location: 'Warehouse A, Aisle 4, Shelf 10'
        },
        { 
          id: 7, 
          component: { id: 7, name: 'Cooling Fan', sku: 'CF-007' },
          quantity_available: 35, 
          quantity_allocated: 10, 
          reorder_threshold: 20,
          location: 'Warehouse B, Aisle 3, Shelf 7'
        },
        { 
          id: 8, 
          component: { id: 8, name: 'Wiring Harness', sku: 'WH-008' },
          quantity_available: 40, 
          quantity_allocated: 15, 
          reorder_threshold: 25,
          location: 'Warehouse B, Aisle 3, Shelf 9'
        },
        { 
          id: 9, 
          component: { id: 9, name: 'Mounting Bracket', sku: 'MB-009' },
          quantity_available: 60, 
          quantity_allocated: 20, 
          reorder_threshold: 30,
          location: 'Warehouse A, Aisle 2, Shelf 15'
        },
        { 
          id: 10, 
          component: { id: 10, name: 'Sensor Array', sku: 'SA-010' },
          quantity_available: 15, 
          quantity_allocated: 5, 
          reorder_threshold: 10,
          location: 'Warehouse B, Aisle 2, Shelf 4'
        }
      ];
      
      const simulatedComponents = simulatedInventoryItems.map(item => item.component);
      
      const simulatedLowStockItems = simulatedInventoryItems.filter(
        item => item.quantity_available <= item.reorder_threshold
      );
      
      setInventoryItems(simulatedInventoryItems);
      setComponents(simulatedComponents);
      setLowStockItems(simulatedLowStockItems);
    } catch (err) {
      console.error('Error fetching inventory data:', err);
      setError('Failed to load inventory data. Please try again later.');
      showError('Failed to load inventory data');
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
      if (dialogType === 'component') {
        if (selectedItem) {
          // Update component - not implemented in demo
          showSuccess('Component updated successfully');
        } else {
          // Create new component
          const componentData = {
            name: formData.get('name'),
            description: formData.get('description'),
            sku: formData.get('sku')
          };
          
          // In a real app, call API
          // await inventoryService.createComponent(componentData);
          showSuccess('Component created successfully');
        }
      } else {
        // Inventory item
        if (selectedItem) {
          // Update inventory item
          const inventoryData = {
            quantity_available: parseInt(formData.get('quantity_available')),
            quantity_allocated: parseInt(formData.get('quantity_allocated')),
            reorder_threshold: parseInt(formData.get('reorder_threshold')),
            location: formData.get('location')
          };
          
          // In a real app, call API
          // await inventoryService.updateInventoryItem(selectedItem.id, inventoryData);
          showSuccess('Inventory item updated successfully');
        } else {
          // Create new inventory item
          const inventoryData = {
            component_id: parseInt(formData.get('component_id')),
            quantity_available: parseInt(formData.get('quantity_available')),
            reorder_threshold: parseInt(formData.get('reorder_threshold')),
            location: formData.get('location')
          };
          
          // In a real app, call API
          // await inventoryService.createInventoryItem(inventoryData);
          showSuccess('Inventory item created successfully');
        }
      }
      
      handleCloseDialog();
      fetchInventoryData();
    } catch (err) {
      console.error('Error saving data:', err);
      showError('Failed to save data');
    }
  };

  // DataGrid columns for inventory items
  const inventoryColumns = [
    { 
      field: 'component', 
      headerName: 'Component', 
      width: 200,
      valueGetter: (params) => params.row.component?.name || 'Unknown'
    },
    { 
      field: 'sku', 
      headerName: 'SKU', 
      width: 120,
      valueGetter: (params) => params.row.component?.sku || 'N/A'
    },
    { field: 'quantity_available', headerName: 'Available', width: 120 },
    { field: 'quantity_allocated', headerName: 'Allocated', width: 120 },
    { field: 'reorder_threshold', headerName: 'Reorder Threshold', width: 150 },
    { field: 'location', headerName: 'Location', width: 250 },
    {
      field: 'status',
      headerName: 'Status',
      width: 120,
      renderCell: (params) => {
        const available = params.row.quantity_available;
        const threshold = params.row.reorder_threshold;
        
        if (available <= threshold) {
          return (
            <Chip 
              label="Low Stock" 
              color="error" 
              size="small" 
              icon={<WarningIcon />}
            />
          );
        } else {
          return (
            <Chip 
              label="In Stock" 
              color="success" 
              size="small" 
              icon={<CheckCircleIcon />}
            />
          );
        }
      }
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
              onClick={() => handleOpenDialog('inventory', params.row)}
            >
              <EditIcon fontSize="small" />
            </IconButton>
          </Tooltip>
        </Box>
      )
    }
  ];

  // DataGrid columns for components
  const componentColumns = [
    { field: 'id', headerName: 'ID', width: 70 },
    { field: 'name', headerName: 'Name', width: 200 },
    { field: 'sku', headerName: 'SKU', width: 150 },
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
              onClick={() => handleOpenDialog('component', params.row)}
            >
              <EditIcon fontSize="small" />
            </IconButton>
          </Tooltip>
        </Box>
      )
    }
  ];

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
        Inventory Management
      </Typography>
      
      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}
      
      <Grid container spacing={3}>
        <Grid item xs={12} md={4}>
          <Card>
            <CardHeader 
              title="Total Components" 
              titleTypographyProps={{ variant: 'h6' }}
            />
            <CardContent>
              <Typography variant="h3" align="center">
                {components.length}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} md={4}>
          <Card>
            <CardHeader 
              title="Low Stock Items" 
              titleTypographyProps={{ variant: 'h6' }}
              avatar={lowStockItems.length > 0 ? <WarningIcon color="error" /> : null}
            />
            <CardContent>
              <Typography 
                variant="h3" 
                align="center"
                color={lowStockItems.length > 0 ? 'error' : 'inherit'}
              >
                {lowStockItems.length}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} md={4}>
          <Card>
            <CardHeader 
              title="Incoming Shipments" 
              titleTypographyProps={{ variant: 'h6' }}
              avatar={<LocalShippingIcon color="primary" />}
            />
            <CardContent>
              <Typography variant="h3" align="center">
                3
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
      
      <Paper sx={{ mt: 3 }}>
        <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
          <Tabs value={tabValue} onChange={handleTabChange} aria-label="inventory tabs">
            <Tab label="Inventory Items" id="inventory-tab-0" />
            <Tab label="Components" id="inventory-tab-1" />
          </Tabs>
        </Box>
        
        <TabPanel value={tabValue} index={0}>
          <Box sx={{ display: 'flex', justifyContent: 'flex-end', mb: 2 }}>
            <Button
              variant="contained"
              startIcon={<AddIcon />}
              onClick={() => handleOpenDialog('inventory')}
            >
              Add Inventory Item
            </Button>
          </Box>
          
          <div style={{ height: 500, width: '100%' }}>
            <DataGrid
              rows={inventoryItems}
              columns={inventoryColumns}
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
              onClick={() => handleOpenDialog('component')}
            >
              Add Component
            </Button>
          </Box>
          
          <div style={{ height: 500, width: '100%' }}>
            <DataGrid
              rows={components}
              columns={componentColumns}
              pageSize={10}
              rowsPerPageOptions={[10, 25, 50]}
              disableSelectionOnClick
            />
          </div>
        </TabPanel>
      </Paper>
      
      {/* Dialog for adding/editing components or inventory items */}
      <Dialog open={openDialog} onClose={handleCloseDialog} maxWidth="sm" fullWidth>
        <DialogTitle>
          {selectedItem 
            ? `Edit ${dialogType === 'component' ? 'Component' : 'Inventory Item'}`
            : `Add New ${dialogType === 'component' ? 'Component' : 'Inventory Item'}`
          }
        </DialogTitle>
        <Box component="form" onSubmit={handleSubmit}>
          <DialogContent>
            {dialogType === 'component' ? (
              // Component form
              <Grid container spacing={2}>
                <Grid item xs={12}>
                  <TextField
                    name="name"
                    label="Component Name"
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
                    rows={3}
                    defaultValue={selectedItem?.description || ''}
                  />
                </Grid>
                <Grid item xs={12}>
                  <TextField
                    name="sku"
                    label="SKU"
                    fullWidth
                    required
                    defaultValue={selectedItem?.sku || ''}
                  />
                </Grid>
              </Grid>
            ) : (
              // Inventory item form
              <Grid container spacing={2}>
                {!selectedItem && (
                  <Grid item xs={12}>
                    <TextField
                      select
                      name="component_id"
                      label="Component"
                      fullWidth
                      required
                      defaultValue={selectedItem?.component?.id || ''}
                    >
                      {components.map((component) => (
                        <MenuItem key={component.id} value={component.id}>
                          {component.name} ({component.sku})
                        </MenuItem>
                      ))}
                    </TextField>
                  </Grid>
                )}
                <Grid item xs={12} sm={6}>
                  <TextField
                    name="quantity_available"
                    label="Quantity Available"
                    type="number"
                    fullWidth
                    required
                    defaultValue={selectedItem?.quantity_available || 0}
                    InputProps={{ inputProps: { min: 0 } }}
                  />
                </Grid>
                {selectedItem && (
                  <Grid item xs={12} sm={6}>
                    <TextField
                      name="quantity_allocated"
                      label="Quantity Allocated"
                      type="number"
                      fullWidth
                      required
                      defaultValue={selectedItem?.quantity_allocated || 0}
                      InputProps={{ inputProps: { min: 0 } }}
                    />
                  </Grid>
                )}
                <Grid item xs={12} sm={6}>
                  <TextField
                    name="reorder_threshold"
                    label="Reorder Threshold"
                    type="number"
                    fullWidth
                    required
                    defaultValue={selectedItem?.reorder_threshold || 10}
                    InputProps={{ inputProps: { min: 1 } }}
                  />
                </Grid>
                <Grid item xs={12}>
                  <TextField
                    name="location"
                    label="Storage Location"
                    fullWidth
                    defaultValue={selectedItem?.location || ''}
                    placeholder="e.g., Warehouse A, Aisle 3, Shelf 12"
                  />
                </Grid>
              </Grid>
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