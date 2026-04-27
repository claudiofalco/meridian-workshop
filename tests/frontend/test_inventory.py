"""
R3 — Browser tests: Inventory browsing flow.
Covers: page load, warehouse filter, category filter, combined filters.
"""

BASE_URL = "http://localhost:3000"


class TestInventoryBrowsing:
    def test_inventory_page_loads(self, page):
        page.goto(f"{BASE_URL}/inventory")
        page.wait_for_selector("tbody tr")
        assert page.locator("tbody tr").count() > 0

    def test_all_warehouses_shown_by_default(self, page):
        page.goto(f"{BASE_URL}/inventory")
        page.wait_for_selector("tbody tr")
        assert page.locator("tbody tr").count() > 10

    def test_filter_by_warehouse_reduces_results(self, page):
        page.goto(f"{BASE_URL}/inventory")
        page.wait_for_selector("tbody tr")
        total = page.locator("tbody tr").count()

        # Location is the 2nd select (index 1) in the FilterBar
        page.locator("select").nth(1).select_option("San Francisco")
        page.wait_for_timeout(600)

        filtered = page.locator("tbody tr").count()
        assert filtered < total
        assert filtered > 0

    def test_filter_by_category_reduces_results(self, page):
        page.goto(f"{BASE_URL}/inventory")
        page.wait_for_selector("tbody tr")
        total = page.locator("tbody tr").count()

        # Category is the 3rd select (index 2)
        page.locator("select").nth(2).select_option("Circuit Boards")
        page.wait_for_timeout(600)

        filtered = page.locator("tbody tr").count()
        assert filtered < total
        assert filtered > 0

    def test_combined_warehouse_and_category_filter(self, page):
        page.goto(f"{BASE_URL}/inventory")
        page.wait_for_selector("tbody tr")

        page.locator("select").nth(1).select_option("London")
        page.locator("select").nth(2).select_option("Sensors")
        page.wait_for_timeout(600)

        # No error regardless of result count
        assert not page.locator(".error").is_visible()

    def test_inventory_table_has_expected_columns(self, page):
        page.goto(f"{BASE_URL}/inventory")
        page.wait_for_selector("thead th")
        # Check for key column headers (case-insensitive partial match)
        page_text = page.locator("thead").inner_text().upper()
        assert "SKU" in page_text
        assert "LOCATION" in page_text
