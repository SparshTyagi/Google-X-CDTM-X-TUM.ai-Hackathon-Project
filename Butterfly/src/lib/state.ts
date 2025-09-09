// File: src/state.ts
// A simple, global store for our analysis results.

import { Trend } from '@/types'; // Make sure your types are defined in src/types.ts

// This interface defines the shape of our application's state
interface AppState {
  isLoading: boolean;
  error: string | null;
  trends: Trend[];
}

// This is the global state object. We will import and modify it directly.
export const analysisState: AppState = {
  isLoading: false,
  error: null,
  trends: [],
}