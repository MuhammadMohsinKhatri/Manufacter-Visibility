import api from './api';

const shipmentService = {
  /**
   * Get all shipments for selection
   */
  async getShipments() {
    try {
      const response = await api.get('/shipment-tracking/shipments');
      return response.data;
    } catch (error) {
      console.error('Error fetching shipments:', error);
      throw error;
    }
  },

  /**
   * Predict delay for a shipment
   */
  async predictDelay(shipmentId) {
    try {
      const response = await api.post('/shipment-tracking/predict-delay', {
        shipment_id: shipmentId
      });
      return response.data;
    } catch (error) {
      console.error('Error predicting delay:', error);
      throw error;
    }
  },

  /**
   * Get shipment status with AI insights
   */
  async getShipmentStatus(shipmentId) {
    try {
      const response = await api.get(`/shipment-tracking/shipments/${shipmentId}/status`);
      return response.data;
    } catch (error) {
      console.error('Error fetching shipment status:', error);
      throw error;
    }
  }
};

export default shipmentService;

