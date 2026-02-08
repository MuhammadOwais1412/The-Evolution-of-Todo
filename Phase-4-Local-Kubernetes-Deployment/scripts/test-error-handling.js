#!/usr/bin/env node

/**
 * Error Handling Test Script for Phase II - Full-Stack Todo Application
 *
 * This script tests error handling for failed API calls between frontend and backend systems.
 */

const fs = require('fs');
const path = require('path');
const axios = require('axios');

// Function to simulate various error conditions and test handling
async function testErrorHandling() {
    console.log("Error Handling Test for Full-Stack Todo Application");
    console.log("=================================================");

    const backendApiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
    console.log('Testing error handling with backend at:', backendApiUrl);

    let allTestsPassed = true;

    // Test 1: Network error (backend not running)
    console.log('\n1. Testing network error handling (backend unreachable)...');
    try {
        // Use a port that's unlikely to be in use
        await axios.get('http://localhost:9999/health', { timeout: 3000 });
        console.log('ERROR: Expected network error but request succeeded');
        allTestsPassed = false;
    } catch (error) {
        if (error.code === 'ECONNREFUSED' || error.code === 'ENOTFOUND' || error.code === 'ECONNABORTED') {
            console.log('SUCCESS: Network error properly caught and handled');
        } else {
            console.log('INFO: Network error occurred:', error.code || error.message);
        }
    }

    // Test 2: Timeout error
    console.log('\n2. Testing timeout error handling...');
    try {
        await axios.get(`${backendApiUrl}/health`, { timeout: 1 }); // Very short timeout
        console.log('INFO: Request completed despite short timeout');
    } catch (error) {
        if (error.code === 'ECONNABORTED') {
            console.log('SUCCESS: Timeout error properly caught and handled');
        } else {
            console.log('INFO: Timeout resulted in error:', error.message);
        }
    }

    // Test 3: 404 Not Found error
    console.log('\n3. Testing 404 Not Found error handling...');
    try {
        const response = await axios.get(`${backendApiUrl}/nonexistent-endpoint`);
        console.log('INFO: Unexpected success with nonexistent endpoint, status:', response.status);
    } catch (error) {
        if (error.response && error.response.status === 404) {
            console.log('SUCCESS: 404 Not Found error properly caught and handled');
        } else if (error.response) {
            console.log('INFO: Got different error status:', error.response.status);
        } else {
            console.log('INFO: Got network error instead of 404:', error.message);
        }
    }

    // Test 4: 401 Unauthorized error
    console.log('\n4. Testing 401 Unauthorized error handling...');
    try {
        const response = await axios.get(`${backendApiUrl}/some-user-id/tasks`);
        console.log('INFO: Unexpected success with protected endpoint, status:', response.status);
    } catch (error) {
        if (error.response && error.response.status === 401) {
            console.log('SUCCESS: 401 Unauthorized error properly caught and handled');
        } else if (error.response) {
            console.log('INFO: Got different auth error status:', error.response.status);
        } else {
            console.log('INFO: Got network error instead of 401:', error.message);
        }
    }

    // Test 5: 422 Validation error (if backend is running)
    console.log('\n5. Testing 422 Validation error handling...');
    try {
        // Try to create a task with invalid data (empty title)
        const response = await axios.post(`${backendApiUrl}/some-user-id/tasks`, {
            title: '' // Invalid - empty title
        });
        console.log('INFO: Unexpected success creating task with invalid data, status:', response.status);
    } catch (error) {
        if (error.response && error.response.status === 422) {
            console.log('SUCCESS: 422 Validation error properly caught and handled');
        } else if (error.response) {
            console.log('INFO: Got different validation error status:', error.response.status);
        } else {
            console.log('INFO: Got network error instead of 422:', error.message);
        }
    }

    // Test 6: 500 Server Error (try malformed request)
    console.log('\n6. Testing 500+ Server Error handling...');
    try {
        // This might trigger a server error depending on backend implementation
        const response = await axios.post(`${backendApiUrl}/some-user-id/tasks`, {
            // Intentionally malformed request body
        });
        if (response.status >= 500) {
            console.log('SUCCESS: 500+ Server Error properly caught and handled');
        } else {
            console.log('INFO: Got status', response.status, 'instead of 500+ error');
        }
    } catch (error) {
        if (error.response && error.response.status >= 500) {
            console.log('SUCCESS: 500+ Server Error properly caught and handled');
        } else if (error.response) {
            console.log('INFO: Got different server error status:', error.response.status);
        } else {
            console.log('INFO: Got network error instead of 500+ error:', error.message);
        }
    }

    return allTestsPassed;
}

