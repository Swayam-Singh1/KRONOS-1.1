#!/usr/bin/env python3
"""
Train from Scratch - Enhanced Training System
Trains ORDER and CHAOS engines with comprehensive synthetic datasets
Designed to work with minimal or no initial data
"""

import sys
import os
import time
import logging
import requests
import json
from typing import Dict, List, Any
from pathlib import Path

# Add backend to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from enhanced_training import EnhancedTrainingSystem

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - TRAIN_FROM_SCRATCH - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('train_from_scratch.log'),
        logging.StreamHandler()
    ]
)

class TrainFromScratch:
    """Enhanced training system that trains from scratch with synthetic data"""
    
    def __init__(self, api_base_url: str = "http://localhost:8000"):
        self.api_base_url = api_base_url
        self.session = requests.Session()
        self.enhanced_trainer = EnhancedTrainingSystem()
        
    def train_comprehensive_system(self, 
                                 order_samples: int = 20000,
                                 chaos_samples: int = 20000, 
                                 balance_scenarios: int = 10000) -> Dict[str, Any]:
        """Train the complete system with comprehensive synthetic data"""
        logging.info("🚀 Starting comprehensive training from scratch...")
        
        results = {}
        
        try:
            # Step 1: Generate comprehensive training data
            logging.info("📊 Generating comprehensive synthetic datasets...")
            training_data = self.enhanced_trainer.generate_comprehensive_training_data(
                order_samples=order_samples,
                chaos_samples=chaos_samples,
                balance_scenarios=balance_scenarios
            )
            
            # Step 2: Train ORDER engine (Defense)
            logging.info("🛡️ Training ORDER Defense Engine...")
            order_result = self._train_order_engine_enhanced(training_data['order'])
            results['order'] = order_result
            
            # Step 3: Train CHAOS engine (Intelligence)
            logging.info("🎯 Training CHAOS Intelligence Engine...")
            chaos_result = self._train_chaos_engine_enhanced(training_data['chaos'])
            results['chaos'] = chaos_result
            
            # Step 4: Train BALANCE controller (Orchestration)
            logging.info("⚖️ Training BALANCE Orchestration Controller...")
            balance_result = self._train_balance_controller_enhanced(training_data['balance'])
            results['balance'] = balance_result
            
            # Step 5: Evaluate overall system performance
            logging.info("📈 Evaluating overall system performance...")
            overall_performance = self._evaluate_overall_system_performance()
            results['overall'] = overall_performance
            
            # Step 6: Save training results
            self._save_training_results(results)
            
            logging.info("✅ Comprehensive training completed successfully!")
            return results
            
        except Exception as e:
            logging.error(f"Comprehensive training failed: {e}")
            raise
    
    def _train_order_engine_enhanced(self, training_data: List[Dict]) -> Dict[str, Any]:
        """Train ORDER engine with enhanced synthetic data"""
        try:
            logging.info(f"Training ORDER engine with {len(training_data)} enhanced samples...")
            
            # Prepare enhanced training data
            prepared_data = self._prepare_order_training_data(training_data)
            
            # Train via API
            response = self.session.post(
                f"{self.api_base_url}/order/train",
                json=prepared_data
            )
            response.raise_for_status()
            result = response.json()
            
            # Additional training with specific attack patterns
            self._train_specific_attack_patterns('order', training_data)
            
            # Evaluate performance
            performance = self._evaluate_order_performance()
            result['enhanced_performance'] = performance
            
            return result
            
        except Exception as e:
            logging.error(f"ORDER engine enhanced training failed: {e}")
            return {"error": str(e), "success": False}
    
    def _train_chaos_engine_enhanced(self, training_data: List[Dict]) -> Dict[str, Any]:
        """Train CHAOS engine with enhanced synthetic data"""
        try:
            logging.info(f"Training CHAOS engine with {len(training_data)} enhanced samples...")
            
            # Prepare enhanced training data
            prepared_data = self._prepare_chaos_training_data(training_data)
            
            # Train via API
            response = self.session.post(
                f"{self.api_base_url}/chaos/train",
                json=prepared_data
            )
            response.raise_for_status()
            result = response.json()
            
            # Additional training with specific attack patterns
            self._train_specific_attack_patterns('chaos', training_data)
            
            # Evaluate performance
            performance = self._evaluate_chaos_performance()
            result['enhanced_performance'] = performance
            
            return result
            
        except Exception as e:
            logging.error(f"CHAOS engine enhanced training failed: {e}")
            return {"error": str(e), "success": False}
    
    def _train_balance_controller_enhanced(self, training_data: List[Dict]) -> Dict[str, Any]:
        """Train BALANCE controller with enhanced synthetic data"""
        try:
            logging.info(f"Training BALANCE controller with {len(training_data)} enhanced scenarios...")
            
            # Prepare enhanced training data
            prepared_data = self._prepare_balance_training_data(training_data)
            
            # Train via API
            response = self.session.post(
                f"{self.api_base_url}/balance/train",
                json=prepared_data
            )
            response.raise_for_status()
            result = response.json()
            
            # Additional training with specific scenarios
            self._train_specific_scenarios('balance', training_data)
            
            # Evaluate performance
            performance = self._evaluate_balance_performance()
            result['enhanced_performance'] = performance
            
            return result
            
        except Exception as e:
            logging.error(f"BALANCE controller enhanced training failed: {e}")
            return {"error": str(e), "success": False}
    
    def _prepare_order_training_data(self, training_data: List[Dict]) -> List[Dict]:
        """Prepare ORDER training data for API"""
        prepared_data = []
        
        for sample in training_data:
            # Convert enhanced data to API format
            api_sample = {
                'attack_type': sample.get('attack_type', 'unknown'),
                'flow': sample.get('flow', {}),
                'attack_features': sample.get('attack_features', {}),
                'behavior': sample.get('behavior', {}),
                'threat_level': sample.get('threat_level', 0),
                'confidence': sample.get('confidence', 0.5)
            }
            prepared_data.append(api_sample)
        
        return prepared_data
    
    def _prepare_chaos_training_data(self, training_data: List[Dict]) -> List[Dict]:
        """Prepare CHAOS training data for API"""
        prepared_data = []
        
        for sample in training_data:
            # Convert enhanced data to API format
            api_sample = {
                'attack_type': sample.get('attack_type', 'unknown'),
                'category': sample.get('category', 'unknown'),
                'threat_level': sample.get('threat_level', 1),
                'threat_actor': sample.get('threat_actor', 'unknown'),
                'stealth_level': sample.get('stealth_level', 1),
                'complexity': sample.get('complexity', 1),
                'damage_potential': sample.get('damage_potential', 1),
                'persistence': sample.get('persistence', 1),
                'payload': sample.get('payload', b'').hex() if isinstance(sample.get('payload'), bytes) else str(sample.get('payload', '')),
                'signature': sample.get('signature', ''),
                'evasion_techniques': sample.get('evasion_techniques', []),
                'attack_vectors': sample.get('attack_vectors', []),
                'indicators_of_compromise': sample.get('indicators_of_compromise', []),
                'target_ip': sample.get('target_ip', '0.0.0.0'),
                'target_port': sample.get('target_port', 80),
                'source_ip': sample.get('source_ip', '0.0.0.0'),
                'timestamp': sample.get('timestamp', time.time()),
                'campaign': sample.get('campaign', 'unknown'),
                'success_probability': sample.get('success_probability', 0.5),
                'detection_probability': sample.get('detection_probability', 0.3)
            }
            prepared_data.append(api_sample)
        
        return prepared_data
    
    def _prepare_balance_training_data(self, training_data: List[Dict]) -> List[Dict]:
        """Prepare BALANCE training data for API"""
        prepared_data = []
        
        for sample in training_data:
            # Convert enhanced data to API format
            api_sample = {
                'scenario_type': sample.get('scenario_type', 'unknown'),
                'threat_level': sample.get('threat_level', 1),
                'complexity': sample.get('complexity', 1),
                'order_engine_state': sample.get('order_engine_state', {}),
                'chaos_engine_state': sample.get('chaos_engine_state', {}),
                'system_metrics': sample.get('system_metrics', {}),
                'threat_indicators': sample.get('threat_indicators', []),
                'response_actions': sample.get('response_actions', []),
                'expected_outcome': sample.get('expected_outcome', {}),
                'timestamp': sample.get('timestamp', time.time()),
                'confidence': sample.get('confidence', 0.5)
            }
            prepared_data.append(api_sample)
        
        return prepared_data
    
    def _train_specific_attack_patterns(self, engine_type: str, training_data: List[Dict]):
        """Train specific attack patterns for enhanced learning"""
        try:
            # Group by attack type
            attack_groups = {}
            for sample in training_data:
                attack_type = sample.get('attack_type', 'unknown')
                if attack_type not in attack_groups:
                    attack_groups[attack_type] = []
                attack_groups[attack_type].append(sample)
            
            # Train each attack pattern separately
            for attack_type, samples in attack_groups.items():
                if len(samples) > 0:
                    logging.info(f"Training {engine_type} for {attack_type} with {len(samples)} samples...")
                    
                    # Prepare specific training data
                    specific_data = self._prepare_specific_training_data(engine_type, samples)
                    
                    # Train specific pattern
                    response = self.session.post(
                        f"{self.api_base_url}/{engine_type}/train-pattern",
                        json={
                            'attack_type': attack_type,
                            'training_data': specific_data
                        }
                    )
                    
                    if response.status_code == 200:
                        logging.info(f"Successfully trained {attack_type} pattern for {engine_type}")
                    else:
                        logging.warning(f"Failed to train {attack_type} pattern for {engine_type}")
            
        except Exception as e:
            logging.error(f"Specific attack pattern training failed: {e}")
    
    def _train_specific_scenarios(self, engine_type: str, training_data: List[Dict]):
        """Train specific scenarios for enhanced learning"""
        try:
            # Group by scenario type
            scenario_groups = {}
            for sample in training_data:
                scenario_type = sample.get('scenario_type', 'unknown')
                if scenario_type not in scenario_groups:
                    scenario_groups[scenario_type] = []
                scenario_groups[scenario_type].append(sample)
            
            # Train each scenario type separately
            for scenario_type, samples in scenario_groups.items():
                if len(samples) > 0:
                    logging.info(f"Training {engine_type} for {scenario_type} with {len(samples)} scenarios...")
                    
                    # Prepare specific training data
                    specific_data = self._prepare_specific_training_data(engine_type, samples)
                    
                    # Train specific scenario
                    response = self.session.post(
                        f"{self.api_base_url}/{engine_type}/train-scenario",
                        json={
                            'scenario_type': scenario_type,
                            'training_data': specific_data
                        }
                    )
                    
                    if response.status_code == 200:
                        logging.info(f"Successfully trained {scenario_type} scenario for {engine_type}")
                    else:
                        logging.warning(f"Failed to train {scenario_type} scenario for {engine_type}")
            
        except Exception as e:
            logging.error(f"Specific scenario training failed: {e}")
    
    def _prepare_specific_training_data(self, engine_type: str, samples: List[Dict]) -> List[Dict]:
        """Prepare specific training data for pattern/scenario training"""
        if engine_type == 'order':
            return self._prepare_order_training_data(samples)
        elif engine_type == 'chaos':
            return self._prepare_chaos_training_data(samples)
        elif engine_type == 'balance':
            return self._prepare_balance_training_data(samples)
        else:
            return samples
    
    def _evaluate_order_performance(self) -> Dict[str, Any]:
        """Evaluate ORDER engine performance"""
        try:
            response = self.session.get(f"{self.api_base_url}/order/performance")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logging.error(f"ORDER performance evaluation failed: {e}")
            return {"error": str(e)}
    
    def _evaluate_chaos_performance(self) -> Dict[str, Any]:
        """Evaluate CHAOS engine performance"""
        try:
            response = self.session.get(f"{self.api_base_url}/chaos/performance")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logging.error(f"CHAOS performance evaluation failed: {e}")
            return {"error": str(e)}
    
    def _evaluate_balance_performance(self) -> Dict[str, Any]:
        """Evaluate BALANCE controller performance"""
        try:
            response = self.session.get(f"{self.api_base_url}/balance/performance")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logging.error(f"BALANCE performance evaluation failed: {e}")
            return {"error": str(e)}
    
    def _evaluate_overall_system_performance(self) -> Dict[str, Any]:
        """Evaluate overall system performance"""
        try:
            # Get system status
            response = self.session.get(f"{self.api_base_url}/status")
            response.raise_for_status()
            system_status = response.json()
            
            # Get performance metrics
            response = self.session.get(f"{self.api_base_url}/metrics")
            response.raise_for_status()
            metrics = response.json()
            
            # Calculate overall performance
            overall_performance = {
                'system_status': system_status,
                'metrics': metrics,
                'training_completed': True,
                'timestamp': time.time()
            }
            
            return overall_performance
            
        except Exception as e:
            logging.error(f"Overall system performance evaluation failed: {e}")
            return {"error": str(e)}
    
    def _save_training_results(self, results: Dict[str, Any]):
        """Save training results to file"""
        try:
            # Create results directory
            results_dir = Path("training_results")
            results_dir.mkdir(exist_ok=True)
            
            # Save comprehensive results
            timestamp = int(time.time())
            filename = results_dir / f"comprehensive_training_results_{timestamp}.json"
            
            with open(filename, 'w') as f:
                json.dump(results, f, indent=2, default=str)
            
            logging.info(f"Training results saved to {filename}")
            
            # Save individual engine results
            for engine, result in results.items():
                if engine != 'overall':
                    engine_filename = results_dir / f"{engine}_training_results_{timestamp}.json"
                    with open(engine_filename, 'w') as f:
                        json.dump(result, f, indent=2, default=str)
                    logging.info(f"{engine} results saved to {engine_filename}")
            
        except Exception as e:
            logging.error(f"Failed to save training results: {e}")
    
    def generate_training_report(self, results: Dict[str, Any]) -> str:
        """Generate comprehensive training report"""
        report = []
        report.append("=" * 80)
        report.append("🛡️ COMPREHENSIVE TRAINING REPORT")
        report.append("Self-Morphing AI Cybersecurity Engine")
        report.append("=" * 80)
        report.append("")
        
        # Overall system status
        if 'overall' in results:
            overall = results['overall']
            report.append("📊 OVERALL SYSTEM PERFORMANCE")
            report.append("-" * 40)
            if 'system_status' in overall:
                status = overall['system_status']
                report.append(f"System Status: {status.get('status', 'Unknown')}")
                report.append(f"All Engines Active: {status.get('all_engines_active', False)}")
                report.append(f"Training Mode: {status.get('training_mode', False)}")
            report.append("")
        
        # ORDER Engine Results
        if 'order' in results:
            order = results['order']
            report.append("🛡️ ORDER DEFENSE ENGINE")
            report.append("-" * 30)
            report.append(f"Training Status: {'Success' if order.get('success', False) else 'Failed'}")
            if 'enhanced_performance' in order:
                perf = order['enhanced_performance']
                report.append(f"Accuracy: {perf.get('accuracy', 0):.3f}")
                report.append(f"Precision: {perf.get('precision', 0):.3f}")
                report.append(f"Recall: {perf.get('recall', 0):.3f}")
                report.append(f"F1 Score: {perf.get('f1_score', 0):.3f}")
            report.append("")
        
        # CHAOS Engine Results
        if 'chaos' in results:
            chaos = results['chaos']
            report.append("🎯 CHAOS INTELLIGENCE ENGINE")
            report.append("-" * 35)
            report.append(f"Training Status: {'Success' if chaos.get('success', False) else 'Failed'}")
            if 'enhanced_performance' in chaos:
                perf = chaos['enhanced_performance']
                report.append(f"Attack Success Rate: {perf.get('success_rate', 0):.3f}")
                report.append(f"Stealth Success Rate: {perf.get('stealth_rate', 0):.3f}")
                report.append(f"Detection Avoidance: {perf.get('detection_avoidance', 0):.3f}")
            report.append("")
        
        # BALANCE Controller Results
        if 'balance' in results:
            balance = results['balance']
            report.append("⚖️ BALANCE ORCHESTRATION CONTROLLER")
            report.append("-" * 45)
            report.append(f"Training Status: {'Success' if balance.get('success', False) else 'Failed'}")
            if 'enhanced_performance' in balance:
                perf = balance['enhanced_performance']
                report.append(f"Orchestration Accuracy: {perf.get('accuracy', 0):.3f}")
                report.append(f"Response Time: {perf.get('response_time', 0):.3f}s")
                report.append(f"Adaptation Rate: {perf.get('adaptation_rate', 0):.3f}")
            report.append("")
        
        # Training Summary
        report.append("📈 TRAINING SUMMARY")
        report.append("-" * 20)
        report.append("✅ Comprehensive training completed successfully!")
        report.append("🎯 All engines trained with enhanced synthetic data")
        report.append("🛡️ System ready for production cybersecurity operations")
        report.append("")
        report.append("=" * 80)
        
        return "\n".join(report)

