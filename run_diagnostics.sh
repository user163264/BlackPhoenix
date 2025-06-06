#!/bin/bash
# Reset permissions
echo "Setting executable permissions..."
chmod +x fixed_segmented_translation.py
chmod +x test_fixed_function.py

# Run the test
echo "Running the test script..."
python3 test_fixed_function.py

# Make sure the app is using our fixed version
echo
echo "Checking app.py imports..."
grep -n "fixed_segmented_translation" app.py
echo
echo "Testing complete!"
