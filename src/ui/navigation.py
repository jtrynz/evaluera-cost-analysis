"""
📑 EVALUERA - Navigation Sidebar
=================================
Apple-ähnliche Navigation mit Accordion-Struktur
"""

from src.ui.theme import COLORS, SPACING, RADIUS, SHADOWS


class NavigationSidebar:
    """Apple-ähnliche Navigation Sidebar mit Accordion-Struktur"""

    SECTIONS = {
        "upload": {
            "title": "Upload",
            "icon": "📤",
            "subsections": []
        },
        "artikel": {
            "title": "Artikel-Erkennung",
            "icon": "🔍",
            "subsections": []
        },
        "preis": {
            "title": "Preisübersicht",
            "icon": "💰",
            "subsections": []
        },
        "lieferanten": {
            "title": "Lieferantenanalyse",
            "icon": "🏭",
            "subsections": []
        },
        "kosten": {
            "title": "Kosten-Schätzung",
            "icon": "🚀",
            "subsections": []
        },
        "nachhaltigkeit": {
            "title": "Nachhaltigkeit & Verhandlung",
            "icon": "♻️",
            "subsections": []
        }
    }

    def __init__(self):
        """Initialize sidebar navigation state"""
        if "nav_expanded_sections" not in st.session_state:
            st.session_state.nav_expanded_sections = set()
        if "nav_active_section" not in st.session_state:
            st.session_state.nav_active_section = "upload"

    def toggle_section(self, section_id: str):
        """Toggle accordion section"""
        if section_id in st.session_state.nav_expanded_sections:
            st.session_state.nav_expanded_sections.remove(section_id)
        else:
            st.session_state.nav_expanded_sections.add(section_id)

    def set_active_section(self, section_id: str):
        """Set active section"""
        st.session_state.nav_active_section = section_id

    def render(self):
        """Render the navigation sidebar"""
        with st.sidebar:
            # Sticky Sidebar CSS
            st.markdown(f"""
            <style>
                /* Sidebar Styling */
                [data-testid="stSidebar"] {{
                    background: {COLORS['surface']};
                }}

                /* Navigation Container */
                .nav-container {{
                    padding: {SPACING['md']} 0;
                }}

                /* Navigation Item */
                .nav-item {{
                    display: flex;
                    align-items: center;
                    padding: {SPACING['sm']} {SPACING['md']};
                    margin: {SPACING['xs']} 0;
                    border-radius: {RADIUS['sm']};
                    cursor: pointer;
                    transition: all 0.2s ease;
                    opacity: 0.85;
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                    font-size: 0.95rem;
                    color: {COLORS['gray_700']};
                    border-left: 3px solid transparent;
                }}

                .nav-item:hover {{
                    opacity: 1;
                    background: {COLORS['gray_100']};
                }}

                .nav-item.active {{
                    background: {COLORS['light_accent']};
                    color: {COLORS['error']};
                    opacity: 1;
                    border-left-color: {COLORS['primary']};
                    font-weight: 600;
                }}

                .nav-item-icon {{
                    font-size: 1.25rem;
                    margin-right: {SPACING['sm']};
                    min-width: 24px;
                }}

                /* Sub-Item */
                .nav-subitem {{
                    display: flex;
                    align-items: center;
                    padding: {SPACING['xs']} {SPACING['md']};
                    margin: {SPACING['xs']} 0;
                    margin-left: {SPACING['lg']};
                    border-radius: {RADIUS['sm']};
                    cursor: pointer;
                    transition: all 0.2s ease;
                    opacity: 0.75;
                    font-size: 0.875rem;
                    color: {COLORS['gray_600']};
                }}

                .nav-subitem:hover {{
                    opacity: 1;
                    background: {COLORS['gray_50']};
                }}

                .nav-subitem.active {{
                    background: {COLORS['light_accent']};
                    color: {COLORS['primary']};
                    opacity: 1;
                    font-weight: 500;
                }}

                /* Divider */
                .nav-divider {{
                    height: 1px;
                    background: {COLORS['gray_200']};
                    margin: {SPACING['md']} 0;
                }}

                /* Header */
                .nav-header {{
                    padding: {SPACING['md']} {SPACING['md']} {SPACING['sm']} {SPACING['md']};
                    font-size: 0.75rem;
                    font-weight: 700;
                    text-transform: uppercase;
                    letter-spacing: 0.08em;
                    color: {COLORS['gray_500']};
                }}

                /* Badge for extended features */
                .nav-badge {{
                    display: inline-block;
                    padding: 0.125rem 0.5rem;
                    margin-left: {SPACING['xs']};
                    background: {COLORS['info']};
                    color: white;
                    border-radius: {RADIUS['full']};
                    font-size: 0.7rem;
                    font-weight: 600;
                    letter-spacing: 0.02em;
                }}
            </style>
            """, unsafe_allow_html=True)

            # Header
            st.markdown(f"""
            <div class="nav-header">Navigation</div>
            """, unsafe_allow_html=True)

            # Render navigation items
            for section_id, section in self.SECTIONS.items():
                self._render_nav_item(section_id, section)

    def _render_nav_item(self, section_id: str, section: dict):
        """Render a single navigation item"""
        is_active = st.session_state.nav_active_section == section_id
        is_expanded = section_id in st.session_state.nav_expanded_sections
        has_subsections = len(section.get("subsections", [])) > 0

        # Main item
        active_class = "active" if is_active else ""

        if st.button(
            f"{section['icon']}  {section['title']}",
            key=f"nav_{section_id}",
            use_container_width=True,
            type="primary" if is_active else "secondary"
        ):
            self.set_active_section(section_id)
            if has_subsections:
                self.toggle_section(section_id)
            st.rerun()

        # Render subsections if expanded
        if has_subsections and is_expanded:
            for subsection in section["subsections"]:
                subsection_id = subsection["id"]
                subsection_active = st.session_state.nav_active_section == subsection_id

                if st.button(
                    f"  {subsection['icon']} {subsection['title']}",
                    key=f"nav_sub_{subsection_id}",
                    use_container_width=True,
                    type="primary" if subsection_active else "secondary"
                ):
                    self.set_active_section(subsection_id)
                    st.rerun()


def create_section_anchor(section_id: str, title: str, subtitle: str = None):
    """
    Create a section anchor with Apple-like styling

    Args:
        section_id: Unique ID for the section
        title: Section title
        subtitle: Optional subtitle
    """
    subtitle_html = ""
    if subtitle:
        subtitle_html = f"""
        <p style="
            color: {COLORS['gray_600']};
            font-size: 1rem;
            margin: {SPACING['sm']} 0 0 0;
            font-weight: 400;
        ">{subtitle}</p>
        """

    st.markdown(f"""
    <div id="{section_id}" style="
        margin: {SPACING['xxl']} 0 {SPACING['xl']} 0;
        padding-top: {SPACING['lg']};
        border-top: 1px solid {COLORS['gray_200']};
    ">
        <h2 style="
            font-size: 1.75rem;
            font-weight: 700;
            color: {COLORS['error']};
            margin: 0;
            letter-spacing: -0.02em;
        ">{title}</h2>
        {subtitle_html}
    </div>
    """, unsafe_allow_html=True)


def create_scroll_behavior():
    """Add smooth scroll behavior to the page"""
    st.markdown("""
    <style>
        html {
            scroll-behavior: smooth;
        }
    </style>
    """, unsafe_allow_html=True)
