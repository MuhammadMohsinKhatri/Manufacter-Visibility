import api from './api';

const inventoryService = {
  // Get all components
  getComponents: async () => {
    const response = await api.get('/inventory/components/');
    return response.data;
  },
  
  // Get component by ID
  getComponent: async (id) => {
    const response = await api.get(`/inventory/components/${id}`);
    return response.data;
  },
  
  // Create new component
  createComponent: async (componentData) => {
    const response = await api.post('/inventory/components/', componentData);
    return response.data;
  },
  
  // Get all inventory items
  getInventoryItems: async () => {
    const response = await api.get('/inventory/items/');
    return response.data;
  },
  
  // Get inventory item by ID
  getInventoryItem: async (id) => {
    const response = await api.get(`/inventory/items/${id}`);
    return response.data;
  },
  
  // Get inventory by component ID
  getInventoryByComponent: async (componentId) => {
    const response = await api.get(`/inventory/by-component/${componentId}`);
    return response.data;
  },
  
  // Create new inventory item
  createInventoryItem: async (inventoryData) => {
    const response = await api.post('/inventory/items/', inventoryData);
    return response.data;
  },
  
  // Update inventory item
  updateInventoryItem: async (id, inventoryData) => {
    const response = await api.put(`/inventory/items/${id}`, inventoryData);
    return response.data;
  },
  
  // Allocate inventory
  allocateInventory: async (allocationData) => {
    const response = await api.post('/inventory/allocate', allocationData);
    return response.data;
  },
  
  // Check component availability
  checkAvailability: async (componentId, quantity) => {
    const response = await api.get(`/inventory/check-availability/${componentId}?quantity=${quantity}`);
    return response.data;
  },
  
  // Check product components availability
  checkProductAvailability: async (productId, quantity) => {
    const response = await api.get(`/inventory/check-product-availability/${productId}?quantity=${quantity}`);
    return response.data;
  },
  
  // Get low stock items
  getLowStockItems: async () => {
    const response = await api.get('/inventory/low-stock');
    return response.data;
  }
};

export default inventoryService;