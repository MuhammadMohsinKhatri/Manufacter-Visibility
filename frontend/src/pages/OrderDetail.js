import React, { useState, useEffect } from 'react';
import { 
  Box, 
  Typography, 
  Button, 
  Paper, 
  CircularProgress,
  Alert,
  Chip,
  Grid,
  Divider,
  Card,
  CardContent,
  CardHeader,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow
} from '@mui/material';
import { useParams, useNavigate } from 'react-router-dom';
import { format } from 'date-fns';

// Icons
import ArrowBackIcon from '@mui/icons-material/ArrowBack';

// Services
import { orderService } from '../services';

// Notification context
import { useNotification } from '../context/NotificationContext';

export default function OrderDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [order, setOrder] = useState(null);
  const [error, setError] = useState(null);
  const { showError } = useNotification();

  useEffect(() => {
    const fetchOrder = async () => {
      try {
        setLoading(true);
        const data = await orderService.getOrder(id);
        setOrder(data);
      } catch (err) {
        console.error('Error fetching order:', err);
        setError('Failed to load order details. Please try again later.');
        showError('Failed to load order details');
      } finally {
        setLoading(false);
      }
    };
    
    fetchOrder();
  }, [id, showError]);

  // For demo purposes, we'll use simulated data
  const simulatedOrder = {
    id: parseInt(id),
    customer: { id: 1, name: 'Acme Corporation', email: 'contact@acme.com' },
    status: id === '1' ? 'DELIVERED' : id === '2' ? 'SHIPPED' : 'IN_PRODUCTION',
    order_date: '2026-01-10T12:00:00Z',
    estimated_delivery: '2026-01-20T12:00:00Z',
    actual_delivery: id === '1' ? '2026-01-19T14:30:00Z' : null,
    notes: 'Regular order, delivered on time',
    items: [
      { id: 1, component_name: 'Circuit Board', quantity: 10, unit_price: 25.50, total: 255.00 },
      { id: 2, component_name: 'Power Supply', quantity: 5, unit_price: 45.00, total: 225.00 },
      { id: 3, component_name: 'LCD Display', quantity: 3, unit_price: 120.00, total: 360.00 }
    ]
  };

  const data = order || simulatedOrder;

  const getStatusColor = (status) => {
    switch (status) {
      case 'PENDING':
        return 'default';
      case 'CONFIRMED':
        return 'primary';
      case 'IN_PRODUCTION':
        return 'warning';
      case 'SHIPPED':
        return 'info';
      case 'DELIVERED':
        return 'success';
      case 'CANCELLED':
        return 'error';
      default:
        return 'default';
    }
  };

  const totalAmount = data.items?.reduce((sum, item) => sum + (item.total || 0), 0) || 0;

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '80vh' }}>
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Box sx={{ mt: 2 }}>
        <Alert severity="error">{error}</Alert>
      </Box>
    );
  }

  return (
    <Box>
      <Box sx={{ display: 'flex', alignItems: 'center', mb: 3 }}>
        <Button
          startIcon={<ArrowBackIcon />}
          onClick={() => navigate('/orders')}
          sx={{ mr: 2 }}
        >
          Back to Orders
        </Button>
        <Typography variant="h4">
          Order #{data.id}
        </Typography>
      </Box>

      <Grid container spacing={3}>
        {/* Order Summary */}
        <Grid item xs={12} md={8}>
          <Card>
            <CardHeader title="Order Details" />
            <CardContent>
              <Grid container spacing={2}>
                <Grid item xs={12} sm={6}>
                  <Typography variant="body2" color="textSecondary">
                    Customer
                  </Typography>
                  <Typography variant="body1" gutterBottom>
                    {data.customer?.name || 'Unknown'}
                  </Typography>
                </Grid>
                <Grid item xs={12} sm={6}>
                  <Typography variant="body2" color="textSecondary">
                    Status
                  </Typography>
                  <Box sx={{ mt: 0.5 }}>
                    <Chip 
                      label={data.status?.replace('_', ' ')} 
                      color={getStatusColor(data.status)} 
                      size="small" 
                    />
                  </Box>
                </Grid>
                <Grid item xs={12} sm={6}>
                  <Typography variant="body2" color="textSecondary">
                    Order Date
                  </Typography>
                  <Typography variant="body1">
                    {data.order_date ? format(new Date(data.order_date), 'MMM dd, yyyy HH:mm') : 'N/A'}
                  </Typography>
                </Grid>
                <Grid item xs={12} sm={6}>
                  <Typography variant="body2" color="textSecondary">
                    Estimated Delivery
                  </Typography>
                  <Typography variant="body1">
                    {data.estimated_delivery ? format(new Date(data.estimated_delivery), 'MMM dd, yyyy') : 'N/A'}
                  </Typography>
                </Grid>
                {data.actual_delivery && (
                  <Grid item xs={12} sm={6}>
                    <Typography variant="body2" color="textSecondary">
                      Actual Delivery
                    </Typography>
                    <Typography variant="body1">
                      {format(new Date(data.actual_delivery), 'MMM dd, yyyy HH:mm')}
                    </Typography>
                  </Grid>
                )}
                {data.notes && (
                  <Grid item xs={12}>
                    <Divider sx={{ my: 2 }} />
                    <Typography variant="body2" color="textSecondary">
                      Notes
                    </Typography>
                    <Typography variant="body1">
                      {data.notes}
                    </Typography>
                  </Grid>
                )}
              </Grid>
            </CardContent>
          </Card>
        </Grid>

        {/* Order Summary Sidebar */}
        <Grid item xs={12} md={4}>
          <Card>
            <CardHeader title="Summary" />
            <CardContent>
              <Box sx={{ mb: 2 }}>
                <Typography variant="body2" color="textSecondary">
                  Items
                </Typography>
                <Typography variant="h6">
                  {data.items?.length || 0}
                </Typography>
              </Box>
              <Divider sx={{ my: 2 }} />
              <Box>
                <Typography variant="body2" color="textSecondary">
                  Total Amount
                </Typography>
                <Typography variant="h5" sx={{ fontWeight: 'bold' }}>
                  ${totalAmount.toFixed(2)}
                </Typography>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        {/* Order Items */}
        <Grid item xs={12}>
          <Card>
            <CardHeader title="Order Items" />
            <CardContent>
              <TableContainer>
                <Table>
                  <TableHead>
                    <TableRow>
                      <TableCell>Component Name</TableCell>
                      <TableCell align="right">Quantity</TableCell>
                      <TableCell align="right">Unit Price</TableCell>
                      <TableCell align="right">Total</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {data.items?.map((item) => (
                      <TableRow key={item.id}>
                        <TableCell>{item.component_name}</TableCell>
                        <TableCell align="right">{item.quantity}</TableCell>
                        <TableCell align="right">${item.unit_price?.toFixed(2)}</TableCell>
                        <TableCell align="right">${item.total?.toFixed(2)}</TableCell>
                      </TableRow>
                    ))}
                    <TableRow>
                      <TableCell colSpan={3} align="right">
                        <Typography variant="h6">
                          Total
                        </Typography>
                      </TableCell>
                      <TableCell align="right">
                        <Typography variant="h6">
                          ${totalAmount.toFixed(2)}
                        </Typography>
                      </TableCell>
                    </TableRow>
                  </TableBody>
                </Table>
              </TableContainer>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
}

