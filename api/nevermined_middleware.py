"""
Nevermined Middleware for Lead Monetization
Handles payment gatekeeping and access control using unmeshed-sdk
"""

import os
from typing import Optional, Dict, Any
from dataclasses import dataclass
from enum import Enum
from dotenv import load_dotenv
from datetime import datetime
import json

load_dotenv()


class PaymentStatus(Enum):
    """Payment status enumeration"""
    PENDING = "pending"
    PAID = "paid"
    FAILED = "failed"
    EXPIRED = "expired"


@dataclass
class PaymentResult:
    """Result of a payment operation"""
    success: bool
    payment_id: Optional[str] = None
    access_token: Optional[str] = None
    error: Optional[str] = None
    asset_id: Optional[str] = None


class NeverminedMiddleware:
    """
    Middleware for Nevermined payment integration
    Uses unmeshed-sdk for monetization
    """
    
    def __init__(self):
        """Initialize Nevermined client"""
        self.api_key = os.getenv("NVM_API_KEY") or os.getenv("NEVERMINED_API_KEY")
        self.network_url = os.getenv("NEVERMINED_NETWORK_URL", "https://nevermined.io")
        
        # Initialize Nevermined SDK if available
        try:
            import unmeshed
            # Initialize with API key
            if self.api_key:
                # Try different initialization methods based on unmeshed SDK API
                try:
                    # Method 1: Direct initialization
                    self.client = unmeshed.Unmeshed(api_key=self.api_key)
                    print("✅ Nevermined SDK initialized with API key")
                except (AttributeError, TypeError):
                    try:
                        # Method 2: Using environment variable
                        os.environ["NVM_API_KEY"] = self.api_key
                        self.client = unmeshed.Unmeshed()
                        print("✅ Nevermined SDK initialized via environment")
                    except Exception:
                        # Method 3: Mock mode if SDK API is different
                        print("⚠️  Using mock mode - unmeshed SDK API may differ")
                        self.client = None
            else:
                print("⚠️  NVM_API_KEY not found, using mock mode")
                self.client = None
        except ImportError:
            print("⚠️  unmeshed-sdk not available, using mock mode")
            self.client = None
        except Exception as e:
            print(f"⚠️  Nevermined initialization: {e}, using mock mode")
            self.client = None
        
        # In-memory storage for demo (use database in production)
        self._payments: Dict[str, Dict[str, Any]] = {}
        self._access_tokens: Dict[str, str] = {}
        self._protected_assets: Dict[str, Dict[str, Any]] = {}
    
    async def register_payment_plan(self, lead_id: str, price: float = 0.01) -> Dict[str, Any]:
        """
        Register a payment plan for a lead
        
        Args:
            lead_id: Unique identifier for the lead
            price: Price in ETH or tokens (default 0.01)
            
        Returns:
            Payment plan details
        """
        if self.client:
            try:
                # Real Nevermined integration
                # plan = await self.client.payments.create_payment_plan(
                #     asset_id=lead_id,
                #     price=price
                # )
                # return plan
                pass
            except Exception as e:
                print(f"Nevermined payment plan creation error: {e}")
        
        # Mock implementation
        plan = {
            "plan_id": f"plan_{lead_id}",
            "lead_id": lead_id,
            "price": price,
            "currency": "ETH",
            "status": "active",
            "payment_url": f"{self.network_url}/pay/{lead_id}"
        }
        
        self._payments[lead_id] = {
            "plan": plan,
            "status": PaymentStatus.PENDING.value
        }
        
        return plan
    
    async def create_protected_asset(self, lead_data: Dict[str, Any], buyability_score: float) -> Dict[str, Any]:
        """
        Create a Protected Asset package for Nevermined
        
        Args:
            lead_data: Complete lead data including processed results
            buyability_score: Buyability score from auditor (1-100)
            
        Returns:
            Protected Asset package
        """
        asset_id = lead_data.get("lead_id", f"asset_{len(self._protected_assets)}")
        
        protected_asset = {
            "asset_id": asset_id,
            "lead_id": lead_data.get("lead_id"),
            "lead_data": lead_data.get("original_lead", {}),
            "processed_result": lead_data.get("processed_result", {}),
            "buyability_score": buyability_score,
            "status": "protected",
            "created_at": lead_data.get("processed_at"),
            "metadata": {
                "source": lead_data.get("original_lead", {}).get("source"),
                "platform": lead_data.get("original_lead", {}).get("platform"),
                "protected": True
            }
        }
        
        # Store protected asset
        self._protected_assets[asset_id] = protected_asset
        
        # Register payment plan
        await self.register_payment_plan(asset_id)
        
        return protected_asset
    
    async def get_payment_url(self, lead_id: str) -> str:
        """
        Get payment URL for a lead
        
        Args:
            lead_id: Lead identifier
            
        Returns:
            Payment URL
        """
        # Register payment plan if not exists
        if lead_id not in self._payments:
            await self.register_payment_plan(lead_id)
        
        payment_info = self._payments.get(lead_id, {})
        plan = payment_info.get("plan", {})
        
        # In production, this would return a Nevermined payment URL
        return plan.get("payment_url", f"{self.network_url}/pay/{lead_id}")
    
    async def process_payment(self, 
                            lead_id: str,
                            payment_method: str = "nevermined",
                            payment_token: Optional[str] = None) -> PaymentResult:
        """
        Process payment for lead access
        
        Args:
            lead_id: Lead identifier
            payment_method: Payment method (default: nevermined)
            payment_token: Optional payment token from frontend
            
        Returns:
            PaymentResult with success status and access token
        """
        if self.client:
            try:
                # Real Nevermined payment processing
                # result = await self.client.payments.process_payment(
                #     plan_id=f"plan_{lead_id}",
                #     payment_token=payment_token
                # )
                # return PaymentResult(
                #     success=result.success,
                #     payment_id=result.payment_id,
                #     access_token=result.access_token,
                #     asset_id=result.asset_id
                # )
                pass
            except Exception as e:
                print(f"Nevermined payment processing error: {e}")
        
        # Mock payment processing
        # Simulate successful payment
        import secrets
        access_token = secrets.token_urlsafe(32)
        
        self._payments[lead_id] = {
            "status": PaymentStatus.PAID.value,
            "payment_id": f"pay_{lead_id}_{secrets.token_hex(8)}",
            "paid_at": datetime.now().isoformat()
        }
        
        self._access_tokens[access_token] = lead_id
        
        return PaymentResult(
            success=True,
            payment_id=self._payments[lead_id]["payment_id"],
            access_token=access_token,
            asset_id=lead_id
        )
    
    async def verify_payment(self, 
                            lead_id: str,
                            access_token: Optional[str] = None) -> Dict[str, Any]:
        """
        Verify if payment has been made for a lead
        
        Args:
            lead_id: Lead identifier
            access_token: Optional access token to verify
            
        Returns:
            Payment status dictionary
        """
        if access_token and access_token in self._access_tokens:
            token_lead_id = self._access_tokens[access_token]
            if token_lead_id == lead_id:
                return {
                    "is_paid": True,
                    "status": PaymentStatus.PAID.value,
                    "access_token": access_token
                }
        
        payment_info = self._payments.get(lead_id, {})
        status = payment_info.get("status", PaymentStatus.PENDING.value)
        
        return {
            "is_paid": status == PaymentStatus.PAID.value,
            "status": status,
            "access_token": None
        }
    
    async def get_protected_asset(self, asset_id: str, access_token: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        Get protected asset if payment verified
        
        Args:
            asset_id: Asset identifier
            access_token: Access token if payment made
            
        Returns:
            Protected asset data or None if not paid
        """
        # Verify payment
        payment_status = await self.verify_payment(asset_id, access_token)
        
        if not payment_status["is_paid"]:
            return None
        
        return self._protected_assets.get(asset_id)
    
    async def generate_mcp_notification(self, lead_id: str, buyability_score: float) -> Dict[str, Any]:
        """
        Generate JSON payload for MCP server notification
        
        Args:
            lead_id: Lead identifier
            buyability_score: Buyability score
            
        Returns:
            MCP notification payload
        """
        payment_url = await self.get_payment_url(lead_id)
        
        notification = {
            "notification_type": "high_value_lead_ready",
            "lead_id": lead_id,
            "buyability_score": buyability_score,
            "status": "ready_for_unlock",
            "payment_url": payment_url,
            "timestamp": datetime.now().isoformat(),
            "message": f"High-value intent lead (Score: {buyability_score}/100) is available for unlock"
        }
        
        return notification
    
    async def revoke_access(self, lead_id: str) -> bool:
        """
        Revoke access to a lead (e.g., for refunds)
        
        Args:
            lead_id: Lead identifier
            
        Returns:
            True if access was revoked
        """
        if lead_id in self._payments:
            self._payments[lead_id]["status"] = PaymentStatus.EXPIRED.value
            return True
        return False


# Create singleton instance
nevermined_middleware = NeverminedMiddleware()
