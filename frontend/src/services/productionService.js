import api from './api';

const productionService = {
  // Get all production lines
  getProductionLines: async () => {
    const response = await api.get('/production/lines/');
    return response.data;
  },
  
  // Get production line by ID
  getProductionLine: async (id) => {
    const response = await api.get(`/production/lines/${id}`);
    return response.data;
  },
  
  // Create new production line
  createProductionLine: async (lineData) => {
    const response = await api.post('/production/lines/', lineData);
    return response.data;
  },
  
  // Get all production schedules
  getProductionSchedules: async (params = {}) => {
    const { start_date, end_date, production_line_id, skip, limit } = params;
    let url = '/production/schedules/';
    
    // Add query parameters if provided
    const queryParams = new URLSearchParams();
    if (start_date) queryParams.append('start_date', start_date.toISOString());
    if (end_date) queryParams.append('end_date', end_date.toISOString());
    if (production_line_id) queryParams.append('production_line_id', production_line_id);
    if (skip) queryParams.append('skip', skip);
    if (limit) queryParams.append('limit', limit);
    
    const queryString = queryParams.toString();
    if (queryString) {
      url += `?${queryString}`;
    }
    
    const response = await api.get(url);
    return response.data;
  },
  
  // Get production schedule by ID
  getProductionSchedule: async (id) => {
    const response = await api.get(`/production/schedules/${id}`);
    return response.data;
  },
  
  // Create new production schedule
  createProductionSchedule: async (scheduleData) => {
    const response = await api.post('/production/schedules/', scheduleData);
    return response.data;
  },
  
  // Update production schedule
  updateProductionSchedule: async (id, scheduleData) => {
    const response = await api.put(`/production/schedules/${id}`, scheduleData);
    return response.data;
  },
  
  // Check production capacity
  checkCapacity: async (capacityCheckData) => {
    const response = await api.post('/production/check-capacity', capacityCheckData);
    return response.data;
  },
  
  // Estimate production time
  estimateProductionTime: async (productId, quantity) => {
    const response = await api.get(`/production/estimate-time/${productId}?quantity=${quantity}`);
    return response.data;
  }
};

export default productionService;