import React, { useState, useEffect } from 'react';
import { 
  Box, 
  Container, 
  Typography, 
  TextField, 
  Button, 
  Paper, 
  Avatar, 
  Alert,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Grid,
  Link
} from '@mui/material';
import LockOutlinedIcon from '@mui/icons-material/LockOutlined';
import { useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

export default function Login() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [demoUser, setDemoUser] = useState('');
  
  const { login, isAuthenticated } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  
  // Redirect if already authenticated
  useEffect(() => {
    if (isAuthenticated) {
      const from = location.state?.from?.pathname || '/';
      navigate(from);
    }
  }, [isAuthenticated, navigate, location]);
  
  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    
    try {
      await login(username, password);
      const from = location.state?.from?.pathname || '/';
      navigate(from);
    } catch (err) {
      setError(err.message || 'Failed to login');
    }
  };
  
  const handleDemoLogin = async (e) => {
    e.preventDefault();
    
    if (!demoUser) {
      setError('Please select a demo user');
      return;
    }
    
    try {
      // All demo users have the same password: 'secret'
      await login(demoUser, 'secret');
      const from = location.state?.from?.pathname || '/';
      navigate(from);
    } catch (err) {
      setError(err.message || 'Failed to login with demo user');
    }
  };
  
  return (
    <Container component="main" maxWidth="xs">
      <Box
        sx={{
          marginTop: 8,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
        }}
      >
        <Paper 
          elevation={3} 
          sx={{ 
            p: 4, 
            display: 'flex', 
            flexDirection: 'column', 
            alignItems: 'center',
            width: '100%'
          }}
        >
          <Avatar sx={{ m: 1, bgcolor: 'secondary.main' }}>
            <LockOutlinedIcon />
          </Avatar>
          <Typography component="h1" variant="h5">
            Manufacturing Visibility
          </Typography>
          
          {error && (
            <Alert severity="error" sx={{ mt: 2, width: '100%' }}>
              {error}
            </Alert>
          )}
          
          <Box component="form" onSubmit={handleSubmit} sx={{ mt: 3, width: '100%' }}>
            <TextField
              margin="normal"
              required
              fullWidth
              id="username"
              label="Username"
              name="username"
              autoComplete="username"
              autoFocus
              value={username}
              onChange={(e) => setUsername(e.target.value)}
            />
            <TextField
              margin="normal"
              required
              fullWidth
              name="password"
              label="Password"
              type="password"
              id="password"
              autoComplete="current-password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
            <Button
              type="submit"
              fullWidth
              variant="contained"
              sx={{ mt: 3, mb: 2 }}
            >
              Sign In
            </Button>
          </Box>
          
          <Divider text="OR" />
          
          <Box component="form" onSubmit={handleDemoLogin} sx={{ mt: 2, width: '100%' }}>
            <Typography variant="subtitle1" align="center" gutterBottom>
              Sign in with a demo account
            </Typography>
            
            <FormControl fullWidth margin="normal">
              <InputLabel id="demo-user-label">Select Demo User</InputLabel>
              <Select
                labelId="demo-user-label"
                id="demo-user"
                value={demoUser}
                label="Select Demo User"
                onChange={(e) => setDemoUser(e.target.value)}
              >
                <MenuItem value="admin">Admin User</MenuItem>
                <MenuItem value="sales_manager">Sales Manager</MenuItem>
                <MenuItem value="production_manager">Production Manager</MenuItem>
                <MenuItem value="inventory_manager">Inventory Manager</MenuItem>
                <MenuItem value="sales_rep">Sales Representative</MenuItem>
              </Select>
            </FormControl>
            
            <Button
              type="submit"
              fullWidth
              variant="outlined"
              sx={{ mt: 2, mb: 2 }}
            >
              Sign In with Demo User
            </Button>
            
            <Typography variant="caption" align="center" display="block">
              All demo users have password: "secret"
            </Typography>
          </Box>
        </Paper>
      </Box>
    </Container>
  );
}

// Custom divider with text
function Divider({ text }) {
  return (
    <Grid container alignItems="center" sx={{ my: 2 }}>
      <Grid item xs>
        <Box sx={{ borderBottom: 1, borderColor: 'divider' }} />
      </Grid>
      <Grid item>
        <Typography variant="body2" color="text.secondary" sx={{ px: 2 }}>
          {text}
        </Typography>
      </Grid>
      <Grid item xs>
        <Box sx={{ borderBottom: 1, borderColor: 'divider' }} />
      </Grid>
    </Grid>
  );
}