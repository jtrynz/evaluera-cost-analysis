"""
EVALUERA - Ultra Professional Design System
Maximum Contrast, Fluid Typography, Professional Loading Animations
WCAG AAA Compliant, Enterprise-Grade UI
"""

ULTRA_PROFESSIONAL_CSS = """
<style>
    /* ========== IMPORTS - PREMIUM FONTS ========== */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;650;700;800;900&display=swap');

    /* ========== DESIGN TOKENS - MAXIMUM CONTRAST ========== */
    :root {
        /* Dark Surfaces - Layered Depth */
        --bg: #0B0F14;
        --surface-1: #111723;
        --surface-2: #16202E;
        --surface-3: #1B2838;

        /* Text - High Contrast (WCAG AAA) */
        --fg-1: #EAF0F6;   /* Primary text (≥12:1 ratio) */
        --fg-2: #C7D1DD;   /* Secondary text (≥7:1 ratio) */
        --fg-3: #9AA7B5;   /* Tertiary text (≥4.5:1 ratio) */

        /* Accent Colors */
        --accent-1: #7B61FF;
        --accent-2: #4BE1EC;
        --focus: #9AD6FF;

        /* Borders & Dividers */
        --line-1: #2B3A4B;
        --line-2: #35475C;

        /* Shadows - Layered */
        --shadow-1: 0 10px 30px rgba(0,0,0,0.35), 0 2px 12px rgba(0,0,0,0.25);
        --shadow-2: 0 4px 16px rgba(0,0,0,0.3);
        --shadow-focus: 0 0 0 3px rgba(154, 214, 255, 0.25);

        /* Radii */
        --radius: 16px;
        --radius-sm: 12px;
        --radius-lg: 20px;
        --radius-full: 9999px;

        /* Spacing Scale */
        --space-1: 8px;
        --space-2: 12px;
        --space-3: 16px;
        --space-4: 24px;
        --space-5: 32px;
        --space-6: 40px;
        --space-8: 64px;
    }

    /* ========== GLOBAL RESETS ========== */
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }

    /* ========== BASE TYPOGRAPHY - FLUID & LARGE ========== */
    html {
        font-family: 'Inter', system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        font-size: clamp(16px, 1.05vw + 14px, 19px);
        line-height: 1.5;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
    }

    html, body, [data-testid="stAppViewContainer"], .main {
        background: var(--bg) !important;
        color: var(--fg-1) !important;
    }

    /* ========== LAYOUT - LARGER CONTAINER ========== */
    .main {
        padding: clamp(16px, 2.4vw, 32px) !important;
        margin: 0 auto !important;
    }

    .block-container {
        max-width: min(1280px, 92vw) !important;
        margin: 0 auto !important;
        padding: clamp(16px, 2.2vw, 28px) !important;
    }

    /* ========== TYPOGRAPHY HIERARCHY - HIGH CONTRAST ========== */
    h1 {
        font-size: clamp(28px, 2.2vw + 22px, 42px);
        font-weight: 700;
        color: var(--fg-1);
        letter-spacing: -0.03em;
        line-height: 1.2;
        margin-bottom: var(--space-3);
    }

    h2 {
        font-size: clamp(22px, 1.6vw + 18px, 32px);
        font-weight: 650;
        color: var(--fg-1);
        letter-spacing: -0.02em;
        line-height: 1.3;
        margin: var(--space-5) 0 var(--space-3) 0;
        position: relative;
        padding-left: var(--space-3);
    }

    h2::before {
        content: '';
        position: absolute;
        left: 0;
        top: 50%;
        transform: translateY(-50%);
        width: 4px;
        height: 28px;
        background: linear-gradient(180deg, var(--accent-1), var(--accent-2));
        border-radius: 2px;
    }

    h3 {
        font-size: clamp(18px, 1.2vw + 16px, 24px);
        font-weight: 600;
        color: var(--fg-1);
        letter-spacing: -0.01em;
        margin: var(--space-4) 0 var(--space-2) 0;
    }

    h4 {
        font-size: clamp(14px, 0.9vw + 13px, 16px);
        font-weight: 600;
        color: var(--fg-2);
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin: var(--space-3) 0 var(--space-2) 0;
    }

    p, div, span, label {
        color: var(--fg-2);
        font-size: clamp(15px, 0.8vw + 14px, 17px);
        line-height: 1.6;
        font-weight: 400;
    }

    /* Strong emphasis */
    strong, b {
        color: var(--fg-1);
        font-weight: 650;
    }

    /* Subtle text */
    .text-muted, caption {
        color: var(--fg-3) !important;
    }

    /* ========== BUTTONS - HIGH CONTRAST ========== */
    .stButton > button {
        background: linear-gradient(90deg, var(--accent-1), var(--accent-2)) !important;
        color: #0A0D12 !important;
        font-weight: 650;
        font-size: clamp(14px, 0.9vw + 13px, 16px);
        border: none !important;
        border-radius: 14px !important;
        padding: 12px 20px !important;
        transition: transform 0.15s ease, box-shadow 0.2s ease, filter 0.2s ease;
        box-shadow: var(--shadow-2);
        letter-spacing: 0.01em;
    }

    .stButton > button:hover {
        transform: translateY(-1px);
        filter: brightness(1.05);
        box-shadow: 0 0 24px rgba(123, 97, 255, 0.4), var(--shadow-2);
    }

    .stButton > button:active {
        transform: translateY(0);
    }

    .stButton > button:focus-visible {
        outline: 2px solid var(--focus);
        outline-offset: 2px;
    }

    .stButton > button[kind="secondary"] {
        background: transparent !important;
        color: var(--fg-1) !important;
        border: 1px solid var(--line-2) !important;
    }

    .stButton > button[kind="secondary"]:hover {
        background: var(--surface-2) !important;
        border-color: var(--accent-1) !important;
    }

    /* Loading Button State */
    .stButton > button[disabled] {
        opacity: 0.6;
        cursor: not-allowed;
        position: relative;
    }

    /* ========== CARDS & SECTIONS - DEPTH & CONTRAST ========== */
    [data-testid="stMetric"],
    .section-card {
        background: linear-gradient(180deg, var(--surface-1), var(--surface-2));
        border: 1px solid var(--line-1);
        border-radius: var(--radius);
        box-shadow: var(--shadow-1);
        padding: clamp(16px, 2.2vw, 28px) !important;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
    }

    [data-testid="stMetric"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 36px rgba(0,0,0,0.4), 0 4px 16px rgba(0,0,0,0.3);
        border-color: var(--line-2);
    }

    [data-testid="stMetricValue"] {
        font-size: clamp(28px, 2vw + 24px, 40px) !important;
        font-weight: 700 !important;
        color: var(--fg-1) !important;
        letter-spacing: -0.02em;
    }

    [data-testid="stMetricLabel"] {
        font-size: clamp(12px, 0.7vw + 11px, 14px) !important;
        color: var(--fg-2) !important;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-bottom: var(--space-2);
    }

    [data-testid="stMetricDelta"] {
        font-size: clamp(14px, 0.8vw + 13px, 16px);
        font-weight: 600;
        margin-top: var(--space-1);
    }

    /* ========== HEADER HERO - GRADIENT BANNER ========== */
    .hero-banner {
        background: linear-gradient(135deg, rgba(123,97,255,0.18), rgba(75,225,236,0.12));
        border: 1px solid var(--line-1);
        border-radius: var(--radius-lg);
        padding: var(--space-6);
        margin-bottom: var(--space-5);
        box-shadow: var(--shadow-1);
        text-align: center;
    }

    /* ========== INPUTS - ACCESSIBLE & READABLE ========== */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div,
    .stTextArea > div > div > textarea {
        background: var(--surface-2) !important;
        border: 1px solid var(--line-2) !important;
        border-radius: var(--radius-sm) !important;
        color: var(--fg-1) !important;
        padding: 10px 12px !important;
        font-size: clamp(14px, 0.9vw + 13px, 16px);
        font-weight: 500;
        transition: all 0.2s ease;
    }

    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus,
    .stSelectbox > div > div:focus-within,
    .stTextArea > div > div > textarea:focus {
        border-color: var(--accent-1) !important;
        box-shadow: var(--shadow-focus) !important;
        outline: none !important;
        background: var(--surface-3) !important;
    }

    /* Input Labels */
    .stTextInput > label,
    .stNumberInput > label,
    .stSelectbox > label,
    .stTextArea > label {
        color: var(--fg-2) !important;
        font-weight: 600;
        font-size: clamp(13px, 0.8vw + 12px, 15px);
        margin-bottom: var(--space-1);
    }

    /* ========== TABS - CLEAR HIERARCHY ========== */
    .stTabs {
        margin: var(--space-5) 0;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: var(--space-2);
        background: var(--surface-1);
        border: 1px solid var(--line-1);
        border-radius: var(--radius-lg);
        padding: var(--space-1);
        box-shadow: var(--shadow-2);
    }

    .stTabs [data-baseweb="tab"] {
        background: transparent;
        color: var(--fg-3);
        font-weight: 600;
        font-size: clamp(14px, 0.9vw + 13px, 16px);
        border: none;
        border-radius: var(--radius-sm);
        padding: var(--space-2) var(--space-4);
        transition: all 0.2s ease;
    }

    .stTabs [data-baseweb="tab"]:hover {
        background: var(--surface-2);
        color: var(--fg-2);
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(90deg, var(--accent-1), var(--accent-2)) !important;
        color: #0A0D12 !important;
        font-weight: 650;
        box-shadow: 0 0 20px rgba(123, 97, 255, 0.3);
    }

    .stTabs [data-baseweb="tab-panel"] {
        background: linear-gradient(180deg, var(--surface-1), var(--surface-2));
        border: 1px solid var(--line-1);
        border-radius: var(--radius);
        padding: var(--space-5);
        margin-top: var(--space-3);
        box-shadow: var(--shadow-1);
    }

    /* ========== FILE UPLOADER - PROFESSIONAL ========== */
    [data-testid="stFileUploader"] {
        background: var(--surface-1);
        border: 2px dashed var(--line-2);
        border-radius: var(--radius);
        padding: var(--space-6);
        transition: all 0.3s ease;
        position: relative;
    }

    [data-testid="stFileUploader"]::before {
        content: '📁';
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        font-size: 4rem;
        opacity: 0.15;
        pointer-events: none;
    }

    [data-testid="stFileUploader"]:hover {
        border-color: var(--accent-1);
        background: var(--surface-2);
        box-shadow: 0 0 30px rgba(123, 97, 255, 0.2);
    }

    [data-testid="stFileUploader"] section {
        border: none;
        background: transparent;
    }

    /* ========== EXPANDER - ACCORDION ========== */
    .streamlit-expanderHeader {
        background: var(--surface-1) !important;
        color: var(--fg-1) !important;
        font-weight: 600;
        font-size: clamp(14px, 0.9vw + 13px, 16px);
        border: 1px solid var(--line-1) !important;
        border-radius: var(--radius-sm) !important;
        padding: var(--space-3) var(--space-4) !important;
        transition: all 0.2s ease;
    }

    .streamlit-expanderHeader:hover {
        background: var(--surface-2) !important;
        border-color: var(--line-2) !important;
    }

    /* ========== ALERTS - HIGH CONTRAST ========== */
    .stAlert {
        background: var(--surface-1) !important;
        border: 1px solid var(--line-1);
        border-left: 4px solid;
        border-radius: var(--radius-sm);
        padding: var(--space-3) var(--space-4);
        color: var(--fg-1);
        box-shadow: var(--shadow-2);
        font-size: clamp(14px, 0.9vw + 13px, 16px);
    }

    div[data-baseweb="notification"][kind="info"] {
        border-left-color: var(--accent-2);
        background: linear-gradient(90deg, rgba(75, 225, 236, 0.08), var(--surface-1)) !important;
    }

    div[data-baseweb="notification"][kind="success"] {
        border-left-color: #00F5A0;
        background: linear-gradient(90deg, rgba(0, 245, 160, 0.08), var(--surface-1)) !important;
    }

    div[data-baseweb="notification"][kind="warning"] {
        border-left-color: #FFB84D;
        background: linear-gradient(90deg, rgba(255, 184, 77, 0.08), var(--surface-1)) !important;
    }

    div[data-baseweb="notification"][kind="error"] {
        border-left-color: #FF6B9D;
        background: linear-gradient(90deg, rgba(255, 107, 157, 0.08), var(--surface-1)) !important;
    }

    /* ========== DATAFRAMES - PROFESSIONAL TABLE ========== */
    .dataframe {
        background: var(--surface-1);
        border: 1px solid var(--line-1);
        border-radius: var(--radius);
        overflow: hidden;
        font-size: clamp(13px, 0.8vw + 12px, 15px);
        box-shadow: var(--shadow-1);
    }

    .dataframe thead th {
        background: var(--surface-2);
        color: var(--fg-1);
        font-weight: 700;
        padding: var(--space-3) var(--space-4);
        border-bottom: 2px solid var(--line-2);
        text-transform: uppercase;
        font-size: clamp(11px, 0.7vw + 10px, 13px);
        letter-spacing: 0.1em;
    }

    .dataframe tbody td {
        background: transparent;
        color: var(--fg-2);
        padding: var(--space-3) var(--space-4);
        border-bottom: 1px solid var(--line-1);
    }

    .dataframe tbody tr {
        transition: all 0.2s ease;
    }

    .dataframe tbody tr:hover {
        background: var(--surface-2);
        transform: translateX(2px);
    }

    /* ========== PROGRESS BAR - SMOOTH ========== */
    .stProgress > div > div {
        height: 8px;
        border-radius: var(--radius-full);
        background: var(--surface-2);
        border: 1px solid var(--line-2);
        overflow: hidden;
    }

    .stProgress > div > div > div {
        background: linear-gradient(90deg, var(--accent-2), var(--accent-1));
        border-radius: var(--radius-full);
        box-shadow: 0 0 20px rgba(123, 97, 255, 0.35);
        transition: width 0.25s ease;
    }

    /* ========== LOADING ANIMATIONS ========== */

    /* 1. Skeleton Loader */
    @keyframes shimmer {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
    }

    .skeleton {
        position: relative;
        overflow: hidden;
        background: linear-gradient(180deg, #1A2330, #192230);
        border-radius: var(--radius-sm);
        height: 40px;
        margin: var(--space-2) 0;
    }

    .skeleton::after {
        content: "";
        position: absolute;
        inset: 0;
        transform: translateX(-100%);
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.06), transparent);
        animation: shimmer 1.2s infinite;
    }

    /* 2. Spinner - Button Loading */
    @keyframes spin {
        to { transform: rotate(360deg); }
    }

    .btn-spinner {
        display: inline-block;
        width: 18px;
        height: 18px;
        border-radius: 50%;
        border: 2px solid rgba(10,13,18,0.3);
        border-top-color: #0A0D12;
        animation: spin 0.8s linear infinite;
    }

    /* 3. Page Loader - Aurora */
    @keyframes rotate {
        to { transform: rotate(360deg); }
    }

    .page-loader {
        position: fixed;
        inset: 0;
        display: flex;
        align-items: center;
        justify-content: center;
        background: rgba(8, 11, 16, 0.75);
        z-index: 9999;
    }

    .aurora {
        width: 160px;
        height: 160px;
        border-radius: 50%;
        background: conic-gradient(from 0deg, var(--accent-1), var(--accent-2), var(--accent-1));
        mask: radial-gradient(circle, transparent 54%, black 55%);
        animation: rotate 2.4s linear infinite;
    }

    /* ========== FOCUS STATES - ACCESSIBLE ========== */
    *:focus-visible {
        outline: 2px solid var(--focus);
        outline-offset: 2px;
        border-radius: 10px;
    }

    /* ========== SCROLLBAR ========== */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }

    ::-webkit-scrollbar-track {
        background: var(--surface-1);
    }

    ::-webkit-scrollbar-thumb {
        background: var(--surface-3);
        border-radius: var(--radius-full);
        border: 2px solid var(--surface-1);
    }

    ::-webkit-scrollbar-thumb:hover {
        background: var(--line-2);
    }

    /* ========== DIVIDER ========== */
    hr {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, var(--line-2), transparent);
        margin: var(--space-5) 0;
    }

    /* ========== SPINNER - STREAMLIT ========== */
    .stSpinner > div {
        border: 3px solid var(--surface-3);
        border-top-color: var(--accent-1);
        border-radius: 50%;
    }

    /* ========== MOTION REDUCTION ========== */
    @media (prefers-reduced-motion: reduce) {
        *,
        *::before,
        *::after {
            animation-duration: 0.01ms !important;
            animation-iteration-count: 1 !important;
            transition-duration: 0.01ms !important;
        }
    }

    /* ========== RESPONSIVE ADJUSTMENTS ========== */
    @media (max-width: 768px) {
        .block-container {
            padding: var(--space-3) !important;
        }

        h1 {
            font-size: clamp(24px, 4vw, 32px);
        }

        h2 {
            font-size: clamp(20px, 3vw, 26px);
        }

        [data-testid="stMetricValue"] {
            font-size: clamp(24px, 4vw, 32px) !important;
        }

        .hero-banner {
            padding: var(--space-4);
        }
    }

    /* ========== HIDE STREAMLIT BRANDING ========== */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* ========== UTILITY CLASSES ========== */
    .text-gradient {
        background: linear-gradient(90deg, var(--accent-1), var(--accent-2));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    .card {
        background: var(--surface-1);
        border: 1px solid var(--line-1);
        border-radius: var(--radius);
        box-shadow: var(--shadow-1);
        padding: var(--space-4);
    }

    /* ========== ARIA ATTRIBUTES FOR LOADING STATES ========== */
    [aria-busy="true"] {
        cursor: wait;
        opacity: 0.7;
    }

    [role="progressbar"] {
        /* Ensure screen readers announce progress */
    }

    .skeleton[aria-hidden="true"] {
        /* Hidden from screen readers */
    }
</style>
"""