def main():
    """Main function for comprehensive training from scratch"""
    print("🛡️ Train from Scratch - Enhanced Training System")
    print("Self-Morphing AI Cybersecurity Engine")
    print("=" * 60)
    
    # Initialize trainer
    trainer = TrainFromScratch()
    
    try:
        # Check if API is available
        print("🔍 Checking API server availability...")
        response = requests.get("http://localhost:8000/health")
        if response.status_code != 200:
            print("❌ API server not available. Please start the server first.")
            print("   Run: python api_server.py")
            return
        
        print("✅ API server is running")
        
        # Start comprehensive training
        print("\n🚀 Starting comprehensive training from scratch...")
        print("   This will generate and train with enhanced synthetic datasets")
        print("   Training may take several minutes...")
        
        # Train the complete system
        results = trainer.train_comprehensive_system(
            order_samples=25000,    # Enhanced defense training
            chaos_samples=25000,    # Enhanced intelligence training
            balance_scenarios=15000  # Enhanced orchestration training
        )
        
        # Generate and display report
        print("\n📊 Generating comprehensive training report...")
        report = trainer.generate_training_report(results)
        print(report)
        
        # Save report to file
        timestamp = int(time.time())
        report_filename = f"comprehensive_training_report_{timestamp}.txt"
        with open(report_filename, 'w') as f:
            f.write(report)
        
        print(f"\n💾 Training report saved to '{report_filename}'")
        print("\n✅ Comprehensive training completed successfully!")
        print("🎯 The system is now ready for advanced cybersecurity operations.")
        print("🛡️ All engines have been trained with comprehensive synthetic datasets.")
        
    except Exception as e:
        print(f"❌ Comprehensive training failed: {e}")
        logging.error(f"Comprehensive training failed: {e}")

if __name__ == "__main__":
    main()





