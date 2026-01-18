import api from './api';

const supplyChainService = {
  // Get external risks
  getExternalRisks: async (params = {}) => {
    const { risk_type, region, start_date, end_date, skip, limit } = params;
    let url = '/supply-chain/risks/';
    
    // Add query parameters if provided
    const queryParams = new URLSearchParams();
    if (risk_type) queryParams.append('risk_type', risk_type);
    if (region) queryParams.append('region', region);
    if (start_date) queryParams.append('start_date', start_date.toISOString());
    if (end_date) queryParams.append('end_date', end_date.toISOString());
    if (skip) queryParams.append('skip', skip);
    if (limit) queryParams.append('limit', limit);
    
    const queryString = queryParams.toString();
    if (queryString) {
      url += `?${queryString}`;
    }
    
    const response = await api.get(url);
    return response.data;
  },
  
  // Create new external risk
  createExternalRisk: async (riskData) => {
    const response = await api.post('/supply-chain/risks/', riskData);
    return response.data;
  },
  
  // Update external risks from all sources
  updateExternalRisks: async () => {
    const response = await api.post('/supply-chain/update-risks/');
    return response.data;
  },
  
  // Assess supply chain risks
  assessRisks: async (assessmentData) => {
    const response = await api.post('/supply-chain/assess-risks/', assessmentData);
    return response.data;
  }
};

export default supplyChainService;