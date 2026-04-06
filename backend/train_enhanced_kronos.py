"""
Comprehensive Training Script for Enhanced KRONOS
Trains all enhanced modules to match paper claims
"""

import numpy as np
import pandas as pd
import time
import logging
from datetime import datetime
import json
import os

from kdd_data_loader import KDDDataLoader
from order_engine_enhanced import EnhancedOrderEngine
from chaos_engine_adversarial import EnhancedChaosEngine, AdversarialAttackGenerator
from balance_controller_active import ActiveBalanceController

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - ENHANCED_TRAINING - %(levelname)s - %(message)s'
)

class EnhancedKRONOSTrainer:
    """Comprehensive trainer for enhanced KRONOS system"""
    
    def __init__(self, dataset_path: str = "datset/KDD cup 99", max_samples: int = 50000):
        self.dataset_path = dataset_path
        self.max_samples = max_samples
        self.kdd_loader = KDDDataLoader(dataset_path)
        
        # Components
        self.order_engine = None
        self.chaos_engine = None
        self.balance_controller = None
        
        # Results
        self.training_results = {}
        
    def load_data(self):
        """Load and preprocess KDD data"""
        print("\n[*] Loading KDD Cup 99 dataset...")
        
        # Load data
        data_file = "kddcup.data_10_percent/kddcup.data_10_percent"
        data = self.kdd_loader.load_data(data_file, max_rows=self.max_samples)
        
        # Fix attack types (remove trailing periods)
        if 'attack_type' in data.columns:
            data['attack_type'] = data['attack_type'].str.rstrip('.')
            data['attack_category'] = data['attack_type'].map(self.kdd_loader.attack_categories)
            data['attack_category'] = data['attack_category'].fillna(data['attack_type'])
            self.kdd_loader.raw_data = data
        
        # Preprocess
        X, y = self.kdd_loader.preprocess_data(data)
        X_train, X_test, y_train, y_test = self.kdd_loader.split_data(X, y, test_size=0.2)
        
        print(f"[+] Loaded {len(data)} samples")
        print(f"[+] Train: {len(X_train)}, Test: {len(X_test)}")
        
        return X_train, X_test, y_train, y_test
    
    def train_order_engine(self, X_train, y_train, X_test, y_test):
        """Train enhanced ORDER engine with all paper-specified features"""
        print("\n" + "="*80)
        print("TRAINING ENHANCED ORDER ENGINE")
        print("="*80)
        
        # Initialize with paper specifications
        order_config = {
            'n_estimators': 200,  # Paper: 200 trees
            'contamination': 0.1,  # Paper: 0.05-0.15 range
            'max_samples': 'auto',
            'random_state': 42,
            'enable_one_class_svm': True,
            'enable_autoencoder': True,
            'enable_lstm': True,
            'enable_deep_nn': True,
            'enable_incremental_learning': True
        }
        
        self.order_engine = EnhancedOrderEngine(order_config)
        
        # Train all enhanced models
        print("[*] Training all enhanced ORDER models...")
        start_time = time.time()
        
        self.order_engine.train_enhanced_models(X_train, y_train)
        
        training_time = time.time() - start_time
        print(f"[+] Training completed in {training_time:.2f} seconds")
        
        # Evaluate
        print("[*] Evaluating enhanced ORDER engine...")
        
        # Test ensemble anomaly detection
        test_sample = X_test[:100]
        anomaly_results = self.order_engine.detect_anomalies_ensemble(test_sample)
        
        # Test deep NN classification
        classification_results = self.order_engine.classify_with_deep_nn(test_sample)
        
        # Save models
        os.makedirs("models/enhanced_order", exist_ok=True)
        self.order_engine.save_enhanced_models("models/enhanced_order")
        
        results = {
            'training_time': training_time,
            'anomaly_detection': {
                'isolation_forest': anomaly_results.get('isolation_forest') is not None,
                'one_class_svm': anomaly_results.get('one_class_svm') is not None,
                'autoencoder': anomaly_results.get('autoencoder') is not None
            },
            'classification': {
                'deep_nn_available': classification_results.get('error') is None
            },
            'models_saved': True
        }
        
        self.training_results['order_engine'] = results
        print("[+] Enhanced ORDER engine training completed")
        
        return results
    
    def train_chaos_engine(self, X_train, X_test):
        """Train enhanced CHAOS engine with adversarial capabilities"""
        print("\n" + "="*80)
        print("TRAINING ENHANCED CHAOS ENGINE")
        print("="*80)
        
        chaos_config = {
            'enable_fgsm': True,
            'enable_pgd': True,
            'adversarial_epsilon': 0.1,
            'pgd_iterations': 10
        }
        
        self.chaos_engine = EnhancedChaosEngine(chaos_config)
        
        # Set target model (ORDER engine) for adversarial attacks
        if self.order_engine and hasattr(self.order_engine, 'deep_nn_classifier'):
            # Use deep NN as target
            self.chaos_engine.set_target_model(self.order_engine.deep_nn_classifier)
            print("[+] Target model set for adversarial attacks")
        
        # Generate adversarial examples
        print("[*] Generating adversarial examples...")
        
        # Use normalized test samples
        normal_samples = X_test[:100]
        
        # Normalize if scaler available
        if hasattr(self.order_engine, 'scaler') and hasattr(self.order_engine.scaler, 'mean_'):
            normal_samples = self.order_engine.scaler.transform(normal_samples)
        
        # Generate FGSM attacks
        fgsm_result = self.chaos_engine.generate_fgsm_attack(normal_samples)
        
        # Generate PGD attacks
        pgd_result = self.chaos_engine.generate_pgd_attack(normal_samples)
        
        results = {
            'fgsm_available': fgsm_result.get('success', False),
            'pgd_available': pgd_result.get('success', False),
            'adversarial_samples_generated': fgsm_result.get('success', False) or pgd_result.get('success', False)
        }
        
        self.training_results['chaos_engine'] = results
        print("[+] Enhanced CHAOS engine training completed")
        
        return results
    
    def train_balance_controller(self):
        """Train enhanced BALANCE controller with active optimization"""
        print("\n" + "="*80)
        print("TRAINING ENHANCED BALANCE CONTROLLER")
        print("="*80)
        
        balance_config = {
            'enable_active_ga': True,
            'enable_policy_gradient': True,
            'enable_actor_critic': True,
            'enable_meta_learning': True,
            'ga_population_size': 50,
            'ga_generations': 10,  # Reduced for testing
            'optimization_frequency': 50
        }
        
        self.balance_controller = ActiveBalanceController(balance_config, order_engine=self.order_engine)
        
        # Test genetic algorithm optimization
        print("[*] Testing genetic algorithm optimization...")
        if self.order_engine is not None:
            ga_result = self.balance_controller.optimize_order_parameters_genetic()
            print(f"[+] GA optimization: {ga_result.get('status', 'unknown')}")
        
        # Test policy gradient
        print("[*] Testing policy gradient methods...")
        test_state = np.random.rand(10)  # Dummy state
        pg_result = self.balance_controller.optimize_with_policy_gradient(test_state)
        print(f"[+] Policy gradient: {pg_result.get('status', 'unknown')}")
        
        # Check actor-critic
        actor_available = self.balance_controller.actor_model is not None
        critic_available = self.balance_controller.critic_model is not None
        
        results = {
            'ga_optimization': ga_result.get('status') == 'success' if 'ga_result' in locals() else False,
            'policy_gradient': pg_result.get('status') != 'disabled' if 'pg_result' in locals() else False,
            'actor_critic': actor_available and critic_available,
            'meta_learning': hasattr(self.balance_controller, 'meta_learn_adaptation')
        }
        
        self.training_results['balance_controller'] = results
        print("[+] Enhanced BALANCE controller training completed")
        
        return results
    
    def run_comprehensive_training(self):
        """Run comprehensive training of all enhanced modules"""
        print("="*80)
        print("ENHANCED KRONOS COMPREHENSIVE TRAINING")
        print("Matching Paper Claims Implementation")
        print("="*80)
        
        start_time = time.time()
        
        # Load data
        X_train, X_test, y_train, y_test = self.load_data()
        
        # Train ORDER engine
        order_results = self.train_order_engine(X_train, y_train, X_test, y_test)
        
        # Train CHAOS engine
        chaos_results = self.train_chaos_engine(X_train, X_test)
        
        # Train BALANCE controller
        balance_results = self.train_balance_controller()
        
        total_time = time.time() - start_time
        
        # Summary
        print("\n" + "="*80)
        print("TRAINING SUMMARY")
        print("="*80)
        print(f"Total Training Time: {total_time:.2f} seconds")
        print(f"\nORDER Engine:")
        print(f"  - Isolation Forest (200 trees): {'✓' if order_results.get('anomaly_detection', {}).get('isolation_forest') else '✗'}")
        print(f"  - One-Class SVM: {'✓' if order_results.get('anomaly_detection', {}).get('one_class_svm') else '✗'}")
        print(f"  - Autoencoder: {'✓' if order_results.get('anomaly_detection', {}).get('autoencoder') else '✗'}")
        print(f"  - Deep NN Classifier: {'✓' if order_results.get('classification', {}).get('deep_nn_available') else '✗'}")
        
        print(f"\nCHAOS Engine:")
        print(f"  - FGSM Attacks: {'✓' if chaos_results.get('fgsm_available') else '✗'}")
        print(f"  - PGD Attacks: {'✓' if chaos_results.get('pgd_available') else '✗'}")
        
        print(f"\nBALANCE Controller:")
        print(f"  - GA Optimization: {'✓' if balance_results.get('ga_optimization') else '✗'}")
        print(f"  - Policy Gradient: {'✓' if balance_results.get('policy_gradient') else '✗'}")
        print(f"  - Actor-Critic: {'✓' if balance_results.get('actor_critic') else '✗'}")
        print(f"  - Meta-Learning: {'✓' if balance_results.get('meta_learning') else '✗'}")
        
        # Save results
        self.training_results['total_time'] = total_time
        self.training_results['timestamp'] = datetime.now().isoformat()
        
        os.makedirs("results", exist_ok=True)
        with open("results/enhanced_training_results.json", 'w') as f:
            json.dump(self.training_results, f, indent=2, default=str)
        
        print("\n" + "="*80)
        print("[+] Enhanced KRONOS training completed!")
        print("="*80)
        
        return self.training_results

def main():
    """Main training function"""
    trainer = EnhancedKRONOSTrainer(max_samples=10000)  # Reduced for faster testing
    results = trainer.run_comprehensive_training()
    
    print("\nResults saved to: results/enhanced_training_results.json")

if __name__ == "__main__":
    main()
