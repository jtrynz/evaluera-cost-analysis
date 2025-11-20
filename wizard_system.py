"""
🧙‍♂️ EVALUERA - 6-Step Wizard System
====================================
Clean step-by-step workflow for cost analysis
"""

import streamlit as st
from ui_theme import wizard_step, section_header, divider, COLORS, SPACING, RADIUS


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

    def next_step(self):
        """Move to next step"""
        current = st.session_state.wizard_current_step
        if current < 6:
            self.complete_step(current)
            st.session_state.wizard_current_step = current + 1
            st.rerun()

    def previous_step(self):
        """Move to previous step"""
        if st.session_state.wizard_current_step > 1:
            st.session_state.wizard_current_step -= 1
            st.rerun()

    def render_progress(self):
        """Render wizard progress indicators"""
        current = self.get_current_step()

        # Show compact progress bar at top
        st.markdown(f"""
        <div style="
            background: {COLORS['surface']};
            border-radius: {RADIUS['md']};
            padding: {SPACING['md']};
            margin-bottom: {SPACING['xl']};
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        ">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: {SPACING['md']};">
                <div>
                    <h3 style="margin: 0; color: {COLORS['gray_900']};">
                        Schritt {current} von 6
                    </h3>
                    <p style="margin: 0; color: {COLORS['gray_500']}; font-size: 0.875rem;">
                        {self.STEPS[current]['title']}
                    </p>
                </div>
                <div style="color: {COLORS['primary']}; font-weight: 600;">
                    {int((current / 6) * 100)}% abgeschlossen
                </div>
            </div>

            <!-- Progress Bar -->
            <div style="
                height: 8px;
                background: {COLORS['gray_200']};
                border-radius: {RADIUS['full']};
                overflow: hidden;
            ">
                <div style="
                    width: {(current / 6) * 100}%;
                    height: 100%;
                    background: linear-gradient(90deg, {COLORS['primary']}, {COLORS['primary_light']});
                    transition: width 0.3s ease;
                    border-radius: {RADIUS['full']};
                "></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    def render_navigation(self, show_next=True, show_previous=True, next_label="Weiter", next_disabled=False):
        """Render navigation buttons"""
        col1, col2, col3 = st.columns([1, 2, 1])

        with col1:
            if show_previous and st.session_state.wizard_current_step > 1:
                if st.button("← Zurück", use_container_width=True):
                    self.previous_step()

        with col3:
            if show_next and st.session_state.wizard_current_step < 6:
                if st.button(next_label + " →", type="primary", use_container_width=True, disabled=next_disabled):
                    self.next_step()

    def render_step_content(self, step_number, content_func):
        """Render content for specific step (collapsible)"""
        current = self.get_current_step()
        is_active = (step_number == current)
        is_completed = self.is_completed(step_number)

        step_info = self.STEPS[step_number]

        # Render step indicator (clickable)
        st.markdown(wizard_step(
            step_number,
            step_info['title'],
            step_info['desc'],
            is_active,
            is_completed
        ), unsafe_allow_html=True)

        # Only show content if active
        if is_active:
            with st.container():
                st.markdown(f"<div style='padding: {SPACING['lg']} 0;'>", unsafe_allow_html=True)
                content_func()
                st.markdown("</div>", unsafe_allow_html=True)

    def render_all_steps_sidebar(self):
        """Render all steps in sidebar for overview"""
        with st.sidebar:
            st.markdown(f"""
            <div style="margin-bottom: {SPACING['lg']};">
                <h3 style="color: {COLORS['gray_900']}; margin-bottom: {SPACING['md']};">
                    Workflow
                </h3>
            </div>
            """, unsafe_allow_html=True)

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
                    st.markdown(f"""
                    <div style="
                        padding: 0.5rem 1rem;
                        color: {COLORS['gray_400']};
                        font-size: 0.875rem;
                        margin-bottom: 0.5rem;
                    ">
                        {step_num}. {step_info['title']}
                    </div>
                    """, unsafe_allow_html=True)


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
    Create a row of compact KPI cards

    Args:
        kpis: List of dicts with keys: label, value, icon, help, trend
    """
    num_kpis = len(kpis)
    cols = st.columns(num_kpis)

    for i, kpi in enumerate(kpis):
        with cols[i]:
            from ui_theme import kpi_card
            kpi_card(
                label=kpi.get('label', ''),
                value=kpi.get('value', ''),
                icon=kpi.get('icon'),
                help_text=kpi.get('help'),
                trend=kpi.get('trend')
            )
