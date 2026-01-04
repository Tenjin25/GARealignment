"""
Simple test of Clarify library
"""
import clarify

print("Clarify library imported successfully")
print(f"Version: {clarify.__version__ if hasattr(clarify, '__version__') else 'unknown'}")
print(f"\nAvailable classes/functions:")
print([item for item in dir(clarify) if not item.startswith('_')])

# Check what's available
if hasattr(clarify, 'Jurisdiction'):
    print("\n✓ Jurisdiction class available")
if hasattr(clarify, 'Parser'):
    print("✓ Parser class available")

print("\nTrying to create a simple jurisdiction...")
try:
    from clarify import Jurisdiction
    # Test with a known working URL
    j = Jurisdiction(url='https://results.enr.clarityelections.com/GA/115465/', level='state', timeout=5)
    print(f"✓ Jurisdiction created: {type(j)}")
except Exception as e:
    print(f"✗ Error: {e}")
