"""
EVALUERA - UI Theme Constants
===============================
Design tokens for Apple-like premium UI components
"""

# ==================== COLOR PALETTE ====================
COLORS = {
    # Primary Brand Colors
    'primary': '#2A4F57',
    'secondary': '#E8F4F7',
    'accent': '#4A90A4',

    # Surface Colors
    'surface': '#FFFFFF',
    'background': '#F8FAFB',

    # Text Colors
    'text_primary': '#1A1A1A',
    'text_secondary': '#6B7280',
    'gray_400': '#9CA3AF',
    'gray_500': '#6B7280',
    'gray_600': '#4B5563',

    # Border & Line Colors
    'gray_200': '#E5E7EB',
    'gray_300': '#D1D5DB',

    # Accent & Status Colors
    'light_accent': '#E8F4F7',
    'dark_accent': '#1E3A41',

    # Status Colors
    'success': '#10B981',
    'warning': '#F59E0B',
    'error': '#EF4444',
    'info': '#3B82F6',
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
