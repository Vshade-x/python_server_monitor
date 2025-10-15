# PYTHON SERVER MONITOR | REAL-TIME HEALTH CHECKER

### 🎯 Project Overview

A robust Python tool designed for DevOps and support teams to verify the live operational status (HTTP response codes) of a bulk list of URLs. It detects failures and reports server health to Excel.

### ✨ Key Features & Technical Robustness

* **Fast HEAD Requests:** Uses `requests.head()` for fast, low-bandwidth status checks instead of full page downloads.
* **Flexible Execution:** Utilizes **`argparse`** to allow the user to check a **bulk list from a CSV** *or* check a **single URL instantly** via the command line.
* **Advanced Error Handling:** Categorizes server responses into **ONLINE (2xx/3xx)**, **CLIENT/SERVER ERROR (4xx/5xx)**, or **CONNECTION FAILED** (DNS/Timeout errors), ensuring clean, actionable reporting.
* **Output:** Exports a structured report to a final `.xlsx` file.
* **Core Technology:** `requests`, `pandas`, `argparse`.

### 🚀 Execution and Usage

**1. Requirements:** Python (3.x) and required libraries: `pip install requests pandas openpyxl`
**2. Data Input:** Create a file named **`url_list.csv`** with a header named **`URL`** and place your list of websites inside.
**3. Execution (BULK):** To process the entire CSV list:
    ```bash
    python health_checker.py
    ```
**4. Execution (INSTANT/SINGLE URL):** To check one site immediately:
    ```bash
    python health_checker.py --url [https://www.github.com](https://www.github.com)
    ```