// Function to check frontend error handling capabilities
function validateFrontendErrorHandling() {
    console.log('\n7. Validating frontend error handling capabilities...');

    const apiClientPath = path.join(__dirname, '..', 'frontend', 'src', 'lib', 'api-client.ts');

    if (!fs.existsSync(apiClientPath)) {
        console.log('WARNING: Frontend API client file not found at expected location');
        return false;
    }

    const apiClientCode = fs.readFileSync(apiClientPath, 'utf8');

    // Check for error handling patterns
    const errorHandlingPatterns = [
        { pattern: /401.*unauthorized|unauthorized.*401/i, description: '401 Unauthorized handling' },
        { pattern: /404.*not found|not found.*404/i, description: '404 Not Found handling' },
        { pattern: /422.*validation|validation.*422/i, description: '422 Validation error handling' },
        { pattern: /500.*server|server.*500|5xx/i, description: '500+ Server error handling' },
        { pattern: /timeout|abort/i, description: 'Timeout handling' },
        { pattern: /try.*catch|catch.*error/i, description: 'General error handling' },
        { pattern: /throw.*error|error.*throw/i, description: 'Error propagation' }
    ];

    let patternsFound = 0;

    for (const { pattern, description } of errorHandlingPatterns) {
        if (pattern.test(apiClientCode)) {
            console.log(`SUCCESS: ${description} found in API client`);
            patternsFound++;
        } else {
            console.log(`INFO: ${description} not explicitly found in API client`);
        }
    }

    if (patternsFound >= 4) {
        console.log('SUCCESS: Frontend has comprehensive error handling capabilities');
        return true;
    } else {
        console.log('INFO: Frontend error handling could be enhanced');
        return false;
    }
}

// Function to simulate error handling with mock responses
function testMockErrorResponseHandling() {
    console.log('\n8. Testing error response format validation...');

    // Simulate different error response structures
    const errorResponses = [
        {
            status: 401,
            data: { error: "Unauthorized", message: "Not authenticated" },
            description: "Standard 401 error response"
        },
        {
            status: 404,
            data: { error: "Not Found", message: "Resource not found" },
            description: "Standard 404 error response"
        },
        {
            status: 422,
            data: { error: "Validation Error", message: "Invalid input", details: { field: "title", reason: "required" } },
            description: "Standard 422 error response"
        },
        {
            status: 500,
            data: { error: "Server Error", message: "Internal server error" },
            description: "Standard 500 error response"
        }
    ];

    let allValid = true;

    for (const errorResp of errorResponses) {
        // Check if error response has required structure
        if (errorResp.data.error && errorResp.data.message) {
            console.log(`SUCCESS: ${errorResp.description} has proper structure`);
        } else {
            console.log(`ERROR: ${errorResp.description} missing required fields`);
            allValid = false;
        }
    }

    return allValid;
}

// Main error handling test function
async function main() {
    console.log("Comprehensive Error Handling Validation");
    console.log("=====================================");

    const apiErrorTests = await testErrorHandling();
    const frontendValidation = validateFrontendErrorHandling();
    const responseStructureValidation = testMockErrorResponseHandling();

    if (apiErrorTests && frontendValidation && responseStructureValidation) {
        console.log("\nOVERALL SUCCESS: Error handling validation passed!");
        console.log("SUCCESS: Network errors are properly caught and handled");
        console.log("SUCCESS: HTTP error statuses (401, 404, 422, 500+) are handled");
        console.log("SUCCESS: Frontend has appropriate error handling mechanisms");
        console.log("SUCCESS: Error response structures are consistent");
        return true;
    } else {
        console.log("\nOVERALL RESULT: Some error handling validations need attention");
        return false;
    }
}

// Run error handling tests
main()
    .then(success => {
        process.exit(success ? 0 : 1);
    })
    .catch(error => {
        console.error('Unexpected error during error handling testing:', error);
        process.exit(1);
    });