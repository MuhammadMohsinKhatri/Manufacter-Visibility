import api from './api';

const orderService = {
  // Get all orders
  getOrders: async () => {
    const response = await api.get('/orders/');
    return response.data;
  },
  
  // Get order by ID
  getOrder: async (id) => {
    const response = await api.get(`/orders/${id}`);
    return response.data;
  },
  
  // Create new order
  createOrder: async (orderData) => {
    const response = await api.post('/orders/', orderData);
    return response.data;
  },
  
  // Update order
  updateOrder: async (id, orderData) => {
    const response = await api.put(`/orders/${id}`, orderData);
    return response.data;
  },
  
  // Delete order
  deleteOrder: async (id) => {
    const response = await api.delete(`/orders/${id}`);
    return response.data;
  },
  
  // Check order feasibility
  checkFeasibility: async (checkData) => {
    const response = await api.post('/orders/check-feasibility', checkData);
    return response.data;
  }
};

export default orderService;