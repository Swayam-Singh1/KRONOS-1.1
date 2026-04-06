#!/usr/bin/env python3
"""
Enhanced Training Configuration
Configures the training system for comprehensive cybersecurity model training
"""

import json
import os
from typing import Dict, Any, List
from pathlib import Path

class EnhancedTrainingConfig:
    """Configuration for enhanced training system"""
    
    def __init__(self):
        self.config = self._load_default_config()
    
    def _load_default_config(self) -> Dict[str, Any]:
        """Load default training configuration"""
        return {
            "training_mode": {
                "comprehensive": True,
                "from_scratch": True,
                "enhanced_synthetic_data": True,
                "minimal_initial_data": True
            },
            
            "data_generation": {
                "order_samples": 25000,
                "chaos_samples": 25000,
                "balance_scenarios": 15000,
                "normal_traffic_ratio": 0.6,
                "attack_traffic_ratio": 0.4,
                "threat_levels": [1, 2, 3, 4, 5],
                "attack_categories": [
                    "network_attacks",
                    "web_attacks", 
                    "system_attacks",
                    "malware_attacks",
                    "social_engineering",
                    "insider_threats",
                    "apt_attacks",
                    "zero_day_attacks"
                ]
            },
            
            "order_engine": {
                "attack_types": [
                    "ddos", "port_scan", "man_in_the_middle",
                    "sql_injection", "xss", "csrf",
                    "buffer_overflow", "privilege_escalation",
                    "trojan", "ransomware", "apt_campaign"
                ],
                "normal_behaviors": [
                    "web_browsing", "email_communication",
                    "file_transfer", "database_access",
                    "video_streaming"
                ],
                "feature_extraction": {
                    "network_features": True,
                    "behavioral_features": True,
                    "attack_features": True,
                    "threat_indicators": True
                },
                "model_parameters": {
                    "anomaly_contamination": 0.1,
                    "n_estimators": 200,
                    "max_depth": 20,
                    "min_samples_split": 5,
                    "min_samples_leaf": 2
                }
            },
            
            "chaos_engine": {
                "attack_patterns": [
                    "ddos", "port_scan", "man_in_the_middle",
                    "sql_injection", "xss", "csrf",
                    "buffer_overflow", "privilege_escalation",
                    "trojan", "ransomware", "apt_campaign"
                ],
                "threat_actors": [
                    "APT1", "Lazarus", "Fancy Bear", "Cobalt Strike"
                ],
                "campaigns": [
                    "Operation Aurora", "WannaCry Campaign", "SolarWinds Supply Chain"
                ],
                "evasion_techniques": [
                    "traffic_spoofing", "distributed_source", "protocol_manipulation",
                    "slow_scan", "fragmented_packets", "source_spoofing",
                    "arp_spoofing", "dns_poisoning", "ssl_stripping",
                    "encoding", "time_based", "boolean_blind",
                    "event_handlers", "dom_manipulation", "token_manipulation",
                    "rop_chains", "aslr_bypass", "dep_bypass",
                    "packing", "obfuscation", "anti_analysis",
                    "living_off_land", "legitimate_tools", "encrypted_communication"
                ],
                "attack_vectors": [
                    "volumetric", "protocol", "application",
                    "tcp_syn", "tcp_connect", "udp_scan",
                    "arp_poisoning", "dns_hijacking", "ssl_interception",
                    "union_based", "error_based", "blind_boolean",
                    "stored", "reflected", "dom_based",
                    "form_submission", "ajax_requests", "image_requests",
                    "stack_overflow", "heap_overflow", "format_string",
                    "kernel_vulnerabilities", "service_misconfigurations", "weak_permissions",
                    "email_attachment", "drive_by_download", "social_engineering",
                    "email_phishing", "vulnerability_exploitation", "lateral_movement",
                    "spear_phishing", "zero_day_exploits", "supply_chain"
                ]
            },
            
            "balance_controller": {
                "scenario_types": [
                    "defense", "intelligence", "response", "adaptation"
                ],
                "threat_levels": [1, 2, 3, 4, 5],
                "complexity_levels": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                "response_actions": [
                    "block_ip", "quarantine_process", "update_firewall", "alert_security",
                    "gather_osint", "analyze_threat", "update_ioc", "share_intelligence",
                    "contain_threat", "eradicate_malware", "recover_systems", "document_incident",
                    "update_models", "adjust_thresholds", "modify_rules", "retrain_ai"
                ],
                "system_metrics": [
                    "cpu_usage", "memory_usage", "disk_usage", "network_usage",
                    "active_connections", "threats_detected", "incidents_created", "response_time"
                ]
            },
            
            "performance_metrics": {
                "order_metrics": [
                    "accuracy", "precision", "recall", "f1_score",
                    "false_positive_rate", "false_negative_rate",
                    "detection_rate", "response_time"
                ],
                "chaos_metrics": [
                    "success_rate", "stealth_rate", "detection_avoidance",
                    "damage_potential", "persistence", "sophistication"
                ],
                "balance_metrics": [
                    "orchestration_accuracy", "response_time", "adaptation_rate",
                    "system_efficiency", "threat_mitigation", "false_positive_rate"
                ]
            },
            
            "training_parameters": {
                "batch_size": 1000,
                "epochs": 100,
                "learning_rate": 0.001,
                "validation_split": 0.2,
                "early_stopping": True,
                "patience": 10,
                "model_checkpointing": True,
                "tensorboard_logging": True
            },
            
            "data_augmentation": {
                "enabled": True,
                "noise_injection": True,
                "feature_perturbation": True,
                "temporal_shift": True,
                "protocol_variation": True,
                "payload_mutation": True
            },
            
            "model_architecture": {
                "order_engine": {
                    "anomaly_detection": "IsolationForest",
                    "classification": "RandomForestClassifier",
                    "neural_network": "MLPClassifier",
                    "ensemble_method": "VotingClassifier"
                },
                "chaos_engine": {
                    "attack_generation": "GeneticAlgorithm",
                    "pattern_recognition": "RandomForestClassifier",
                    "stealth_optimization": "ParticleSwarmOptimization",
                    "adaptation": "ReinforcementLearning"
                },
                "balance_controller": {
                    "orchestration": "NeuralNetwork",
                    "decision_making": "RandomForestClassifier",
                    "adaptation": "GeneticAlgorithm",
                    "optimization": "BayesianOptimization"
                }
            },
            
            "evaluation": {
                "cross_validation": True,
                "k_folds": 5,
                "stratified_sampling": True,
                "performance_metrics": True,
                "confusion_matrix": True,
                "roc_curves": True,
                "precision_recall_curves": True
            },
            
            "deployment": {
                "production_ready": True,
                "scalable": True,
                "real_time": True,
                "autonomous": True,
                "self_healing": True,
                "self_optimizing": True
            }
        }
    
    def save_config(self, filename: str = "enhanced_training_config.json"):
        """Save configuration to file"""
        try:
            with open(filename, 'w') as f:
                json.dump(self.config, f, indent=2)
            print(f"✅ Configuration saved to {filename}")
        except Exception as e:
            print(f"❌ Failed to save configuration: {e}")
    
    def load_config(self, filename: str = "enhanced_training_config.json"):
        """Load configuration from file"""
        try:
            if os.path.exists(filename):
                with open(filename, 'r') as f:
                    self.config = json.load(f)
                print(f"✅ Configuration loaded from {filename}")
            else:
                print(f"⚠️ Configuration file {filename} not found, using defaults")
        except Exception as e:
            print(f"❌ Failed to load configuration: {e}")
    
    def update_config(self, section: str, updates: Dict[str, Any]):
        """Update configuration section"""
        if section in self.config:
            self.config[section].update(updates)
            print(f"✅ Updated {section} configuration")
        else:
            self.config[section] = updates
            print(f"✅ Added new {section} configuration")
    
    def get_config(self, section: str = None) -> Dict[str, Any]:
        """Get configuration or specific section"""
        if section:
            return self.config.get(section, {})
        return self.config
    
    def validate_config(self) -> bool:
        """Validate configuration"""
        try:
            # Check required sections
            required_sections = [
                "training_mode", "data_generation", "order_engine",
                "chaos_engine", "balance_controller", "performance_metrics"
            ]
            
            for section in required_sections:
                if section not in self.config:
                    print(f"❌ Missing required section: {section}")
                    return False
            
            # Validate data generation parameters
            data_gen = self.config["data_generation"]
            if data_gen["order_samples"] <= 0:
                print("❌ Invalid order_samples value")
                return False
            
            if data_gen["chaos_samples"] <= 0:
                print("❌ Invalid chaos_samples value")
                return False
            
            if data_gen["balance_scenarios"] <= 0:
                print("❌ Invalid balance_scenarios value")
                return False
            
            # Validate ratios
            normal_ratio = data_gen["normal_traffic_ratio"]
            attack_ratio = data_gen["attack_traffic_ratio"]
            
            if abs(normal_ratio + attack_ratio - 1.0) > 0.01:
                print("❌ Traffic ratios must sum to 1.0")
                return False
            
            print("✅ Configuration validation passed")
            return True
            
        except Exception as e:
            print(f"❌ Configuration validation failed: {e}")
            return False
    
    def generate_training_script(self, output_file: str = "run_enhanced_training.py"):
        """Generate training script based on configuration"""
        script_content = f'''#!/usr/bin/env python3
"""
Generated Enhanced Training Script
Based on configuration: {self.config['training_mode']}
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from train_from_scratch import TrainFromScratch

def main():
    """Run enhanced training based on configuration"""
    print("🛡️ Enhanced Training Script")
    print("Generated from configuration")
    print("=" * 40)
    
    # Initialize trainer
    trainer = TrainFromScratch()
    
    # Get configuration parameters
    data_gen = {self.config['data_generation']}
    
    try:
        # Run comprehensive training
        results = trainer.train_comprehensive_system(
            order_samples={data_gen['order_samples']},
            chaos_samples={data_gen['chaos_samples']},
            balance_scenarios={data_gen['balance_scenarios']}
        )
        
        print("✅ Enhanced training completed successfully!")
        return results
        
    except Exception as e:
        print(f"❌ Enhanced training failed: {{e}}")
        return None

if __name__ == "__main__":
    main()
'''
        
        try:
            with open(output_file, 'w') as f:
                f.write(script_content)
            print(f"✅ Training script generated: {output_file}")
        except Exception as e:
            print(f"❌ Failed to generate training script: {e}")
    
    def print_config_summary(self):
        """Print configuration summary"""
        print("🛡️ Enhanced Training Configuration Summary")
        print("=" * 50)
        
        # Training mode
        mode = self.config['training_mode']
        print(f"Training Mode: {mode['comprehensive']}")
        print(f"From Scratch: {mode['from_scratch']}")
        print(f"Enhanced Synthetic Data: {mode['enhanced_synthetic_data']}")
        print(f"Minimal Initial Data: {mode['minimal_initial_data']}")
        print()
        
        # Data generation
        data_gen = self.config['data_generation']
        print(f"ORDER Samples: {data_gen['order_samples']:,}")
        print(f"CHAOS Samples: {data_gen['chaos_samples']:,}")
        print(f"BALANCE Scenarios: {data_gen['balance_scenarios']:,}")
        print(f"Normal Traffic Ratio: {data_gen['normal_traffic_ratio']:.1%}")
        print(f"Attack Traffic Ratio: {data_gen['attack_traffic_ratio']:.1%}")
        print()
        
        # Attack types
        order_attacks = len(self.config['order_engine']['attack_types'])
        chaos_attacks = len(self.config['chaos_engine']['attack_patterns'])
        print(f"ORDER Attack Types: {order_attacks}")
        print(f"CHAOS Attack Patterns: {chaos_attacks}")
        print()
        
        # Performance metrics
        metrics = self.config['performance_metrics']
        print(f"ORDER Metrics: {len(metrics['order_metrics'])}")
        print(f"CHAOS Metrics: {len(metrics['chaos_metrics'])}")
        print(f"BALANCE Metrics: {len(metrics['balance_metrics'])}")
        print()
        
        print("✅ Configuration ready for enhanced training")

def main():
    """Main function for configuration management"""
    print("🛡️ Enhanced Training Configuration Manager")
    print("=" * 50)
    
    # Initialize configuration
    config = EnhancedTrainingConfig()
    
    # Print current configuration
    config.print_config_summary()
    
    # Validate configuration
    if config.validate_config():
        print("\n✅ Configuration is valid and ready for use")
        
        # Save configuration
        config.save_config()
        
        # Generate training script
        config.generate_training_script()
        
        print("\n🚀 Ready to run enhanced training!")
        print("   Run: python train_from_scratch.py")
        print("   Or: python run_enhanced_training.py")
    else:
        print("\n❌ Configuration validation failed")
        print("   Please check the configuration and try again")

if __name__ == "__main__":
    main()





