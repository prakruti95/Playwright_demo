"""
Interactive Live Visual Demonstration of Northline Store Automation.
Uses the tested Page Object Models to showcase the complete journey in Chromium.
"""
import time
from playwright.sync_api import sync_playwright
from framework.pages import (
    HomePage, ProductsPage, ProductDetailPage, 
    CartPage, CheckoutPage, OrderConfirmationPage
)
from framework.config import TEST_SHIPPING_ADDRESS

def run_visual_demo():
    print("=========================================================", flush=True)
    print("  LAUNCHING PLAYWRIGHT CHROMIUM VISUALLY ON YOUR SCREEN  ", flush=True)
    print("=========================================================", flush=True)
    
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,
            slow_mo=500,
            args=["--start-maximized"]
        )
        context = browser.new_context(no_viewport=True)
        page = context.new_page()
        
        home = HomePage(page)
        products = ProductsPage(page)
        pdp = ProductDetailPage(page)
        cart = CartPage(page)
        checkout = CheckoutPage(page)
        order_confirm = OrderConfirmationPage(page)
        
        print("\n[Step 1] Navigating to Store Homepage...", flush=True)
        home.load()
        time.sleep(1)
        
        print("[Step 2] Testing Theme Toggle (Dark / Light)...", flush=True)
        home.toggle_theme()
        time.sleep(1)
        home.toggle_theme()
        time.sleep(1)
        
        print("[Step 3] Navigating to Product Catalog...", flush=True)
        products.load()
        time.sleep(1)
        print(f"         Total products rendered: {products.get_products_count()}", flush=True)
        
        print("[Step 4] Filtering by 'Living' Category...", flush=True)
        products.filter_by_category("living")
        time.sleep(1)
        print(f"         Living products count: {products.get_products_count()}", flush=True)
        
        print("[Step 5] Resetting Filter to 'All products'...", flush=True)
        products.filter_by_category("all")
        time.sleep(1)
        print(f"         Catalog reset count: {products.get_products_count()}", flush=True)
        
        print("[Step 6] Sorting products by 'Price: low to high'...", flush=True)
        products.select_sort("Price: low to high")
        time.sleep(1)
        prices = products.get_product_prices()
        print(f"         Sorted prices: {prices}", flush=True)
        
        print("[Step 7] Navigating to Product Detail Page (Ceramic Pour-Over Set)...", flush=True)
        pdp.load("ceramic-pour-over-set")
        time.sleep(1)
        print(f"         Product title: '{pdp.get_title_text()}', Price: ${pdp.get_price_value():.2f}", flush=True)
        
        print("[Step 8] Testing Product Details Tabs (Specifications & Reviews)...", flush=True)
        pdp.tab_specifications.click()
        time.sleep(1)
        pdp.tab_reviews.click()
        time.sleep(1)
        pdp.tab_description.click()
        time.sleep(1)
        
        print("[Step 9] Adding Product to Cart...", flush=True)
        pdp.add_to_cart()
        time.sleep(1.5)
        
        print("[Step 10] Navigating to Dedicated Cart Page & Updating Quantity...", flush=True)
        cart.load()
        time.sleep(1)
        print(f"         Initial subtotal: ${cart.get_subtotal():.2f}", flush=True)
        cart.increment_item(0)
        time.sleep(1.5)
        print(f"         Updated subtotal: ${cart.get_subtotal():.2f}", flush=True)
        
        print("[Step 11] Proceeding to Checkout Form...", flush=True)
        checkout.load()
        time.sleep(1)
        
        print("[Step 12] Entering Shipping Address...", flush=True)
        checkout.fill_shipping_address(TEST_SHIPPING_ADDRESS)
        time.sleep(1)
        
        print("[Step 13] Submitting to Review Step...", flush=True)
        checkout.submit_shipping_form()
        time.sleep(1.5)
        
        print("[Step 14] Placing Order...", flush=True)
        checkout.place_order()
        time.sleep(2)
        
        print("\n=========================================================", flush=True)
        if order_confirm.is_confirmed():
            order_num = order_confirm.get_order_number()
            print("  SUCCESS! ORDER CONFIRMED!", flush=True)
            print(f"  Order Receipt Number: {order_num}", flush=True)
        print("=========================================================", flush=True)
        
        print("\nLeaving browser open for 6 seconds for visual inspection...", flush=True)
        time.sleep(6)
        browser.close()
        print("Visual demonstration finished cleanly!", flush=True)

if __name__ == "__main__":
    run_visual_demo()
