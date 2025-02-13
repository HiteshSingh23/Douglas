from pages.verifyPerfum import Perfum

def test_loadUrl(browser):
    pg = Perfum(browser)
    pg.load_url()

def test_accept_cookies(browser):
    pg = Perfum(browser)
    pg.accept_cookies()

def test_performFilter(browser):
    pg = Perfum(browser)
    pg.click_perfume()

    # Directly call the function to apply filters from Excel
    pg.apply_filters(
        file_path=r'C:\Users\Fleek\PycharmProjects\TestShadow\resources\filters.xlsx',  # Update with your actual file path
        column_name="Filters"  # Column header to read data from
    )
