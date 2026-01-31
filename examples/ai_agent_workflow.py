#!/usr/bin/env python3
"""
Example: AI Agent workflow with continuous review feedback
"""

import sys
sys.path.append('..')
from greptile_api import GreptileAPI

# Simulated AI agent functions
def generate_code(description):
    """Simulate AI generating code"""
    return '''
def process_payment(card_number, amount, user_id):
    # Process payment
    charge = stripe.Charge.create(
        amount=amount * 100,
        currency='usd',
        source=card_number,
        description=f'Payment from user {user_id}'
    )
    
    # Log transaction
    log_data = f"Payment of ${amount} from card {card_number} for user {user_id}"
    logger.info(log_data)
    
    return charge.id
'''

def improve_code(code, feedback):
    """Simulate AI improving code based on feedback"""
    return '''
import stripe
import logging
from typing import Optional
import os

# Configure secure logging
logger = logging.getLogger(__name__)

def process_payment(card_token: str, amount_cents: int, user_id: str) -> Optional[str]:
    """
    Process payment securely using Stripe token
    
    Args:
        card_token: Stripe token (not raw card number)
        amount_cents: Amount in cents to avoid float precision issues
        user_id: User identifier
    
    Returns:
        Charge ID if successful, None otherwise
    """
    try:
        charge = stripe.Charge.create(
            amount=amount_cents,
            currency='usd',
            source=card_token,  # Use token, not card number
            description=f'Payment for user {user_id}',
            metadata={'user_id': user_id}
        )
        
        # Log without sensitive data
        logger.info(
            "Payment processed",
            extra={
                "user_id": user_id,
                "amount_cents": amount_cents,
                "charge_id": charge.id
            }
        )
        
        return charge.id
        
    except stripe.error.CardError as e:
        logger.warning(f"Card declined for user {user_id}: {e.user_message}")
        return None
    except Exception as e:
        logger.error(f"Payment processing error: {str(e)}")
        return None
'''

# Initialize Greptile
try:
    api = GreptileAPI()
    # Validate API key is present
    if not api.api_key:
        print("❌ Please set GREPTILE_API_KEY environment variable or create ~/secrets/greptile_api_key")
        sys.exit(1)
except Exception as e:
    print(f"❌ Failed to initialize API: {e}")
    sys.exit(1)

print("🤖 AI Agent Workflow Demo\n")
print("Step 1: Generate initial code")
print("-" * 60)

# Generate initial code
code_v1 = generate_code("payment processing function")
print(code_v1)

# Review the generated code
print("\nStep 2: Review with Greptile")
print("-" * 60)

review_result = api.query_repository(
    "bigph00t/strainwise",
    f"""Review this payment processing code:
    
```python
{code_v1}
```

Identify:
- Security issues
- Best practices violations
- Missing error handling
- Logging concerns
"""
)

if review_result['success']:
    review = review_result['response']
    print("📝 Review feedback:")
    print(review)
    
    # Check if improvements needed
    if "security" in review.lower() or "issue" in review.lower():
        print("\nStep 3: AI improves code based on feedback")
        print("-" * 60)
        
        # Improve code
        code_v2 = improve_code(code_v1, review)
        print(code_v2)
        
        # Review again
        print("\nStep 4: Review improved code")
        print("-" * 60)
        
        final_review = api.query_repository(
            "bigph00t/strainwise",
            f"""Final review of improved code:
            
```python
{code_v2}
```
            
Is this production-ready?"""
        )
        
        if final_review['success']:
            print("✅ Final review:")
            print(final_review['response'])
    else:
        print("\n✅ Code passed initial review!")
else:
    print(f"❌ Review failed: {review_result.get('error', 'Unknown error')}")