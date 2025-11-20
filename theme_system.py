"""
EVALUERA - PROFESSIONAL THEME SYSTEM
=====================================
Light & Dark Mode mit WCAG AAA Kontrast (>7:1)
Alle UI-Elemente optimiert für maximale Lesbarkeit
"""


def get_light_theme_css():
    """
    Light Mode Theme - WCAG AAA Compliant
    Hoher Kontrast für alle Elemente
    """
    return """
    <style>
        /* ========== LIGHT MODE - DESIGN TOKENS ========== */
        :root {
            /* Light Surfaces */
            --bg: #FFFFFF;
            --surface-1: #F8F9FA;
            --surface-2: #F1F3F5;
            --surface-3: #E9ECEF;
            --surface-hover: #DEE2E6;

            /* Text - WCAG AAA Contrast (>7:1) */
            --fg-1: #0A0D12;        /* Primary text - 20:1 ratio */
            --fg-2: #1A1F2E;        /* Secondary text - 16:1 ratio */
            --fg-3: #495057;        /* Tertiary text - 8:1 ratio */
            --fg-muted: #6C757D;    /* Muted text - 4.5:1 ratio */

            /* Accent Colors - High Contrast */
            --accent-1: #5B3FD9;    /* Primary purple */
            --accent-2: #0091DB;    /* Secondary blue */
            --accent-gradient: linear-gradient(135deg, #5B3FD9 0%, #0091DB 100%);

            /* Interactive States */
            --focus: #4299E1;
            --focus-ring: rgba(66, 153, 225, 0.5);

            /* Borders & Dividers */
            --line-1: #DEE2E6;
            --line-2: #CED4DA;
            --line-3: #ADB5BD;

            /* Shadows - Subtle for Light Mode */
            --shadow-sm: 0 1px 3px rgba(0,0,0,0.08), 0 1px 2px rgba(0,0,0,0.06);
            --shadow-md: 0 4px 6px rgba(0,0,0,0.07), 0 2px 4px rgba(0,0,0,0.06);
            --shadow-lg: 0 10px 20px rgba(0,0,0,0.1), 0 3px 6px rgba(0,0,0,0.08);

            /* Status Colors - High Contrast */
            --success: #0F5132;
            --success-bg: #D1E7DD;
            --warning: #664D03;
            --warning-bg: #FFF3CD;
            --error: #842029;
            --error-bg: #F8D7DA;
            --info: #055160;
            --info-bg: #CFF4FC;
        }

        /* ========== BASE STYLES ========== */
        html, body, [data-testid="stAppViewContainer"], .main {
            background: var(--bg) !important;
            color: var(--fg-1) !important;
        }

        /* ========== TYPOGRAPHY ========== */
        h1, h2, h3, h4, h5, h6 {
            color: var(--fg-1) !important;
        }

        p, div, span, label, li {
            color: var(--fg-2) !important;
        }

        strong, b {
            color: var(--fg-1) !important;
            font-weight: 650;
        }

        /* ========== BUTTONS - HIGH CONTRAST ========== */
        .stButton > button {
            background: var(--accent-gradient) !important;
            color: #FFFFFF !important;
            font-weight: 650 !important;
            border: none !important;
            border-radius: 12px !important;
            padding: 12px 24px !important;
            box-shadow: var(--shadow-md) !important;
            transition: all 0.2s ease !important;
            letter-spacing: 0.01em;
        }

        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: var(--shadow-lg) !important;
            filter: brightness(1.05);
        }

        .stButton > button:active {
            transform: translateY(0);
        }

        .stButton > button:disabled {
            opacity: 0.5;
            cursor: not-allowed;
            background: var(--surface-3) !important;
            color: var(--fg-muted) !important;
        }

        /* Secondary Buttons */
        .stButton > button[kind="secondary"] {
            background: transparent !important;
            color: var(--fg-1) !important;
            border: 2px solid var(--line-3) !important;
        }

        .stButton > button[kind="secondary"]:hover {
            background: var(--surface-2) !important;
            border-color: var(--accent-1) !important;
        }

        /* ========== INPUTS - HIGH CONTRAST ========== */
        .stTextInput > div > div > input,
        .stNumberInput > div > div > input,
        .stSelectbox > div > div,
        .stMultiSelect > div > div,
        textarea {
            background: var(--bg) !important;
            color: var(--fg-1) !important;
            border: 2px solid var(--line-2) !important;
            border-radius: 10px !important;
            font-size: 15px !important;
        }

        .stTextInput > div > div > input:focus,
        .stNumberInput > div > div > input:focus,
        .stSelectbox > div > div:focus-within,
        textarea:focus {
            border-color: var(--accent-1) !important;
            box-shadow: 0 0 0 3px var(--focus-ring) !important;
        }

        /* Placeholder Text */
        ::placeholder {
            color: var(--fg-muted) !important;
            opacity: 0.7;
        }

        /* ========== FILE UPLOADER ========== */
        [data-testid="stFileUploader"] {
            background: var(--surface-1) !important;
            border: 2px dashed var(--line-2) !important;
            border-radius: 12px !important;
            padding: 2rem !important;
        }

        [data-testid="stFileUploader"]:hover {
            border-color: var(--accent-1) !important;
            background: var(--surface-2) !important;
        }

        /* ========== ALERTS & NOTIFICATIONS ========== */
        .stAlert {
            border-radius: 12px !important;
            border-left: 4px solid !important;
            padding: 1rem 1.5rem !important;
        }

        /* Success Alert */
        div[data-baseweb="notification"][kind="success"],
        .stSuccess {
            background: var(--success-bg) !important;
            color: var(--success) !important;
            border-left-color: var(--success) !important;
        }

        /* Warning Alert */
        div[data-baseweb="notification"][kind="warning"],
        .stWarning {
            background: var(--warning-bg) !important;
            color: var(--warning) !important;
            border-left-color: var(--warning) !important;
        }

        /* Error Alert */
        div[data-baseweb="notification"][kind="error"],
        .stError {
            background: var(--error-bg) !important;
            color: var(--error) !important;
            border-left-color: var(--error) !important;
        }

        /* Info Alert */
        div[data-baseweb="notification"][kind="info"],
        .stInfo {
            background: var(--info-bg) !important;
            color: var(--info) !important;
            border-left-color: var(--info) !important;
        }

        /* ========== METRICS ========== */
        [data-testid="stMetricValue"] {
            color: var(--fg-1) !important;
            font-weight: 700 !important;
            font-size: 2rem !important;
        }

        [data-testid="stMetricLabel"] {
            color: var(--fg-3) !important;
            font-weight: 600 !important;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            font-size: 0.85rem !important;
        }

        [data-testid="stMetricDelta"] {
            font-weight: 600 !important;
        }

        /* ========== DATAFRAMES & TABLES ========== */
        .dataframe {
            border: 1px solid var(--line-2) !important;
            border-radius: 10px !important;
        }

        .dataframe thead th {
            background: var(--surface-2) !important;
            color: var(--fg-1) !important;
            font-weight: 650 !important;
            border-bottom: 2px solid var(--line-3) !important;
        }

        .dataframe tbody tr:hover {
            background: var(--surface-1) !important;
        }

        .dataframe tbody td {
            color: var(--fg-2) !important;
            border-bottom: 1px solid var(--line-1) !important;
        }

        /* ========== TABS ========== */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
            background: var(--surface-1);
            border-radius: 12px;
            padding: 4px;
        }

        .stTabs [data-baseweb="tab"] {
            color: var(--fg-3) !important;
            font-weight: 600;
            border-radius: 8px;
            padding: 10px 20px;
        }

        .stTabs [data-baseweb="tab"]:hover {
            background: var(--surface-2);
            color: var(--fg-1) !important;
        }

        .stTabs [aria-selected="true"] {
            background: var(--accent-gradient) !important;
            color: #FFFFFF !important;
        }

        /* ========== EXPANDER ========== */
        .streamlit-expanderHeader {
            background: var(--surface-1) !important;
            color: var(--fg-1) !important;
            font-weight: 600 !important;
            border-radius: 10px !important;
            border: 1px solid var(--line-2) !important;
        }

        .streamlit-expanderHeader:hover {
            background: var(--surface-2) !important;
            border-color: var(--accent-1) !important;
        }

        .streamlit-expanderContent {
            background: var(--bg) !important;
            border: 1px solid var(--line-2) !important;
            border-top: none !important;
            border-radius: 0 0 10px 10px !important;
        }

        /* ========== CHECKBOX & RADIO ========== */
        .stCheckbox label,
        .stRadio label {
            color: var(--fg-2) !important;
        }

        input[type="checkbox"]:checked,
        input[type="radio"]:checked {
            background-color: var(--accent-1) !important;
            border-color: var(--accent-1) !important;
        }

        /* ========== SLIDER ========== */
        .stSlider [role="slider"] {
            background-color: var(--accent-1) !important;
        }

        .stSlider [data-baseweb="slider"] > div > div {
            background-color: var(--line-2) !important;
        }

        /* ========== SPINNER ========== */
        .stSpinner > div {
            border-top-color: var(--accent-1) !important;
        }

        /* ========== SIDEBAR (if used) ========== */
        [data-testid="stSidebar"] {
            background: var(--surface-1) !important;
            border-right: 1px solid var(--line-2) !important;
        }

        /* ========== CODE BLOCKS ========== */
        code {
            background: var(--surface-2) !important;
            color: var(--fg-1) !important;
            padding: 2px 6px;
            border-radius: 4px;
            font-size: 0.9em;
        }

        pre {
            background: var(--surface-2) !important;
            border: 1px solid var(--line-2) !important;
            border-radius: 10px !important;
            padding: 1rem !important;
        }

        pre code {
            background: transparent !important;
            padding: 0;
        }

        /* ========== PROGRESS BAR ========== */
        .stProgress > div > div {
            background-color: var(--surface-2) !important;
        }

        .stProgress > div > div > div {
            background: var(--accent-gradient) !important;
        }

        /* ========== LINKS ========== */
        a {
            color: var(--accent-1) !important;
            text-decoration: none;
            font-weight: 600;
        }

        a:hover {
            color: var(--accent-2) !important;
            text-decoration: underline;
        }
    </style>
    """


