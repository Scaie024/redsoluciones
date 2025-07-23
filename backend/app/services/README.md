# Google Sheets Service (v2)

A robust and feature-rich service for interacting with Google Sheets API with built-in error handling, caching, and performance monitoring.

## Features

- **Automatic Reconnection**: Handles connection drops with exponential backoff
- **Intelligent Caching**: Reduces API calls with configurable TTL
- **Circuit Breaker**: Prevents cascading failures
- **Detailed Metrics**: Tracks performance and error rates
- **Retry Mechanism**: Automatic retries with jitter to prevent thundering herd
- **Comprehensive Logging**: Detailed logs for debugging and monitoring
- **Type Hints**: Full Python type annotations for better IDE support

## Installation

1. Install the required dependencies:
   ```bash
   pip install gspread google-auth oauth2client
   ```

2. Set up Google Cloud credentials:
   - Create a service account in Google Cloud Console
   - Download the JSON key file
   - Set the `GOOGLE_APPLICATION_CREDENTIALS` environment variable to point to your key file

## Usage

```python
from app.services.sheets_service_v2 import SheetsServiceV2
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize the service
service = SheetsServiceV2()

# Get all rows
rows = service.get_all_rows()
print(f"Found {len(rows)} rows")

# Add a new row
new_row = {
    'ID': 12345,
    'Name': 'John Doe',
    'Email': 'john@example.com',
    'Status': 'Active'
}
service.add_row(new_row)

# Update a row
service.update_row(12345, {'Status': 'Inactive'})

# Search for rows
results = service.search_rows('John')
print(f"Found {len(results)} matching rows")

# Get performance metrics
metrics = service.get_performance_metrics()
print(f"Average response time: {metrics['response_time']['avg']:.2f}ms")
```

## Configuration

The service can be configured using class constants:

```python
# In your application setup:
from app.services.sheets_service_v2 import SheetsServiceV2

# Customize settings
SheetsServiceV2.DEFAULT_CACHE_TTL = 300  # 5 minutes
SheetsServiceV2.MAX_RETRIES = 5
SheetsServiceV2.INITIAL_RETRY_DELAY = 2  # seconds
```

## Error Handling

The service provides detailed error information through logs. Common exceptions include:

- `CircuitBreakerError`: Raised when the circuit is open
- `GoogleAPIError`: For Google API specific errors
- `ValueError`: For invalid input parameters

## Testing

Run the test suite with:

```bash
# Set up test environment
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/credentials.json"
export TEST_SHEET_ID="your-test-sheet-id"

# Run tests
python -m pytest tests/test_sheets_service_v2.py -v
```

## Performance Monitoring

The service tracks various metrics that can be accessed via:

```python
metrics = service.get_performance_metrics()
print(metrics)
```

Metrics include:
- Total API calls
- Error rates
- Response time percentiles
- Cache hit/miss ratios
- Circuit breaker state

## Best Practices

1. **Reuse Instances**: Create one instance per sheet and reuse it
2. **Cache Wisely**: Use appropriate TTL values based on data volatility
3. **Monitor Metrics**: Regularly check performance metrics to identify bottlenecks
4. **Handle Exceptions**: Always wrap service calls in try/except blocks
5. **Clean Up**: Use context managers or explicit cleanup for long-running processes

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
