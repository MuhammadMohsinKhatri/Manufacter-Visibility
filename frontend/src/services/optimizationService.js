import api from './api';

const optimizationService = {
  /**
   * Optimize production schedule for multiple orders
   */
  async optimizeProductionSchedule(orderIds, startDate, endDate, objectives = null) {
    try {
      const response = await api.post('/optimization/production-schedule', {
        order_ids: orderIds,
        start_date: startDate instanceof Date ? startDate.toISOString() : startDate,
        end_date: endDate instanceof Date ? endDate.toISOString() : endDate,
        objectives: objectives
      });
      return response.data;
    } catch (error) {
      console.error('Error optimizing production schedule:', error);
      throw error;
    }
  },

  /**
   * Optimize staff assignment for production tasks
   */
  async optimizeStaffAssignment(productionScheduleId, taskRequirements) {
    try {
      const response = await api.post('/optimization/staff-assignment', {
        production_schedule_id: productionScheduleId,
        task_requirements: taskRequirements
      });
      return response.data;
    } catch (error) {
      console.error('Error optimizing staff assignment:', error);
      throw error;
    }
  },

  /**
   * Complete order fulfillment optimization
   */
  async optimizeOrderFulfillment(orderIds, optimizeFor = 'time', startDate = null, endDate = null) {
    try {
      const payload = {
        order_ids: orderIds,
        optimize_for: optimizeFor
      };
      
      // Add dates if provided
      if (startDate) {
        payload.start_date = startDate instanceof Date ? startDate.toISOString() : startDate;
      }
      if (endDate) {
        payload.end_date = endDate instanceof Date ? endDate.toISOString() : endDate;
      }
      
      const response = await api.post('/optimization/order-fulfillment', payload);
      return response.data;
    } catch (error) {
      console.error('Error optimizing order fulfillment:', error);
      throw error;
    }
  },

  /**
   * Staff Management
   */
  async getStaff(department = null, isAvailable = null) {
    try {
      const params = {};
      if (department) params.department = department;
      if (isAvailable !== null) params.is_available = isAvailable;
      
      const response = await api.get('/optimization/staff', { params });
      return response.data;
    } catch (error) {
      console.error('Error fetching staff:', error);
      throw error;
    }
  },

  async createStaff(staffData) {
    try {
      const response = await api.post('/optimization/staff', staffData);
      return response.data;
    } catch (error) {
      console.error('Error creating staff:', error);
      throw error;
    }
  },

  async updateStaff(staffId, staffData) {
    try {
      const response = await api.put(`/optimization/staff/${staffId}`, staffData);
      return response.data;
    } catch (error) {
      console.error('Error updating staff:', error);
      throw error;
    }
  },

  async getStaffWorkload(staffId) {
    try {
      const response = await api.get(`/optimization/staff/${staffId}/workload`);
      return response.data;
    } catch (error) {
      console.error('Error fetching staff workload:', error);
      throw error;
    }
  },

  async getTaskAssignments(productionScheduleId = null, staffId = null, status = null) {
    try {
      const params = {};
      if (productionScheduleId) params.production_schedule_id = productionScheduleId;
      if (staffId) params.staff_id = staffId;
      if (status) params.status = status;
      
      const response = await api.get('/optimization/task-assignments', { params });
      return response.data;
    } catch (error) {
      console.error('Error fetching task assignments:', error);
      throw error;
    }
  }
};

export default optimizationService;

