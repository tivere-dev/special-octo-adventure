import api from './api';

export const businessService = {
  setupBusiness: async (businessName, currency, logo = null) => {
    const formData = new FormData();
    formData.append('business_name', businessName);
    formData.append('currency', currency);
    if (logo) {
      formData.append('business_logo', logo);
    }

    const response = await api.post('/business/setup/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  getBusiness: async () => {
    const response = await api.get('/business/me/');
    return response.data;
  },

  updateBusiness: async (data) => {
    const formData = new FormData();
    
    if (data.business_name) {
      formData.append('business_name', data.business_name);
    }
    if (data.currency) {
      formData.append('currency', data.currency);
    }
    if (data.business_logo) {
      formData.append('business_logo', data.business_logo);
    }

    const response = await api.put('/business/update/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },
};
