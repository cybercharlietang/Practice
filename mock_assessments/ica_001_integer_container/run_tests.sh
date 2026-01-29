#!/bin/bash
# Run tests for Integer Container assessment

echo "=========================================="
echo "Integer Container - Test Runner"
echo "=========================================="
echo ""

cd "$(dirname "$0")"

# Check if pytest is available, fall back to unittest
if command -v pytest &> /dev/null; then
    echo "Running with pytest..."
    echo ""
    
    if [ "$1" == "1" ]; then
        echo "Level 1 Tests:"
        pytest tests/level_1_tests.py -v
    elif [ "$1" == "2" ]; then
        echo "Level 2 Tests:"
        pytest tests/level_2_tests.py -v
    elif [ "$1" == "sandbox" ]; then
        echo "Sandbox Tests:"
        pytest sandbox_tests.py -v
    else
        echo "All Tests:"
        pytest tests/ sandbox_tests.py -v
    fi
else
    echo "Running with unittest..."
    echo ""
    
    if [ "$1" == "1" ]; then
        echo "Level 1 Tests:"
        python -m unittest tests.level_1_tests -v
    elif [ "$1" == "2" ]; then
        echo "Level 2 Tests:"
        python -m unittest tests.level_2_tests -v
    elif [ "$1" == "sandbox" ]; then
        echo "Sandbox Tests:"
        python -m unittest sandbox_tests -v
    else
        echo "All Tests:"
        python -m unittest discover -s tests -v
        python -m unittest sandbox_tests -v
    fi
fi

echo ""
echo "=========================================="
echo "Test run complete"
echo "=========================================="
