"""
ValidationService - Domain service for validation operations
"""

from typing import Tuple


class ValidationService:
    """Domain service for validation operations"""
    
    def validate_image(self, image_data: bytes) -> Tuple[bool, str]:
        """
        Validate image data
        
        Args:
            image_data: Raw image bytes
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        # Check file size (max 10MB)
        if len(image_data) > 10 * 1024 * 1024:
            return False, "Image size exceeds 10MB limit"
        
        # Check file signature
        if not self._is_valid_image(image_data):
            return False, "Invalid image format"
        
        return True, ""
    
    def _is_valid_image(self, image_data: bytes) -> bool:
        """Check if data is a valid image"""
        # Check common image signatures
        signatures = [
            b'\xff\xd8\xff',  # JPEG
            b'\x89PNG\r\n\x1a\n',  # PNG
            b'GIF87a',  # GIF
            b'GIF89a',  # GIF
            b'RIFF',  # WebP
        ]
        
        return any(image_data.startswith(sig) for sig in signatures)
    
    def validate_product(self, product_data: dict) -> Tuple[bool, str]:
        """
        Validate product data
        
        Args:
            product_data: Product data dictionary
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        # Check required fields
        if "product_id" not in product_data:
            return False, "Missing required field: product_id"
        
        if "site_id" not in product_data:
            return False, "Missing required field: site_id"
        
        # Validate product_id
        product_id = product_data["product_id"]
        if not isinstance(product_id, str) or len(product_id) == 0:
            return False, "Invalid product_id"
        
        # Validate site_id
        site_id = product_data["site_id"]
        if not isinstance(site_id, str) or len(site_id) == 0:
            return False, "Invalid site_id"
        
        return True, ""