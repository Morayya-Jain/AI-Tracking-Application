"""
Runtime hook template for PyInstaller.

This file is used as a TEMPLATE by the build script.
The build script replaces the placeholder values with actual API keys
and saves it as runtime_hook.py before running PyInstaller.

DO NOT COMMIT ACTUAL KEYS TO THIS FILE.
"""

import os

# These placeholders are replaced by the build script with actual values
# The format %%KEY_NAME%% is used to make it easy to do text replacement

# AI API Keys
BUNDLED_OPENAI_API_KEY = "%%OPENAI_API_KEY%%"
BUNDLED_GEMINI_API_KEY = "%%GEMINI_API_KEY%%"

# Stripe Payment Keys
BUNDLED_STRIPE_SECRET_KEY = "%%STRIPE_SECRET_KEY%%"
BUNDLED_STRIPE_PUBLISHABLE_KEY = "%%STRIPE_PUBLISHABLE_KEY%%"
BUNDLED_STRIPE_PRICE_ID = "%%STRIPE_PRICE_ID%%"

# Set environment variables so config.py can pick them up
# Only set if the placeholder was actually replaced (not empty and not the placeholder itself)

# AI Keys
if BUNDLED_OPENAI_API_KEY and not BUNDLED_OPENAI_API_KEY.startswith("%%"):
    os.environ["BUNDLED_OPENAI_API_KEY"] = BUNDLED_OPENAI_API_KEY

if BUNDLED_GEMINI_API_KEY and not BUNDLED_GEMINI_API_KEY.startswith("%%"):
    os.environ["BUNDLED_GEMINI_API_KEY"] = BUNDLED_GEMINI_API_KEY

# Stripe Keys
if BUNDLED_STRIPE_SECRET_KEY and not BUNDLED_STRIPE_SECRET_KEY.startswith("%%"):
    os.environ["BUNDLED_STRIPE_SECRET_KEY"] = BUNDLED_STRIPE_SECRET_KEY

if BUNDLED_STRIPE_PUBLISHABLE_KEY and not BUNDLED_STRIPE_PUBLISHABLE_KEY.startswith("%%"):
    os.environ["BUNDLED_STRIPE_PUBLISHABLE_KEY"] = BUNDLED_STRIPE_PUBLISHABLE_KEY

if BUNDLED_STRIPE_PRICE_ID and not BUNDLED_STRIPE_PRICE_ID.startswith("%%"):
    os.environ["BUNDLED_STRIPE_PRICE_ID"] = BUNDLED_STRIPE_PRICE_ID
