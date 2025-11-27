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
        """Render wizard progress indicators"""
        current = self.get_current_step()
        progress_pct = int((current / 6) * 100)
        
        # VisionOS Progress Bar
        st.markdown(f"""
        <div style="
            margin-bottom: {SPACING['xl']};
            padding: 0 4px;
        ">
            <div style="display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 8px;">
                <div>
                    <div style="
                        font-size: 12px; 
                        font-weight: 600; 
                        color: {COLORS['accent']}; 
                        text-transform: uppercase; 
                        letter-spacing: 0.05em;
                        margin-bottom: 4px;
                    ">
                        Schritt {current} von 6
                    </div>
                    <div style="
                        font-size: 18px; 
                        font-weight: 600; 
                        color: {COLORS['primary']};
                    ">
                        {self.STEPS[current]['title']}
                    </div>
                </div>
                <div style="
                    font-size: 14px; 
                    font-weight: 600; 
                    color: {COLORS['text_secondary']};
                ">
                    {progress_pct}%
                </div>
            </div>
            
            <div style="
                height: 6px; 
                background: rgba(0,0,0,0.05); 
                border-radius: {RADIUS['full']}; 
                overflow: hidden;
            ">
                <div style="
                    width: {progress_pct}%; 
                    height: 100%; 
                    background: linear-gradient(90deg, {COLORS['accent']}, {COLORS['primary']}); 
                    border-radius: {RADIUS['full']};
                    transition: width 0.5s cubic-bezier(0.4, 0, 0.2, 1);
                    box-shadow: 0 0 10px {COLORS['accent_glass']};
                "></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    def render_navigation(self, show_next=True, show_previous=True, next_label="Weiter", next_disabled=False):
        """Render navigation buttons"""
        current = st.session_state.wizard_current_step
        
        st.markdown(f"""
        <div style="
            display: flex; 
            justify-content: space-between; 
            align-items: center; 
            margin-top: {SPACING['xl']};
            padding-top: {SPACING['lg']};
            border-top: 1px solid {COLORS['border_medium']};
        ">
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            if show_previous and current > 1:
                if st.button("← Zurück", key=f"wizard_prev_{current}", use_container_width=False):
                    self.previous_step()
                    
        with col2:
            if show_next and current < 6:
                # Align right
                st.markdown("""<div style="text-align: right;">""", unsafe_allow_html=True)
                if st.button(next_label, key=f"wizard_next_{current}", type="primary", use_container_width=False, disabled=next_disabled):
                    self.next_step()
                st.markdown("</div>", unsafe_allow_html=True)
                
        st.markdown("</div>", unsafe_allow_html=True)

    def render_step_content(self, step_number, content_func):
        """Render content for specific step"""
        current = self.get_current_step()
        
        # Only render if active
        if step_number == current:
            # Wrap in animation container
            st.markdown('<div class="fade-in">', unsafe_allow_html=True)
            content_func()
            st.markdown('</div>', unsafe_allow_html=True)

    def render_all_steps_sidebar(self):
        """Render all steps in sidebar for overview"""
        with st.sidebar:
            st.markdown(f"""
            <div style="margin-bottom: {SPACING['lg']};">
                <h3 style="
                    color: {COLORS['primary']}; 
                    font-size: 14px; 
                    text-transform: uppercase; 
                    letter-spacing: 0.05em;
                    margin-bottom: {SPACING['md']};
                ">
                    Fortschritt
                </h3>
            </div>
            """, unsafe_allow_html=True)

            for step_num in range(1, 7):
                step_info = self.STEPS[step_num]
                is_active = (step_num == st.session_state.wizard_current_step)
                is_completed = self.is_completed(step_num)
                
                wizard_step(step_num, step_info['title'], step_info['desc'], is_active, is_completed)


def create_data_table(df, columns_config=None, max_height=400):
    """
    Create a clean, minimal data table
    """
    if columns_config is None:
        columns_config = {}

    st.dataframe(
        df,
        column_config=columns_config,
        use_container_width=True,
        height=max_height,
        hide_index=True,
    )


def create_compact_kpi_row(kpis):
    """
    Create a row of compact KPI cards
    """
    num_kpis = len(kpis)
    cols = st.columns(num_kpis)

    for i, kpi in enumerate(kpis):
        with cols[i]:
            label = kpi.get('label', '')
            value = kpi.get('value', '')
            icon = kpi.get('icon', '')
            help_text = kpi.get('help', '')
            trend = kpi.get('trend')

            trend_html = ""
            if trend == "positive":
                trend_html = f"<span style='color: {COLORS['success']}; font-size: 0.875rem; margin-left: 0.5rem;'>↓</span>" # Lower cost is good
            elif trend == "negative":
                trend_html = f"<span style='color: {COLORS['error']}; font-size: 0.875rem; margin-left: 0.5rem;'>↑</span>"

            st.markdown(f"""
            <div style="
                background: rgba(255,255,255,0.6); 
                border: 1px solid {COLORS['border_medium']}; 
                border-radius: {RADIUS['md']}; 
                padding: {SPACING['md']}; 
                box-shadow: {SHADOWS['sm']};
                transition: transform 0.2s ease;
            " onmouseover="this.style.transform='translateY(-2px)'" onmouseout="this.style.transform='translateY(0)'">
                <div style="display: flex; align-items: center;">
                    <span style="font-size: 1.5rem; margin-right: 0.75rem; opacity: 0.8;">{icon}</span>
                    <div style="flex: 1;">
                        <div style="font-size: 11px; color: {COLORS['text_secondary']}; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 2px;">{label}</div>
                        <div style="font-size: 1.25rem; font-weight: 700; color: {COLORS['primary']};">{value} {trend_html}</div>
                        {f"<div style='font-size: 11px; color: {COLORS['text_tertiary']}; margin-top: 2px;'>{help_text}</div>" if help_text else ""}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
