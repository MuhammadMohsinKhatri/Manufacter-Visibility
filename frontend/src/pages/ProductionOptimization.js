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
  Chip,
  Tabs,
  Tab,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Divider,
  LinearProgress,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  IconButton,
  Tooltip,
  Stack
} from '@mui/material';
import { DataGrid } from '@mui/x-data-grid';
import { format } from 'date-fns';

// Icons
import AutoAwesomeIcon from '@mui/icons-material/AutoAwesome';
import PeopleIcon from '@mui/icons-material/People';
import ScheduleIcon from '@mui/icons-material/Schedule';
import AssignmentIcon from '@mui/icons-material/Assignment';
import AddIcon from '@mui/icons-material/Add';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import WarningIcon from '@mui/icons-material/Warning';
import TrendingUpIcon from '@mui/icons-material/TrendingUp';
import PersonAddIcon from '@mui/icons-material/PersonAdd';
import WorkIcon from '@mui/icons-material/Work';

// Services
import optimizationService from '../services/optimizationService';
import { orderService } from '../services';
import { useNotification } from '../context/NotificationContext';

export default function ProductionOptimization() {
  const [activeTab, setActiveTab] = useState(0);
  const [loading, setLoading] = useState(false);
  const [optimizing, setOptimizing] = useState(false);
  const [error, setError] = useState(null);
  
  // Data states
  const [orders, setOrders] = useState([]);
  const [selectedOrders, setSelectedOrders] = useState([]);
  const [staff, setStaff] = useState([]);
  const [taskAssignments, setTaskAssignments] = useState([]);
  const [optimizationResult, setOptimizationResult] = useState(null);
  
  // Dialog states
  const [openStaffDialog, setOpenStaffDialog] = useState(false);
  const [openOptimizeDialog, setOpenOptimizeDialog] = useState(false);
  const [newStaff, setNewStaff] = useState({
    name: '',
    employee_id: '',
    department: 'production',
    skill_level: 'intermediate',
    specialization: '',
    hourly_rate: 0,
    max_hours_per_day: 8
  });
  
  const [optimizationParams, setOptimizationParams] = useState({
    start_date: new Date(),
    end_date: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000),
    optimize_for: 'time'
  });
  
  const { showSuccess, showError } = useNotification();

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      setLoading(true);
      const [ordersData, staffData] = await Promise.all([
        orderService.getOrders(),
        optimizationService.getStaff()
      ]);
      setOrders(ordersData);
      setStaff(staffData);
    } catch (err) {
      console.error('Error fetching data:', err);
      setError('Failed to load data');
    } finally {
      setLoading(false);
    }
  };

  const handleOptimizeProduction = async () => {
    if (selectedOrders.length === 0) {
      showError('Please select at least one order to optimize');
      return;
    }

    try {
      setOptimizing(true);
      setError(null);
      
      const result = await optimizationService.optimizeOrderFulfillment(
        selectedOrders,
        optimizationParams.optimize_for,
        optimizationParams.start_date,
        optimizationParams.end_date
      );
      
      // Fetch task assignments after optimization
      if (result.production_schedules > 0) {
        const assignments = await optimizationService.getTaskAssignments();
        setTaskAssignments(assignments);
      }
      
      setOptimizationResult(result);
      showSuccess('Production schedule optimized successfully!');
      setActiveTab(1); // Switch to results tab
      
      // Refresh data
      await fetchData();
    } catch (err) {
      console.error('Error optimizing production:', err);
      setError(err.response?.data?.detail || 'Failed to optimize production schedule');
      showError('Failed to optimize production schedule');
    } finally {
      setOptimizing(false);
    }
  };

  const handleCreateStaff = async () => {
    try {
      await optimizationService.createStaff(newStaff);
      showSuccess('Staff member created successfully');
      setOpenStaffDialog(false);
      setNewStaff({
        name: '',
        employee_id: '',
        department: 'production',
        skill_level: 'intermediate',
        specialization: '',
        hourly_rate: 0,
        max_hours_per_day: 8
      });
      await fetchData();
    } catch (err) {
      console.error('Error creating staff:', err);
      showError('Failed to create staff member');
    }
  };

  const orderColumns = [
    { field: 'id', headerName: 'ID', width: 80 },
    { field: 'order_date', headerName: 'Date', width: 120, 
      valueFormatter: (params) => params.value ? format(new Date(params.value), 'MM/dd/yyyy') : 'N/A' },
    { field: 'status', headerName: 'Status', width: 120,
      renderCell: (params) => (
        <Chip 
          label={params.value || 'Unknown'} 
          color={params.value === 'confirmed' ? 'success' : 'default'}
          size="small"
        />
      )
    },
    { field: 'estimated_delivery', headerName: 'Delivery', width: 120,
      valueFormatter: (params) => params.value ? format(new Date(params.value), 'MM/dd/yyyy') : 'N/A' }
  ];

  const staffColumns = [
    { field: 'id', headerName: 'ID', width: 80 },
    { field: 'name', headerName: 'Name', width: 150 },
    { field: 'employee_id', headerName: 'Employee ID', width: 120 },
    { field: 'department', headerName: 'Department', width: 120 },
    { field: 'skill_level', headerName: 'Skill Level', width: 120,
      renderCell: (params) => (
        <Chip 
          label={params.value || 'Unknown'} 
          color={params.value === 'expert' ? 'success' : params.value === 'senior' ? 'primary' : 'default'}
          size="small"
        />
      )
    },
    { field: 'specialization', headerName: 'Specialization', width: 150 },
    { field: 'hourly_rate', headerName: 'Rate ($/hr)', width: 100,
      valueFormatter: (params) => `$${params.value?.toFixed(2) || '0.00'}` },
    { field: 'is_available', headerName: 'Available', width: 100,
      renderCell: (params) => (
        <Chip 
          label={params.value ? 'Yes' : 'No'} 
          color={params.value ? 'success' : 'default'}
          size="small"
        />
      )
    },
    { field: 'current_workload_hours', headerName: 'Workload (hrs)', width: 120 }
  ];

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3, flexWrap: 'wrap', gap: 2 }}>
        <Typography variant="h4">
          Production Optimization & Resource Management
        </Typography>
        <Box sx={{ display: 'flex', gap: 2 }}>
          <Button
            variant="outlined"
            startIcon={<PersonAddIcon />}
            onClick={() => setOpenStaffDialog(true)}
          >
            Add Staff
          </Button>
          <Button
            variant="contained"
            startIcon={<AutoAwesomeIcon />}
            onClick={() => setOpenOptimizeDialog(true)}
            disabled={selectedOrders.length === 0}
          >
            Optimize Schedule
          </Button>
        </Box>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError(null)}>
          {error}
        </Alert>
      )}

      <Paper sx={{ mb: 3 }}>
        <Tabs 
          value={activeTab} 
          onChange={(e, newValue) => setActiveTab(newValue)}
          indicatorColor="primary"
          textColor="primary"
        >
          <Tab label="Order Selection" icon={<AssignmentIcon />} iconPosition="start" />
          <Tab label="Optimization Results" icon={<TrendingUpIcon />} iconPosition="start" />
          <Tab label="Staff Management" icon={<PeopleIcon />} iconPosition="start" />
          <Tab label="Task Assignments" icon={<WorkIcon />} iconPosition="start" />
        </Tabs>
      </Paper>

      {/* Tab 0: Order Selection */}
      {activeTab === 0 && (
        <Box>
          <Card sx={{ mb: 3 }}>
            <CardHeader
              title="Select Orders to Optimize"
              subheader="Choose orders that need production scheduling optimization"
            />
            <CardContent>
              <Paper sx={{ height: 400, width: '100%' }}>
                {loading ? (
                  <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100%' }}>
                    <CircularProgress />
                  </Box>
                ) : (
                  <DataGrid
                    rows={orders}
                    columns={orderColumns}
                    checkboxSelection
                    onRowSelectionModelChange={(newSelection) => {
                      setSelectedOrders(newSelection);
                    }}
                    rowSelectionModel={selectedOrders}
                    pageSize={10}
                    rowsPerPageOptions={[10, 25, 50]}
                  />
                )}
              </Paper>
              <Box sx={{ mt: 2 }}>
                <Typography variant="body2" color="text.secondary">
                  Selected: {selectedOrders.length} order(s)
                </Typography>
              </Box>
            </CardContent>
          </Card>
        </Box>
      )}

      {/* Tab 1: Optimization Results */}
      {activeTab === 1 && (
        <Box>
          {optimizationResult ? (
            <Grid container spacing={3}>
              <Grid item xs={12}>
                <Card elevation={3} sx={{ bgcolor: '#e8f5e9', border: '2px solid #4caf50' }}>
                  <CardHeader
                    title="Optimization Complete"
                    avatar={<CheckCircleIcon color="success" />}
                  />
                  <CardContent>
                    <Grid container spacing={2}>
                      <Grid item xs={12} sm={6} md={3}>
                        <Typography variant="h3" color="success.main">
                          {optimizationResult.total_makespan_days?.toFixed(1) || 'N/A'}
                        </Typography>
                        <Typography variant="body2" color="text.secondary">
                          Total Makespan (Days)
                        </Typography>
                      </Grid>
                      <Grid item xs={12} sm={6} md={3}>
                        <Typography variant="h3" color="primary.main">
                          {optimizationResult.production_schedules || 0}
                        </Typography>
                        <Typography variant="body2" color="text.secondary">
                          Production Schedules Created
                        </Typography>
                      </Grid>
                      <Grid item xs={12} sm={6} md={3}>
                        <Typography variant="h3" color="info.main">
                          {optimizationResult.staff_assignments?.length || 0}
                        </Typography>
                        <Typography variant="body2" color="text.secondary">
                          Staff Assignments
                        </Typography>
                      </Grid>
                      <Grid item xs={12} sm={6} md={3}>
                        <Typography variant="h3" color="warning.main">
                          ${optimizationResult.total_cost?.toFixed(2) || '0.00'}
                        </Typography>
                        <Typography variant="body2" color="text.secondary">
                          Total Cost
                        </Typography>
                      </Grid>
                    </Grid>
                    <Divider sx={{ my: 2 }} />
                    <Chip 
                      label={`Status: ${optimizationResult.optimization_status || 'COMPLETED'}`}
                      color="success"
                      size="large"
                    />
                  </CardContent>
                </Card>
              </Grid>

              {optimizationResult.staff_assignments && optimizationResult.staff_assignments.length > 0 && (
                <Grid item xs={12}>
                  <Card>
                    <CardHeader title="Staff Assignments" />
                    <CardContent>
                      <TableContainer>
                        <Table>
                          <TableHead>
                            <TableRow>
                              <TableCell>Staff Member</TableCell>
                              <TableCell>Task Type</TableCell>
                              <TableCell>Hours</TableCell>
                              <TableCell>Start Time</TableCell>
                              <TableCell>End Time</TableCell>
                              <TableCell>Cost</TableCell>
                            </TableRow>
                          </TableHead>
                          <TableBody>
                            {optimizationResult.staff_assignments.map((assignment, idx) => (
                              <TableRow key={idx}>
                                <TableCell>{assignment.staff_name}</TableCell>
                                <TableCell>
                                  <Chip label={assignment.task_type} size="small" />
                                </TableCell>
                                <TableCell>{assignment.assigned_hours}</TableCell>
                                <TableCell>
                                  {assignment.start_time ? format(new Date(assignment.start_time), 'MM/dd/yyyy HH:mm') : 'N/A'}
                                </TableCell>
                                <TableCell>
                                  {assignment.end_time ? format(new Date(assignment.end_time), 'MM/dd/yyyy HH:mm') : 'N/A'}
                                </TableCell>
                                <TableCell>${assignment.cost?.toFixed(2) || '0.00'}</TableCell>
                              </TableRow>
                            ))}
                          </TableBody>
                        </Table>
                      </TableContainer>
                    </CardContent>
                  </Card>
                </Grid>
              )}
            </Grid>
          ) : (
            <Alert severity="info">
              Run optimization to see results here. Select orders and click "Optimize Schedule".
            </Alert>
          )}
        </Box>
      )}

      {/* Tab 2: Staff Management */}
      {activeTab === 2 && (
        <Box>
          <Card>
            <CardHeader
              title="Staff Members"
              subheader="Manage production staff and their skills"
            />
            <CardContent>
              <Paper sx={{ height: 500, width: '100%' }}>
                {loading ? (
                  <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100%' }}>
                    <CircularProgress />
                  </Box>
                ) : (
                  <DataGrid
                    rows={staff}
                    columns={staffColumns}
                    pageSize={10}
                    rowsPerPageOptions={[10, 25, 50]}
                  />
                )}
              </Paper>
            </CardContent>
          </Card>
        </Box>
      )}

      {/* Tab 3: Task Assignments */}
      {activeTab === 3 && (
        <Box>
          <Card>
            <CardHeader
              title="Task Assignments"
              subheader="View and manage task assignments to staff"
            />
            <CardContent>
              {taskAssignments.length > 0 ? (
                <TableContainer>
                  <Table>
                    <TableHead>
                      <TableRow>
                        <TableCell>Staff</TableCell>
                        <TableCell>Task Type</TableCell>
                        <TableCell>Hours</TableCell>
                        <TableCell>Status</TableCell>
                        <TableCell>Start Time</TableCell>
                        <TableCell>End Time</TableCell>
                      </TableRow>
                    </TableHead>
                    <TableBody>
                      {taskAssignments.map((task) => (
                        <TableRow key={task.id}>
                          <TableCell>{task.staff_name || `Staff #${task.staff_id}`}</TableCell>
                          <TableCell>
                            <Chip label={task.task_type} size="small" />
                          </TableCell>
                          <TableCell>{task.assigned_hours}</TableCell>
                          <TableCell>
                            <Chip 
                              label={task.status} 
                              color={task.status === 'completed' ? 'success' : task.status === 'in_progress' ? 'primary' : 'default'}
                              size="small"
                            />
                          </TableCell>
                          <TableCell>
                            {task.start_time ? format(new Date(task.start_time), 'MM/dd/yyyy HH:mm') : 'N/A'}
                          </TableCell>
                          <TableCell>
                            {task.end_time ? format(new Date(task.end_time), 'MM/dd/yyyy HH:mm') : 'N/A'}
                          </TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </TableContainer>
              ) : (
                <Alert severity="info">
                  No task assignments yet. Run optimization to create assignments.
                </Alert>
              )}
            </CardContent>
          </Card>
        </Box>
      )}

      {/* Create Staff Dialog */}
      <Dialog open={openStaffDialog} onClose={() => setOpenStaffDialog(false)} maxWidth="md" fullWidth>
        <DialogTitle>Add New Staff Member</DialogTitle>
        <DialogContent>
          <Grid container spacing={2} sx={{ mt: 1 }}>
            <Grid item xs={12} sm={6}>
              <TextField
                label="Name"
                fullWidth
                value={newStaff.name}
                onChange={(e) => setNewStaff({...newStaff, name: e.target.value})}
                required
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                label="Employee ID"
                fullWidth
                value={newStaff.employee_id}
                onChange={(e) => setNewStaff({...newStaff, employee_id: e.target.value})}
                required
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                select
                label="Department"
                fullWidth
                value={newStaff.department}
                onChange={(e) => setNewStaff({...newStaff, department: e.target.value})}
              >
                <MenuItem value="production">Production</MenuItem>
                <MenuItem value="quality">Quality Control</MenuItem>
                <MenuItem value="maintenance">Maintenance</MenuItem>
                <MenuItem value="logistics">Logistics</MenuItem>
              </TextField>
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                select
                label="Skill Level"
                fullWidth
                value={newStaff.skill_level}
                onChange={(e) => setNewStaff({...newStaff, skill_level: e.target.value})}
              >
                <MenuItem value="junior">Junior</MenuItem>
                <MenuItem value="intermediate">Intermediate</MenuItem>
                <MenuItem value="senior">Senior</MenuItem>
                <MenuItem value="expert">Expert</MenuItem>
              </TextField>
            </Grid>
            <Grid item xs={12}>
              <TextField
                label="Specialization"
                fullWidth
                value={newStaff.specialization}
                onChange={(e) => setNewStaff({...newStaff, specialization: e.target.value})}
                placeholder="e.g., Assembly, Welding, Quality Control"
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                label="Hourly Rate ($)"
                type="number"
                fullWidth
                value={newStaff.hourly_rate}
                onChange={(e) => setNewStaff({...newStaff, hourly_rate: parseFloat(e.target.value) || 0})}
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                label="Max Hours Per Day"
                type="number"
                fullWidth
                value={newStaff.max_hours_per_day}
                onChange={(e) => setNewStaff({...newStaff, max_hours_per_day: parseInt(e.target.value) || 8})}
              />
            </Grid>
          </Grid>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenStaffDialog(false)}>Cancel</Button>
          <Button onClick={handleCreateStaff} variant="contained" disabled={!newStaff.name || !newStaff.employee_id}>
            Create
          </Button>
        </DialogActions>
      </Dialog>

      {/* Optimization Dialog */}
      <Dialog open={openOptimizeDialog} onClose={() => setOpenOptimizeDialog(false)} maxWidth="sm" fullWidth>
        <DialogTitle>Optimize Production Schedule</DialogTitle>
        <DialogContent>
          <Stack spacing={3} sx={{ mt: 2 }}>
            <TextField
              select
              label="Optimize For"
              fullWidth
              value={optimizationParams.optimize_for}
              onChange={(e) => setOptimizationParams({...optimizationParams, optimize_for: e.target.value})}
            >
              <MenuItem value="time">Minimize Time (Fastest Completion)</MenuItem>
              <MenuItem value="cost">Minimize Cost (Lowest Cost)</MenuItem>
              <MenuItem value="utilization">Maximize Utilization (Best Resource Use)</MenuItem>
            </TextField>
            <TextField
              label="Start Date"
              type="datetime-local"
              fullWidth
              value={optimizationParams.start_date ? format(optimizationParams.start_date, "yyyy-MM-dd'T'HH:mm") : ''}
              onChange={(e) => setOptimizationParams({
                ...optimizationParams, 
                start_date: e.target.value ? new Date(e.target.value) : new Date()
              })}
              InputLabelProps={{ shrink: true }}
            />
            <TextField
              label="End Date"
              type="datetime-local"
              fullWidth
              value={optimizationParams.end_date ? format(optimizationParams.end_date, "yyyy-MM-dd'T'HH:mm") : ''}
              onChange={(e) => setOptimizationParams({
                ...optimizationParams, 
                end_date: e.target.value ? new Date(e.target.value) : new Date(Date.now() + 30 * 24 * 60 * 60 * 1000)
              })}
              InputLabelProps={{ shrink: true }}
            />
            <Alert severity="info">
              Optimizing {selectedOrders.length} order(s). This will create production schedules and assign staff automatically.
            </Alert>
          </Stack>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenOptimizeDialog(false)}>Cancel</Button>
          <Button 
            onClick={handleOptimizeProduction} 
            variant="contained" 
            disabled={optimizing || selectedOrders.length === 0}
            startIcon={optimizing ? <CircularProgress size={20} /> : <AutoAwesomeIcon />}
          >
            {optimizing ? 'Optimizing...' : 'Run Optimization'}
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
}

