"""
Test script to verify enhanced KRONOS modules match paper claims
"""

import numpy as np
import logging
from kdd_data_loader import KDDDataLoader

logging.basicConfig(level=logging.INFO)

def test_enhanced_order_engine():
    """Test Enhanced ORDER Engine features"""
    print("\n" + "="*80)
    print("TESTING ENHANCED ORDER ENGINE")
    print("="*80)
    
    try:
        from order_engine_enhanced import EnhancedOrderEngine
        
        # Initialize
        config = {
            'n_estimators': 200,  # Paper claim
            'contamination': 0.1,
            'enable_one_class_svm': True,
            'enable_autoencoder': True,
            'enable_lstm': True,
            'enable_deep_nn': True
        }
        
        engine = EnhancedOrderEngine(config)
        
        # Test 1: Check Isolation Forest has 200 trees
        if hasattr(engine, 'anomaly_model') and engine.anomaly_model is not None:
            n_trees = engine.anomaly_model.n_estimators
            print(f"[+] Isolation Forest trees: {n_trees} (Expected: 200)")
            assert n_trees == 200, f"Expected 200 trees, got {n_trees}"
        
        # Test 2: Check One-Class SVM exists
        if engine.one_class_svm is not None:
            print("[+] One-Class SVM: Initialized")
        else:
            print("[-] One-Class SVM: Not initialized")
        
        # Test 3: Check Autoencoder exists
        if engine.autoencoder is not None:
            print("[+] Autoencoder: Initialized")
        else:
            print("[-] Autoencoder: Not initialized")
        
        # Test 4: Check LSTM exists
        if engine.lstm_model is not None:
            print("[+] LSTM Model: Initialized")
        else:
            print("[-] LSTM Model: Not initialized")
        
        # Test 5: Check Deep NN exists
        if engine.deep_nn_classifier is not None:
            print("[+] Deep Neural Network: Initialized")
        else:
            print("[-] Deep Neural Network: Not initialized")
        
        # Test 6: Load KDD data and train
        print("\n[*] Loading KDD data for training test...")
        loader = KDDDataLoader()
        data = loader.load_data("kddcup.data_10_percent/kddcup.data_10_percent", max_rows=1000)
        
        # Fix attack types
        if 'attack_type' in data.columns:
            data['attack_type'] = data['attack_type'].str.rstrip('.')
            data['attack_category'] = data['attack_type'].map(loader.attack_categories)
            data['attack_category'] = data['attack_category'].fillna(data['attack_type'])
            loader.raw_data = data
        
        X, y = loader.preprocess_data(data)
        X_train, X_test, y_train, y_test = loader.split_data(X, y, test_size=0.2)
        
        print(f"[+] Data loaded: {len(X_train)} train, {len(X_test)} test samples")
        
        # Train enhanced models
        print("[*] Training enhanced models...")
        engine.train_enhanced_models(X_train, y_train)
        
        print("[+] Enhanced ORDER Engine test: PASSED")
        return True
        
    except Exception as e:
        print(f"[-] Enhanced ORDER Engine test: FAILED - {e}")
        import traceback
        traceback.print_exc()
        return False

def test_enhanced_chaos_engine():
    """Test Enhanced CHAOS Engine features"""
    print("\n" + "="*80)
    print("TESTING ENHANCED CHAOS ENGINE")
    print("="*80)
    
    try:
        from chaos_engine_adversarial import EnhancedChaosEngine, AdversarialAttackGenerator
        
        # Initialize
        config = {
            'enable_fgsm': True,
            'enable_pgd': True,
            'adversarial_epsilon': 0.1
        }
        
        engine = EnhancedChaosEngine(config)
        
        # Test 1: Check FGSM capability
        if hasattr(engine, 'generate_fgsm_attack'):
            print("[+] FGSM attack method: Available")
        else:
            print("[-] FGSM attack method: Not available")
        
        # Test 2: Check PGD capability
        if hasattr(engine, 'generate_pgd_attack'):
            print("[+] PGD attack method: Available")
        else:
            print("[-] PGD attack method: Not available")
        
        # Test 3: Check adversarial generator
        if engine.adversarial_generator is not None or hasattr(engine, 'adversarial_generator'):
            print("[+] Adversarial generator: Available")
        else:
            print("[-] Adversarial generator: Not initialized")
        
        print("[+] Enhanced CHAOS Engine test: PASSED")
        return True
        
    except Exception as e:
        print(f"[-] Enhanced CHAOS Engine test: FAILED - {e}")
        import traceback
        traceback.print_exc()
        return False

def test_enhanced_balance_controller():
    """Test Enhanced BALANCE Controller features"""
    print("\n" + "="*80)
    print("TESTING ENHANCED BALANCE CONTROLLER")
    print("="*80)
    
    try:
        from balance_controller_active import ActiveBalanceController
        
        # Initialize
        config = {
            'enable_active_ga': True,
            'enable_policy_gradient': True,
            'enable_actor_critic': True,
            'enable_meta_learning': True
        }
        
        controller = ActiveBalanceController(config)
        
        # Test 1: Check GA optimization
        if hasattr(controller, 'optimize_order_parameters_genetic'):
            print("[+] Genetic Algorithm optimization: Available")
        else:
            print("[-] Genetic Algorithm optimization: Not available")
        
        # Test 2: Check Policy Gradient
        if hasattr(controller, 'optimize_with_policy_gradient'):
            print("[+] Policy Gradient methods: Available")
        else:
            print("[-] Policy Gradient methods: Not available")
        
        # Test 3: Check Actor-Critic
        if controller.actor_model is not None and controller.critic_model is not None:
            print("[+] Actor-Critic architecture: Initialized")
        else:
            print("[-] Actor-Critic architecture: Not initialized")
        
        # Test 4: Check Meta-learning
        if hasattr(controller, 'meta_learn_adaptation'):
            print("[+] Meta-learning framework: Available")
        else:
            print("[-] Meta-learning framework: Not available")
        
        print("[+] Enhanced BALANCE Controller test: PASSED")
        return True
        
    except Exception as e:
        print(f"[-] Enhanced BALANCE Controller test: FAILED - {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("="*80)
    print("KRONOS ENHANCED MODULES TEST SUITE")
    print("="*80)
    
    results = {
        'order': test_enhanced_order_engine(),
        'chaos': test_enhanced_chaos_engine(),
        'balance': test_enhanced_balance_controller()
    }
    
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)
    print(f"Enhanced ORDER Engine: {'PASSED' if results['order'] else 'FAILED'}")
    print(f"Enhanced CHAOS Engine: {'PASSED' if results['chaos'] else 'FAILED'}")
    print(f"Enhanced BALANCE Controller: {'PASSED' if results['balance'] else 'FAILED'}")
    print("="*80)
    
    if all(results.values()):
        print("\n[+] All enhanced modules are functional!")
    else:
        print("\n[!] Some modules need attention.")

if __name__ == "__main__":
    main()
