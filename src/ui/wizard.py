"""
🧙‍♂️ EVALUERA - 6-Step Wizard System
====================================
Clean step-by-step workflow for cost analysis
"""

import streamlit as st
from src.ui.theme import wizard_step, section_header, divider, COLORS, SPACING, RADIUS


class WizardManager:
    """Manages the 6-step wizard workflow"""

    STEPS = {
        1: {"title": "Upload", "desc": "Excel/CSV Datei hochladen"},
        2: {"title": "Artikel-Erkennung", "desc": "Artikel suchen und auswählen"},
        3: {"title": "Preisübersicht", "desc": "Preis-Statistiken und Vergleiche"},
        4: {"title": "Lieferantenanalyse", "desc": "Lieferanten auswählen und analysieren"},
        5: {"title": "Kosten-Schätzung", "desc": "Material- und Fertigungskosten"},
        6: {"title": "Nachhaltigkeit & Verhandlung", "desc": "CBAM, CO₂ und Verhandlungstipps"},
    }

    def __init__(self):
        # Initialize session state
        if "wizard_current_step" not in st.session_state:
            st.session_state.wizard_current_step = 1

        if "wizard_completed_steps" not in st.session_state:
            st.session_state.wizard_completed_steps = set()

    def get_current_step(self):
        """Get current step number"""
        return st.session_state.wizard_current_step

    def set_step(self, step_number):
        """Set current step"""
        if 1 <= step_number <= 6:
            st.session_state.wizard_current_step = step_number

    def complete_step(self, step_number):
        """Mark step as completed"""
        st.session_state.wizard_completed_steps.add(step_number)

    def is_completed(self, step_number):
        """Check if step is completed"""
        return step_number in st.session_state.wizard_completed_steps

    def sync_navigation_to_step(self, target_step):
        """Sync navigation sidebar active section with wizard step"""
        # Mapping: wizard step -> navigation section
        step_to_nav = {
            1: "upload",
            2: "artikel",
            3: "preise",
            4: "lieferanten",
            5: "kosten",
            6: "nachhaltigkeit"
        }

        if target_step in step_to_nav:
            st.session_state.nav_active_section = step_to_nav[target_step]

    def next_step(self):
        """Move to next step"""
        current = st.session_state.wizard_current_step
        if current < 6:
            self.complete_step(current)
            st.session_state.wizard_current_step = current + 1
            self.sync_navigation_to_step(current + 1)
            st.rerun()

    def previous_step(self):
        """Move to previous step"""
        if st.session_state.wizard_current_step > 1:
            st.session_state.wizard_current_step -= 1
            self.sync_navigation_to_step(st.session_state.wizard_current_step)
            st.rerun()



    def render_progress(self):
        """Render hybrid progress indicator - Circular + Horizontal Steps (Nano Banana Style)"""
        current = self.get_current_step()
        progress_pct = int((current / 6) * 100)
        
        # Step labels for horizontal progress
        step_labels = [
            "1. Upload Data",
            "2. AI Processing", 
            "3. Cost Modeling",
            "4. Supplier Matching",
            "5. Savings Forecast",
            "6. Final Report"
        ]

        # Hybrid Progress Bar: Circular (left) + Horizontal Steps (right)
        st.markdown(f"""
        <style>
            /* Container for hybrid progress */
            .hybrid-progress-container {{
                background: rgba(255, 255, 255, 0.90);
                backdrop-filter: blur(24px) saturate(115%);
                -webkit-backdrop-filter: blur(24px) saturate(115%);
                border: 1px solid rgba(255, 255, 255, 0.7);
                border-radius: {RADIUS['xl']};
                padding: {SPACING['lg']};
                margin-bottom: {SPACING['xl']};
                box-shadow: 
                    0 10px 36px rgba(42, 79, 87, 0.09),
                    inset 0 1px 0 rgba(255, 255, 255, 0.5);
                display: flex;
                align-items: center;
                gap: {SPACING['xl']};
            }}

            /* Circular Progress (Left) */
            .circular-progress {{
                flex-shrink: 0;
                width: 120px;
                height: 120px;
                position: relative;
                display: flex;
                align-items: center;
                justify-content: center;
            }}

            .circular-progress svg {{
                transform: rotate(-90deg);
            }}

            .circular-progress-text {{
                position: absolute;
                text-align: center;
            }}

            .circular-progress-percentage {{
                font-size: 1.75rem;
                font-weight: 700;
                color: {COLORS['primary']};
                line-height: 1;
            }}

            .circular-progress-label {{
                font-size: 0.625rem;
                color: {COLORS['gray_600']};
                font-weight: 600;
                text-transform: uppercase;
                letter-spacing: 0.05em;
                margin-top: 0.25rem;
            }}

            /* Horizontal Steps (Right) */
            .horizontal-steps {{
                flex: 1;
                display: flex;
                flex-direction: column;
                gap: {SPACING['sm']};
            }}

            .steps-title {{
                font-size: 0.75rem;
                color: {COLORS['gray_500']};
                font-weight: 600;
                text-transform: uppercase;
                letter-spacing: 0.06em;
                margin-bottom: {SPACING['xs']};
            }}

            .steps-row {{
                display: flex;
                align-items: center;
                gap: {SPACING['xs']};
            }}

            .step-bubble {{
                flex: 1;
                display: flex;
                flex-direction: column;
                align-items: center;
                gap: {SPACING['xs']};
                position: relative;
            }}

            .step-circle {{
                width: 32px;
                height: 32px;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 0.75rem;
                font-weight: 700;
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                z-index: 2;
            }}

            .step-circle.completed {{
                background: linear-gradient(135deg, {COLORS['success']} 0%, #059669 100%);
                color: white;
                box-shadow: 0 2px 8px rgba(16, 185, 129, 0.3);
            }}

            .step-circle.active {{
                background: linear-gradient(135deg, {COLORS['primary']} 0%, #5DA59F 100%);
                color: white;
                box-shadow: 
                    0 0 0 4px rgba(42, 79, 87, 0.1),
                    0 4px 12px rgba(42, 79, 87, 0.3);
                animation: pulse-glow 2s ease-in-out infinite;
            }}

            .step-circle.pending {{
                background: rgba(229, 231, 235, 0.8);
                color: {COLORS['gray_400']};
                border: 2px solid rgba(209, 213, 219, 0.6);
            }}

            .step-label {{
                font-size: 0.625rem;
                color: {COLORS['gray_600']};
                text-align: center;
                line-height: 1.2;
                max-width: 80px;
            }}

            .step-label.active {{
                color: {COLORS['primary']};
                font-weight: 600;
            }}

            .step-label.completed {{
                color: {COLORS['success']};
                font-weight: 600;
            }}

            /* Connector Line */
            .step-connector {{
                flex: 1;
                height: 3px;
                background: rgba(229, 231, 235, 0.6);
                border-radius: {RADIUS['full']};
                margin: 0 -4px;
                position: relative;
                overflow: hidden;
            }}

            .step-connector.completed {{
                background: linear-gradient(90deg, 
                    {COLORS['success']} 0%, 
                    #10B981 100%);
            }}

            .step-connector.active {{
                background: linear-gradient(90deg, 
                    {COLORS['primary']} 0%, 
                    rgba(42, 79, 87, 0.3) 100%);
            }}

            @keyframes pulse-glow {{
                0%, 100% {{ box-shadow: 0 0 0 4px rgba(42, 79, 87, 0.1), 0 4px 12px rgba(42, 79, 87, 0.3); }}
                50% {{ box-shadow: 0 0 0 8px rgba(42, 79, 87, 0.15), 0 6px 18px rgba(42, 79, 87, 0.4); }}
            }}
        </style>

        <div class="hybrid-progress-container">
            <!-- Circular Progress -->
            <div class="circular-progress">
                <svg width="120" height="120">
                    <!-- Background circle -->
                    <circle cx="60" cy="60" r="54" fill="none" stroke="rgba(229, 231, 235, 0.6)" stroke-width="8"/>
                    <!-- Progress circle -->
                    <circle 
                        cx="60" cy="60" r="54" 
                        fill="none" 
                        stroke="url(#progressGradient)" 
                        stroke-width="8" 
                        stroke-linecap="round"
                        stroke-dasharray="{339.29 * progress_pct / 100} 339.29"
                        style="transition: stroke-dasharray 0.6s cubic-bezier(0.4, 0, 0.2, 1);"
                    />
                    <defs>
                        <linearGradient id="progressGradient" x1="0%" y1="0%" x2="100%" y2="0%">
                            <stop offset="0%" style="stop-color:{COLORS['primary']};stop-opacity:1" />
                            <stop offset="100%" style="stop-color:#A7FFE5;stop-opacity:1" />
                        </linearGradient>
                    </defs>
                </svg>
                <div class="circular-progress-text">
                    <div class="circular-progress-percentage">{progress_pct}%</div>
                    <div class="circular-progress-label">Step {current}: Data Upload</div>
                </div>
            </div>

            <!-- Horizontal Steps -->
            <div class="horizontal-steps">
                <div class="steps-title">Step 1 Progress Bar</div>
                <div class="steps-row">
        """, unsafe_allow_html=True)
        
        # Render step bubbles dynamically
        for i in range(1, 7):
            is_completed = i < current
            is_active = i == current
            is_pending = i > current
            
            # State classes
            circle_class = "completed" if is_completed else ("active" if is_active else "pending")
            label_class = "completed" if is_completed else ("active" if is_active else "")
            
            # Icon/Number
            icon = "✓" if is_completed else str(i)
            
            st.markdown(f"""
                <div class="step-bubble">
                    <div class="step-circle {circle_class}">{icon}</div>
                    <div class="step-label {label_class}">{step_labels[i-1]}</div>
                </div>
            """, unsafe_allow_html=True)
            
            # Connector (except after last step)
            if i < 6:
                connector_class = "completed" if i < current else ("active" if i == current else "")
                st.markdown(f'<div class="step-connector {connector_class}"></div>', unsafe_allow_html=True)
        
        st.markdown("""
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)



    def render_navigation(self, show_next=True, show_previous=True, next_label="Weiter", next_disabled=False):
        """Render navigation buttons with ABSOLUTE FIXED positioning - ULTRA ROBUST VERSION"""
        current = st.session_state.wizard_current_step

        # INJECT CSS - runs every time to ensure persistence
        st.markdown(f"""
        <style>
            /* ========== FORCE FIXED POSITIONING - MULTI-LEVEL TARGETING ========== */

            /* Target the wrapping container generated by Streamlit */
            .wizard-nav-wrapper-{current} {{
                position: fixed !important;
                right: 2.4rem !important;
                bottom: 2.2rem !important;
                z-index: 999999 !important;
                display: flex !important;
                gap: 0.75rem !important;
                align-items: center !important;
                width: auto !important;
                height: auto !important;
                margin: 0 !important;
                padding: 0 !important;
            }}

            /* Mobile responsive */
            @media (max-width: 900px) {{
                .wizard-nav-wrapper-{current} {{
                    left: 50% !important;
                    right: auto !important;
                    transform: translateX(-50%) !important;
                    bottom: 1.5rem !important;
                    flex-direction: row !important;
                }}
            }}

            /* ========== APPLE-LIKE PRIMARY BUTTON ========== */
            .wizard-nav-wrapper-{current} .stButton > button[kind="primary"] {{
                background: linear-gradient(135deg, #2F4A56 0%, #1e3640 100%) !important;
                backdrop-filter: blur(14px) saturate(180%) !important;
                -webkit-backdrop-filter: blur(14px) saturate(180%) !important;
                color: #FFFFFF !important;
                border: none !important;
                border-radius: 14px !important;
                padding: 16px 32px !important;
                font-size: 16px !important;
                font-weight: 600 !important;
                letter-spacing: 0.02em !important;
                box-shadow:
                    0 10px 30px rgba(47, 74, 86, 0.42),
                    0 0 0 1px rgba(255, 255, 255, 0.14) inset,
                    0 2px 10px rgba(0, 0, 0, 0.2) !important;
                transition: all 0.28s cubic-bezier(0.4, 0, 0.2, 1) !important;
                white-space: nowrap !important;
                min-width: 140px !important;
            }}

            .wizard-nav-wrapper-{current} .stButton > button[kind="primary"]:hover:not(:disabled) {{
                transform: translateY(-4px) scale(1.05) !important;
                box-shadow:
                    0 18px 45px rgba(47, 74, 86, 0.52),
                    0 0 0 1px rgba(255, 255, 255, 0.24) inset,
                    0 4px 18px rgba(0, 0, 0, 0.26) !important;
            }}

            .wizard-nav-wrapper-{current} .stButton > button[kind="primary"]:active:not(:disabled) {{
                transform: translateY(-1px) scale(1.02) !important;
                box-shadow:
                    0 6px 20px rgba(47, 74, 86, 0.38),
                    0 0 0 1px rgba(255, 255, 255, 0.1) inset,
                    0 1px 6px rgba(0, 0, 0, 0.16) !important;
            }}

            .wizard-nav-wrapper-{current} .stButton > button[kind="primary"]:disabled {{
                opacity: 0.45 !important;
                cursor: not-allowed !important;
                transform: none !important;
            }}

            /* ========== SECONDARY BUTTON (Zurück) ========== */
            .wizard-nav-wrapper-{current} .stButton > button:not([kind="primary"]) {{
                background: rgba(255, 255, 255, 0.92) !important;
                backdrop-filter: blur(12px) !important;
                border: 1.8px solid rgba(47, 74, 86, 0.28) !important;
                border-radius: 14px !important;
                padding: 16px 28px !important;
                font-weight: 600 !important;
                color: #2F4A56 !important;
                box-shadow: 0 6px 16px rgba(0, 0, 0, 0.11) !important;
                transition: all 0.26s ease !important;
                white-space: nowrap !important;
                min-width: 120px !important;
            }}

            .wizard-nav-wrapper-{current} .stButton > button:not([kind="primary"]):hover {{
                background: rgba(255, 255, 255, 1) !important;
                border-color: #2F4A56 !important;
                transform: translateY(-3px) scale(1.04) !important;
                box-shadow: 0 10px 24px rgba(0, 0, 0, 0.15) !important;
            }}

            .wizard-nav-wrapper-{current} .stButton > button:not([kind="primary"]):active {{
                transform: translateY(-1px) scale(1.01) !important;
                box-shadow: 0 5px 14px rgba(0, 0, 0, 0.1) !important;
            }}

            /* Prevent layout shift - add bottom padding */
            [data-testid="stAppViewContainer"] {{
                padding-bottom: 130px !important;
            }}

            /* Force wrapper children to be inline */
            .wizard-nav-wrapper-{current} > div {{
                display: inline-block !important;
                margin: 0 !important;
            }}
        </style>
        """, unsafe_allow_html=True)

        # RENDER: Wrapper div with unique class
        st.markdown(f'<div class="wizard-nav-wrapper-{current}">', unsafe_allow_html=True)

        # Create button layout
        cols = st.columns([1, 1] if (show_previous and current > 1) else [1])

        # Back button
        if show_previous and current > 1:
            with cols[0]:
                if st.button("← Zurück", key=f"wizard_prev_{current}", use_container_width=True):
                    self.previous_step()

        # Next button
        target_col = cols[1] if (show_previous and current > 1) else cols[0]
        with target_col:
            if show_next and current < 6:
                if st.button(next_label + " →", key=f"wizard_next_{current}", type="primary", use_container_width=True, disabled=next_disabled):
                    self.next_step()

        st.markdown('</div>', unsafe_allow_html=True)

    def render_step_content(self, step_number, content_func):
        """Render content for specific step (collapsible)"""
        current = self.get_current_step()
        is_active = (step_number == current)
        is_completed = self.is_completed(step_number)

        step_info = self.STEPS[step_number]

        # Render step indicator (clickable)
        from src.ui.theme import COLORS, RADIUS, SPACING

        if is_completed:
            bg = COLORS['success']
            text_color = "#ffffff"
            icon = "✓"
        elif is_active:
            bg = COLORS['primary']
            text_color = "#ffffff"
            icon = str(step_number)
        else:
            bg = COLORS['gray_200']
            text_color = COLORS['gray_500']
            icon = str(step_number)

        st.markdown(f"""<div style="display: flex; align-items: center; gap: 1rem; padding: {SPACING['md']}; margin-bottom: {SPACING['sm']}; background: {COLORS['surface']}; border-radius: {RADIUS['md']}; border: 2px solid {bg if is_active else COLORS['gray_200']}; opacity: {1 if (is_active or is_completed) else 0.6};"><div style="width: 40px; height: 40px; border-radius: 50%; background: {bg}; color: {text_color} !important; display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 1rem;">{icon}</div><div style="flex: 1;"><div style="font-weight: 600; color: {COLORS['error']}; font-size: 1rem;">{step_info['title']}</div><div style="font-size: 0.875rem; color: {COLORS['gray_500']};">{step_info['desc']}</div></div></div>""", unsafe_allow_html=True)

        # Only show content if active
        if is_active:
            # Add some spacing
            st.markdown(f"<div style='margin-top: {SPACING['md']};'></div>", unsafe_allow_html=True)
            content_func()

    def render_all_steps_sidebar(self):
        """Render all steps in sidebar for overview"""
        with st.sidebar:
            st.markdown(f"""<div style="margin-bottom: {SPACING['lg']};"><h3 style="color: {COLORS['error']}; margin-bottom: {SPACING['md']};">Workflow</h3></div>""", unsafe_allow_html=True)

            for step_num in range(1, 7):
                step_info = self.STEPS[step_num]
                is_active = (step_num == st.session_state.wizard_current_step)
                is_completed = self.is_completed(step_num)

                # Make clickable
                if is_completed or is_active:
                    if st.button(
                        f"{'✓' if is_completed else step_num}. {step_info['title']}",
                        key=f"sidebar_step_{step_num}",
                        use_container_width=True,
                        type="primary" if is_active else "secondary"
                    ):
                        self.set_step(step_num)
                        st.rerun()
                else:
                    st.markdown(f"""<div style="padding: 0.5rem 1rem; color: {COLORS['gray_400']}; font-size: 0.875rem; margin-bottom: 0.5rem;">{step_num}. {step_info['title']}</div>""", unsafe_allow_html=True)


def create_data_table(df, columns_config=None, max_height=400):
    """
    Create a clean, minimal data table

    Args:
        df: pandas DataFrame
        columns_config: Dict of column configurations
        max_height: Max table height in pixels
    """
    if columns_config is None:
        columns_config = {}

    # Use Streamlit's native dataframe with custom styling
    st.dataframe(
        df,
        column_config=columns_config,
        use_container_width=True,
        height=max_height,
        hide_index=True,
    )


def create_compact_kpi_row(kpis):
    """
    Create a row of premium glassmorphism KPI cards
    
    Args:
        kpis: List of dicts with keys: label, value, icon, help, trend
    """
    from src.ui.theme import COLORS, SPACING, RADIUS, SHADOWS
    
    num_kpis = len(kpis)
    cols = st.columns(num_kpis)
    
    for i, kpi in enumerate(kpis):
        with cols[i]:
            label = kpi.get('label', '')
            value = kpi.get('value', '')
            icon = kpi.get('icon', '')
            help_text = kpi.get('help', '')
            trend = kpi.get('trend')
            
            # Icon with colored circle background
            icon_html = f"""
            <div style="
                width: 48px;
                height: 48px;
                border-radius: 50%;
                background: linear-gradient(135deg, 
                    rgba(42, 79, 87, 0.10) 0%, 
                    rgba(93, 165, 159, 0.10) 100%);
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 1.5rem;
                margin-bottom: 0.75rem;
                box-shadow: 0 2px 8px rgba(42, 79, 87, 0.08);
                transition: transform 0.28s cubic-bezier(0.4, 0, 0.2, 1);
            ">{icon}</div>
            """ if icon else ""
            
            help_html = f"<div style='font-size: 0.75rem; color: {COLORS['gray_500']}; margin-top: 0.375rem; line-height: 1.4;'>{help_text}</div>" if help_text else ""
            
            trend_html = ""
            if trend == "positive":
                trend_html = f"<span style='color: {COLORS['success']}; font-size: 1rem; margin-left: 0.5rem;'>↑</span>"
            elif trend == "negative":
                trend_html = f"<span style='color: {COLORS['error']}; font-size: 1rem; margin-left: 0.5rem;'>↓</span>"
            
            st.markdown(f"""
            <style>
                .kpi-card-{i} {{
                    background: rgba(255, 255, 255, 0.88);
                    backdrop-filter: blur(20px) saturate(110%);
                    -webkit-backdrop-filter: blur(20px) saturate(110%);
                    border: 1px solid rgba(255, 255, 255, 0.6);
                    border-radius: {RADIUS['lg']};
                    padding: {SPACING['lg']};
                    box-shadow: 
                        0 6px 24px rgba(42, 79, 87, 0.08),
                        inset 0 1px 0 rgba(255, 255, 255, 0.4);
                    transition: all 0.28s cubic-bezier(0.4, 0, 0.2, 1);
                    height: 100%;
                }}
                
                .kpi-card-{i}:hover {{
                    transform: translateY(-3px);
                    box-shadow: 
                        0 10px 32px rgba(42, 79, 87, 0.12),
                        inset 0 1px 0 rgba(255, 255, 255, 0.6);
                }}
                
                .kpi-card-{i}:hover .kpi-icon-circle {{
                    transform: scale(1.08);
                }}
            </style>
            <div class="kpi-card-{i}">
                <div class="kpi-icon-circle">{icon_html}</div>
                <div style="font-size: 0.75rem; color: {COLORS['gray_500']}; text-transform: uppercase; letter-spacing: 0.06em; margin-bottom: 0.5rem; font-weight: 600;">{label}</div>
                <div style="font-size: 1.75rem; font-weight: 700; color: {COLORS['primary']}; letter-spacing: -0.02em; line-height: 1.2;">
                    {value} {trend_html}
                </div>
                {help_html}
            </div>
            """, unsafe_allow_html=True)
