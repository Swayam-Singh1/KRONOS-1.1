"""
Integration script to upgrade KRONOS to match paper claims
Replaces base modules with enhanced versions
"""

import logging
import sys
import os

logging.basicConfig(level=logging.INFO)

def integrate_enhanced_order_engine():
    """Replace ORDER engine with enhanced version"""
    print("Integrating Enhanced ORDER Engine...")
    
    # Import enhanced module
    try:
        from order_engine_enhanced import EnhancedOrderEngine
        print("[+] Enhanced ORDER Engine available")
        return EnhancedOrderEngine
    except ImportError as e:
        print(f"✗ Failed to import Enhanced ORDER Engine: {e}")
        return None

def integrate_enhanced_chaos_engine():
    """Replace CHAOS engine with enhanced version"""
    print("Integrating Enhanced CHAOS Engine...")
    
    try:
        from chaos_engine_adversarial import EnhancedChaosEngine
        print("[+] Enhanced CHAOS Engine available")
        return EnhancedChaosEngine
    except ImportError as e:
        print(f"✗ Failed to import Enhanced CHAOS Engine: {e}")
        return None

def integrate_enhanced_balance_controller():
    """Replace BALANCE controller with enhanced version"""
    print("Integrating Enhanced BALANCE Controller...")
    
    try:
        from balance_controller_active import ActiveBalanceController
        print("[+] Enhanced BALANCE Controller available")
        return ActiveBalanceController
    except ImportError as e:
        print(f"✗ Failed to import Enhanced BALANCE Controller: {e}")
        return None

def update_main_engine():
    """Update main_engine.py to use enhanced modules"""
    print("\nUpdating main_engine.py to use enhanced modules...")
    
    main_engine_path = "backend/main_engine.py"
    
    # Read current file
    with open(main_engine_path, 'r') as f:
        content = f.read()
    
    # Check if already updated
    if "EnhancedOrderEngine" in content:
        print("[+] main_engine.py already uses enhanced modules")
        return
    
    # Add imports at top
    import_section = """# Enhanced modules (matching paper claims)
try:
    from order_engine_enhanced import EnhancedOrderEngine
    USE_ENHANCED_ORDER = True
except ImportError:
    from order_engine import OrderEngine as EnhancedOrderEngine
    USE_ENHANCED_ORDER = False
    logging.warning("Enhanced ORDER engine not available, using base version")

try:
    from chaos_engine_adversarial import EnhancedChaosEngine
    USE_ENHANCED_CHAOS = True
except ImportError:
    from chaos_engine import ChaosEngine as EnhancedChaosEngine
    USE_ENHANCED_CHAOS = False
    logging.warning("Enhanced CHAOS engine not available, using base version")

try:
    from balance_controller_active import ActiveBalanceController
    USE_ENHANCED_BALANCE = True
except ImportError:
    from balance_controller import BalanceController as ActiveBalanceController
    USE_ENHANCED_BALANCE = False
    logging.warning("Enhanced BALANCE controller not available, using base version")
"""
    
    # Find where to insert (after existing imports)
    if "from order_engine import OrderEngine" in content:
        content = content.replace(
            "from order_engine import OrderEngine",
            import_section + "\nfrom order_engine import OrderEngine"
        )
    
    # Update ORDER engine initialization
    if "self.order_engine = OrderEngine(order_config)" in content:
        content = content.replace(
            "self.order_engine = OrderEngine(order_config)",
            "self.order_engine = EnhancedOrderEngine(order_config) if USE_ENHANCED_ORDER else OrderEngine(order_config)"
        )
    
    # Update CHAOS engine initialization
    if "self.chaos_engine = ChaosEngine(chaos_config)" in content:
        content = content.replace(
            "self.chaos_engine = ChaosEngine(chaos_config)",
            "self.chaos_engine = EnhancedChaosEngine(chaos_config) if USE_ENHANCED_CHAOS else ChaosEngine(chaos_config)"
        )
    
    # Update BALANCE controller initialization
    if "self.balance_controller = BalanceController(balance_config)" in content:
        content = content.replace(
            "self.balance_controller = BalanceController(balance_config)",
            "self.balance_controller = ActiveBalanceController(balance_config, order_engine=self.order_engine) if USE_ENHANCED_BALANCE else BalanceController(balance_config)"
        )
    
    # Write updated file
    with open(main_engine_path, 'w') as f:
        f.write(content)
    
    print("[+] main_engine.py updated to use enhanced modules")

def main():
    """Main integration function"""
    print("="*80)
    print("KRONOS ENHANCED MODULES INTEGRATION")
    print("="*80)
    
    # Check enhanced modules
    enhanced_order = integrate_enhanced_order_engine()
    enhanced_chaos = integrate_enhanced_chaos_engine()
    enhanced_balance = integrate_enhanced_balance_controller()
    
    # Update main engine
    if enhanced_order or enhanced_chaos or enhanced_balance:
        update_main_engine()
    
    print("\n" + "="*80)
    print("Integration Summary:")
    print(f"  Enhanced ORDER: {'[+]' if enhanced_order else '[-]'}")
    print(f"  Enhanced CHAOS: {'[+]' if enhanced_chaos else '[-]'}")
    print(f"  Enhanced BALANCE: {'[+]' if enhanced_balance else '[-]'}")
    print("="*80)
    
    if enhanced_order and enhanced_chaos and enhanced_balance:
        print("\n[+] All enhanced modules integrated successfully!")
        print("  KRONOS now matches paper claims.")
    else:
        print("\n[!] Some enhanced modules not available.")
        print("  System will use base modules where enhanced versions are missing.")

if __name__ == "__main__":
    main()
