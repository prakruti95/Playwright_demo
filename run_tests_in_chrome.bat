@echo off
title Northline Store Automation - Live Chrome Test Runner
echo =====================================================================
echo  Running Northline Store E2E Tests Visibly in Google Chrome...
echo =====================================================================
echo.
cd /d "C:\Users\tops\Desktop\northline-store-automation"
python -m pytest tests/e2e/test_order_confirmation.py tests/e2e/test_cart_operations.py tests/e2e/test_filters_sorting.py --headed --browser-channel chrome --slowmo 500 -v
echo.
echo Opening interactive test report in Google Chrome...
start chrome "%cd%\test-results\report.html"
echo.
echo =====================================================================
echo  Execution Complete! Press any key to exit.
echo =====================================================================
pause
