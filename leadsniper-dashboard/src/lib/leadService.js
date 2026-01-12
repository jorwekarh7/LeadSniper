import mockLeads from './mockLeads.js';

/**
 * @type {boolean} Whether to force mock mode
 */
let mockMode = false;

/**
 * Set mock mode
 * @param {boolean} mode
 */
export function setMockMode(mode) {
  mockMode = mode;
}

/**
 * Fetch leads from API or fallback to mock
 * @returns {Promise<import('./types').Lead[]>}
 */
export async function listLeads() {
  if (mockMode) {
    return Promise.resolve(mockLeads);
  }

  try {
    const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/leads`);
    if (!response.ok) {
      throw new Error('API request failed');
    }
    return await response.json();
  } catch (error) {
    console.warn('API unavailable, falling back to mock data:', error.message);
    return mockLeads;
  }
}

/**
 * Fetch single lead by ID from API or fallback to mock
 * @param {string} id
 * @returns {Promise<import('./types').Lead | null>}
 */
export async function getLead(id) {
  if (mockMode) {
    return Promise.resolve(mockLeads.find(lead => lead.id === id) || null);
  }

  try {
    const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/leads/${id}`);
    if (!response.ok) {
      throw new Error('API request failed');
    }
    return await response.json();
  } catch (error) {
    console.warn('API unavailable, falling back to mock data:', error.message);
    return mockLeads.find(lead => lead.id === id) || null;
  }
}
