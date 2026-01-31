#!/usr/bin/env python3
"""
Quick test to verify Greptile integration is working
"""

from greptile_api import GreptileAPI

# Test code with an obvious issue
test_code = """
def get_user(user_id):
    # This has a SQL injection vulnerability
    query = f"SELECT * FROM users WHERE id = {user_id}"
    return db.execute(query)
"""

print("🧪 Testing Greptile Integration...\n")

try:
    api = GreptileAPI()
    print("✅ API initialized successfully")
    
    # Test review
    result = api.query_repository(
        "bigph00t/strainwise",
        f"Review this code for security issues:\n```python\n{test_code}\n```"
    )
    
    if result['success']:
        print("✅ Review completed successfully!")
        print("\n📝 Review:")
        print("-" * 50)
        print(result['response'][:300] + "...")
        print("-" * 50)
        
        # Check if it caught the SQL injection
        if "sql" in result['response'].lower() and "injection" in result['response'].lower():
            print("\n✅ Correctly identified SQL injection vulnerability!")
        else:
            print("\n⚠️  SQL injection not explicitly mentioned")
    else:
        print(f"❌ Review failed: {result.get('error', 'Unknown')}")
        
except Exception as e:
    print(f"❌ Error: {str(e)}")
    
print("\n🎉 Test complete!")