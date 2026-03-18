QA Testing Assignment
This repository contains the complete QA testing assignment covering both Manual Exploratory Testing and Automation Testing for two web applications.

📋 Assignment Overview
DetailsObjectiveEvaluate product-level thinking, bug finding ability, and automation skillsSheet 1Manual Exploratory Testing — OrangeHRMSheet 2Automation Testing — SauceDemo

🔍 Sheet 1 — Manual Exploratory Testing (OrangeHRM)
Application: https://opensource-demo.orangehrmlive.com/
Type: Manual Exploratory Testing
Credentials Used: Admin / admin123
What Was Tested

Login & Authentication
Dashboard
Admin Panel / User Management
PIM (Employee Management)
Leave Management
Recruitment Module
Attendance / Punch Timing
Session & Security Behavior

Summary of Findings
SeverityCount🔴 High5🟡 Medium9🟢 Low / Observation4Total18
Key Bugs Found

Normal user can delete and edit Admin accounts (privilege escalation)
Forgot Password accepts any input (name, numbers) and still shows success message
Leave module completely non-functional for regular users
User count in Admin panel is inaccurate (filter shows wrong numbers)
No session timeout — security risk for sensitive HR data
Recruitment records show (Deleted) for hiring managers — data integrity issue

📄 Full report: OrangeHRM_Bug_Report_Sheet1.xlsx

🤖 Sheet 2 — Automation Testing (SauceDemo)
Application: https://www.saucedemo.com/
Framework: Selenium + Python + Pytest
Test File: saucedemo_tests/test_saucedemo.py
Test Results
TC #Test CaseTypeStatusTC01Valid LoginSmoke✅ PASSTC02Invalid LoginFunctional✅ PASSTC03Product Listing ValidationFunctional✅ PASSTC04Add Products to CartFunctional✅ PASSTC05Cart Content ValidationFunctional✅ PASSTC06Checkout Flow (Happy Path)Functional✅ PASSTC07LogoutSmoke✅ PASS
Total: 7 / 7 Passed ✅
Key Observations from Automation

Checkout form accepts invalid postal codes without any validation error
No brute force protection on login — multiple failed attempts not blocked
Back button after logout may restore session — session not fully invalidated
No account lockout mechanism detected for repeated failed logins

📄 Full report: saucedemo_tests/QA_Assignment_Complete.xlsx

🚀 How to Run the Automation Tests
Prerequisites

Python 3.x installed
Google Chrome browser installed

Installation
bashpip install selenium pytest webdriver-manager
Run Tests
bashcd saucedemo_tests
pytest test_saucedemo.py -v
Expected Output
test_saucedemo.py::test_valid_login        PASSED
test_saucedemo.py::test_invalid_login      PASSED
test_saucedemo.py::test_product_listing    PASSED
test_saucedemo.py::test_add_to_cart        PASSED
test_saucedemo.py::test_cart_contents      PASSED
test_saucedemo.py::test_checkout_flow      PASSED
test_saucedemo.py::test_logout             PASSED

7 passed in Xs

📁 Repository Structure
├── README.md
├── OrangeHRM_Bug_Report_Sheet1.xlsx        ← Manual testing report
└── saucedemo_tests/
    ├── test_saucedemo.py                   ← Automation test scripts
    └── QA_Assignment_Complete.xlsx         ← Automation test report
