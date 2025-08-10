"""Pydantic v2 compatibility patch for SecretStr."""

import warnings
from typing import Any, Dict

# Suppress the specific warning about __modify_schema__
warnings.filterwarnings("ignore", message=".*__modify_schema__.*")

# Monkey patch for SecretStr compatibility
def patch_secret_str():
    """Apply compatibility patch for SecretStr in Pydantic v2."""
    try:
        from pydantic.types import SecretStr
        
        # If SecretStr has __modify_schema__ but not __get_pydantic_json_schema__
        if hasattr(SecretStr, '__modify_schema__') and not hasattr(SecretStr, '__get_pydantic_json_schema__'):
            def __get_pydantic_json_schema__(cls, core_schema: Dict[str, Any], handler) -> Dict[str, Any]:
                """Compatibility method for Pydantic v2."""
                json_schema = handler(core_schema)
                json_schema.update({
                    'type': 'string',
                    'writeOnly': True,
                    'format': 'password'
                })
                return json_schema
            
            # Add the new method
            SecretStr.__get_pydantic_json_schema__ = classmethod(__get_pydantic_json_schema__)
            
    except ImportError:
        # If SecretStr is not available, skip patching
        pass
    except Exception as e:
        # Log the error but don't fail
        print(f"Warning: Failed to apply SecretStr patch: {e}")

# Apply the patch when this module is imported
patch_secret_str()