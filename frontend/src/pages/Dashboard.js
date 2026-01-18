import React, { useState, useEffect } from 'react';
import { 
  Box, 
  Grid, 
  Card, 
  CardContent, 
  CardHeader, 
  Typography, 
  List, 
  ListItem, 
  ListItemText, 
  Chip,
  Divider,
  CircularProgress,
  Button,
  Alert
} from '@mui/material';
import { useNavigate } from 'react-router-dom';

// Charts
import { Bar, Pie, Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  PointElement,
  LineElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';

// Services
import { 
  orderService, 
  inventoryService, 
  productionService, 
  supplyChainService 
} from '../services';

// Notification context
import { useNotification } from '../context/NotificationContext';

// Register ChartJS components
ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  PointElement,
  LineElement,
  ArcElement,
  Title,
  Tooltip,
  Legend
);

export default function Dashboard() {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [dashboardData, setDashboardData] = useState({
    orders: [],
    lowStockItems: [],
    productionSchedules: [],
    supplyChainRisks: []
  });
  const navigate = useNavigate();
  const { showError } = useNotification();

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        setLoading(true);
        
        // For a real application, these would be API calls
        // For the demo, we'll use simulated data
        
        // Fetch orders
        const orders = await orderService.getOrders();
        
        // Fetch low stock items
        const lowStockItems = await inventoryService.getLowStockItems();
        
        // Fetch production schedules
        const productionSchedules = await productionService.getProductionSchedules({
          start_date: new Date(),
          end_date: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000) // 7 days from now
        });
        
        // Fetch supply chain risks
        const riskAssessment = await supplyChainService.assessRisks({
          time_horizon_days: 30
        });
        
        setDashboardData({
          orders,
          lowStockItems,
          productionSchedules,
          supplyChainRisks: riskAssessment.risks || []
        });
      } catch (err) {
        console.error('Error fetching dashboard data:', err);
        setError('Failed to load dashboard data. Please try again later.');
        showError('Failed to load dashboard data');
      } finally {
        setLoading(false);
      }
    };
    
    fetchDashboardData();
  }, [showError]);

  // For demo purposes, we'll simulate the data since the API isn't actually running
  const simulatedData = {
    orders: [
      { id: 1, customer: { name: 'Acme Corporation' }, status: 'DELIVERED', order_date: '2026-01-10T12:00:00Z' },
      { id: 2, customer: { name: 'Globex Industries' }, status: 'SHIPPED', order_date: '2026-01-15T12:00:00Z' },
      { id: 3, customer: { name: 'Initech Systems' }, status: 'IN_PRODUCTION', order_date: '2026-01-17T12:00:00Z' },
      { id: 4, customer: { name: 'Umbrella Corporation' }, status: 'CONFIRMED', order_date: '2026-01-17T12:00:00Z' },
      { id: 5, customer: { name: 'Stark Industries' }, status: 'PENDING', order_date: '2026-01-17T12:00:00Z' }
    ],
    lowStockItems: [
      { component_name: 'Circuit Board', quantity_available: 5, reorder_threshold: 20, shortage: 15 },
      { component_name: 'Power Supply', quantity_available: 8, reorder_threshold: 15, shortage: 7 },
      { component_name: 'LCD Display', quantity_available: 3, reorder_threshold: 10, shortage: 7 }
    ],
    productionSchedules: [
      { id: 3, order_id: 3, production_line: { name: 'Assembly Line A' }, status: 'in_progress', scheduled_start: '2026-01-12T08:00:00Z', scheduled_end: '2026-01-22T17:00:00Z' },
      { id: 4, order_id: 4, production_line: { name: 'Assembly Line B' }, status: 'scheduled', scheduled_start: '2026-01-22T08:00:00Z', scheduled_end: '2026-02-01T17:00:00Z' }
    ],
    supplyChainRisks: [
      { risk_type: 'weather', region: 'Southeast Asia', description: 'Tropical storm approaching manufacturing hubs', risk_level: 'HIGH' },
      { risk_type: 'logistics', region: 'Asia Pacific', description: 'Port congestion at Shanghai port', risk_level: 'MEDIUM' },
      { risk_type: 'market', region: 'Global', description: 'Semiconductor shortage affecting electronics supply', risk_level: 'CRITICAL' }
    ],
    orderStatusData: {
      labels: ['Pending', 'Confirmed', 'In Production', 'Shipped', 'Delivered', 'Cancelled'],
      datasets: [
        {
          label: 'Order Status',
          data: [1, 1, 1, 1, 1, 0],
          backgroundColor: [
            '#9e9e9e',
            '#2196f3',
            '#ff9800',
            '#9c27b0',
            '#4caf50',
            '#f44336'
          ]
        }
      ]
    },
    inventoryData: {
      labels: ['Circuit Board', 'Power Supply', 'LCD Display', 'Steel Frame', 'Rubber Gasket'],
      datasets: [
        {
          label: 'Available',
          data: [5, 8, 3, 50, 120],
          backgroundColor: '#2196f3'
        },
        {
          label: 'Allocated',
          data: [10, 5, 2, 20, 30],
          backgroundColor: '#ff9800'
        },
        {
          label: 'Reorder Threshold',
          data: [20, 15, 10, 30, 50],
          backgroundColor: '#f44336'
        }
      ]
    },
    productionCapacityData: {
      labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
      datasets: [
        {
          label: 'Available Capacity (hours)',
          data: [24, 18, 12, 6, 8, 16, 24],
          borderColor: '#4caf50',
          backgroundColor: 'rgba(76, 175, 80, 0.2)',
          fill: true
        },
        {
          label: 'Scheduled Production (hours)',
          data: [16, 22, 28, 34, 32, 24, 16],
          borderColor: '#f44336',
          backgroundColor: 'rgba(244, 67, 54, 0.2)',
          fill: true
        }
      ]
    }
  };

  // Use simulated data for the demo
  const data = simulatedData;

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
      <Typography variant="h4" gutterBottom>
        Manufacturing Visibility Dashboard
      </Typography>
      
      <Grid container spacing={3}>
        {/* Order Status */}
        <Grid item xs={12} md={6} lg={3}>
          <Card className="dashboard-card">
            <CardHeader title="Order Status" />
            <CardContent className="dashboard-card-content">
              <Box sx={{ height: 200 }}>
                <Pie data={data.orderStatusData} options={{ maintainAspectRatio: false }} />
              </Box>
              <Button 
                variant="outlined" 
                fullWidth 
                sx={{ mt: 2 }}
                onClick={() => navigate('/orders')}
              >
                View Orders
              </Button>
            </CardContent>
          </Card>
        </Grid>
        
        {/* Low Stock Items */}
        <Grid item xs={12} md={6} lg={3}>
          <Card className="dashboard-card">
            <CardHeader 
              title="Low Stock Items" 
              titleTypographyProps={{ color: data.lowStockItems.length > 0 ? 'error' : 'inherit' }}
            />
            <CardContent className="dashboard-card-content">
              {data.lowStockItems.length > 0 ? (
                <List dense>
                  {data.lowStockItems.map((item, index) => (
                    <React.Fragment key={index}>
                      <ListItem>
                        <ListItemText
                          primary={item.component_name}
                          secondary={`Available: ${item.quantity_available} (Need ${item.shortage} more)`}
                        />
                        <Chip 
                          label="Low" 
                          color="error" 
                          size="small" 
                          variant="outlined" 
                        />
                      </ListItem>
                      {index < data.lowStockItems.length - 1 && <Divider />}
                    </React.Fragment>
                  ))}
                </List>
              ) : (
                <Typography variant="body2" color="textSecondary" align="center">
                  No low stock items
                </Typography>
              )}
              <Button 
                variant="outlined" 
                fullWidth 
                sx={{ mt: 2 }}
                onClick={() => navigate('/inventory')}
              >
                View Inventory
              </Button>
            </CardContent>
          </Card>
        </Grid>
        
        {/* Production Schedule */}
        <Grid item xs={12} md={6} lg={3}>
          <Card className="dashboard-card">
            <CardHeader title="Production Schedule" />
            <CardContent className="dashboard-card-content">
              {data.productionSchedules.length > 0 ? (
                <List dense>
                  {data.productionSchedules.map((schedule, index) => (
                    <React.Fragment key={index}>
                      <ListItem>
                        <ListItemText
                          primary={`Order #${schedule.order_id}`}
                          secondary={`${schedule.production_line.name} - ${schedule.status}`}
                        />
                        <Chip 
                          label={schedule.status === 'in_progress' ? 'Active' : 'Scheduled'} 
                          color={schedule.status === 'in_progress' ? 'primary' : 'default'} 
                          size="small" 
                          variant="outlined" 
                        />
                      </ListItem>
                      {index < data.productionSchedules.length - 1 && <Divider />}
                    </React.Fragment>
                  ))}
                </List>
              ) : (
                <Typography variant="body2" color="textSecondary" align="center">
                  No upcoming production schedules
                </Typography>
              )}
              <Button 
                variant="outlined" 
                fullWidth 
                sx={{ mt: 2 }}
                onClick={() => navigate('/production')}
              >
                View Production
              </Button>
            </CardContent>
          </Card>
        </Grid>
        
        {/* Supply Chain Risks */}
        <Grid item xs={12} md={6} lg={3}>
          <Card className="dashboard-card">
            <CardHeader 
              title="Supply Chain Risks" 
              titleTypographyProps={{ 
                color: data.supplyChainRisks.some(risk => 
                  risk.risk_level === 'HIGH' || risk.risk_level === 'CRITICAL'
                ) ? 'error' : 'inherit' 
              }}
            />
            <CardContent className="dashboard-card-content">
              {data.supplyChainRisks.length > 0 ? (
                <List dense>
                  {data.supplyChainRisks.map((risk, index) => (
                    <React.Fragment key={index}>
                      <ListItem>
                        <ListItemText
                          primary={risk.description}
                          secondary={`${risk.risk_type} - ${risk.region}`}
                        />
                        <Chip 
                          label={risk.risk_level} 
                          color={
                            risk.risk_level === 'LOW' ? 'success' :
                            risk.risk_level === 'MEDIUM' ? 'warning' : 'error'
                          }
                          size="small" 
                        />
                      </ListItem>
                      {index < data.supplyChainRisks.length - 1 && <Divider />}
                    </React.Fragment>
                  ))}
                </List>
              ) : (
                <Typography variant="body2" color="textSecondary" align="center">
                  No active supply chain risks
                </Typography>
              )}
              <Button 
                variant="outlined" 
                fullWidth 
                sx={{ mt: 2 }}
                onClick={() => navigate('/supply-chain')}
              >
                View Supply Chain
              </Button>
            </CardContent>
          </Card>
        </Grid>
        
        {/* Inventory Levels */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardHeader title="Inventory Levels" />
            <CardContent>
              <Box sx={{ height: 300 }}>
                <Bar 
                  data={data.inventoryData} 
                  options={{ 
                    maintainAspectRatio: false,
                    scales: {
                      y: {
                        beginAtZero: true,
                        title: {
                          display: true,
                          text: 'Quantity'
                        }
                      },
                      x: {
                        title: {
                          display: true,
                          text: 'Component'
                        }
                      }
                    }
                  }} 
                />
              </Box>
            </CardContent>
          </Card>
        </Grid>
        
        {/* Production Capacity */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardHeader title="Production Capacity (Next 7 Days)" />
            <CardContent>
              <Box sx={{ height: 300 }}>
                <Line 
                  data={data.productionCapacityData} 
                  options={{ 
                    maintainAspectRatio: false,
                    scales: {
                      y: {
                        beginAtZero: true,
                        title: {
                          display: true,
                          text: 'Hours'
                        }
                      },
                      x: {
                        title: {
                          display: true,
                          text: 'Day'
                        }
                      }
                    }
                  }} 
                />
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
}