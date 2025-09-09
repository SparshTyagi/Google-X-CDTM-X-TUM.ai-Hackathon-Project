// File: src/api.ts (Corrected and Final Version)

import { Trend, Subtrend, Startup } from '@/types';
import { analysisState } from './state'; // Import our new state store

// --- Configuration ---
// These are the details for your live, deployed backend.
const API_BASE_URL = "https://trend-agent-api-launch-703557862737.europe-west1.run.app";

// CRITICAL: You must replace this placeholder with the actual secret key from your deployment command.
const API_KEY = "your-super-secret-key"; 

// The frontend timeout MUST be equal to or longer than the backend timeout (900s).
const API_TIMEOUT = 900 * 1000;

// ====================================================================================
// THE ONLY FUNCTION THAT MAKES A NETWORK CALL
// ====================================================================================

/**
 * Triggers the full analysis on the backend, fetches the complete data structure,
 * and stores it in the local analysisState for fast access by the UI.
 * Your UI should call this function once when the analysis needs to start.
 */
export const runFullAnalysis = async (): Promise<void> => {
  // 1. Set the global loading state so your UI can show a spinner.
  analysisState.isLoading = true;
  analysisState.error = null;
  console.log("Starting full analysis... This may take several minutes.");

  try {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), API_TIMEOUT);

    // 2. Call the backend's single 'analyze' endpoint.
    const response = await fetch(`${API_BASE_URL}/analyze`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-API-KEY": API_KEY,
      },
      signal: controller.signal,
    });
    
    clearTimeout(timeoutId);

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || `Server returned an error: ${response.statusText}`);
    }

    const result = await response.json();
    
    // 3. The backend returns a JSON object where the 'report' field is a STRING.
    // We must parse this inner string to get the actual data object.
    const reportData = JSON.parse(result.report);

    // 4. Store the successful result in our global state.
    analysisState.trends = reportData.trends || [];
    console.log("Analysis complete. Data stored locally.", analysisState.trends);
    
  } catch (error) {
    const errorMessage = error instanceof Error ? error.message : "An unknown error occurred.";
    console.error("Failed to run full analysis:", errorMessage);
    analysisState.error = errorMessage;
    analysisState.trends = []; // Clear any stale data on error
  } finally {
    // 5. Always set loading to false when the process is finished.
    analysisState.isLoading = false;
  }
};

// ====================================================================================
// FUNCTIONS TO READ DATA FROM THE LOCAL STATE (INSTANTANEOUS)
// ====================================================================================

/**
 * Gets the top-level trends from the local state. Does NOT make a network call.
 */
export const getTrends = async (limit?: number): Promise<Trend[]> => {
  const trends = analysisState.trends;
  return limit ? trends.slice(0, limit) : trends;
};

/**
 * Gets the subtrends for a specific trend ID from the local state.
 */
export const getSubtrends = async (trendId: string): Promise<Subtrend[]> => {
  const trend = analysisState.trends.find(t => t.id === trendId);
  return trend ? trend.subtrends : [];
};

/**
 * Gets the startups for a specific subtrend ID from the local state.
 */
export const getStartups = async (subtrendId: string): Promise<Startup[]> => {
  // Search through all trends and their subtrends to find the matching one.
  for (const trend of analysisState.trends) {
    const subtrend = trend.subtrends.find(st => st.id === subtrendId);
    if (subtrend) {
      return subtrend.startups;
    }
  }
  return []; // Return empty if not found
};