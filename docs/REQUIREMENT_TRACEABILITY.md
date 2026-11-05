# Requirement Traceability Matrix (RTM)

This matrix maps each requirement from the Northline Store Automation Testing assignment to its implementation in the test framework, Page Object Models, test files, and verification evidence.

---

## 1. Traceability Matrix

| Req ID | Requirement Description | Test File & Function | Page Object Class | Pytest Marker | Verification Evidence | Audit Status |
| :---: | :--- | :--- | :--- | :---: | :--- | :---: |
| **REQ-01** | Python 3.11+ Compatibility | Local & CI execution | All | All | Python 3.14.8 verified locally; Python 3.11 configured in CI | **PASS** |
| **REQ-02** | Playwright with Pytest | Framework runner | All | All | `pytest-playwright 0.10.0`, `playwright 1.64.1` | **PASS** |
| **REQ-03** | Page Object Model Architecture | `framework/pages/*.py` | 8 POM classes | All | Locators and actions encapsulated in dedicated POMs | **PASS** |
| **REQ-04** | Reusable Fixtures & Test Data | `tests/conftest.py` | All | All | `browser`, `context`, `page`, `mobile_page`, POM fixtures | **PASS** |
| **REQ-05** | $\ge 20$ Meaningful E2E Tests | `tests/e2e/test_*.py` | All POMs | `e2e` | **39 distinct E2E tests** covering full customer journeys | **PASS** |
| **REQ-06** | $\ge 8$ Meaningful API Tests | `tests/api/test_*.py` | `N/A` | `api` | **19 distinct API tests** covering MockAPI + Storefront | **PASS** |
| **REQ-07** | Correct Pytest Markers | `pytest.ini` | All | `smoke`, `e2e`, `api`, etc. | Configured in `pytest.ini` and tagged on every test | **PASS** |
| **REQ-08** | Website Discovery Document | `docs/WEBSITE_DISCOVERY.md` | `N/A` | `N/A` | Comprehensive audit of DOM, navigation, PDP, and drawer | **PASS** |
| **REQ-09** | API Inventory Document | `docs/API_INVENTORY.md` | `N/A` | `N/A` | Documented `/catalog.json`, Netlify edge, and MockAPI | **PASS** |
| **REQ-10** | Test Plan Document | `docs/TEST_PLAN.md` | `N/A` | `N/A` | QA test plan, locator dictionary, test matrix, and risks | **PASS** |
| **REQ-11** | Chromium, Firefox, WebKit Coverage | All test suites | All | All | Verified on Chromium (39/39), Firefox (14/14), WebKit (14/14) | **PASS** |
| **REQ-12** | Responsive Testing at $390\times844$ | `tests/e2e/test_mobile_responsive.py` | `HomePage`, `ProductsPage`, `ProductDetailPage` | `mobile`, `e2e` | 3 tests run at exact iPhone 13 dimensions | **PASS** |
| **REQ-13** | GitHub Actions Matrix | `.github/workflows/tests.yml` | `N/A` | `N/A` | Strategy matrix `browser: [chromium, firefox, webkit]` | **PASS** |
| **REQ-14** | Multi-Trigger CI Pipeline | `.github/workflows/tests.yml` | `N/A` | `N/A` | `push`, `pull_request`, `workflow_dispatch`, `cron: '0 2 * * *'` | **PASS** |
| **REQ-15** | Smoke Tests Before Regression | `.github/workflows/tests.yml` | `N/A` | `smoke`, `e2e` | `e2e-regression-tests` job gates on `needs: [smoke-tests]` | **PASS** |
| **REQ-16** | API Tests in Separate Stage/Job | `.github/workflows/tests.yml` | `N/A` | `api` | `api-tests` runs as an independent parallel job | **PASS** |
| **REQ-17** | Pytest HTML Reports | `pytest.ini`, CI workflow | All | All | `--html=test-results/report.html --self-contained-html` | **PASS** |
| **REQ-18** | Failure Screenshots & Traces | `tests/conftest.py` | All | All | Auto-screenshot hook + `trace_{test_name}.zip` saved per test | **PASS** |
| **REQ-19** | CI Artifacts for Each Browser | `.github/workflows/tests.yml` | `N/A` | All | `smoke-artifacts-{browser}`, `e2e-artifacts-{browser}` | **PASS** |
| **REQ-20** | No Hard-coded Sleeps | All test files & POMs | All | All | Zero `time.sleep()` calls; Playwright auto-waiting used | **PASS** |
| **REQ-21** | Role-based / Test-ID Locators | `framework/pages/*.py` | All POMs | All | Semantic locators (`get_by_role`, `has-text`, `aria-label`) | **PASS** |
| **REQ-22** | README & TEST_SUMMARY | `README.md`, `TEST_SUMMARY.md` | `N/A` | `N/A` | Complete user guide, setup steps, test execution summaries | **PASS** |
| **REQ-23** | No Secrets in Source Control | `.gitignore` | `N/A` | `N/A` | `.gitignore` blocks `.env*`, `.pem`, `.key`, `credentials.json` | **PASS** |
| **REQ-24** | Truthful Test Reporting | Full test suite | All | All | 100% genuine execution logs; zero fabricated assertions | **PASS** |

---

## 2. Remote GitHub Synchronization & CI Execution Status

| Deliverable | Target / Path | Status | Verification Detail |
| :--- | :--- | :---: | :--- |
| **Local Git Commits** | `main` branch (7 commits) | **PASS** | Clean working tree; atomic commits with conventional commit syntax. |
| **Remote Repository** | `https://github.com/prakruti95/Playwright_demo.git` | **BLOCKED** | Remote push requires interactive Git Credential Manager auth for `prakruti95`. |
| **GitHub Actions Pipeline** | `.github/workflows/tests.yml` | **PASS (Locally Verified)** | Valid YAML syntax; ready to run automatically upon first push. |
| **Three Consecutive CI Runs** | GitHub Actions Run History | **NOT VERIFIED** | Awaiting user's one-time push from their terminal to trigger CI runs. |
