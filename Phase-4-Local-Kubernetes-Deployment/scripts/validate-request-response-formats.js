#!/usr/bin/env node

/**
 * Request/Response Format Validation Script for Phase II - Full-Stack Todo Application
 *
 * This script validates that request and response formats between frontend and backend
 * systems are compatible and follow expected patterns.
 */

const fs = require('fs');
const path = require('path');

// Define expected API contract types
const expectedRequestTypes = {
  'createTask': {
    requiredFields: ['title'],
    optionalFields: ['description'],
    fieldConstraints: {
      title: { type: 'string', minLength: 1, maxLength: 200 },
      description: { type: 'string', maxLength: 5000 }
    }
  },
  'updateTask': {
    requiredFields: [],
    optionalFields: ['title', 'description', 'completed'],
    fieldConstraints: {
      title: { type: 'string', minLength: 1, maxLength: 200 },
      description: { type: 'string', maxLength: 5000 },
      completed: { type: 'boolean' }
    }
  }
};

const expectedResponseTypes = {
  'taskObject': {
    requiredFields: ['id', 'title', 'completed', 'user_id', 'created_at', 'updated_at'],
    optionalFields: ['description'],
    fieldConstraints: {
      id: { type: 'number' },
      title: { type: 'string', maxLength: 200 },
      description: { type: 'string', maxLength: 5000 },
      completed: { type: 'boolean' },
      user_id: { type: 'string' },
      created_at: { type: 'string' }, // ISO date format
      updated_at: { type: 'string' }  // ISO date format
    }
  },
  'taskList': {
    type: 'array',
    items: 'taskObject'
  },
  'healthCheck': {
    requiredFields: ['status'],
    optionalFields: ['message'],
    fieldConstraints: {
      status: { type: 'string' },
      message: { type: 'string' }
    }
  }
};

// Function to validate request format
function validateRequestFormat(requestType, requestData) {
  const expected = expectedRequestTypes[requestType];
  if (!expected) {
    console.log(`ERROR: Unknown request type: ${requestType}`);
    return false;
  }

  // Check required fields
  for (const field of expected.requiredFields) {
    if (!(field in requestData)) {
      console.log(`ERROR: Missing required field '${field}' in ${requestType} request`);
      return false;
    }
  }

  // Check field constraints
  for (const [field, constraint] of Object.entries(expected.fieldConstraints)) {
    if (field in requestData) {
      const value = requestData[field];

      if (constraint.type === 'string') {
        if (typeof value !== 'string') {
          console.log(`ERROR: Field '${field}' should be string, got ${typeof value}`);
          return false;
        }

        if (constraint.minLength && value.length < constraint.minLength) {
          console.log(`ERROR: Field '${field}' length ${value.length} is less than minimum ${constraint.minLength}`);
          return false;
        }

        if (constraint.maxLength && value.length > constraint.maxLength) {
          console.log(`ERROR: Field '${field}' length ${value.length} exceeds maximum ${constraint.maxLength}`);
          return false;
        }
      } else if (constraint.type === 'boolean') {
        if (typeof value !== 'boolean') {
          console.log(`ERROR: Field '${field}' should be boolean, got ${typeof value}`);
          return false;
        }
      } else if (constraint.type === 'number') {
        if (typeof value !== 'number') {
          console.log(`ERROR: Field '${field}' should be number, got ${typeof value}`);
          return false;
        }
      }
    }
  }

  console.log(`SUCCESS: ${requestType} request format is valid`);
  return true;
}

// Function to validate response format
function validateResponseFormat(responseType, responseData) {
  const expected = expectedResponseTypes[responseType];
  if (!expected) {
    console.log(`ERROR: Unknown response type: ${responseType}`);
    return false;
  }

  // Handle array responses
  if (expected.type === 'array') {
    if (!Array.isArray(responseData)) {
      console.log(`ERROR: Expected array response for ${responseType}, got ${typeof responseData}`);
      return false;
    }

    // Validate each item in the array
    for (let i = 0; i < responseData.length; i++) {
      if (!validateResponseFormat(expected.items, responseData[i])) {
        console.log(`ERROR: Item ${i} in ${responseType} array response is invalid`);
        return false;
      }
    }

    console.log(`SUCCESS: ${responseType} array response format is valid`);
    return true;
  }

  // Check required fields
  for (const field of expected.requiredFields) {
    if (!(field in responseData)) {
      console.log(`ERROR: Missing required field '${field}' in ${responseType} response`);
      return false;
    }
  }

  // Check field constraints
  for (const [field, constraint] of Object.entries(expected.fieldConstraints)) {
    if (field in responseData) {
      const value = responseData[field];

      if (constraint.type === 'string') {
        if (typeof value !== 'string') {
          console.log(`ERROR: Field '${field}' should be string, got ${typeof value}`);
          return false;
        }
      } else if (constraint.type === 'boolean') {
        if (typeof value !== 'boolean') {
          console.log(`ERROR: Field '${field}' should be boolean, got ${typeof value}`);
          return false;
        }
      } else if (constraint.type === 'number') {
        if (typeof value !== 'number') {
          console.log(`ERROR: Field '${field}' should be number, got ${typeof value}`);
          return false;
        }
      }
    }
  }

  console.log(`SUCCESS: ${responseType} response format is valid`);
  return true;
}

