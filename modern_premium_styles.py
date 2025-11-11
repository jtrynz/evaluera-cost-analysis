"""
EVALUERA - Modern Premium Design System
Apple/Notion/Linear inspired aesthetic with Glassmorphism
"""

MODERN_PREMIUM_CSS = """
<style>
    /* ========== IMPORTS - PREMIUM FONTS ========== */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=SF+Pro+Display:wght@300;400;500;600;700&display=swap');

    /* ========== CSS VARIABLES - MODERN PREMIUM THEME ========== */
    :root {
        /* Background - Premium Dark with Depth */
        --ev-bg-primary: #0F0F14;
        --ev-bg-secondary: #1A1A24;
        --ev-bg-elevated: #24243A;
        --ev-bg-card: rgba(26, 26, 36, 0.6);
        --ev-bg-glass: rgba(36, 36, 58, 0.4);
        --ev-bg-hover: rgba(42, 42, 62, 0.8);

        /* Text - High Contrast with Hierarchy */
        --ev-text-primary: #FFFFFF;
        --ev-text-secondary: #B4B4C8;
        --ev-text-muted: #8B8B9F;
        --ev-text-accent: #7B61FF;

        /* Gradient Accents - Premium Brand Colors */
        --ev-gradient-primary: linear-gradient(135deg, #7B61FF 0%, #4BE1EC 100%);
        --ev-gradient-secondary: linear-gradient(135deg, #FF6B9D 0%, #FFA06B 100%);
        --ev-gradient-success: linear-gradient(135deg, #00F5A0 0%, #00D9F5 100%);
        --ev-gradient-warm: linear-gradient(135deg, #FA709A 0%, #FEE140 100%);

        /* Solid Accent Colors */
        --ev-primary: #7B61FF;
        --ev-primary-light: #9B82FF;
        --ev-cyan: #4BE1EC;
        --ev-success: #00F5A0;
        --ev-warning: #FFB84D;
        --ev-danger: #FF6B9D;

        /* Borders & Dividers - Subtle */
        --ev-border: rgba(255, 255, 255, 0.08);
        --ev-border-light: rgba(255, 255, 255, 0.12);
        --ev-border-accent: rgba(123, 97, 255, 0.3);

        /* Shadows - Layered Depth */
        --ev-shadow-sm: 0 2px 8px rgba(0, 0, 0, 0.2);
        --ev-shadow-md: 0 4px 16px rgba(0, 0, 0, 0.3);
        --ev-shadow-lg: 0 8px 32px rgba(0, 0, 0, 0.4);
        --ev-shadow-xl: 0 12px 48px rgba(0, 0, 0, 0.5);
        --ev-shadow-glow-primary: 0 0 30px rgba(123, 97, 255, 0.4);
        --ev-shadow-glow-cyan: 0 0 30px rgba(75, 225, 236, 0.4);

        /* Spacing - Consistent System */
        --ev-space-xs: 0.25rem;
        --ev-space-sm: 0.5rem;
        --ev-space-md: 1rem;
        --ev-space-lg: 1.5rem;
        --ev-space-xl: 2rem;
        --ev-space-2xl: 3rem;

        /* Border Radius - Smooth & Modern */
        --ev-radius-sm: 8px;
        --ev-radius-md: 12px;
        --ev-radius-lg: 16px;
        --ev-radius-xl: 20px;
        --ev-radius-full: 9999px;

        /* Backdrop Blur */
        --ev-blur-sm: blur(8px);
        --ev-blur-md: blur(16px);
        --ev-blur-lg: blur(24px);

        /* Typography */
        --font-sans: 'Inter', 'SF Pro Display', -apple-system, BlinkMacSystemFont, sans-serif;
        --font-display: 'SF Pro Display', 'Inter', sans-serif;
    }

    /* ========== GLOBAL RESETS ========== */
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }

    html, body, [data-testid="stAppViewContainer"], .main {
        font-family: var(--font-sans) !important;
        background: var(--ev-bg-primary) !important;
        color: var(--ev-text-primary) !important;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
    }

    /* ========== LAYOUT - CENTERED MAX-WIDTH ========== */
    .main {
        padding: 2rem !important;
        margin: 0 auto !important;
    }

    .block-container {
        max-width: 1200px !important;
        margin: 0 auto !important;
        padding: 2rem 1.5rem !important;
    }

    /* ========== HEADER SECTION - GLASSMORPHISM ========== */
    .main > .block-container > div:first-child {
        background: var(--ev-bg-glass);
        backdrop-filter: var(--ev-blur-md);
        border: 1px solid var(--ev-border-light);
        border-radius: var(--ev-radius-xl);
        padding: 2rem;
        margin-bottom: 2rem;
        box-shadow: var(--ev-shadow-lg);
        position: relative;
        overflow: hidden;
    }

    .main > .block-container > div:first-child::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: var(--ev-gradient-primary);
        opacity: 0.8;
    }

    /* ========== TYPOGRAPHY - MODERN HIERARCHY ========== */
    h1 {
        font-family: var(--font-display);
        font-size: 2.5rem;
        font-weight: 800;
        letter-spacing: -0.03em;
        line-height: 1.2;
        background: var(--ev-gradient-primary);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
        text-align: center;
    }

    h2 {
        font-family: var(--font-display);
        font-size: 1.75rem;
        font-weight: 700;
        color: var(--ev-text-primary);
        letter-spacing: -0.02em;
        margin: 2rem 0 1rem 0;
        position: relative;
        padding-left: 1rem;
    }

    h2::before {
        content: '';
        position: absolute;
        left: 0;
        top: 50%;
        transform: translateY(-50%);
        width: 4px;
        height: 24px;
        background: var(--ev-gradient-primary);
        border-radius: 2px;
    }

    h3 {
        font-size: 1.25rem;
        font-weight: 600;
        color: var(--ev-text-primary);
        letter-spacing: -0.01em;
        margin: 1.5rem 0 0.75rem 0;
    }

    h4 {
        font-size: 1rem;
        font-weight: 600;
        color: var(--ev-text-secondary);
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin: 1rem 0 0.5rem 0;
    }

    p, div, span, label {
        color: var(--ev-text-secondary);
        font-size: 0.95rem;
        line-height: 1.6;
        font-weight: 400;
    }

    /* ========== BUTTONS - GRADIENT WITH GLOW ========== */
    .stButton > button {
        background: var(--ev-gradient-primary) !important;
        color: white !important;
        font-weight: 600;
        font-size: 0.95rem;
        border: none !important;
        border-radius: var(--ev-radius-md) !important;
        padding: 0.875rem 2rem !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: var(--ev-shadow-md);
        letter-spacing: 0.01em;
        position: relative;
        overflow: hidden;
    }

    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(135deg, rgba(255,255,255,0.2) 0%, rgba(255,255,255,0) 100%);
        opacity: 0;
        transition: opacity 0.3s ease;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: var(--ev-shadow-glow-primary), var(--ev-shadow-lg);
    }

    .stButton > button:hover::before {
        opacity: 1;
    }

    .stButton > button:active {
        transform: translateY(0);
    }

    .stButton > button[kind="secondary"] {
        background: var(--ev-bg-elevated) !important;
        border: 1.5px solid var(--ev-border-light) !important;
        color: var(--ev-text-primary) !important;
    }

    .stButton > button[kind="secondary"]:hover {
        background: var(--ev-bg-hover) !important;
        border-color: var(--ev-primary) !important;
        box-shadow: 0 0 20px rgba(123, 97, 255, 0.2);
    }

    /* ========== CARDS & METRICS - GLASSMORPHISM ========== */
    [data-testid="stMetric"],
    [data-testid="stMetricValue"] {
        background: var(--ev-bg-glass) !important;
        backdrop-filter: var(--ev-blur-md);
        border: 1px solid var(--ev-border) !important;
        border-radius: var(--ev-radius-lg) !important;
        padding: 1.5rem !important;
        box-shadow: var(--ev-shadow-sm);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }

    [data-testid="stMetric"]::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: var(--ev-gradient-primary);
        opacity: 0;
        transition: opacity 0.3s ease;
    }

    [data-testid="stMetric"]:hover {
        transform: translateY(-4px);
        box-shadow: var(--ev-shadow-lg);
        border-color: var(--ev-border-light);
    }

    [data-testid="stMetric"]:hover::after {
        opacity: 1;
    }

    [data-testid="stMetricValue"] {
        font-size: 2.25rem !important;
        font-weight: 700 !important;
        color: var(--ev-text-primary) !important;
        letter-spacing: -0.02em;
    }

    [data-testid="stMetricLabel"] {
        font-size: 0.8rem !important;
        color: var(--ev-text-muted) !important;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 0.5rem;
    }

    [data-testid="stMetricDelta"] {
        font-size: 0.9rem;
        font-weight: 600;
    }

    /* ========== TABS - MODERN PILL STYLE ========== */
    .stTabs {
        background: transparent;
        margin: 1.5rem 0;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
        background: var(--ev-bg-glass);
        backdrop-filter: var(--ev-blur-sm);
        border: 1px solid var(--ev-border);
        border-radius: var(--ev-radius-full);
        padding: 0.5rem;
        box-shadow: var(--ev-shadow-sm);
    }

    .stTabs [data-baseweb="tab"] {
        background: transparent;
        color: var(--ev-text-muted);
        font-weight: 600;
        font-size: 0.9rem;
        border: none;
        border-radius: var(--ev-radius-full);
        padding: 0.75rem 1.5rem;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
    }

    .stTabs [data-baseweb="tab"]:hover {
        background: var(--ev-bg-hover);
        color: var(--ev-text-primary);
    }

    .stTabs [aria-selected="true"] {
        background: var(--ev-gradient-primary) !important;
        color: white !important;
        box-shadow: var(--ev-shadow-glow-primary);
    }

    .stTabs [data-baseweb="tab-panel"] {
        background: var(--ev-bg-glass);
        backdrop-filter: var(--ev-blur-md);
        border: 1px solid var(--ev-border);
        border-radius: var(--ev-radius-lg);
        padding: 2rem;
        margin-top: 1rem;
        box-shadow: var(--ev-shadow-md);
    }

    /* ========== EXPANDER - ACCORDION STYLE ========== */
    .streamlit-expanderHeader {
        background: var(--ev-bg-glass) !important;
        backdrop-filter: var(--ev-blur-sm);
        color: var(--ev-text-primary) !important;
        font-weight: 600;
        border: 1px solid var(--ev-border) !important;
        border-radius: var(--ev-radius-md) !important;
        padding: 1rem 1.5rem !important;
        transition: all 0.25s ease;
    }

    .streamlit-expanderHeader:hover {
        background: var(--ev-bg-hover) !important;
        border-color: var(--ev-border-light) !important;
    }

    /* ========== INPUTS - PREMIUM STYLE ========== */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div,
    .stTextArea > div > div > textarea {
        background: var(--ev-bg-glass) !important;
        backdrop-filter: var(--ev-blur-sm);
        border: 1.5px solid var(--ev-border) !important;
        border-radius: var(--ev-radius-md) !important;
        color: var(--ev-text-primary) !important;
        padding: 0.875rem 1rem !important;
        transition: all 0.25s ease;
        font-size: 0.95rem;
        font-weight: 500;
    }

    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus,
    .stSelectbox > div > div:focus-within,
    .stTextArea > div > div > textarea:focus {
        border-color: var(--ev-primary) !important;
        box-shadow: 0 0 0 3px rgba(123, 97, 255, 0.15) !important;
        outline: none !important;
        background: var(--ev-bg-elevated) !important;
    }

    /* ========== FILE UPLOADER - DRAG & DROP GLOW ========== */
    [data-testid="stFileUploader"] {
        background: var(--ev-bg-glass);
        backdrop-filter: var(--ev-blur-md);
        border: 2px dashed var(--ev-border-light);
        border-radius: var(--ev-radius-lg);
        padding: 2.5rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
    }

    [data-testid="stFileUploader"]::before {
        content: '📁';
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        font-size: 3rem;
        opacity: 0.2;
        pointer-events: none;
    }

    [data-testid="stFileUploader"]:hover {
        border-color: var(--ev-primary);
        background: var(--ev-bg-hover);
        box-shadow: var(--ev-shadow-glow-primary);
    }

    [data-testid="stFileUploader"] section {
        border: none;
        background: transparent;
    }

    /* ========== ALERTS - MODERN NOTIFICATION STYLE ========== */
    .stAlert {
        background: var(--ev-bg-glass) !important;
        backdrop-filter: var(--ev-blur-md);
        border: 1px solid var(--ev-border);
        border-left: 4px solid;
        border-radius: var(--ev-radius-md);
        padding: 1rem 1.5rem;
        color: var(--ev-text-primary);
        box-shadow: var(--ev-shadow-sm);
    }

    div[data-baseweb="notification"][kind="info"] {
        border-left-color: var(--ev-cyan);
        background: rgba(75, 225, 236, 0.08) !important;
    }

    div[data-baseweb="notification"][kind="success"] {
        border-left-color: var(--ev-success);
        background: rgba(0, 245, 160, 0.08) !important;
    }

    div[data-baseweb="notification"][kind="warning"] {
        border-left-color: var(--ev-warning);
        background: rgba(255, 184, 77, 0.08) !important;
    }

    div[data-baseweb="notification"][kind="error"] {
        border-left-color: var(--ev-danger);
        background: rgba(255, 107, 157, 0.08) !important;
    }

    /* ========== DATAFRAMES - SLEEK TABLE DESIGN ========== */
    .dataframe {
        background: var(--ev-bg-glass);
        backdrop-filter: var(--ev-blur-md);
        border: 1px solid var(--ev-border);
        border-radius: var(--ev-radius-lg);
        overflow: hidden;
        font-size: 0.9rem;
        box-shadow: var(--ev-shadow-sm);
    }

    .dataframe thead th {
        background: var(--ev-bg-elevated);
        color: var(--ev-text-primary);
        font-weight: 700;
        padding: 1rem 1.25rem;
        border-bottom: 2px solid var(--ev-border-light);
        text-transform: uppercase;
        font-size: 0.75rem;
        letter-spacing: 0.1em;
    }

    .dataframe tbody td {
        background: transparent;
        color: var(--ev-text-secondary);
        padding: 1rem 1.25rem;
        border-bottom: 1px solid var(--ev-border);
    }

    .dataframe tbody tr {
        transition: all 0.2s ease;
    }

    .dataframe tbody tr:hover {
        background: var(--ev-bg-hover);
        transform: translateX(2px);
    }

    /* ========== PROGRESS BAR - GRADIENT ========== */
    .stProgress > div > div {
        background: var(--ev-bg-elevated);
        border-radius: var(--ev-radius-full);
        overflow: hidden;
        height: 8px;
    }

    .stProgress > div > div > div {
        background: var(--ev-gradient-primary);
        border-radius: var(--ev-radius-full);
        box-shadow: 0 0 10px rgba(123, 97, 255, 0.5);
    }

    /* ========== SCROLLBAR - MODERN THIN STYLE ========== */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }

    ::-webkit-scrollbar-track {
        background: var(--ev-bg-secondary);
    }

    ::-webkit-scrollbar-thumb {
        background: var(--ev-bg-hover);
        border-radius: var(--ev-radius-full);
        border: 2px solid var(--ev-bg-secondary);
    }

    ::-webkit-scrollbar-thumb:hover {
        background: var(--ev-primary);
    }

    /* ========== DIVIDER - GRADIENT LINE ========== */
    hr {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, var(--ev-border-light), transparent);
        margin: 2rem 0;
    }

    /* ========== SPINNER - ANIMATED ========== */
    .stSpinner > div {
        border: 3px solid var(--ev-bg-hover);
        border-top-color: var(--ev-primary);
        border-radius: 50%;
    }

    /* ========== ANIMATIONS ========== */
    @keyframes fade-in-up {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    @keyframes glow-pulse {
        0%, 100% {
            box-shadow: 0 0 20px rgba(123, 97, 255, 0.3);
        }
        50% {
            box-shadow: 0 0 40px rgba(123, 97, 255, 0.6);
        }
    }

    @keyframes gradient-shift {
        0% {
            background-position: 0% 50%;
        }
        50% {
            background-position: 100% 50%;
        }
        100% {
            background-position: 0% 50%;
        }
    }

    /* Apply fade-in to main content */
    .block-container > div {
        animation: fade-in-up 0.5s ease-out;
    }

    /* ========== UTILITY CLASSES ========== */
    .glass-card {
        background: var(--ev-bg-glass);
        backdrop-filter: var(--ev-blur-md);
        border: 1px solid var(--ev-border);
        border-radius: var(--ev-radius-lg);
        padding: 1.5rem;
        box-shadow: var(--ev-shadow-md);
    }

    .gradient-text {
        background: var(--ev-gradient-primary);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    .glow-on-hover {
        transition: all 0.3s ease;
    }

    .glow-on-hover:hover {
        box-shadow: var(--ev-shadow-glow-primary);
    }

    /* ========== RESPONSIVE ADJUSTMENTS ========== */
    @media (max-width: 768px) {
        .block-container {
            padding: 1rem !important;
        }

        h1 {
            font-size: 2rem;
        }

        h2 {
            font-size: 1.5rem;
        }

        [data-testid="stMetricValue"] {
            font-size: 1.75rem !important;
        }
    }

    /* ========== HIDE STREAMLIT BRANDING ========== */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* ========== CUSTOM CONTAINER BACKGROUNDS ========== */
    .main > .block-container > div {
        background: var(--ev-bg-glass);
        backdrop-filter: var(--ev-blur-sm);
        border: 1px solid var(--ev-border);
        border-radius: var(--ev-radius-lg);
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: var(--ev-shadow-sm);
    }
</style>
"""
