"""
Test script to verify agent import and initialization.
Run this to ensure your agents can be properly imported by the FastAPI app.
"""
import sys
from pathlib import Path

# Add agents to path (same way the app does it)
project_root = Path(__file__).parent
agents_path = project_root / "agents" / "src"
sys.path.insert(0, str(agents_path))

print("=" * 60)
print("Testing Agent Integration")
print("=" * 60)

print(f"\n1. Agents path: {agents_path}")
print(f"   Exists: {agents_path.exists()}")

try:
    print("\n2. Attempting to import PharmaResearcher...")
    from pharma_researcher.crew import PharmaResearcher
    print("   ✅ Successfully imported PharmaResearcher!")
    
    print("\n3. Attempting to initialize crew...")
    crew = PharmaResearcher()
    print("   ✅ Successfully initialized crew!")
    
    print("\n4. Checking crew configuration...")
    print(f"   Agents config: {crew.agents_config}")
    print(f"   Tasks config: {crew.tasks_config}")
    
    print("\n" + "=" * 60)
    print("✅ All checks passed! Your agents are ready to use.")
    print("=" * 60)
    
except ImportError as e:
    print(f"\n   ❌ Import failed: {e}")
    print("\nTroubleshooting:")
    print("1. Check that agents/src/pharma_researcher/ exists")
    print("2. Verify crew.py is in that directory")
    print("3. Ensure all agent dependencies are installed")
    
except Exception as e:
    print(f"\n   ❌ Initialization failed: {e}")
    print("\nTroubleshooting:")
    print("1. Check agents/src/pharma_researcher/config/ exists")
    print("2. Verify agents.yaml and tasks.yaml are present")
    print("3. Check for any configuration errors")
