import React, { useState, useEffect } from 'react';
import { 
  Box, 
  Typography, 
  Button, 
  Paper, 
  CircularProgress,
  Alert,
  Chip,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  MenuItem,
  Grid,
  IconButton,
  Tooltip
} from '@mui/material';
import { DataGrid } from '@mui/x-data-grid';
import { useNavigate } from 'react-router-dom';
import { format } from 'date-fns';

// Icons
import AddIcon from '@mui/icons-material/Add';
import VisibilityIcon from '@mui/icons-material/Visibility';
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/Delete';
import CheckCircleOutlineIcon from '@mui/icons-material/CheckCircleOutline';

// Services
import { orderService } from '../services';

// Notification context
import { useNotification } from '../context/NotificationContext';

export default function OrderManagement() {
  const [loading, setLoading] = useState(true);
  const [orders, setOrders] = useState([]);
  const [error, setError] = useState(null);
  const [openDialog, setOpenDialog] = useState(false);
  const [deleteConfirmOpen, setDeleteConfirmOpen] = useState(false);
  const [selectedOrder, setSelectedOrder] = useState(null);
  const navigate = useNavigate();
  const { showSuccess, showError } = useNotification();

  useEffect(() => {
    fetchOrders();
  }, []);

  const fetchOrders = async () => {
    try {
      setLoading(true);
      const data = await orderService.getOrders();
      setOrders(data);
    } catch (err) {
      console.error('Error fetching orders:', err);
      setError('Failed to load orders. Please try again later.');
      showError('Failed to load orders');
    } finally {
      setLoading(false);
    }
  };

  const handleViewOrder = (id) => {
    navigate(`/orders/${id}`);
  };

  const handleEditOrder = (order) => {
    setSelectedOrder(order);
    setOpenDialog(true);
  };

  const handleDeleteClick = (order) => {
    setSelectedOrder(order);
    setDeleteConfirmOpen(true);
  };

  const handleDeleteConfirm = async () => {
    try {
      await orderService.deleteOrder(selectedOrder.id);
      showSuccess('Order deleted successfully');
      fetchOrders();
    } catch (err) {
      console.error('Error deleting order:', err);
      showError('Failed to delete order');
    } finally {
      setDeleteConfirmOpen(false);
      setSelectedOrder(null);
    }
  };

  const handleCreateOrder = () => {
    setSelectedOrder(null);
    setOpenDialog(true);
  };

  const handleDialogClose = () => {
    setOpenDialog(false);
    setSelectedOrder(null);
  };

  const handleOrderSubmit = async (event) => {
    event.preventDefault();
    const formData = new FormData(event.target);
    
    try {
      if (selectedOrder) {
        // Update existing order
        const updateData = {
          status: formData.get('status'),
          notes: formData.get('notes')
        };
        
        await orderService.updateOrder(selectedOrder.id, updateData);
        showSuccess('Order updated successfully');
      } else {
        // Create new order
        // In a real app, this would include order items
        const orderData = {
          customer_id: parseInt(formData.get('customer_id')),
          notes: formData.get('notes'),
          items: [] // Would be populated in a real app
        };
        
        await orderService.createOrder(orderData);
        showSuccess('Order created successfully');
      }
      
      handleDialogClose();
      fetchOrders();
    } catch (err) {
      console.error('Error saving order:', err);
      showError('Failed to save order');
    }
  };

  const handleCheckFeasibility = () => {
    navigate('/orders/feasibility');
  };

  // For demo purposes, we'll use simulated data
  const simulatedOrders = [
    { 
      id: 1, 
      customer: { id: 1, name: 'Acme Corporation' }, 
      status: 'DELIVERED', 
      order_date: '2026-01-10T12:00:00Z',
      estimated_delivery: '2026-01-20T12:00:00Z',
      actual_delivery: '2026-01-19T14:30:00Z',
      notes: 'Regular order, delivered on time'
    },
    { 
      id: 2, 
      customer: { id: 2, name: 'Globex Industries' }, 
      status: 'SHIPPED', 
      order_date: '2026-01-15T12:00:00Z',
      estimated_delivery: '2026-01-25T12:00:00Z',
      actual_delivery: null,
      notes: 'Expedited shipping requested'
    },
    { 
      id: 3, 
      customer: { id: 3, name: 'Initech Systems' }, 
      status: 'IN_PRODUCTION', 
      order_date: '2026-01-17T12:00:00Z',
      estimated_delivery: '2026-02-01T12:00:00Z',
      actual_delivery: null,
      notes: 'Custom configuration requested'
    },
    { 
      id: 4, 
      customer: { id: 4, name: 'Umbrella Corporation' }, 
      status: 'CONFIRMED', 
      order_date: '2026-01-17T12:00:00Z',
      estimated_delivery: '2026-02-10T12:00:00Z',
      actual_delivery: null,
      notes: 'Standard order'
    },
    { 
      id: 5, 
      customer: { id: 5, name: 'Stark Industries' }, 
      status: 'PENDING', 
      order_date: '2026-01-17T12:00:00Z',
      estimated_delivery: '2026-02-15T12:00:00Z',
      actual_delivery: null,
      notes: 'Awaiting component availability confirmation'
    }
  ];

  // Use simulated data for the demo
  const data = simulatedOrders;

  const columns = [
    { field: 'id', headerName: 'Order ID', width: 100 },
    { 
      field: 'customer', 
      headerName: 'Customer', 
      width: 200,
      valueGetter: (params) => params.row.customer?.name || 'Unknown'
    },
    { 
      field: 'order_date', 
      headerName: 'Order Date', 
      width: 150,
      valueFormatter: (params) => format(new Date(params.value), 'MM/dd/yyyy')
    },
    { 
      field: 'estimated_delivery', 
      headerName: 'Est. Delivery', 
      width: 150,
      valueFormatter: (params) => params.value ? format(new Date(params.value), 'MM/dd/yyyy') : 'N/A'
    },
    { 
      field: 'status', 
      headerName: 'Status', 
      width: 150,
      renderCell: (params) => {
        const status = params.value;
        let color;
        switch (status) {
          case 'PENDING':
            color = 'default';
            break;
          case 'CONFIRMED':
            color = 'primary';
            break;
          case 'IN_PRODUCTION':
            color = 'warning';
            break;
          case 'SHIPPED':
            color = 'info';
            break;
          case 'DELIVERED':
            color = 'success';
            break;
          case 'CANCELLED':
            color = 'error';
            break;
          default:
            color = 'default';
        }
        
        return (
          <Chip 
            label={status.replace('_', ' ')} 
            color={color} 
            size="small" 
          />
        );
      }
    },
    {
      field: 'actions',
      headerName: 'Actions',
      width: 200,
      sortable: false,
      renderCell: (params) => (
        <Box>
          <Tooltip title="View">
            <IconButton 
              size="small" 
              onClick={() => handleViewOrder(params.row.id)}
            >
              <VisibilityIcon fontSize="small" />
            </IconButton>
          </Tooltip>
          <Tooltip title="Edit">
            <IconButton 
              size="small" 
              onClick={() => handleEditOrder(params.row)}
            >
              <EditIcon fontSize="small" />
            </IconButton>
          </Tooltip>
          <Tooltip title="Delete">
            <IconButton 
              size="small" 
              onClick={() => handleDeleteClick(params.row)}
              color="error"
            >
              <DeleteIcon fontSize="small" />
            </IconButton>
          </Tooltip>
        </Box>
      )
    }
  ];

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
        <Typography variant="h4">
          Order Management
        </Typography>
        <Box>
          <Button
            variant="outlined"
            startIcon={<CheckCircleOutlineIcon />}
            onClick={handleCheckFeasibility}
            sx={{ mr: 2 }}
          >
            Check Feasibility
          </Button>
          <Button
            variant="contained"
            startIcon={<AddIcon />}
            onClick={handleCreateOrder}
          >
            New Order
          </Button>
        </Box>
      </Box>
      
      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}
      
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
      
      {/* Order Form Dialog */}
      <Dialog open={openDialog} onClose={handleDialogClose} maxWidth="md" fullWidth>
        <DialogTitle>
          {selectedOrder ? `Edit Order #${selectedOrder.id}` : 'Create New Order'}
        </DialogTitle>
        <Box component="form" onSubmit={handleOrderSubmit}>
          <DialogContent>
            <Grid container spacing={2}>
              <Grid item xs={12} sm={6}>
                <TextField
                  select
                  name="customer_id"
                  label="Customer"
                  fullWidth
                  required
                  defaultValue={selectedOrder?.customer?.id || ''}
                  disabled={!!selectedOrder}
                >
                  <MenuItem value={1}>Acme Corporation</MenuItem>
                  <MenuItem value={2}>Globex Industries</MenuItem>
                  <MenuItem value={3}>Initech Systems</MenuItem>
                  <MenuItem value={4}>Umbrella Corporation</MenuItem>
                  <MenuItem value={5}>Stark Industries</MenuItem>
                </TextField>
              </Grid>
              <Grid item xs={12} sm={6}>
                {selectedOrder && (
                  <TextField
                    select
                    name="status"
                    label="Status"
                    fullWidth
                    required
                    defaultValue={selectedOrder?.status || 'PENDING'}
                  >
                    <MenuItem value="PENDING">Pending</MenuItem>
                    <MenuItem value="CONFIRMED">Confirmed</MenuItem>
                    <MenuItem value="IN_PRODUCTION">In Production</MenuItem>
                    <MenuItem value="SHIPPED">Shipped</MenuItem>
                    <MenuItem value="DELIVERED">Delivered</MenuItem>
                    <MenuItem value="CANCELLED">Cancelled</MenuItem>
                  </TextField>
                )}
              </Grid>
              <Grid item xs={12}>
                <TextField
                  name="notes"
                  label="Notes"
                  fullWidth
                  multiline
                  rows={4}
                  defaultValue={selectedOrder?.notes || ''}
                />
              </Grid>
            </Grid>
          </DialogContent>
          <DialogActions>
            <Button onClick={handleDialogClose}>Cancel</Button>
            <Button type="submit" variant="contained">
              {selectedOrder ? 'Update' : 'Create'}
            </Button>
          </DialogActions>
        </Box>
      </Dialog>
      
      {/* Delete Confirmation Dialog */}
      <Dialog open={deleteConfirmOpen} onClose={() => setDeleteConfirmOpen(false)}>
        <DialogTitle>Confirm Delete</DialogTitle>
        <DialogContent>
          <Typography>
            Are you sure you want to delete Order #{selectedOrder?.id}?
          </Typography>
          <Typography color="error" variant="body2" sx={{ mt: 1 }}>
            This action cannot be undone.
          </Typography>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDeleteConfirmOpen(false)}>Cancel</Button>
          <Button onClick={handleDeleteConfirm} color="error" variant="contained">
            Delete
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
}