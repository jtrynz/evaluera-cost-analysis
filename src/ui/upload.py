"""
Premium Upload Component - Nano Banana Style
===========================================
Drag & Drop Upload Zone mit Glassmorphism
"""

import streamlit as st
from src.ui.theme import COLORS, SPACING, RADIUS, SHADOWS


def premium_upload_zone(uploaded_file_callback=None):
    """
    Premium Drag & Drop Upload Zone im nano banana Stil
    
    Args:
        uploaded_file_callback: Optional callback function when file is uploaded
    
    Returns:
        uploaded_file or None
    """
    
    # CSS für Premium Upload Zone
    st.markdown(f"""
    <style>
        .premium-upload-container {{
            background: rgba(255, 255, 255, 0.88);
            backdrop-filter: blur(24px) saturate(115%);
            -webkit-backdrop-filter: blur(24px) saturate(115%);
            border: 1px solid rgba(255, 255, 255, 0.7);
            border-radius: {RADIUS['xl']};
            padding: {SPACING['xxl']};
            box-shadow: 
                0 10px 36px rgba(42, 79, 87, 0.09),
                inset 0 1px 0 rgba(255, 255, 255, 0.5);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            margin: {SPACING['lg']} 0;
        }}
        
        .premium-upload-container:hover {{
            box-shadow: 
                0 14px 44px rgba(42, 79, 87, 0.11),
                inset 0 1px 0 rgba(255, 255, 255, 0.7);
        }}
        
        .upload-icon-container {{
            text-align: center;
            margin-bottom: {SPACING['lg']};
        }}
        
        .upload-cloud-icon {{
            font-size: 4rem;
            color: {COLORS['primary']};
            opacity: 0.6;
            transition: all 0.3s ease;
        }}
        
        .premium-upload-container:hover .upload-cloud-icon {{
            transform: scale(1.1);
            opacity: 0.8;
        }}
        
        .upload-title {{
            font-size: 1.5rem;
            font-weight: 700;
            color: {COLORS['gray_900']};
            text-align: center;
            margin-bottom: {SPACING['sm']};
        }}
        
        .upload-subtitle {{
            font-size: 0.875rem;
            color: {COLORS['gray_500']};
            text-align: center;
            margin-bottom: {SPACING['lg']};
        }}
        
        .upload-button-container {{
            text-align: center;
            margin-top: {SPACING['md']};
        }}
        
        /* Override Streamlit file uploader styling */
        .stFileUploader {{
            border: 2px dashed rgba(42, 79, 87, 0.2);
            border-radius: {RADIUS['lg']};
            padding: {SPACING['xl']};
            background: rgba(255, 255, 255, 0.5);
            transition: all 0.3s ease;
        }}
        
        .stFileUploader:hover {{
            border-color: rgba(42, 79, 87, 0.4);
            background: rgba(255, 255, 255, 0.7);
        }}
        
        .stFileUploader [data-testid="stFileUploaderDropzone"] {{
            border: none !important;
            background: transparent !important;
        }}
        
        .upload-status-message {{
            margin-top: {SPACING['md']};
            padding: {SPACING['md']};
            border-radius: {RADIUS['md']};
            background: linear-gradient(135deg, 
                rgba(42, 79, 87, 0.08) 0%, 
                rgba(93, 165, 159, 0.08) 100%);
            border-left: 4px solid {COLORS['primary']};
            font-size: 0.875rem;
            color: {COLORS['gray_700']};
        }}
    </style>
    """, unsafe_allow_html=True)
    
    # HTML Container
    st.markdown("""
    <div class="premium-upload-container">
        <div class="upload-icon-container">
            <div class="upload-cloud-icon">☁️</div>
        </div>
        <div class="upload-title">Drag & Drop Your Data Here</div>
        <div class="upload-subtitle">Supported formats: XLSX, CSV, XML | Max file size: 500MB</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Streamlit File Uploader (versteckt unter dem Design)
    uploaded_file = st.file_uploader(
        "Browse Files",
        type=["csv", "xlsx", "xml"],
        key="premium_file_upload",
        label_visibility="collapsed"
    )
    
    # Status Message
    if uploaded_file:
        st.markdown(f"""
        <div class="upload-status-message">
            ✅ <strong>File upload complete.</strong> AI analysis starting... ({uploaded_file.name})
        </div>
        """, unsafe_allow_html=True)
        
        if uploaded_file_callback:
            uploaded_file_callback(uploaded_file)
    
    return uploaded_file


def upload_status_toast(message, status="info"):
    """
    Display a premium toast-style status message
    
    Args:
        message: Message to display
        status: "success", "error", "info", "warning"
    """
    icon_map = {
        "success": "✅",
        "error": "❌",
        "info": "ℹ️",
        "warning": "⚠️"
    }
    
    color_map = {
        "success": COLORS['success'],
        "error": COLORS['error'],
        "info": COLORS['info'],
        "warning": COLORS['warning']
    }
    
    icon = icon_map.get(status, "ℹ️")
    color = color_map.get(status, COLORS['info'])
    
    st.markdown(f"""
    <div style="
        padding: {SPACING['md']};
        border-radius: {RADIUS['md']};
        background: rgba(255, 255, 255, 0.95);
        border-left: 4px solid {color};
        box-shadow: {SHADOWS['md']};
        margin: {SPACING['sm']} 0;
        font-size: 0.9rem;
    ">
        {icon} {message}
    </div>
    """, unsafe_allow_html=True)
