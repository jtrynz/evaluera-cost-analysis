#!/usr/bin/env python3
"""
Security Module für EVALUERA
Implementiert Security Best Practices für Production Deployment
"""

import os
import re
import hashlib
import secrets
from typing import Optional, Any, Dict, List
from pathlib import Path
import mimetypes


# ==================== CONFIGURATION ====================

class SecurityConfig:
    """Security Konfiguration für Production"""

    # File Upload Limits
    MAX_FILE_SIZE_MB = 100
    MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024

    # Allowed File Extensions
    ALLOWED_EXCEL_EXTENSIONS = {'.xlsx', '.xls', '.csv'}
    ALLOWED_IMAGE_EXTENSIONS = {'.pdf', '.png', '.jpg', '.jpeg'}
    ALLOWED_3D_EXTENSIONS = {'.step', '.stp', '.stl', '.iges', '.igs'}

    # Allowed MIME types
    ALLOWED_MIME_TYPES = {
        # Excel/CSV
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',  # xlsx
        'application/vnd.ms-excel',  # xls
        'text/csv',
        'application/csv',
        # Images/PDFs
        'application/pdf',
        'image/png',
        'image/jpeg',
        'image/jpg',
        # 3D Files
        'application/octet-stream',  # STEP, STL, IGES
        'model/step',
        'model/stl',
        'model/iges',
    }

    # Rate Limiting (für zukünftiges Deployment)
    MAX_API_CALLS_PER_MINUTE = 30
    MAX_API_CALLS_PER_HOUR = 500

    # Session Security
    SESSION_COOKIE_SECURE = True  # HTTPS only
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    SESSION_MAX_AGE_SECONDS = 3600  # 1 hour

    # Input Validation
    MAX_STRING_LENGTH = 1000
    MAX_DESCRIPTION_LENGTH = 5000
    MAX_QUANTITY = 10_000_000
    MAX_PRICE = 1_000_000.0

    # Environment Variables (Required)
    REQUIRED_ENV_VARS = [
        'OPENAI_API_KEY',
    ]

    # Optional Environment Variables
    OPTIONAL_ENV_VARS = [
        'TRADING_ECONOMICS_API_KEY',
    ]


# ==================== INPUT VALIDATION ====================

class InputValidator:
    """Validiert und sanitized User Inputs"""

    @staticmethod
    def sanitize_string(value: str, max_length: int = SecurityConfig.MAX_STRING_LENGTH) -> str:
        """
        Sanitized String Input (XSS Protection)

        Args:
            value: Input string
            max_length: Maximum allowed length

        Returns:
            Sanitized string
        """
        if not isinstance(value, str):
            return ""

        # Remove null bytes
        value = value.replace('\x00', '')

        # Limit length
        value = value[:max_length]

        # Basic HTML escaping (Streamlit does this automatically, but be safe)
        value = value.replace('<', '&lt;').replace('>', '&gt;')

        return value.strip()

    @staticmethod
    def validate_number(
        value: Any,
        min_value: Optional[float] = None,
        max_value: Optional[float] = None,
        allow_negative: bool = False
    ) -> Optional[float]:
        """
        Validate numeric input

        Args:
            value: Input value
            min_value: Minimum allowed value
            max_value: Maximum allowed value
            allow_negative: Whether negative numbers are allowed

        Returns:
            Validated number or None if invalid
        """
        try:
            num = float(value)

            # Check for NaN or Inf
            if not (num == num):  # NaN check
                return None
            if num == float('inf') or num == float('-inf'):
                return None

            # Check negative
            if not allow_negative and num < 0:
                return None

            # Check bounds
            if min_value is not None and num < min_value:
                return None
            if max_value is not None and num > max_value:
                return None

            return num
        except (ValueError, TypeError):
            return None

    @staticmethod
    def validate_email(email: str) -> bool:
        """Basic email validation"""
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(email_regex, email))

    @staticmethod
    def validate_filename(filename: str) -> bool:
        """
        Validate filename (prevent path traversal)

        Args:
            filename: Filename to validate

        Returns:
            True if safe, False otherwise
        """
        # Check for path traversal attempts
        if '..' in filename or '/' in filename or '\\' in filename:
            return False

        # Check for null bytes
        if '\x00' in filename:
            return False

        # Check length
        if len(filename) > 255:
            return False

        # Check for suspicious patterns
        suspicious_patterns = ['<', '>', ':', '"', '|', '?', '*', '\n', '\r']
        if any(p in filename for p in suspicious_patterns):
            return False

        return True


# ==================== FILE UPLOAD SECURITY ====================

