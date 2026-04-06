"""
Enhanced Training System with KDD Cup 99 Integration
Comprehensive training using real-world dataset for Self-Morphing AI Cybersecurity Engine
"""

import numpy as np
import pandas as pd
import logging
import time
import json
import os
from typing import Dict, List, Tuple, Optional, Any
from datetime import datetime, timedelta
from dataclasses import dataclass
import pickle
import joblib

from kdd_data_loader import KDDDataLoader, AttackCategory
from kdd_order_integration import KDDOrderIntegration
from kdd_chaos_integration import KDDChaosIntegration
from order_engine import OrderEngine
from chaos_engine import ChaosEngine
from balance_controller import BalanceController
from enhanced_training import EnhancedTrainingSystem

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - KDD_ENHANCED_TRAINING - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('kdd_enhanced_training.log'),
        logging.StreamHandler()
    ]
)

class KDDEnhancedTrainingSystem:
    """Enhanced training system with KDD Cup 99 integration"""
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or self._default_config()
        
        # Initialize components
        self.kdd_loader = KDDDataLoader()
        self.order_engine = None
        self.chaos_engine = None
        self.balance_controller = None
        
        # Integration components
        self.kdd_order_integration = None
        self.kdd_chaos_integration = None
        self.enhanced_training = None
        
        # Training results
        self.training_results = {}
        self.training_history = []
        
        logging.info("KDD Enhanced Training System initialized")
    
    def _default_config(self) -> Dict[str, Any]:
        """Default configuration for KDD enhanced training"""
        return {
            'kdd_dataset_size': 50000,
            'use_full_dataset': False,
            'train_order_engine': True,
            'train_chaos_engine': True,
            'train_balance_controller': True,
            'cross_validation_folds': 5,
            'test_size': 0.2,
            'random_state': 42,
            'save_models': True,
            'models_dir': 'models/kdd_enhanced',
            'results_dir': 'training_results/kdd_enhanced',
            'visualization': True,
            'detailed_logging': True
        }
    
    def initialize_components(self):
        """Initialize all system components"""
        try:
            logging.info("Initializing system components...")
            
            # Initialize core engines
            order_config = {
                'contamination': 0.1,
                'n_estimators': 100,
                'random_state': 42,
                'model_save_path': f"{self.config['models_dir']}/order_model.pkl"
            }
            self.order_engine = OrderEngine(order_config)
            
            chaos_config = {
                'max_concurrent_attacks': 5,
                'attack_interval': 1.0,
                'stealth_threshold': 0.7,
                'adaptation_threshold': 0.3
            }
            self.chaos_engine = ChaosEngine(chaos_config)
            
            balance_config = {
                'population_size': 50,
                'control_interval': 5.0,
                'learning_rate': 0.1,
                'save_path': f"{self.config['models_dir']}/balance_controller.pkl"
            }
            self.balance_controller = BalanceController(balance_config)
            
            # Initialize integration components
            self.kdd_order_integration = KDDOrderIntegration(self.order_engine, self.kdd_loader)
            self.kdd_chaos_integration = KDDChaosIntegration(self.chaos_engine, self.kdd_loader)
            
            # Initialize enhanced training
            self.enhanced_training = EnhancedTrainingSystem()
            
            logging.info("All components initialized successfully")
            
        except Exception as e:
            logging.error(f"Component initialization failed: {e}")
            raise
    
    def run_comprehensive_training(self) -> Dict[str, Any]:
        """Run comprehensive training with KDD data"""
        try:
            logging.info("Starting comprehensive KDD-enhanced training...")
            
            # Initialize components
            self.initialize_components()
            
            # Create directories
            os.makedirs(self.config['models_dir'], exist_ok=True)
            os.makedirs(self.config['results_dir'], exist_ok=True)
            
            training_start_time = time.time()
            training_results = {
                'training_id': f"kdd_enhanced_{int(time.time())}",
                'start_time': datetime.now().isoformat(),
                'config': self.config,
                'components_trained': [],
                'performance_metrics': {},
                'errors': []
            }
            
            # 1. Train ORDER engine with KDD data
            if self.config['train_order_engine']:
                try:
                    logging.info("Training ORDER engine with KDD data...")
                    order_results = self.kdd_order_integration.train_with_kdd_data(
                        use_full_dataset=self.config['use_full_dataset'],
                        max_samples=self.config['kdd_dataset_size']
                    )
                    training_results['components_trained'].append('order_engine')
                    training_results['performance_metrics']['order_engine'] = order_results
                    logging.info("ORDER engine training completed")
                except Exception as e:
                    error_msg = f"ORDER engine training failed: {e}"
                    logging.error(error_msg)
                    training_results['errors'].append(error_msg)
            
            # 2. Train CHAOS engine with KDD data
            if self.config['train_chaos_engine']:
                try:
                    logging.info("Training CHAOS engine with KDD data...")
                    chaos_analysis = self.kdd_chaos_integration.analyze_kdd_attacks(
                        max_samples=self.config['kdd_dataset_size']
                    )
                    training_results['components_trained'].append('chaos_engine')
                    training_results['performance_metrics']['chaos_engine'] = chaos_analysis
                    logging.info("CHAOS engine training completed")
                except Exception as e:
                    error_msg = f"CHAOS engine training failed: {e}"
                    logging.error(error_msg)
                    training_results['errors'].append(error_msg)
            
            # 3. Train BALANCE controller with KDD data
            if self.config['train_balance_controller']:
                try:
                    logging.info("Training BALANCE controller with KDD data...")
                    balance_results = self._train_balance_controller_with_kdd()
                    training_results['components_trained'].append('balance_controller')
                    training_results['performance_metrics']['balance_controller'] = balance_results
                    logging.info("BALANCE controller training completed")
                except Exception as e:
                    error_msg = f"BALANCE controller training failed: {e}"
                    logging.error(error_msg)
                    training_results['errors'].append(error_msg)
            
            # 4. Run integrated system testing
            try:
                logging.info("Running integrated system testing...")
                system_test_results = self._run_integrated_system_test()
                training_results['performance_metrics']['system_test'] = system_test_results
                logging.info("Integrated system testing completed")
            except Exception as e:
                error_msg = f"System testing failed: {e}"
                logging.error(error_msg)
                training_results['errors'].append(error_msg)
            
            # 5. Generate comprehensive report
            training_results['end_time'] = datetime.now().isoformat()
            training_results['total_training_time'] = time.time() - training_start_time
            training_results['success'] = len(training_results['errors']) == 0
            
            # Save training results
            self._save_training_results(training_results)
            
            # Store in history
            self.training_history.append(training_results)
            self.training_results = training_results
            
            logging.info(f"Comprehensive KDD-enhanced training completed in {training_results['total_training_time']:.2f} seconds")
            
            return training_results
            
        except Exception as e:
            logging.error(f"Comprehensive training failed: {e}")
            return {'error': str(e), 'success': False}
    
    def _train_balance_controller_with_kdd(self) -> Dict[str, Any]:
        """Train BALANCE controller using KDD data insights"""
        try:
            logging.info("Training BALANCE controller with KDD insights...")
            
            # Load KDD data for analysis
            data = self.kdd_loader.load_data(
                "kddcup.data_10_percent" if not self.config['use_full_dataset'] else "kddcup.data",
                max_rows=self.config['kdd_dataset_size']
            )
            
            # Analyze attack patterns for BALANCE controller
            attack_categories = data['attack_category'].value_counts()
            attack_types = data['attack_type'].value_counts()
            
            # Generate training scenarios based on KDD patterns
            training_scenarios = self._generate_balance_training_scenarios(data)
            
            # Train BALANCE controller with scenarios
            balance_results = {
                'scenarios_generated': len(training_scenarios),
                'attack_categories_analyzed': len(attack_categories),
                'attack_types_analyzed': len(attack_types),
                'training_accuracy': 0.0,
                'adaptation_events': 0,
                'optimization_iterations': 0
            }
            
            # Simulate training scenarios
            for scenario in training_scenarios:
                try:
                    # Update BALANCE controller with scenario
                    self.balance_controller.update_state(scenario['state'])
                    action = self.balance_controller.select_action()
                    reward = self.balance_controller.calculate_reward(scenario['state'], action)
                    
                    # Store experience
                    experience = {
                        'state': scenario['state'],
                        'action': action,
                        'reward': reward,
                        'timestamp': time.time()
                    }
                    
                    self.balance_controller.store_experience(experience)
                    balance_results['adaptation_events'] += 1
                    
                except Exception as e:
                    logging.warning(f"Scenario training failed: {e}")
            
            # Optimize BALANCE controller
            optimization_results = self.balance_controller.optimize()
            balance_results['optimization_iterations'] = optimization_results.get('iterations', 0)
            balance_results['training_accuracy'] = optimization_results.get('accuracy', 0.0)
            
            logging.info(f"BALANCE controller trained with {len(training_scenarios)} scenarios")
            
            return balance_results
            
        except Exception as e:
            logging.error(f"BALANCE controller KDD training failed: {e}")
            raise
    
    def _generate_balance_training_scenarios(self, data: pd.DataFrame) -> List[Dict[str, Any]]:
        """Generate training scenarios for BALANCE controller from KDD data"""
        scenarios = []
        
        try:
            # Group data by attack category
            for category in data['attack_category'].unique():
                if category == 'normal':
                    continue
                
                category_data = data[data['attack_category'] == category]
                
                # Generate scenarios for each attack category
                for _, row in category_data.sample(min(100, len(category_data))).iterrows():
                    scenario = {
                        'state': {
                            'defense_accuracy': self._calculate_defense_accuracy(row),
                            'attack_success_rate': self._calculate_attack_success_rate(row),
                            'system_balance': self._calculate_system_balance(row),
                            'total_interactions': 1,
                            'defense_mutations': 0,
                            'attack_adaptations': 0,
                            'overall_performance': 0.5,
                            'timestamp': time.time()
                        },
                        'attack_type': row['attack_type'],
                        'attack_category': category,
                        'intensity': self._calculate_attack_intensity(row)
                    }
                    scenarios.append(scenario)
            
            logging.info(f"Generated {len(scenarios)} training scenarios from KDD data")
            return scenarios
            
        except Exception as e:
            logging.error(f"Scenario generation failed: {e}")
            return []
    
    def _calculate_defense_accuracy(self, row: pd.Series) -> float:
        """Calculate defense accuracy based on KDD row"""
        # Base accuracy on attack characteristics
        accuracy = 0.5
        
        # Higher accuracy for attacks with more failed logins (easier to detect)
        if row['num_failed_logins'] > 5:
            accuracy += 0.2
        elif row['num_failed_logins'] > 2:
            accuracy += 0.1
        
        # Higher accuracy for attacks with root shell attempts
        if row['root_shell'] > 0:
            accuracy += 0.1
        
        # Higher accuracy for attacks with su attempts
        if row['su_attempted'] > 0:
            accuracy += 0.1
        
        return min(1.0, max(0.0, accuracy))
    
    def _calculate_attack_success_rate(self, row: pd.Series) -> float:
        """Calculate attack success rate based on KDD row"""
        # Base success rate
        success_rate = 0.3
        
        # Higher success for attacks with root access
        if row['root_shell'] > 0:
            success_rate += 0.4
        elif row['su_attempted'] > 0:
            success_rate += 0.2
        
        # Higher success for attacks with file creations
        if row['num_file_creations'] > 0:
            success_rate += 0.1
        
        # Higher success for attacks with shell access
        if row['num_shells'] > 0:
            success_rate += 0.2
        
        return min(1.0, max(0.0, success_rate))
    
    def _calculate_system_balance(self, row: pd.Series) -> float:
        """Calculate system balance based on KDD row"""
        defense_accuracy = self._calculate_defense_accuracy(row)
        attack_success_rate = self._calculate_attack_success_rate(row)
        
        # Balance is higher when defense is better and attack success is lower
        balance = defense_accuracy * (1 - attack_success_rate)
        return balance
    
    def _calculate_attack_intensity(self, row: pd.Series) -> float:
        """Calculate attack intensity based on KDD row"""
        intensity = 0.5
        
        # Higher intensity for attacks with more failed logins
        intensity += min(0.3, row['num_failed_logins'] / 10)
        
        # Higher intensity for attacks with root access
        if row['root_shell'] > 0:
            intensity += 0.3
        
        # Higher intensity for attacks with su attempts
        if row['su_attempted'] > 0:
            intensity += 0.2
        
        return min(1.0, max(0.1, intensity))
    
    def _run_integrated_system_test(self) -> Dict[str, Any]:
        """Run integrated system test with KDD data"""
        try:
            logging.info("Running integrated system test...")
            
            test_results = {
                'test_id': f"integrated_test_{int(time.time())}",
                'start_time': datetime.now().isoformat(),
                'order_engine_test': {},
                'chaos_engine_test': {},
                'balance_controller_test': {},
                'system_integration_test': {}
            }
            
            # Test ORDER engine with KDD flows
            try:
                order_test = self.kdd_order_integration.test_order_engine_with_kdd(1000)
                test_results['order_engine_test'] = order_test
            except Exception as e:
                test_results['order_engine_test'] = {'error': str(e)}
            
            # Test CHAOS engine with KDD attacks
            try:
                chaos_test = self.kdd_chaos_integration.simulate_kdd_attacks(100)
                test_results['chaos_engine_test'] = chaos_test
            except Exception as e:
                test_results['chaos_engine_test'] = {'error': str(e)}
            
            # Test BALANCE controller
            try:
                balance_status = self.balance_controller.get_status()
                test_results['balance_controller_test'] = balance_status
            except Exception as e:
                test_results['balance_controller_test'] = {'error': str(e)}
            
            # Test system integration
            try:
                integration_test = self._test_system_integration()
                test_results['system_integration_test'] = integration_test
            except Exception as e:
                test_results['system_integration_test'] = {'error': str(e)}
            
            test_results['end_time'] = datetime.now().isoformat()
            test_results['success'] = all('error' not in test for test in test_results.values() if isinstance(test, dict))
            
            logging.info("Integrated system test completed")
            return test_results
            
        except Exception as e:
            logging.error(f"Integrated system test failed: {e}")
            return {'error': str(e)}
    
    def _test_system_integration(self) -> Dict[str, Any]:
        """Test integration between all components"""
        try:
            # Generate KDD-based network flows
            flows = self.kdd_order_integration.generate_kdd_network_flows(100)
            
            # Generate KDD-based attacks
            attacks = self.kdd_chaos_integration.generate_kdd_based_attacks(50)
            
            # Process flows through ORDER engine
            order_results = []
            for flow in flows:
                result = self.order_engine.process_flow(flow)
                order_results.append(result)
            
            # Process attacks through CHAOS engine
            chaos_results = []
            for attack in attacks:
                try:
                    attack_id = self.chaos_engine.launch_attack(
                        attack['attack_type'],
                        attack['target_ip'],
                        attack['target_port']
                    )
                    chaos_results.append({'attack_id': attack_id, 'success': True})
                except Exception as e:
                    chaos_results.append({'error': str(e), 'success': False})
            
            # Test BALANCE controller coordination
            balance_state = self.balance_controller.get_status()
            
            integration_results = {
                'flows_processed': len(flows),
                'attacks_processed': len(attacks),
                'order_detections': sum(1 for r in order_results if r.get('is_anomaly', False)),
                'chaos_successes': sum(1 for r in chaos_results if r.get('success', False)),
                'balance_active': balance_state.get('active', False),
                'system_coordination': True
            }
            
            return integration_results
            
        except Exception as e:
            logging.error(f"System integration test failed: {e}")
            return {'error': str(e)}
    
    def _save_training_results(self, results: Dict[str, Any]):
        """Save training results to file"""
        try:
            results_file = f"{self.config['results_dir']}/training_results_{results['training_id']}.json"
            
            with open(results_file, 'w') as f:
                json.dump(results, f, indent=2, default=str)
            
            logging.info(f"Training results saved to {results_file}")
            
        except Exception as e:
            logging.error(f"Failed to save training results: {e}")
    
    def get_training_status(self) -> Dict[str, Any]:
        """Get current training status"""
        return {
            'training_history_count': len(self.training_history),
            'last_training': self.training_history[-1] if self.training_history else None,
            'components_initialized': all([
                self.order_engine is not None,
                self.chaos_engine is not None,
                self.balance_controller is not None
            ]),
            'kdd_integration_active': all([
                self.kdd_order_integration is not None,
                self.kdd_chaos_integration is not None
            ]),
            'config': self.config
        }
    
    def load_training_results(self, training_id: str) -> Dict[str, Any]:
        """Load specific training results"""
        try:
            results_file = f"{self.config['results_dir']}/training_results_{training_id}.json"
            
            with open(results_file, 'r') as f:
                results = json.load(f)
            
            return results
            
        except Exception as e:
            logging.error(f"Failed to load training results: {e}")
            return {'error': str(e)}

def main():
    """Example usage of KDD Enhanced Training System"""
    try:
        # Initialize training system
        config = {
            'kdd_dataset_size': 10000,
            'use_full_dataset': False,
            'train_order_engine': True,
            'train_chaos_engine': True,
            'train_balance_controller': True
        }
        
        training_system = KDDEnhancedTrainingSystem(config)
        
        # Run comprehensive training
        results = training_system.run_comprehensive_training()
        
        print("Training Results:")
        print(json.dumps(results, indent=2))
        
        # Get training status
        status = training_system.get_training_status()
        print("\nTraining Status:")
        print(json.dumps(status, indent=2))
        
    except Exception as e:
        logging.error(f"KDD Enhanced Training example failed: {e}")

if __name__ == "__main__":
    main()
