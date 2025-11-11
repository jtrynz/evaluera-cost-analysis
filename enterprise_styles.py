"""
EVALUERA - Enterprise Design System
Ultra-professionelles, krasses Dashboard-Design
"""

ENTERPRISE_CSS = """
<style>
    /* ========== IMPORTS ========== */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600;700&display=swap');

    /* ========== CSS VARIABLES - MAXIMUM CONTRAST PROFESSIONAL ========== */
    :root {
        /* Background - Pure Black Professional */
        --ev-bg-primary: #000000;
        --ev-bg-secondary: #0d0d0d;
        --ev-bg-elevated: #1a1a1a;
        --ev-bg-card: #141414;
        --ev-bg-hover: #1f1f1f;

        /* Text - Maximum Contrast */
        --ev-text-primary: #ffffff;
        --ev-text-secondary: #b3b3b3;
        --ev-text-muted: #808080;
        --ev-text-inverse: #000000;

        /* Accent Colors - High Contrast */
        --ev-primary: #3b82f6;
        --ev-primary-hover: #60a5fa;
        --ev-success: #22c55e;
        --ev-warning: #eab308;
        --ev-danger: #ef4444;
        --ev-info: #06b6d4;

        /* NO Gradients - Solid Professional */
        --ev-gradient-1: #3b82f6;
        --ev-gradient-2: #22c55e;
        --ev-gradient-3: #3b82f6;
        --ev-gradient-4: #ef4444;

        /* Borders - High Contrast */
        --ev-border: #2a2a2a;
        --ev-border-light: #404040;
        --ev-border-accent: #3b82f6;

        /* Shadows - Subtle Professional */
        --ev-shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.8);
        --ev-shadow-md: 0 2px 4px rgba(0, 0, 0, 0.9);
        --ev-shadow-lg: 0 4px 8px rgba(0, 0, 0, 0.95);
        --ev-shadow-glow: none;
        --ev-shadow-glow-success: none;
        --ev-shadow-glow-danger: none;

        /* Spacing */
        --ev-space-xs: 0.25rem;
        --ev-space-sm: 0.5rem;
        --ev-space-md: 1rem;
        --ev-space-lg: 1.5rem;
        --ev-space-xl: 2rem;

        /* Border Radius */
        --ev-radius-sm: 6px;
        --ev-radius-md: 10px;
        --ev-radius-lg: 14px;

        /* Typography */
        --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        --font-mono: 'JetBrains Mono', 'Courier New', monospace;
    }

    /* ========== GLOBAL RESET ========== */
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }

    html, body, [data-testid="stAppViewContainer"], .main {
        background: var(--ev-bg-primary) !important;
        color: var(--ev-text-primary) !important;
        font-family: var(--font-sans) !important;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
    }

    /* ========== FULL WIDTH - NO PADDING ========== */
    .main {
        padding: 0 !important;
        margin: 0 !important;
    }

    .block-container {
        max-width: 100% !important;
        padding: 1.5rem 2.5rem !important;
        margin: 0 !important;
    }

    section[data-testid="stSidebar"] {
        background: var(--ev-bg-secondary);
        border-right: 1px solid var(--ev-border);
    }

    /* ========== TYPOGRAPHY ========== */
    h1 {
        font-size: 2.5rem;
        font-weight: 700;
        letter-spacing: -0.02em;
        color: var(--ev-text-primary);
        margin-bottom: 0.5rem;
        line-height: 1.2;
        text-transform: uppercase;
        border-bottom: 2px solid var(--ev-border-light);
        padding-bottom: 1rem;
    }

    h2 {
        font-size: 1.875rem;
        font-weight: 700;
        color: var(--ev-text-primary);
        letter-spacing: -0.02em;
        margin: 1.5rem 0 1rem 0;
    }

    h3 {
        font-size: 1.5rem;
        font-weight: 600;
        color: var(--ev-text-primary);
        letter-spacing: -0.01em;
        margin: 1rem 0 0.75rem 0;
    }

    p, div, span {
        color: var(--ev-text-secondary);
        font-size: 0.95rem;
        line-height: 1.6;
    }

    /* ========== STREAMLIT COLUMNS ========== */
    [data-testid="column"] {
        padding: 0 0.75rem !important;
    }

    /* ========== BUTTONS - PROFESSIONAL ========== */
    .stButton > button {
        background: var(--ev-primary);
        color: #ffffff;
        font-weight: 600;
        font-size: 0.9rem;
        border: none;
        border-radius: 2px;
        padding: 0.75rem 2rem;
        transition: background 0.15s ease;
        box-shadow: none;
        letter-spacing: 0.05em;
        text-transform: uppercase;
    }

    .stButton > button:hover {
        background: var(--ev-primary-hover);
        transform: none;
        box-shadow: none;
    }

    .stButton > button:active {
        background: #2563eb;
    }

    .stButton > button[kind="secondary"] {
        background: transparent;
        color: var(--ev-text-primary);
        border: 2px solid var(--ev-border-light);
    }

    .stButton > button[kind="secondary"]:hover {
        background: var(--ev-bg-elevated);
        border-color: var(--ev-primary);
    }

    /* ========== METRICS / CARDS - PROFESSIONAL ========== */
    [data-testid="stMetric"] {
        background: var(--ev-bg-card);
        border: 2px solid var(--ev-border-light);
        border-radius: 0;
        padding: 1.5rem;
        box-shadow: none;
        transition: border-color 0.15s ease;
        position: relative;
    }

    [data-testid="stMetric"]:hover {
        border-color: var(--ev-primary);
        transform: none;
        box-shadow: none;
    }

    [data-testid="stMetricValue"] {
        font-size: 2.25rem;
        font-weight: 700;
        color: var(--ev-text-primary);
        font-family: var(--font-mono);
        letter-spacing: -0.02em;
    }

    [data-testid="stMetricLabel"] {
        font-size: 0.8rem;
        color: var(--ev-text-muted);
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-bottom: 0.5rem;
    }

    [data-testid="stMetricDelta"] {
        font-size: 0.9rem;
        font-weight: 600;
    }

    /* ========== TABS - PROFESSIONAL ========== */
    .stTabs {
        background: transparent;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 0;
        background: transparent;
        border-radius: 0;
        padding: 0;
        border-bottom: 2px solid var(--ev-border);
    }

    .stTabs [data-baseweb="tab"] {
        background: transparent;
        color: var(--ev-text-secondary);
        font-weight: 600;
        font-size: 0.85rem;
        border: none;
        border-radius: 0;
        padding: 1rem 2rem;
        transition: all 0.15s ease;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    .stTabs [data-baseweb="tab"]:hover {
        background: var(--ev-bg-elevated);
        color: var(--ev-text-primary);
    }

    .stTabs [aria-selected="true"] {
        background: transparent !important;
        color: var(--ev-primary) !important;
        border-bottom: 2px solid var(--ev-primary) !important;
        box-shadow: none;
    }

    .stTabs [data-baseweb="tab-panel"] {
        background: var(--ev-bg-card);
        border: 2px solid var(--ev-border);
        border-radius: 0;
        padding: 2rem;
        margin-top: 0;
        box-shadow: none;
    }

    /* ========== EXPANDER ========== */
    .streamlit-expanderHeader {
        background: var(--ev-bg-card);
        color: var(--ev-text-primary);
        font-weight: 600;
        border: 1px solid var(--ev-border);
        border-radius: var(--ev-radius-sm);
        padding: 1rem 1.5rem;
        transition: all 0.2s ease;
    }

    .streamlit-expanderHeader:hover {
        background: var(--ev-bg-hover);
        border-color: var(--ev-border-light);
    }

    /* ========== INPUTS - PROFESSIONAL ========== */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div,
    .stTextArea > div > div > textarea {
        background: var(--ev-bg-elevated) !important;
        border: 2px solid var(--ev-border-light) !important;
        border-radius: 0 !important;
        color: var(--ev-text-primary) !important;
        padding: 0.875rem 1rem !important;
        transition: border-color 0.15s ease;
        font-size: 0.95rem;
        font-weight: 500;
    }

    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus,
    .stSelectbox > div > div:focus-within,
    .stTextArea > div > div > textarea:focus {
        border-color: var(--ev-primary) !important;
        box-shadow: none !important;
        outline: none !important;
        background: var(--ev-bg-card) !important;
    }

    /* ========== FILE UPLOADER ========== */
    [data-testid="stFileUploader"] {
        background: var(--ev-bg-card);
        border: 2px dashed var(--ev-border-light);
        border-radius: var(--ev-radius-md);
        padding: 2rem;
        transition: all 0.3s ease;
    }

    [data-testid="stFileUploader"]:hover {
        border-color: var(--ev-primary);
        background: var(--ev-bg-hover);
        box-shadow: 0 0 30px rgba(99, 102, 241, 0.2);
    }

    [data-testid="stFileUploader"] section {
        border: none;
        background: transparent;
    }

    /* ========== ALERTS / NOTIFICATIONS ========== */
    .stAlert {
        background: var(--ev-bg-card);
        border: 1px solid var(--ev-border);
        border-left: 4px solid;
        border-radius: var(--ev-radius-sm);
        padding: 1rem 1.5rem;
        color: var(--ev-text-primary);
    }

    div[data-baseweb="notification"][kind="info"] {
        border-left-color: var(--ev-info);
        background: rgba(59, 130, 246, 0.1);
    }

    div[data-baseweb="notification"][kind="success"] {
        border-left-color: var(--ev-success);
        background: rgba(16, 185, 129, 0.1);
    }

    div[data-baseweb="notification"][kind="warning"] {
        border-left-color: var(--ev-warning);
        background: rgba(245, 158, 11, 0.1);
    }

    div[data-baseweb="notification"][kind="error"] {
        border-left-color: var(--ev-danger);
        background: rgba(239, 68, 68, 0.1);
    }

    /* ========== DATAFRAMES / TABLES - PROFESSIONAL ========== */
    .dataframe {
        background: var(--ev-bg-card);
        border: 2px solid var(--ev-border-light);
        border-radius: 0;
        overflow: hidden;
        font-size: 0.85rem;
    }

    .dataframe thead th {
        background: var(--ev-bg-secondary);
        color: var(--ev-text-primary);
        font-weight: 700;
        padding: 1rem 1.25rem;
        border-bottom: 2px solid var(--ev-primary);
        text-transform: uppercase;
        font-size: 0.75rem;
        letter-spacing: 0.1em;
        font-family: var(--font-mono);
    }

    .dataframe tbody td {
        background: var(--ev-bg-card);
        color: var(--ev-text-secondary);
        padding: 1rem 1.25rem;
        border-bottom: 1px solid var(--ev-border);
        font-family: var(--font-mono);
    }

    .dataframe tbody tr:hover {
        background: var(--ev-bg-elevated);
        border-left: 3px solid var(--ev-primary);
    }

    /* ========== PROGRESS BAR ========== */
    .stProgress > div > div {
        background: var(--ev-bg-elevated);
        border-radius: 100px;
        overflow: hidden;
        height: 8px;
    }

    .stProgress > div > div > div {
        background: var(--ev-gradient-1);
        border-radius: 100px;
    }

    /* ========== SCROLLBAR ========== */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }

    ::-webkit-scrollbar-track {
        background: var(--ev-bg-secondary);
    }

    ::-webkit-scrollbar-thumb {
        background: var(--ev-bg-hover);
        border-radius: 100px;
        border: 2px solid var(--ev-bg-secondary);
    }

    ::-webkit-scrollbar-thumb:hover {
        background: var(--ev-border-light);
    }

    /* ========== DIVIDER ========== */
    hr {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, var(--ev-border), transparent);
        margin: 2rem 0;
    }

    /* ========== LOADING SPINNER ========== */
    .stSpinner > div {
        border: 3px solid var(--ev-bg-hover);
        border-top-color: var(--ev-primary);
        border-radius: 50%;
    }

    /* ========== ANIMATIONS ========== */
    @keyframes glow-pulse {
        0%, 100% {
            box-shadow: 0 0 20px rgba(99, 102, 241, 0.3);
        }
        50% {
            box-shadow: 0 0 40px rgba(99, 102, 241, 0.6);
        }
    }

    @keyframes slide-up {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    .animate-slide-up {
        animation: slide-up 0.5s cubic-bezier(0.4, 0, 0.2, 1);
    }

    /* ========== CUSTOM COMPONENTS ========== */

    /* Gradient Card */
    .gradient-card {
        background: var(--ev-bg-card);
        border: 1px solid var(--ev-border);
        border-radius: var(--ev-radius-lg);
        padding: 2rem;
        position: relative;
        overflow: hidden;
        box-shadow: var(--ev-shadow-md);
    }

    .gradient-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: var(--ev-gradient-3);
    }

    /* Stats Badge */
    .stats-badge {
        display: inline-block;
        padding: 0.5rem 1rem;
        border-radius: var(--ev-radius-full);
        font-weight: 600;
        font-size: 0.85rem;
        letter-spacing: 0.02em;
    }

    .stats-badge-success {
        background: rgba(16, 185, 129, 0.2);
        color: var(--ev-success);
        border: 1px solid rgba(16, 185, 129, 0.3);
    }

    .stats-badge-warning {
        background: rgba(245, 158, 11, 0.2);
        color: var(--ev-warning);
        border: 1px solid rgba(245, 158, 11, 0.3);
    }

    .stats-badge-danger {
        background: rgba(239, 68, 68, 0.2);
        color: var(--ev-danger);
        border: 1px solid rgba(239, 68, 68, 0.3);
    }

    /* ========== SIDEBAR SPECIFIC ========== */
    section[data-testid="stSidebar"] > div {
        background: var(--ev-bg-secondary);
        padding: 1.5rem 1rem;
    }

    /* ========== HIDE STREAMLIT BRANDING ========== */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* ========== UTILITY CLASSES ========== */
    .text-gradient {
        background: var(--ev-gradient-3);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    .glow {
        animation: glow-pulse 3s infinite;
    }

    .hover-scale {
        transition: transform 0.2s ease;
    }

    .hover-scale:hover {
        transform: scale(1.02);
    }
</style>
"""