class FileUploadValidator:
    """Validates uploaded files"""

    @staticmethod
    def validate_file_extension(filename: str, allowed_extensions: set) -> bool:
        """
        Validate file extension

        Args:
            filename: Name of uploaded file
            allowed_extensions: Set of allowed extensions (e.g., {'.xlsx', '.csv'})

        Returns:
            True if extension is allowed
        """
        ext = Path(filename).suffix.lower()
        return ext in allowed_extensions

    @staticmethod
    def validate_file_size(file_bytes: bytes) -> bool:
        """
        Validate file size

        Args:
            file_bytes: File content as bytes

        Returns:
            True if size is within limit
        """
        return len(file_bytes) <= SecurityConfig.MAX_FILE_SIZE_BYTES

    @staticmethod
    def validate_mime_type(filename: str, file_bytes: bytes) -> bool:
        """
        Validate MIME type

        Args:
            filename: Original filename
            file_bytes: File content

        Returns:
            True if MIME type is allowed
        """
        # Guess MIME type from filename
        mime_type, _ = mimetypes.guess_type(filename)

        if mime_type in SecurityConfig.ALLOWED_MIME_TYPES:
            return True

        # For binary files (STEP, STL, etc.), check extension
        ext = Path(filename).suffix.lower()
        if ext in SecurityConfig.ALLOWED_3D_EXTENSIONS:
            return True

        return False

    @staticmethod
    def validate_upload(
        filename: str,
        file_bytes: bytes,
        allowed_extensions: set
    ) -> Dict[str, Any]:
        """
        Comprehensive file upload validation

        Args:
            filename: Original filename
            file_bytes: File content
            allowed_extensions: Allowed file extensions

        Returns:
            Dict with 'ok' (bool) and 'error' (str) if not ok
        """
        # Validate filename
        if not InputValidator.validate_filename(filename):
            return {
                'ok': False,
                'error': 'Ungültiger Dateiname. Keine Sonderzeichen oder Pfade erlaubt.'
            }

        # Validate extension
        if not FileUploadValidator.validate_file_extension(filename, allowed_extensions):
            allowed = ', '.join(allowed_extensions)
            return {
                'ok': False,
                'error': f'Ungültiger Dateityp. Erlaubt: {allowed}'
            }

        # Validate size
        if not FileUploadValidator.validate_file_size(file_bytes):
            return {
                'ok': False,
                'error': f'Datei zu groß. Maximum: {SecurityConfig.MAX_FILE_SIZE_MB} MB'
            }

        # Validate MIME type
        if not FileUploadValidator.validate_mime_type(filename, file_bytes):
            return {
                'ok': False,
                'error': 'Ungültiger Dateityp (MIME type check failed)'
            }

        return {'ok': True}


# ==================== API KEY MANAGEMENT ====================

class APIKeyManager:
    """Manages API Keys securely"""

    @staticmethod
    def get_api_key(key_name: str, required: bool = True) -> Optional[str]:
        """
        Get API key from environment

        Args:
            key_name: Name of environment variable
            required: Whether the key is required

        Returns:
            API key or None

        Raises:
            ValueError: If required key is missing
        """
        key = os.getenv(key_name)

        if required and not key:
            raise ValueError(
                f"❌ FEHLER: {key_name} nicht gefunden!\n"
                f"Bitte setzen Sie die Umgebungsvariable oder fügen Sie sie zur .env Datei hinzu."
            )

        return key

    @staticmethod
    def validate_api_key_format(key: str, key_type: str = 'openai') -> bool:
        """
        Validate API key format

        Args:
            key: API key string
            key_type: Type of key ('openai', 'trading_economics')

        Returns:
            True if format is valid
        """
        if not key:
            return False

        if key_type == 'openai':
            # OpenAI keys start with 'sk-' and have specific length
            return key.startswith('sk-') and len(key) > 20

        elif key_type == 'trading_economics':
            # Trading Economics format: clientid:secretkey
            return ':' in key and len(key) > 10

        return True

    @staticmethod
    def mask_api_key(key: str, visible_chars: int = 8) -> str:
        """
        Mask API key for logging

        Args:
            key: API key to mask
            visible_chars: Number of characters to show

        Returns:
            Masked key
        """
        if not key or len(key) < visible_chars:
            return "****"

        return f"{key[:visible_chars]}{'*' * (len(key) - visible_chars)}"


# ==================== ENVIRONMENT VALIDATION ====================

