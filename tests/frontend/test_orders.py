"""
R3 — Browser tests: Order filtering flow.
Covers: page load, status filter, warehouse filter, combined filters.
"""

BASE_URL = "http://localhost:3000"


class TestOrderFiltering:
    def test_orders_page_loads(self, page):
        page.goto(f"{BASE_URL}/orders")
        assert page.locator("h2").filter(has_text="Orders").is_visible()
        page.wait_for_selector("tbody tr")
        assert page.locator("tbody tr").count() > 0

    def test_filter_by_status_delivered(self, page):
        page.goto(f"{BASE_URL}/orders")
        page.wait_for_selector("tbody tr")
        total = page.locator("tbody tr").count()

        # Order Status is the 4th select (index 3)
        page.locator("select").nth(3).select_option("Delivered")
        page.wait_for_timeout(500)

        filtered = page.locator("tbody tr").count()
        assert filtered < total
        assert filtered > 0

    def test_filter_by_warehouse(self, page):
        page.goto(f"{BASE_URL}/orders")
        page.wait_for_selector("tbody tr")
        total = page.locator("tbody tr").count()

        page.locator("select").nth(1).select_option("Tokyo")
        page.wait_for_timeout(500)

        filtered = page.locator("tbody tr").count()
        assert filtered < total
        assert filtered > 0

    def test_filter_by_month(self, page):
        page.goto(f"{BASE_URL}/orders")
        page.wait_for_selector("tbody tr")
        total = page.locator("tbody tr").count()

        # Time Period is the 1st select (index 0)
        page.locator("select").nth(0).select_option("January")
        page.wait_for_timeout(500)

        filtered = page.locator("tbody tr").count()
        assert filtered < total
        assert filtered > 0

    def test_combined_status_and_warehouse_filter(self, page):
        page.goto(f"{BASE_URL}/orders")
        page.wait_for_selector("tbody tr")

        page.locator("select").nth(1).select_option("London")
        page.locator("select").nth(3).select_option("Shipped")
        page.wait_for_timeout(500)

        # No error state, result may be empty
        assert not page.locator(".error").is_visible()

    def test_orders_table_has_expected_columns(self, page):
        page.goto(f"{BASE_URL}/orders")
        page.wait_for_selector("thead th")
        headers = page.locator("thead").inner_text().upper()
        assert "ORDER" in headers
        assert "STATUS" in headers
        assert "CUSTOMER" in headers
