#!/bin/bash

# Activate the virtual environment
source dash_env/bin/activate

# Run the test suite using pytest
pytest

# Capture the exit code of pytest
exit_code=$?

# Return appropriate exit code
if [ $exit_code -eq 0 ]; then
  echo "All tests passed!"
  exit 0
else
  echo "Some tests failed!"
  exit 1
fi
