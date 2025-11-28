"""
KPI Cards Component - Nano Banana Style
=======================================
Right-side stacked KPI cards with glassmorphism
"""

import streamlit as st
from src.ui.theme import COLORS, SPACING, RADIUS, SHADOWS


def render_kpi_sidebar():
    """
    Render the right-side KPI cards in nano banana style
    Displays Savings Potential and AI Confidence Score
    """
    
    # CSS for KPI Sidebar
    st.markdown(f"""
    <style>
        .kpi-sidebar {{
            display: flex;
            flex-direction: column;
            gap: {SPACING['md']};
        }}
        
        .kpi-card-vertical {{
            background: rgba(255, 255, 255, 0.90);
            backdrop-filter: blur(24px) saturate(115%);
            -webkit-backdrop-filter: blur(24px) saturate(115%);
            border: 1px solid rgba(255, 255, 255, 0.7);
            border-radius: {RADIUS['lg']};
            padding: {SPACING['lg']};
            box-shadow: 
                0 8px 28px rgba(42, 79, 87, 0.09),
                inset 0 1px 0 rgba(255, 255, 255, 0.5);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }}
        
        .kpi-card-vertical:hover {{
            transform: translateY(-2px);
            box-shadow: 
                0 12px 36px rgba(42, 79, 87, 0.12),
                inset 0 1px 0 rgba(255, 255, 255, 0.7);
        }}
        
        .kpi-label {{
            font-size: 0.75rem;
            color: {COLORS['gray_500']};
            text-transform: uppercase;
            letter-spacing: 0.06em;
            font-weight: 600;
            margin-bottom: {SPACING['xs']};
        }}
        
        .kpi-value {{
            font-size: 2rem;
            font-weight: 700;
            color: {COLORS['primary']};
            letter-spacing: -0.02em;
            line-height: 1.2;
            margin-bottom: {SPACING['xs']};
        }}
        
        .kpi-value-large {{
            font-size: 2.5rem;
        }}
        
        .kpi-trend {{
            display: inline-flex;
            align-items: center;
            font-size: 0.875rem;
            color: {COLORS['success']};
            margin-left: {SPACING['xs']};
        }}
        
        .kpi-mini-chart {{
            margin-top: {SPACING['sm']};
            height: 40px;
            background: linear-gradient(to top, 
                rgba(42, 79, 87, 0.1) 0%, 
                rgba(93, 165, 159, 0.15) 50%, 
                rgba(167, 255, 229, 0.2) 100%);
            border-radius: {RADIUS['sm']};
            position: relative;
            overflow: hidden;
        }}
        
        .kpi-mini-chart::after {{
            content: '';
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            height: 70%;
            background: linear-gradient(135deg, 
                {COLORS['primary']} 0%, 
                #5DA59F 100%);
            opacity: 0.3;
            clip-path: polygon(0 100%, 20% 80%, 40% 85%, 60% 60%, 80% 50%, 100% 30%, 100% 100%);
        }}
    </style>
    """, unsafe_allow_html=True)
    
    # Savings Potential Card
    st.markdown(f"""
    <div class="kpi-card-vertical">
        <div class="kpi-label">Savings Potential</div>
        <div class="kpi-value kpi-value-large">
            $1.2M
            <span class="kpi-trend">↗</span>
        </div>
        <div class="kpi-mini-chart"></div>
    </div>
    """, unsafe_allow_html=True)
    
    # AI Confidence Score Card
    st.markdown(f"""
    <div class="kpi-card-vertical">
        <div class="kpi-label">AI Confidence Score</div>
        <div class="kpi-value">98%</div>
    </div>
    """, unsafe_allow_html=True)


def with_kpi_layout(content_func):
    """
    Wrapper to render content with KPI sidebar on the right
    
    Args:
        content_func: Function that renders the main content
    """
    # Create layout with main content (70%) and KPI sidebar (30%)
    col_main, col_kpi = st.columns([7, 3], gap="large")
    
    with col_main:
        # Render main content
        content_func()
    
    with col_kpi:
        # Render KPI sidebar
        render_kpi_sidebar()
