import type { Task, TaskCreate, TaskUpdate, ErrorResponse } from "@/types/api";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

// Store JWT token from Better Auth
let jwtToken: string | null = null;

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
 * Fetch wrapper that injects JWT token and handles errors
 */
async function apiFetch<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const headers: HeadersInit = {
    "Content-Type": "application/json",
    ...options.headers,
  };

  // Add JWT token if available
  if (jwtToken) {
    (headers as Record<string, string>)["Authorization"] = `Bearer ${jwtToken}`;
  }

  // Add timeout (5 seconds)
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), 5000);
  options.signal = controller.signal;

  try {
    const response = await fetch(`${API_URL}${endpoint}`, {
      ...options,
      headers,
      signal: controller.signal,
    });

    clearTimeout(timeoutId);

    if (!response.ok) {
      // Handle 401 Unauthorized - redirect to login
      if (response.status === 401) {
        jwtToken = null;
        if (typeof window !== "undefined") {
          window.location.href = "/login";
        }
        throw new Error("Unauthorized - please log in again");
      }

      // Handle 404 Not Found
      if (response.status === 404) {
        const error: ErrorResponse = await response.json().catch(() => ({
          error: "Not found",
          message: "Resource not found",
        }));
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
        throw new Error("Server error - please try again later");
      }

      // Other errors
      const error: ErrorResponse = await response.json().catch(() => ({
        error: "Unknown error",
        message: "API request failed",
      }));
      throw new Error(error.message || "API request failed");
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
  }
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
 */
export async function deleteTask(userId: string, taskId: number): Promise<void> {
  return apiFetch(`/${userId}/tasks/${taskId}`, {
    method: "DELETE",
  });
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