class EnvironmentValidator:
    """Validates environment configuration"""

    @staticmethod
    def validate_required_env_vars() -> Dict[str, Any]:
        """
        Validate all required environment variables

        Returns:
            Dict with 'ok' (bool), 'missing' (list), 'warnings' (list)
        """
        missing = []
        warnings = []

        # Check required
        for var in SecurityConfig.REQUIRED_ENV_VARS:
            if not os.getenv(var):
                missing.append(var)

        # Check optional (warnings only)
        for var in SecurityConfig.OPTIONAL_ENV_VARS:
            if not os.getenv(var):
                warnings.append(f"{var} (optional) nicht gesetzt")

        return {
            'ok': len(missing) == 0,
            'missing': missing,
            'warnings': warnings
        }

    @staticmethod
    def validate_production_ready() -> Dict[str, Any]:
        """
        Check if application is production-ready

        Returns:
            Dict with status and issues
        """
        issues = []

        # Check environment variables
        env_check = EnvironmentValidator.validate_required_env_vars()
        if not env_check['ok']:
            issues.append({
                'severity': 'critical',
                'issue': 'Fehlende Umgebungsvariablen',
                'details': env_check['missing']
            })

        # Check .env file security
        env_file = Path('.env')
        if env_file.exists():
            # Check file permissions (Unix only)
            if hasattr(os, 'stat'):
                stat_info = env_file.stat()
                mode = stat_info.st_mode
                # Check if world-readable (security risk)
                if mode & 0o004:
                    issues.append({
                        'severity': 'warning',
                        'issue': '.env Datei ist world-readable',
                        'details': 'Setzen Sie Berechtigungen auf 600 (nur Owner read/write)'
                    })

        # Check if running in development mode
        if os.getenv('STREAMLIT_SERVER_ENV') != 'production':
            issues.append({
                'severity': 'info',
                'issue': 'Development Mode erkannt',
                'details': 'Setzen Sie STREAMLIT_SERVER_ENV=production für Deployment'
            })

        return {
            'production_ready': len([i for i in issues if i['severity'] == 'critical']) == 0,
            'issues': issues
        }


# ==================== SECURITY UTILITIES ====================

def generate_secure_token(length: int = 32) -> str:
    """Generate cryptographically secure token"""
    return secrets.token_urlsafe(length)


def hash_data(data: str) -> str:
    """Hash data using SHA-256"""
    return hashlib.sha256(data.encode()).hexdigest()


def sanitize_error_message(error: Exception, debug_mode: bool = False) -> str:
    """
    Sanitize error messages for user display

    Args:
        error: Exception object
        debug_mode: If True, return full error

    Returns:
        Sanitized error message
    """
    if debug_mode:
        return str(error)

    # Generic error messages for production
    error_type = type(error).__name__

    safe_messages = {
        'ValueError': 'Ungültige Eingabe. Bitte überprüfen Sie Ihre Daten.',
        'FileNotFoundError': 'Datei nicht gefunden.',
        'PermissionError': 'Zugriff verweigert.',
        'ConnectionError': 'Verbindungsfehler. Bitte versuchen Sie es später erneut.',
        'TimeoutError': 'Zeitüberschreitung. Bitte versuchen Sie es erneut.',
    }

    return safe_messages.get(error_type, 'Ein Fehler ist aufgetreten. Bitte kontaktieren Sie den Support.')


# ==================== STARTUP VALIDATION ====================

def validate_security_on_startup() -> None:
    """
    Run security checks on application startup
    Should be called at the beginning of the app
    """
    print("\n" + "=" * 80)
    print("🔒 SECURITY VALIDATION")
    print("=" * 80)

    # Check environment variables
    env_check = EnvironmentValidator.validate_required_env_vars()

    if env_check['ok']:
        print("✅ Alle erforderlichen Umgebungsvariablen gesetzt")
    else:
        print("❌ FEHLER: Fehlende Umgebungsvariablen:")
        for var in env_check['missing']:
            print(f"   - {var}")
        raise EnvironmentError(
            f"Fehlende Umgebungsvariablen: {', '.join(env_check['missing'])}\n"
            "Bitte erstellen Sie eine .env Datei oder setzen Sie die Variablen."
        )

    if env_check['warnings']:
        print("\n⚠️  Warnungen:")
        for warning in env_check['warnings']:
            print(f"   - {warning}")

    # Check production readiness
    prod_check = EnvironmentValidator.validate_production_ready()

    if prod_check['production_ready']:
        print("\n✅ Anwendung ist production-ready")
    else:
        print("\n⚠️  Production-Readiness Issues:")
        for issue in prod_check['issues']:
            severity_emoji = {
                'critical': '🔴',
                'warning': '🟡',
                'info': 'ℹ️ '
            }.get(issue['severity'], '❓')
            print(f"   {severity_emoji} {issue['issue']}")
            if issue.get('details'):
                print(f"      → {issue['details']}")

    # Security limits
    print(f"\n📊 Security Limits:")
    print(f"   - Max File Size: {SecurityConfig.MAX_FILE_SIZE_MB} MB")
    print(f"   - Max API Calls/Minute: {SecurityConfig.MAX_API_CALLS_PER_MINUTE}")
    print(f"   - Max API Calls/Hour: {SecurityConfig.MAX_API_CALLS_PER_HOUR}")
    print(f"   - Session Max Age: {SecurityConfig.SESSION_MAX_AGE_SECONDS}s")

    print("=" * 80 + "\n")


# ==================== EXPORTS ====================

__all__ = [
    'SecurityConfig',
    'InputValidator',
    'FileUploadValidator',
    'APIKeyManager',
    'EnvironmentValidator',
    'generate_secure_token',
    'hash_data',
    'sanitize_error_message',
    'validate_security_on_startup',
]
