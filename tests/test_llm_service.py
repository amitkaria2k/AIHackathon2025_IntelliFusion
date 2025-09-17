from services.llm_service import llm_service

print("Testing LLM Service...")
response = llm_service.generate_response([{'role': 'user', 'content': 'Hello, test message'}])

print(f"Success: {response.get('success')}")
print(f"Has response: {'response' in response}")
print(f"Response length: {len(response.get('response', ''))}")
print(f"Sample response: {response.get('response', '')[:100]}...")

print("\n=== Full Response Structure ===")
for key, value in response.items():
    if key == 'response':
        print(f"{key}: {str(value)[:200]}...")
    else:
        print(f"{key}: {value}")
