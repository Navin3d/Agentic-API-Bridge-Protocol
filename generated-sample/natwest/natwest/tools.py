import requests
import json
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field

BASE_URL = "http://localhost:8001"
SESSION = requests.Session()
SESSION.headers.update({"Accept": "application/json"})

# Pydantic Models
class ValidationError(BaseModel):
    loc: List[str] = Field(..., title="Location")
    msg: str = Field(..., title="Message")
    type: str = Field(..., title="Error Type")

class HTTPValidationError(BaseModel):
    detail: Optional[List[ValidationError]] = Field(None, title="Detail")

class PaymentInitiationRequest(BaseModel):
    """
    Request body for initiating a payment.
    Fields:
      debtor_account (str): The account number of the sender.
      creditor_account (str): The account number of the recipient.
      amount (float): Amount to send.
      currency (str): Currency code (e.g. 'INR', 'USD').
      reference (Optional[str]): Payment reference (optional).
    """
    debtor_account: str = Field(..., title="Debtor Account")
    creditor_account: str = Field(..., title="Creditor Account")
    amount: float = Field(..., title="Amount")
    currency: str = Field(..., title="Currency")
    reference: Optional[str] = Field(..., title="Reference")

class PaymentInitiationResponse(BaseModel):
    """
    Response body for payment initiation.
    Fields:
      payment_id (str): Unique identifier for the payment.
      status (str): Status of the payment (e.g. 'PENDING').
      created_at (str): ISO timestamp of creation.
    """
    payment_id: str = Field(..., title="Payment Id")
    status: str = Field(..., title="Status")
    created_at: str = Field(..., title="Created At")

class PaymentStatusResponse(BaseModel):
    """
    Response for payment status query.
    Fields:
      payment_id (str): Unique identifier for the payment.
      status (str): Current status (e.g. 'PENDING', 'COMPLETED').
      processed_at (Optional[str]): ISO timestamp when processed, or None if pending.
      amount (float): Payment amount.
      currency (str): Currency code.
      reference (Optional[str]): Payment reference (optional).
    """
    payment_id: str = Field(..., title="Payment Id")
    status: str = Field(..., title="Status")
    processed_at: Optional[str] = Field(..., title="Processed At")
    amount: float = Field(..., title="Amount")
    currency: str = Field(..., title="Currency")
    reference: Optional[str] = Field(..., title="Reference")

class PayoutRequest(BaseModel):
    """
    Request body for sending a payout.
    Fields:
      payee_name (str): Name of the payout recipient.
      payee_bank_details (str): Bank details (e.g., account or IFSC).
      amount (float): Amount to send.
      currency (str): Currency code.
      reference (Optional[str]): Payment reference (optional).
    """
    payee_name: str = Field(..., title="Payee Name")
    payee_bank_details: str = Field(..., title="Payee Bank Details")
    amount: float = Field(..., title="Amount")
    currency: str = Field(..., title="Currency")
    reference: Optional[str] = Field(..., title="Reference")

class PayoutResponse(BaseModel):
    """
    Response for payout initiation.
    Fields:
      payout_id (str): Unique identifier for this payout.
      status (e.g., 'SENT').
      sent_at (str): UTC ISO timestamp when sent.
    """
    payout_id: str = Field(..., title="Payout Id")
    status: str = Field(..., title="Status")
    sent_at: str = Field(..., title="Sent At")


# API Functions
def initiate_payment(request: PaymentInitiationRequest) -> PaymentInitiationResponse:
    """
    Initiate a single payment by providing sender, recipient, amount and currency details.

    Args:
        request (PaymentInitiationRequest): Payment initiation payload.

    Returns:
        PaymentInitiationResponse: Contains new payment ID, status, and creation time.

    Raises:
        requests.exceptions.RequestException: For network-related errors.
        ValueError: For invalid input or API-specific errors.
    """
    url = f"{BASE_URL}/payments/initiate"
    try:
        response = SESSION.post(url, json=request.model_dump(), timeout=30)
        response.raise_for_status()
        return PaymentInitiationResponse.model_validate_json(response.text)
    except requests.exceptions.RequestException as e:
        raise requests.exceptions.RequestException(f"API request failed: {e}")
    except Exception as e:
        try:
            error_data = response.json()
            if "detail" in error_data:
                validation_error = HTTPValidationError.model_validate(error_data)
                raise ValueError(f"API Validation Error: {validation_error.detail}")
        except json.JSONDecodeError:
            pass # Not a JSON error response
        except UnboundLocalError: # response might not be defined if request failed before assignment
            pass
        raise ValueError(f"Failed to initiate payment: {e}")


def get_payment_status(payment_id: str) -> PaymentStatusResponse:
    """
    Check the current status and details of a specific payment using its payment_id.

    Args:
        payment_id (str): The unique payment identifier returned at creation.

    Returns:
        PaymentStatusResponse: Contains status, processed timestamp, amount, currency and reference.

    Raises:
        requests.exceptions.RequestException: For network-related errors.
        ValueError: For invalid payment_id or API-specific errors.
    """
    if not payment_id:
        raise ValueError("payment_id cannot be empty.")
    url = f"{BASE_URL}/payments/{payment_id}/status"
    try:
        response = SESSION.get(url, timeout=30)
        response.raise_for_status()
        return PaymentStatusResponse.model_validate_json(response.text)
    except requests.exceptions.RequestException as e:
        raise requests.exceptions.RequestException(f"API request failed: {e}")
    except Exception as e:
        try:
            error_data = response.json()
            if "detail" in error_data:
                validation_error = HTTPValidationError.model_validate(error_data)
                raise ValueError(f"API Validation Error: {validation_error.detail}")
        except json.JSONDecodeError:
            pass # Not a JSON error response
        except UnboundLocalError: # response might not be defined if request failed before assignment
            pass
        raise ValueError(f"Failed to get payment status for {payment_id}: {e}")

def send_payout(request: PayoutRequest) -> PayoutResponse:
    """
    Initiate a payout to a recipient’s account.

    Args:
        request (PayoutRequest): Payout details including payee name, bank details, amount, and currency.

    Returns:
        PayoutResponse: Contains new payout ID, status, and sent timestamp.

    Raises:
        requests.exceptions.RequestException: For network-related errors.
        ValueError: For invalid input or API-specific errors.
    """
    url = f"{BASE_URL}/payouts/send"
    try:
        response = SESSION.post(url, json=request.model_dump(), timeout=30)
        response.raise_for_status()
        return PayoutResponse.model_validate_json(response.text)
    except requests.exceptions.RequestException as e:
        raise requests.exceptions.RequestException(f"API request failed: {e}")
    except Exception as e:
        try:
            error_data = response.json()
            if "detail" in error_data:
                validation_error = HTTPValidationError.model_validate(error_data)
                raise ValueError(f"API Validation Error: {validation_error.detail}")
        except json.JSONDecodeError:
            pass # Not a JSON error response
        except UnboundLocalError: # response might not be defined if request failed before assignment
            pass
        raise ValueError(f"Failed to send payout: {e}")

tool_list = [
    initiate_payment,
    get_payment_status,
    send_payout
]