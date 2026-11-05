# Northline Store Automation — Requirements Specification & Audit

This document formally details all 24 requirements specified in the QA Automation Engineering Assignment and audits their implementation, verification method, and compliance status.

---

## 1. Requirements Compliance Matrix

| ID | Requirement Statement | Category | Compliance Status | Verified Artifact / Test Evidence |
| :---: | :--- | :---: | :---: | :--- |
| **REQ-01** | **Python 3.11+ Compatibility** | Environment | **PASS** | Verified on Python 3.14.8 locally; CI configured with `python-version: "3.11"`. |
| **REQ-02** | **Playwright with Pytest** | Framework | **PASS** | `playwright 1.64.1` with `pytest-playwright 0.10.0` and `pytest 9.2.0`. |
| **REQ-03** | **Page Object Model (POM)** | Architecture | **PASS** | 8 POM classes located in `framework/pages/` inheriting from `BasePage`. |
| **REQ-04** | **Reusable Fixtures & Test Data** | Architecture | **PASS** | Fixtures in `tests/conftest.py`; synthetic credentials & financial constants in `framework/config.py`. |
| **REQ-05** | **$\ge$ 20 Meaningful E2E Tests** | E2E Testing | **PASS** | **39 E2E tests** implemented across 9 suites covering user journeys end-to-end. |
| **REQ-06** | **$\ge$ 8 Meaningful API Tests** | API Testing | **PASS** | **19 API tests** (14 MockAPI endpoints + 5 Storefront contracts & route mocking). |
| **REQ-07** | **Correct Pytest Markers** | Test Runner | **PASS** | Configured in `pytest.ini` (`smoke`, `e2e`, `api`, `regression`, `catalog`, `cart`, `checkout`, `mobile`). |
| **REQ-08** | **Website Discovery Document** | Documentation | **PASS** | `docs/WEBSITE_DISCOVERY.md` detailing real UI elements, navigation, PDP, drawer, and checkout. |
| **REQ-09** | **API Inventory Document** | Documentation | **PASS** | `docs/API_INVENTORY.md` detailing `/catalog.json`, live Netlify edge behavior, and MockAPI schema. |
| **REQ-10** | **Test Plan Document** | Documentation | **PASS** | `docs/TEST_PLAN.md` with test strategy, test matrix, locator dictionary, and risks. |
| **REQ-11** | **Multi-Browser Coverage** | Browser Engines | **PASS** | Cross-engine verification across Chromium, Firefox, and WebKit (Safari). |
| **REQ-12** | **Mobile Responsive ($390\times844$)** | Responsive | **PASS** | `tests/e2e/test_mobile_responsive.py` with iPhone 13 dimensions (`390x844`), testing drawer and filters. |
| **REQ-13** | **GitHub Actions Matrix** | DevOps | **PASS** | `.github/workflows/tests.yml` with strategy matrix `[chromium, firefox, webkit]`. |
| **REQ-14** | **Multi-Trigger CI Pipeline** | DevOps | **PASS** | Triggers on `push` to `main`, `pull_request` to `main`, `workflow_dispatch`, and nightly `cron: '0 2 * * *'`. |
| **REQ-15** | **Smoke Tests Before Regression** | DevOps | **PASS** | `e2e-regression-tests` job gates on `needs: [smoke-tests]` in GitHub Actions. |
| **REQ-16** | **API Tests in Separate Stage** | DevOps | **PASS** | `api-tests` is isolated into its own independent job with dedicated reporting. |
| **REQ-17** | **Pytest HTML Reports** | Reporting | **PASS** | Configured with `--html=test-results/report.html --self-contained-html`. |
| **REQ-18** | **Failure Screenshots & Traces** | Diagnostics | **PASS** | Captured on failure (`tests/conftest.py` hook); individual Playwright traces zipped per test. |
| **REQ-19** | **CI Artifacts per Browser** | DevOps | **PASS** | Unique artifact names: `smoke-artifacts-${{ matrix.browser }}`, `e2e-artifacts-${{ matrix.browser }}`, `api-test-report`. |
| **REQ-20** | **No Hard-coded Sleeps** | Code Quality | **PASS** | Zero `time.sleep()` calls; strict usage of Playwright auto-waiting and locator `.wait_for()`. |
| **REQ-21** | **Role/Label/Test-ID Locators** | Code Quality | **PASS** | User-facing role locators (`get_by_role`, `has-text`, `aria-label`, semantic tags) across all POMs. |
| **REQ-22** | **README & TEST_SUMMARY** | Documentation | **PASS** | Comprehensive `README.md` and `TEST_SUMMARY.md` documenting setup, run commands, and test results. |
| **REQ-23** | **No Secrets in Source Control** | Security | **PASS** | `.gitignore` blocks `.env*`, `.pem`, `.key`, `credentials.json`; GitHub Secrets used in workflow. |
| **REQ-24** | **No Invented Endpoints/Data** | Integrity | **PASS** | Strictly adheres to discovered Netlify edge behavior, `/catalog.json`, and supplied MockAPI contract. |

---

## 2. Detailed Technical Specifications

### A. Environment & Runtimes
- **Language:** Python 3.11+ (Local environment: 3.14.8, CI runner: 3.11)
- **Frameworks:** Playwright 1.64.1, Pytest 9.2.0, Pytest-Playwright 0.10.0, Pytest-HTML 4.2.0, Requests 2.34.2
- **Operating System:** Cross-platform (Windows 10 / Ubuntu 22.04 LTS runner)

### B. Base URLs & Network Decoupling
Per project requirements, the storefront website and MockAPI endpoints are maintained independently:
- `WEBSITE_BASE_URL`: `https://ecomcicid.netlify.app`
- `API_BASE_URL`: `https://681444af225ff1af16285b31.mockapi.io/electronicapi`
- Aliases `BASE_URL` and `MOCK_API_BASE_URL` provide backwards compatibility.

### C. Test Metrics
- **Total Test Cases:** 58 tests
- **E2E Tests:** 39 tests across 9 test suites
- **API Tests:** 19 tests across 2 test suites
- **Smoke Tests:** 14 critical-path tests
- **Pass Rate:** 100% (58 Passed, 0 Failed, 0 Skipped)