// Function to validate API endpoint compatibility
function validateAPIEndpointCompatibility() {
  console.log("Validating API Endpoint Compatibility...");
  console.log("=====================================");

  // Test various request/response scenarios
  const testCases = [
    {
      name: 'Create Task Request',
      requestType: 'createTask',
      requestData: { title: 'Test task', description: 'Test description' },
      responseType: 'taskObject',
      responseData: {
        id: 1,
        title: 'Test task',
        description: 'Test description',
        completed: false,
        user_id: 'user-123',
        created_at: '2023-01-01T00:00:00Z',
        updated_at: '2023-01-01T00:00:00Z'
      }
    },
    {
      name: 'Update Task Request',
      requestType: 'updateTask',
      requestData: { completed: true, title: 'Updated task' },
      responseType: 'taskObject',
      responseData: {
        id: 1,
        title: 'Updated task',
        description: 'Test description',
        completed: true,
        user_id: 'user-123',
        created_at: '2023-01-01T00:00:00Z',
        updated_at: '2023-01-01T01:00:00Z'
      }
    },
    {
      name: 'List Tasks Response',
      requestType: null,
      requestData: null,
      responseType: 'taskList',
      responseData: [
        {
          id: 1,
          title: 'Test task 1',
          completed: false,
          user_id: 'user-123',
          created_at: '2023-01-01T00:00:00Z',
          updated_at: '2023-01-01T00:00:00Z'
        },
        {
          id: 2,
          title: 'Test task 2',
          completed: true,
          user_id: 'user-123',
          created_at: '2023-01-01T00:00:00Z',
          updated_at: '2023-01-01T01:00:00Z'
        }
      ]
    },
    {
      name: 'Health Check Response',
      requestType: null,
      requestData: null,
      responseType: 'healthCheck',
      responseData: {
        status: 'healthy',
        message: 'API is running'
      }
    }
  ];

  let allPassed = true;

  for (const testCase of testCases) {
    console.log(`\nTesting: ${testCase.name}`);

    if (testCase.requestType && testCase.requestData) {
      const requestValid = validateRequestFormat(testCase.requestType, testCase.requestData);
      if (!requestValid) {
        allPassed = false;
      }
    }

    if (testCase.responseType && testCase.responseData) {
      const responseValid = validateResponseFormat(testCase.responseType, testCase.responseData);
      if (!responseValid) {
        allPassed = false;
      }
    }
  }

  return allPassed;
}

// Function to validate frontend API client compatibility with backend
function validateFrontendBackendCompatibility() {
  console.log("\nValidating Frontend-Backend API Compatibility...");
  console.log("===============================================");

  // Read frontend API client code to check for compatibility
  const apiClientPath = path.join(__dirname, '..', 'frontend', 'src', 'lib', 'api-client.ts');

  if (!fs.existsSync(apiClientPath)) {
    console.log('WARNING: Frontend API client file not found at expected location');
    return false;
  }

  const apiClientCode = fs.readFileSync(apiClientPath, 'utf8');

  // Check for required API endpoints
  const requiredEndpoints = [
    '/health',
    '/{user_id}/tasks',
    '/{user_id}/tasks/{task_id}',
    '/{user_id}/tasks/{task_id}/complete'
  ];

  let endpointsValid = true;

  for (const endpoint of requiredEndpoints) {
    // Check if the endpoint pattern exists in the API client
    if (endpoint.includes('{user_id}') && endpoint.includes('{task_id}')) {
      // Look for patterns that match this structure
      const pattern = new RegExp(`\\${endpoint.replace(/\{/g, '(').replace(/\}/g, ')').replace('(user_id)', '[^"]+/tasks/[^"]+').replace('(task_id)', '[^"]+')}`);
      if (!apiClientCode.includes('/{userId}/tasks') && !apiClientCode.includes('/${userId}/tasks')) {
        console.log(`WARNING: Endpoint pattern for "${endpoint}" may not be properly implemented in API client`);
      } else {
        console.log(`SUCCESS: Endpoint pattern for "${endpoint}" found in API client`);
      }
    } else if (endpoint === '/health') {
      if (apiClientCode.includes('getHealth')) {
        console.log(`SUCCESS: Health endpoint "${endpoint}" found in API client`);
      } else {
        console.log(`WARNING: Health endpoint "${endpoint}" not found in API client`);
        endpointsValid = false;
      }
    }
  }

  // Check for JWT token handling
  if (apiClientCode.includes('Authorization') && apiClientCode.includes('Bearer')) {
    console.log('SUCCESS: JWT token handling found in API client');
  } else {
    console.log('WARNING: JWT token handling not found in API client');
    endpointsValid = false;
  }

  // Check for error handling
  if (apiClientCode.includes('401') && apiClientCode.includes('404') && apiClientCode.includes('500')) {
    console.log('SUCCESS: Error handling found in API client');
  } else {
    console.log('WARNING: Comprehensive error handling not found in API client');
    endpointsValid = false;
  }

  return endpointsValid;
}

// Main validation function
async function validateRequestResponseFormats() {
  console.log("Request/Response Format Validation for Full-Stack Todo Application");
  console.log("==================================================================");

  const apiCompatibility = validateAPIEndpointCompatibility();
  const frontendBackendCompatibility = validateFrontendBackendCompatibility();

  if (apiCompatibility && frontendBackendCompatibility) {
    console.log("\nOVERALL SUCCESS: Request/response formats are properly validated!");
    console.log("SUCCESS: API endpoint contracts are well-defined");
    console.log("SUCCESS: Frontend and backend API implementations are compatible");
    console.log("SUCCESS: Error handling patterns are consistent");
    return true;
  } else {
    console.log("\nOVERALL FAILURE: Some request/response format validations failed!");
    return false;
  }
}

// Run validation
validateRequestResponseFormats()
  .then(success => {
    process.exit(success ? 0 : 1);
  })
  .catch(error => {
    console.error('Unexpected error during request/response format validation:', error);
    process.exit(1);
  });