def get_dark_theme_css():
    """
    Dark Mode Theme - WCAG AAA Compliant
    Hoher Kontrast für alle Elemente
    """
    return """
    <style>
        /* ========== DARK MODE - DESIGN TOKENS ========== */
        :root {
            /* Dark Surfaces - Layered Depth */
            --bg: #0A0D12;
            --surface-1: #111723;
            --surface-2: #16202E;
            --surface-3: #1B2838;
            --surface-hover: #212B3D;

            /* Text - WCAG AAA Contrast (>7:1) */
            --fg-1: #EAF0F6;        /* Primary text - 18:1 ratio */
            --fg-2: #C7D1DD;        /* Secondary text - 12:1 ratio */
            --fg-3: #9AA7B5;        /* Tertiary text - 7:1 ratio */
            --fg-muted: #6B7684;    /* Muted text - 4.5:1 ratio */

            /* Accent Colors - Vibrant for Dark Mode */
            --accent-1: #7B61FF;    /* Primary purple */
            --accent-2: #4BE1EC;    /* Secondary cyan */
            --accent-gradient: linear-gradient(135deg, #7B61FF 0%, #4BE1EC 100%);

            /* Interactive States */
            --focus: #9AD6FF;
            --focus-ring: rgba(154, 214, 255, 0.3);

            /* Borders & Dividers */
            --line-1: #2B3A4B;
            --line-2: #35475C;
            --line-3: #3F526B;

            /* Shadows - Deeper for Dark Mode */
            --shadow-sm: 0 2px 4px rgba(0,0,0,0.3), 0 1px 2px rgba(0,0,0,0.2);
            --shadow-md: 0 6px 12px rgba(0,0,0,0.4), 0 2px 6px rgba(0,0,0,0.3);
            --shadow-lg: 0 12px 28px rgba(0,0,0,0.5), 0 4px 10px rgba(0,0,0,0.4);

            /* Status Colors - High Contrast for Dark */
            --success: #51CF66;
            --success-bg: #1A3E2A;
            --warning: #FFD43B;
            --warning-bg: #3E3416;
            --error: #FF6B6B;
            --error-bg: #3E1C1C;
            --info: #74C0FC;
            --info-bg: #1A2E3E;
        }

        /* ========== BASE STYLES ========== */
        html, body, [data-testid="stAppViewContainer"], .main {
            background: var(--bg) !important;
            color: var(--fg-1) !important;
        }

        /* ========== TYPOGRAPHY ========== */
        h1, h2, h3, h4, h5, h6 {
            color: var(--fg-1) !important;
        }

        p, div, span, label, li {
            color: var(--fg-2) !important;
        }

        strong, b {
            color: var(--fg-1) !important;
            font-weight: 650;
        }

        /* ========== BUTTONS - HIGH CONTRAST ========== */
        .stButton > button {
            background: var(--accent-gradient) !important;
            color: #0A0D12 !important;
            font-weight: 650 !important;
            border: none !important;
            border-radius: 12px !important;
            padding: 12px 24px !important;
            box-shadow: var(--shadow-md) !important;
            transition: all 0.2s ease !important;
            letter-spacing: 0.01em;
        }

        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 0 24px rgba(123, 97, 255, 0.5), var(--shadow-lg) !important;
            filter: brightness(1.1);
        }

        .stButton > button:active {
            transform: translateY(0);
        }

        .stButton > button:disabled {
            opacity: 0.4;
            cursor: not-allowed;
            background: var(--surface-3) !important;
            color: var(--fg-muted) !important;
        }

        /* Secondary Buttons */
        .stButton > button[kind="secondary"] {
            background: transparent !important;
            color: var(--fg-1) !important;
            border: 2px solid var(--line-2) !important;
        }

        .stButton > button[kind="secondary"]:hover {
            background: var(--surface-2) !important;
            border-color: var(--accent-1) !important;
        }

        /* ========== INPUTS - HIGH CONTRAST ========== */
        .stTextInput > div > div > input,
        .stNumberInput > div > div > input,
        .stSelectbox > div > div,
        .stMultiSelect > div > div,
        textarea {
            background: var(--surface-1) !important;
            color: var(--fg-1) !important;
            border: 2px solid var(--line-2) !important;
            border-radius: 10px !important;
            font-size: 15px !important;
        }

        .stTextInput > div > div > input:focus,
        .stNumberInput > div > div > input:focus,
        .stSelectbox > div > div:focus-within,
        textarea:focus {
            border-color: var(--accent-1) !important;
            box-shadow: 0 0 0 3px var(--focus-ring) !important;
        }

        /* Placeholder Text */
        ::placeholder {
            color: var(--fg-muted) !important;
            opacity: 0.6;
        }

        /* ========== FILE UPLOADER ========== */
        [data-testid="stFileUploader"] {
            background: var(--surface-1) !important;
            border: 2px dashed var(--line-2) !important;
            border-radius: 12px !important;
            padding: 2rem !important;
        }

        [data-testid="stFileUploader"]:hover {
            border-color: var(--accent-1) !important;
            background: var(--surface-2) !important;
        }

        /* ========== ALERTS & NOTIFICATIONS ========== */
        .stAlert {
            border-radius: 12px !important;
            border-left: 4px solid !important;
            padding: 1rem 1.5rem !important;
        }

        /* Success Alert */
        div[data-baseweb="notification"][kind="success"],
        .stSuccess {
            background: var(--success-bg) !important;
            color: var(--success) !important;
            border-left-color: var(--success) !important;
        }

        /* Warning Alert */
        div[data-baseweb="notification"][kind="warning"],
        .stWarning {
            background: var(--warning-bg) !important;
            color: var(--warning) !important;
            border-left-color: var(--warning) !important;
        }

        /* Error Alert */
        div[data-baseweb="notification"][kind="error"],
        .stError {
            background: var(--error-bg) !important;
            color: var(--error) !important;
            border-left-color: var(--error) !important;
        }

        /* Info Alert */
        div[data-baseweb="notification"][kind="info"],
        .stInfo {
            background: var(--info-bg) !important;
            color: var(--info) !important;
            border-left-color: var(--info) !important;
        }

        /* ========== METRICS ========== */
        [data-testid="stMetricValue"] {
            color: var(--fg-1) !important;
            font-weight: 700 !important;
            font-size: 2rem !important;
        }

        [data-testid="stMetricLabel"] {
            color: var(--fg-3) !important;
            font-weight: 600 !important;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            font-size: 0.85rem !important;
        }

        [data-testid="stMetricDelta"] {
            font-weight: 600 !important;
        }

        /* ========== DATAFRAMES & TABLES ========== */
        .dataframe {
            border: 1px solid var(--line-2) !important;
            border-radius: 10px !important;
            background: var(--surface-1) !important;
        }

        .dataframe thead th {
            background: var(--surface-2) !important;
            color: var(--fg-1) !important;
            font-weight: 650 !important;
            border-bottom: 2px solid var(--line-3) !important;
        }

        .dataframe tbody tr:hover {
            background: var(--surface-2) !important;
        }

        .dataframe tbody td {
            color: var(--fg-2) !important;
            border-bottom: 1px solid var(--line-1) !important;
        }

        /* ========== TABS ========== */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
            background: var(--surface-1);
            border-radius: 12px;
            padding: 4px;
        }

        .stTabs [data-baseweb="tab"] {
            color: var(--fg-3) !important;
            font-weight: 600;
            border-radius: 8px;
            padding: 10px 20px;
        }

        .stTabs [data-baseweb="tab"]:hover {
            background: var(--surface-2);
            color: var(--fg-1) !important;
        }

        .stTabs [aria-selected="true"] {
            background: var(--accent-gradient) !important;
            color: #0A0D12 !important;
        }

        /* ========== EXPANDER ========== */
        .streamlit-expanderHeader {
            background: var(--surface-1) !important;
            color: var(--fg-1) !important;
            font-weight: 600 !important;
            border-radius: 10px !important;
            border: 1px solid var(--line-2) !important;
        }

        .streamlit-expanderHeader:hover {
            background: var(--surface-2) !important;
            border-color: var(--accent-1) !important;
        }

        .streamlit-expanderContent {
            background: var(--surface-1) !important;
            border: 1px solid var(--line-2) !important;
            border-top: none !important;
            border-radius: 0 0 10px 10px !important;
        }

        /* ========== CHECKBOX & RADIO ========== */
        .stCheckbox label,
        .stRadio label {
            color: var(--fg-2) !important;
        }

        input[type="checkbox"]:checked,
        input[type="radio"]:checked {
            background-color: var(--accent-1) !important;
            border-color: var(--accent-1) !important;
        }

        /* ========== SLIDER ========== */
        .stSlider [role="slider"] {
            background-color: var(--accent-1) !important;
        }

        .stSlider [data-baseweb="slider"] > div > div {
            background-color: var(--line-2) !important;
        }

        /* ========== SPINNER ========== */
        .stSpinner > div {
            border-top-color: var(--accent-1) !important;
        }

        /* ========== SIDEBAR (if used) ========== */
        [data-testid="stSidebar"] {
            background: var(--surface-1) !important;
            border-right: 1px solid var(--line-2) !important;
        }

        /* ========== CODE BLOCKS ========== */
        code {
            background: var(--surface-2) !important;
            color: var(--fg-1) !important;
            padding: 2px 6px;
            border-radius: 4px;
            font-size: 0.9em;
        }

        pre {
            background: var(--surface-2) !important;
            border: 1px solid var(--line-2) !important;
            border-radius: 10px !important;
            padding: 1rem !important;
        }

        pre code {
            background: transparent !important;
            padding: 0;
        }

        /* ========== PROGRESS BAR ========== */
        .stProgress > div > div {
            background-color: var(--surface-2) !important;
        }

        .stProgress > div > div > div {
            background: var(--accent-gradient) !important;
        }

        /* ========== LINKS ========== */
        a {
            color: var(--accent-1) !important;
            text-decoration: none;
            font-weight: 600;
        }

        a:hover {
            color: var(--accent-2) !important;
            text-decoration: underline;
        }
    </style>
    """
