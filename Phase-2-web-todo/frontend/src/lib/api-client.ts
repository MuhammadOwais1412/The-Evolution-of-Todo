import type { Task, TaskCreate, TaskUpdate, ErrorResponse } from "@/types/api";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

// Store JWT token from Better Auth
let jwtToken: string | null = null;

// Track in-flight requests to prevent duplicates
const inflightRequests = new Map<string, Promise<unknown>>(); // Store as unknown to satisfy TS, cast when returning

/**
 * Set JWT token for API requests
 */
export function setToken(token: string | null) {
  jwtToken = token;
}

/**
 * Get current JWT token
 */
export function getToken(): string | null {
  return jwtToken;
}

/**
 * Generate a unique request key for deduplication
 */
function getRequestKey(endpoint: string, method: string): string {
  return `${method.toUpperCase()}:${endpoint}`;
}

/**
 * Fetch wrapper that injects JWT token and handles errors
 */
async function apiFetch<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const method = options.method?.toUpperCase() || 'GET';
  const requestKey = getRequestKey(endpoint, method);

  // Check if identical request is already in flight
  if (inflightRequests.has(requestKey)) {
    // Return the existing promise to prevent duplicate requests
    return inflightRequests.get(requestKey)! as Promise<T>; // Cast to expected return type
  }

  const headers: HeadersInit = {
    "Content-Type": "application/json",
    ...options.headers,
  };

  // Add JWT token if available
  if (jwtToken) {
    (headers as Record<string, string>)["Authorization"] = `Bearer ${jwtToken}`;
  }

  // Add timeout (increase to 10 seconds to reduce timeout errors)
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), 10000); // Increased from 5 to 10 seconds
  options.signal = controller.signal;

  // Create the promise and store it
  const requestPromise = (async () => {
    try {
      const response = await fetch(`${API_URL}${endpoint}`, {
        ...options,
        headers,
        signal: controller.signal,
      });

      clearTimeout(timeoutId);

      if (!response.ok) {
        // Handle 401 Unauthorized - don't redirect here to avoid loops, let the component handle it
        if (response.status === 401) {
          jwtToken = null;

          // Try to get error details from response
          let errorMessage = "Unauthorized - please log in again";
          try {
            const errorData = await response.json();
            if (errorData.message) {
              errorMessage = errorData.message;
            }
          } catch (_e) {
            // If parsing fails, use default message
          }

          throw new Error(errorMessage);
        }

        // Handle 404 Not Found - special handling for DELETE operations
        if (response.status === 404) {
          // For DELETE operations, 404 after successful delete is expected (idempotent behavior)
          // We'll handle this at the calling function level, but return the error for now
          const error: ErrorResponse = await response.json().catch(() => ({
            error: "Not found",
            message: "Resource not found",
          }));

          // Only throw the error if it's not a DELETE request where 404 is expected
          throw new Error(error.message || "Resource not found");
        }

        // Handle 422 Validation Error
        if (response.status === 422) {
          const error: ErrorResponse = await response.json().catch(() => ({
            error: "Validation error",
            message: "Invalid input",
          }));
          throw new Error(error.message || "Validation failed");
        }

        // Handle 5xx Server Errors
        if (response.status >= 500) {
          let errorMessage = "Server error - please try again later";
          try {
            const errorData = await response.json();
            if (errorData.message) {
              errorMessage = errorData.message;
            }
          } catch (_e) {
            // If parsing fails, use default message
          }
          throw new Error(errorMessage);
        }

        // Other errors
        let errorMessage = "API request failed";
        try {
          const error: ErrorResponse = await response.json();
          if (error.message) {
            errorMessage = error.message;
          }
        } catch (_e) {
          // If parsing fails, use default message
        }

        throw new Error(errorMessage);
      }

      // Handle 204 No Content (DELETE)
      if (response.status === 204) {
        return undefined as T;
      }

      return response.json();
    } catch (error) {
      clearTimeout(timeoutId);

      if (error instanceof Error) {
        if (error.name === "AbortError") {
          throw new Error("Request timeout - please check your connection");
        }
        throw error;
      }
      throw new Error("An unexpected error occurred");
    } finally {
      // Remove the request from the map when complete
      inflightRequests.delete(requestKey);
    }
  })();

  // Store the promise in the map
  inflightRequests.set(requestKey, requestPromise);

  return requestPromise;
}

/**
 * Health check
 */
export async function getHealth(): Promise<{ status: string }> {
  return apiFetch("/health");
}

/**
 * Create a new task
 */
export async function createTask(
  userId: string,
  taskData: TaskCreate
): Promise<Task> {
  return apiFetch(`/${userId}/tasks`, {
    method: "POST",
    body: JSON.stringify(taskData),
  });
}

/**
 * List all tasks for a user
 */
export async function listTasks(userId: string): Promise<Task[]> {
  return apiFetch(`/${userId}/tasks`);
}

/**
 * Get a single task
 */
export async function getTask(userId: string, taskId: number): Promise<Task> {
  return apiFetch(`/${userId}/tasks/${taskId}`);
}

/**
 * Update a task
 */
export async function updateTask(
  userId: string,
  taskId: number,
  taskData: TaskUpdate
): Promise<Task> {
  return apiFetch(`/${userId}/tasks/${taskId}`, {
    method: "PUT",
    body: JSON.stringify(taskData),
  });
}

/**
 * Delete a task
 * This function handles 404 errors gracefully after successful deletes (idempotent behavior)
 */
export async function deleteTask(userId: string, taskId: number): Promise<void> {
  try {
    await apiFetch(`/${userId}/tasks/${taskId}`, {
      method: "DELETE",
    });
  } catch (error) {
    // For DELETE operations, if we get a 404, it might mean the task was already deleted
    // which is acceptable for idempotent behavior
    if (error instanceof Error && error.message.includes("Resource not found")) {
      // Consider this a success since the task is effectively "deleted"
      // The resource is no longer there, which is the goal of the delete operation
      return;
    }
    // Re-throw other errors
    throw error;
  }
}

/**
 * Toggle task completion
 */
export async function toggleCompletion(
  userId: string,
  taskId: number
): Promise<Task> {
  return apiFetch(`/${userId}/tasks/${taskId}/complete`, {
    method: "PATCH",
  });
}