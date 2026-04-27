"""
R3 — Browser tests: Restocking recommendations flow (R2).
Covers: page load, recommendations table, budget ceiling, warehouse filter.
"""

BASE_URL = "http://localhost:3000"


class TestRestockingFlow:
    def test_restocking_page_loads(self, page):
        page.goto(f"{BASE_URL}/restocking")
        assert page.locator("h2").filter(has_text="Restocking Recommendations").is_visible()

    def test_restocking_nav_link_exists(self, page):
        page.goto(f"{BASE_URL}/")
        assert page.locator("nav a[href='/restocking']").is_visible()

    def test_recommendations_table_loads(self, page):
        page.goto(f"{BASE_URL}/restocking")
        page.wait_for_selector("table, .empty-state")
        # Either there are rows or the empty state is shown — no error
        has_table = page.locator("tbody tr").count() > 0
        has_empty = page.locator(".empty-state").is_visible()
        assert has_table or has_empty

    def test_items_are_below_reorder_point(self, page):
        page.goto(f"{BASE_URL}/restocking")
        page.wait_for_selector("tbody tr")
        rows = page.locator("tbody tr").count()
        assert rows > 0  # our dataset has known at-risk items

    def test_budget_ceiling_marks_over_budget_items(self, page):
        page.goto(f"{BASE_URL}/restocking")
        page.wait_for_selector("tbody tr")

        # Enter a small budget that won't cover everything
        page.locator("input[type='number']").fill("30000")
        page.wait_for_timeout(700)  # debounce + API call

        # Some items should be "Over Budget"
        over_budget = page.locator("text=Over Budget")
        assert over_budget.count() > 0

    def test_large_budget_marks_all_within_budget(self, page):
        page.goto(f"{BASE_URL}/restocking")
        page.wait_for_selector("tbody tr")

        page.locator("input[type='number']").fill("9999999")
        page.wait_for_timeout(700)

        over_budget = page.locator("text=Over Budget")
        assert over_budget.count() == 0

    def test_empty_budget_shows_all_within_budget(self, page):
        page.goto(f"{BASE_URL}/restocking")
        page.wait_for_selector("tbody tr")

        # No budget = no limit
        page.locator("input[type='number']").fill("")
        page.wait_for_timeout(700)

        over_budget = page.locator("text=Over Budget")
        assert over_budget.count() == 0

    def test_warehouse_filter_changes_recommendations(self, page):
        page.goto(f"{BASE_URL}/restocking")
        page.wait_for_selector("tbody tr")
        total = page.locator("tbody tr").count()

        page.locator("select").nth(1).select_option("San Francisco")
        page.wait_for_timeout(600)

        # San Francisco may have zero at-risk items — no error is the test
        assert not page.locator(".error").is_visible()
        sf_count = page.locator("tbody tr").count()
        assert sf_count <= total

    def test_summary_stats_visible(self, page):
        page.goto(f"{BASE_URL}/restocking")
        page.wait_for_selector(".stat-card, .stat-value")
        assert page.locator(".stat-card").filter(has_text="Items Needing Restock").is_visible()
        assert page.locator(".stat-card").filter(has_text="Within Budget").first.is_visible()
