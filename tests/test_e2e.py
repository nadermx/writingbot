"""
End-to-end browser tests using Playwright.

Run with: pytest tests/test_e2e.py --headed
Or headless: pytest tests/test_e2e.py

Requires: pip install playwright pytest-playwright && playwright install chromium

Set BASE_URL env var to test against a different server:
    BASE_URL=https://writingbot.ai pytest tests/test_e2e.py
"""
import os

import pytest
from playwright.sync_api import expect

BASE_URL = os.environ.get('BASE_URL', 'http://localhost:8000')


# ------------------------------------------------------------------
# Smoke tests — core pages load without errors
# ------------------------------------------------------------------

CORE_PAGES = [
    '/',
    '/paraphrasing-tool/',
    '/grammar-check/',
    '/summarize/',
    '/ai-content-detector/',
    '/ai-humanizer/',
    '/translate/',
    '/citation-generator/',
    '/word-counter/',
    '/ai-writing-tools/',
    '/pdf-tools/',
    '/pricing/',
    '/blog/',
]


@pytest.mark.parametrize('path', CORE_PAGES)
def test_page_loads_without_console_errors(page, path):
    """Each core page loads with HTTP 200 and no JS console errors."""
    errors = []
    page.on('console', lambda msg: errors.append(msg.text) if msg.type == 'error' else None)
    response = page.goto(f'{BASE_URL}{path}', wait_until='domcontentloaded')
    assert response.status == 200, f'{path} returned {response.status}'
    # Filter out expected/noisy console errors (e.g., favicon, analytics)
    real_errors = [e for e in errors if 'favicon' not in e.lower() and '404' not in e]
    assert len(real_errors) == 0, f'{path} had JS console errors: {real_errors}'


# ------------------------------------------------------------------
# Mobile viewport tests — CTA buttons visible on small screens
# ------------------------------------------------------------------

def test_homepage_cta_buttons_visible_on_mobile(page):
    """Homepage CTA buttons are visible and clickable at 375px width (iPhone SE)."""
    page.set_viewport_size({'width': 375, 'height': 667})
    page.goto(f'{BASE_URL}/', wait_until='domcontentloaded')

    # Find the two CTA buttons in the hero
    primary_btn = page.locator('a[href*="paraphrasing-tool"]').first
    secondary_btn = page.locator('a[href="#tools"]').first

    expect(primary_btn).to_be_visible()
    expect(secondary_btn).to_be_visible()

    # Buttons should not overflow the viewport
    primary_box = primary_btn.bounding_box()
    assert primary_box is not None, 'Primary CTA button not rendered'
    assert primary_box['x'] >= 0, 'Primary CTA overflows left'
    assert primary_box['x'] + primary_box['width'] <= 375, 'Primary CTA overflows right'


# ------------------------------------------------------------------
# Navigation — mobile hamburger menu
# ------------------------------------------------------------------

def test_mobile_hamburger_menu(page):
    """Mobile hamburger menu opens and shows nav links."""
    page.set_viewport_size({'width': 375, 'height': 667})
    page.goto(f'{BASE_URL}/', wait_until='domcontentloaded')

    # The navbar toggler should be visible on mobile
    toggler = page.locator('.navbar-toggler').first
    expect(toggler).to_be_visible()

    # Click it to open the menu
    toggler.click()
    page.wait_for_timeout(500)  # Wait for collapse animation

    # Nav links should now be visible
    nav = page.locator('.navbar-collapse')
    expect(nav).to_be_visible()


# ------------------------------------------------------------------
# Alpine.js initialization — no x-cloak elements remain visible
# ------------------------------------------------------------------

def test_no_xcloak_elements_visible(page):
    """After Alpine.js initializes, no [x-cloak] elements should remain visible."""
    page.goto(f'{BASE_URL}/', wait_until='networkidle')
    # Wait a moment for Alpine to initialize
    page.wait_for_timeout(1000)

    # x-cloak elements should either be removed or hidden by CSS
    visible_cloaked = page.locator('[x-cloak]:visible')
    count = visible_cloaked.count()
    assert count == 0, f'{count} x-cloak elements still visible after Alpine init'


def test_ai_tool_generator_no_loading_flash(page):
    """AI tool generator page should not show 'Generating...' on initial load."""
    page.goto(f'{BASE_URL}/ai-writing-tools/ai-essay-writer/', wait_until='domcontentloaded')
    # Wait for Alpine.js to initialize
    page.wait_for_timeout(1000)

    # The loading span should be hidden (x-cloak + x-show="loading")
    loading_span = page.locator('span:has-text("Generating...")')
    if loading_span.count() > 0:
        expect(loading_span.first).not_to_be_visible()


# ------------------------------------------------------------------
# Paraphraser — interactive demo on homepage
# ------------------------------------------------------------------

def test_homepage_paraphraser_demo(page):
    """Homepage demo: click Paraphrase, see output appear."""
    page.goto(f'{BASE_URL}/', wait_until='domcontentloaded')

    # The demo section should have a textarea with pre-filled text
    textarea = page.locator('textarea').first
    expect(textarea).to_be_visible()
    assert len(textarea.input_value()) > 0, 'Demo textarea should have pre-filled text'

    # Click the paraphrase button
    paraphrase_btn = page.locator('button:has-text("Paraphrase")').first
    expect(paraphrase_btn).to_be_visible()
    paraphrase_btn.click()

    # Wait for the mock paraphrase to complete (800ms delay in demo)
    page.wait_for_timeout(1200)

    # Output text should appear
    output = page.locator('p').filter(has_text='swift brown fox')
    expect(output.first).to_be_visible(timeout=3000)


# ------------------------------------------------------------------
# Tool page structure tests
# ------------------------------------------------------------------

def test_paraphraser_page_has_form(page):
    """Paraphraser page has a text input area and submit button."""
    page.goto(f'{BASE_URL}/paraphrasing-tool/', wait_until='domcontentloaded')

    # Should have a textarea for input
    textarea = page.locator('textarea').first
    expect(textarea).to_be_visible()

    # Should have a paraphrase/submit button
    submit_btn = page.locator('button[type="submit"], button:has-text("Paraphrase")').first
    expect(submit_btn).to_be_visible()


def test_grammar_page_has_form(page):
    """Grammar checker page has a text input area and check button."""
    page.goto(f'{BASE_URL}/grammar-check/', wait_until='domcontentloaded')

    textarea = page.locator('textarea').first
    expect(textarea).to_be_visible()

    check_btn = page.locator('button[type="submit"], button:has-text("Check")').first
    expect(check_btn).to_be_visible()


# ------------------------------------------------------------------
# Desktop navigation — dropdowns work
# ------------------------------------------------------------------

def test_desktop_nav_dropdowns(page):
    """Desktop nav dropdowns open on hover/click."""
    page.set_viewport_size({'width': 1280, 'height': 800})
    page.goto(f'{BASE_URL}/', wait_until='domcontentloaded')

    # Find a dropdown toggle in the navbar
    dropdown_toggle = page.locator('.navbar .dropdown-toggle').first
    if dropdown_toggle.count() > 0:
        expect(dropdown_toggle).to_be_visible()
        dropdown_toggle.click()
        page.wait_for_timeout(300)

        # Dropdown menu should become visible
        dropdown_menu = page.locator('.navbar .dropdown-menu.show').first
        expect(dropdown_menu).to_be_visible()
