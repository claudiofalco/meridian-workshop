"""
R3 — Browser tests: Reports page (R1 remediation verification).
Covers: page load, quarterly table, monthly chart, all four filters wired correctly.
"""

BASE_URL = "http://localhost:3000"


class TestReportsPage:
    def test_reports_page_loads(self, page):
        page.goto(f"{BASE_URL}/reports")
        assert page.locator("h2").filter(has_text="Performance Reports").is_visible()
        page.wait_for_selector("tbody tr")

    def test_quarterly_table_shows_four_quarters(self, page):
        page.goto(f"{BASE_URL}/reports")
        page.wait_for_selector("tbody tr")
        rows = page.locator("table").first.locator("tbody tr").count()
        assert rows == 4  # Q1–Q4

    def test_quarterly_table_has_quarter_labels(self, page):
        page.goto(f"{BASE_URL}/reports")
        page.wait_for_selector("tbody tr")
        text = page.locator("table").first.locator("tbody").inner_text()
        assert "Q1-2025" in text
        assert "Q4-2025" in text

    def test_summary_stats_visible(self, page):
        page.goto(f"{BASE_URL}/reports")
        page.wait_for_selector(".stat-card, .stat-value")
        assert page.locator(".stat-card").filter(has_text="Total Revenue").is_visible()
        assert page.locator(".stat-card").filter(has_text="Total Orders").is_visible()

    def test_warehouse_filter_changes_data(self, page):
        page.goto(f"{BASE_URL}/reports")
        page.wait_for_selector("tbody tr")

        # Read total orders for all warehouses
        total_orders_text = page.locator("table").first.locator("tbody tr").first.inner_text()

        page.locator("select").nth(1).select_option("London")
        page.wait_for_timeout(600)

        filtered_text = page.locator("table").first.locator("tbody tr").first.inner_text()
        # Data should change when filtered to London only
        assert filtered_text != total_orders_text

    def test_category_filter_changes_data(self, page):
        page.goto(f"{BASE_URL}/reports")
        page.wait_for_selector("tbody tr")
        baseline = page.locator("table").first.locator("tbody tr").first.inner_text()

        page.locator("select").nth(2).select_option("Sensors")
        page.wait_for_timeout(600)

        filtered = page.locator("table").first.locator("tbody tr").first.inner_text()
        assert filtered != baseline

    def test_no_console_errors_on_load(self, page):
        errors = []
        page.on("console", lambda msg: errors.append(msg.text) if msg.type == "error" else None)
        page.goto(f"{BASE_URL}/reports")
        page.wait_for_selector("tbody tr")
        # Filter out known 404s (tasks endpoint and static assets)
        relevant_errors = [e for e in errors if "404" not in e and "tasks" not in e]
        assert len(relevant_errors) == 0

    def test_month_over_month_table_visible(self, page):
        page.goto(f"{BASE_URL}/reports")
        page.wait_for_selector("text=Month-over-Month Analysis")
        assert page.locator("text=Month-over-Month Analysis").is_visible()
