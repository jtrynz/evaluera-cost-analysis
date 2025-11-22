"""
EVALUERA - UI Theme Constants
===============================
Design tokens for Apple-like premium UI components
"""

# ==================== COLOR PALETTE ====================
# Apple-inspired Premium Color System
COLORS = {
    # Primary Brand Colors (New Premium Palette)
    'primary': '#2A4F57',        # Deep Teal - Primary actions
    'secondary': '#B8D4D1',      # Soft Mint - Hover states
    'accent': '#8FAEAB',         # Muted Sage - Links & highlights

    # Surface Colors
    'surface': '#FFFFFF',        # Pure white surfaces
    'surface_light': '#E7F1EF',  # Light tint - Input backgrounds
    'background': '#F5F9F8',     # Subtle off-white

    # Dark Mode / Gradient Colors
    'dark_primary': '#1E2E32',   # Dark accent for gradients
    'dark_deep': '#0F1A1C',      # Deep dark for backgrounds
    'dark_overlay': '#0A1214',   # Deepest dark

    # Text Colors (High Contrast)
    'text_primary': '#1A1A1A',   # Primary text
    'text_secondary': '#4B5563', # Secondary text
    'text_muted': '#6B7280',     # Muted text
    'text_light': '#9CA3AF',     # Placeholder text

    # Border & Line Colors
    'border_light': '#E5E7EB',
    'border': '#D1D5DB',
    'border_dark': '#9CA3AF',

    # Legacy Compatibility
    'gray_200': '#E5E7EB',
    'gray_300': '#D1D5DB',
    'gray_400': '#9CA3AF',
    'gray_500': '#6B7280',
    'gray_600': '#4B5563',

    # Accent & Status Colors (Refined)
    'light_accent': '#E7F1EF',
    'dark_accent': '#1E2E32',

    # Status Colors (Apple-like)
    'success': '#34C759',        # Apple green
    'warning': '#FF9500',        # Apple orange
    'error': '#FF3B30',          # Apple red
    'info': '#007AFF',           # Apple blue
}

# ==================== BORDER RADIUS ====================
RADIUS = {
    'xs': '4px',
    'sm': '6px',
    'md': '12px',
    'lg': '16px',
    'xl': '20px',
    'xxl': '24px',
    'full': '9999px',
}

# ==================== SPACING SCALE ====================
SPACING = {
    'xs': '4px',
    'sm': '8px',
    'md': '12px',
    'lg': '16px',
    'xl': '24px',
    'xxl': '32px',
    'xxxl': '48px',
}

# ==================== SHADOWS ====================
SHADOWS = {
    'none': 'none',
    'xs': '0 1px 2px rgba(0, 0, 0, 0.05)',
    'sm': '0 1px 3px rgba(0, 0, 0, 0.1), 0 1px 2px rgba(0, 0, 0, 0.06)',
    'md': '0 4px 6px rgba(0, 0, 0, 0.1), 0 2px 4px rgba(0, 0, 0, 0.06)',
    'lg': '0 10px 15px rgba(0, 0, 0, 0.1), 0 4px 6px rgba(0, 0, 0, 0.05)',
    'xl': '0 20px 25px rgba(0, 0, 0, 0.1), 0 10px 10px rgba(0, 0, 0, 0.04)',
    'xxl': '0 25px 50px rgba(0, 0, 0, 0.15)',
    'inner': 'inset 0 2px 4px rgba(0, 0, 0, 0.06)',
}

# ==================== TYPOGRAPHY ====================
TYPOGRAPHY = {
    # Font Families
    'font_primary': '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif',
    'font_mono': '"SF Mono", Monaco, "Cascadia Code", "Roboto Mono", Consolas, "Courier New", monospace',

    # Font Sizes
    'text_xs': '12px',
    'text_sm': '14px',
    'text_base': '16px',
    'text_lg': '18px',
    'text_xl': '20px',
    'text_xxl': '24px',
    'text_xxxl': '30px',

    # Font Weights
    'weight_light': '300',
    'weight_normal': '400',
    'weight_medium': '500',
    'weight_semibold': '600',
    'weight_bold': '700',
    'weight_extrabold': '800',

    # Line Heights
    'leading_tight': '1.25',
    'leading_normal': '1.5',
    'leading_relaxed': '1.75',

    # Letter Spacing
    'tracking_tight': '-0.02em',
    'tracking_normal': '0',
    'tracking_wide': '0.025em',
}

# ==================== TRANSITIONS ====================
TRANSITIONS = {
    'fast': '0.15s ease',
    'base': '0.2s ease',
    'slow': '0.3s ease',
    'spring': '0.3s cubic-bezier(0.4, 0, 0.2, 1)',
}

# ==================== BREAKPOINTS ====================
BREAKPOINTS = {
    'sm': '640px',
    'md': '768px',
    'lg': '1024px',
    'xl': '1280px',
    'xxl': '1536px',
}
