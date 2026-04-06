"""
KDD Cup 99 Integration for CHAOS Engine
Real-world attack simulation and intelligence gathering using KDD dataset
"""

import numpy as np
import pandas as pd
import logging
import random
import time
from typing import Dict, List, Tuple, Optional, Any
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum

from kdd_data_loader import KDDDataLoader, AttackCategory
from chaos_engine import ChaosEngine, AttackType, AttackPayload, AttackResult

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - KDD_CHAOS - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('kdd_chaos_integration.log'),
        logging.StreamHandler()
    ]
)

class KDDChaosIntegration:
    """Integration of KDD Cup 99 data with CHAOS engine"""
    
    def __init__(self, chaos_engine: ChaosEngine, kdd_loader: KDDDataLoader):
        self.chaos_engine = chaos_engine
        self.kdd_loader = kdd_loader
        self.kdd_attack_patterns = {}
        self.attack_statistics = {}
        self.simulation_history = []
        
        logging.info("KDD-CHAOS integration initialized")
    
    def analyze_kdd_attacks(self, max_samples: int = 10000) -> Dict[str, Any]:
        """Analyze KDD attack patterns for CHAOS engine"""
        try:
            logging.info("Analyzing KDD attack patterns...")
            
            # Load KDD data
            data = self.kdd_loader.load_data("kddcup.data_10_percent", max_rows=max_samples)
            
            # Analyze attack patterns
            attack_analysis = {}
            
            for attack_type in data['attack_type'].unique():
                if attack_type == 'normal':
                    continue
                
                attack_data = data[data['attack_type'] == attack_type]
                category = self.kdd_loader.attack_categories.get(attack_type, 'unknown')
                
                # Analyze characteristics
                analysis = {
                    'count': len(attack_data),
                    'category': category,
                    'avg_duration': attack_data['duration'].mean(),
                    'avg_src_bytes': attack_data['src_bytes'].mean(),
                    'avg_dst_bytes': attack_data['dst_bytes'].mean(),
                    'common_protocols': attack_data['protocol_type'].value_counts().head(3).to_dict(),
                    'common_services': attack_data['service'].value_counts().head(3).to_dict(),
                    'common_flags': attack_data['flag'].value_counts().head(3).to_dict(),
                    'avg_failed_logins': attack_data['num_failed_logins'].mean(),
                    'root_shell_rate': (attack_data['root_shell'] > 0).mean(),
                    'su_attempted_rate': (attack_data['su_attempted'] > 0).mean()
                }
                
                attack_analysis[attack_type] = analysis
            
            self.kdd_attack_patterns = attack_analysis
            
            # Calculate overall statistics
            self.attack_statistics = {
                'total_attacks': len(data[data['attack_type'] != 'normal']),
                'attack_types': len(data['attack_type'].unique()) - 1,  # Exclude 'normal'
                'categories': data['attack_category'].value_counts().to_dict(),
                'most_common_attacks': data['attack_type'].value_counts().head(10).to_dict(),
                'analysis_timestamp': datetime.now().isoformat()
            }
            
            logging.info(f"Analyzed {len(attack_analysis)} attack types")
            logging.info(f"Total attacks: {self.attack_statistics['total_attacks']}")
            
            return {
                'attack_patterns': attack_analysis,
                'statistics': self.attack_statistics
            }
            
        except Exception as e:
            logging.error(f"KDD attack analysis failed: {e}")
            return {'error': str(e)}
    
    def generate_kdd_based_attacks(self, n_attacks: int = 100, 
                                  attack_types: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """Generate attacks based on KDD patterns"""
        try:
            if not self.kdd_attack_patterns:
                self.analyze_kdd_attacks()
            
            attacks = []
            available_attack_types = list(self.kdd_attack_patterns.keys())
            
            if attack_types:
                available_attack_types = [at for at in attack_types if at in available_attack_types]
            
            for _ in range(n_attacks):
                # Select random attack type
                attack_type = random.choice(available_attack_types)
                pattern = self.kdd_attack_patterns[attack_type]
                
                # Generate attack based on KDD patterns
                attack = self._generate_attack_from_pattern(attack_type, pattern)
                attacks.append(attack)
            
            logging.info(f"Generated {len(attacks)} KDD-based attacks")
            return attacks
            
        except Exception as e:
            logging.error(f"KDD-based attack generation failed: {e}")
            return []
    
    def _generate_attack_from_pattern(self, attack_type: str, pattern: Dict[str, Any]) -> Dict[str, Any]:
        """Generate individual attack from KDD pattern"""
        try:
            # Map KDD attack types to CHAOS attack types
            attack_mapping = {
                'back': AttackType.DDOS,
                'buffer_overflow': AttackType.BUFFER_OVERFLOW,
                'ftp_write': AttackType.MALWARE,
                'guess_passwd': AttackType.BRUTE_FORCE,
                'imap': AttackType.BRUTE_FORCE,
                'ipsweep': AttackType.MAN_IN_THE_MIDDLE,
                'land': AttackType.DDOS,
                'loadmodule': AttackType.MALWARE,
                'multihop': AttackType.MAN_IN_THE_MIDDLE,
                'neptune': AttackType.DDOS,
                'nmap': AttackType.MAN_IN_THE_MIDDLE,
                'perl': AttackType.MALWARE,
                'phf': AttackType.SQL_INJECTION,
                'pod': AttackType.DDOS,
                'portsweep': AttackType.MAN_IN_THE_MIDDLE,
                'rootkit': AttackType.MALWARE,
                'satan': AttackType.MAN_IN_THE_MIDDLE,
                'smurf': AttackType.DDOS,
                'spy': AttackType.MALWARE,
                'teardrop': AttackType.DDOS,
                'warezclient': AttackType.MALWARE,
                'warezmaster': AttackType.MALWARE
            }
            
            chaos_attack_type = attack_mapping.get(attack_type, AttackType.MALWARE)
            
            # Generate target information
            target_ip = f"10.0.{random.randint(1, 255)}.{random.randint(1, 255)}"
            
            # Select port based on common services
            if pattern['common_services']:
                service = random.choice(list(pattern['common_services'].keys()))
                target_port = self._get_service_port(service)
            else:
                target_port = random.randint(1024, 65535)
            
            # Calculate intensity based on KDD characteristics
            intensity = self._calculate_intensity(pattern)
            
            # Calculate stealth level
            stealth_level = self._calculate_stealth_level(pattern)
            
            # Generate payload size based on KDD patterns
            payload_size = int(np.random.normal(
                pattern['avg_src_bytes'] + pattern['avg_dst_bytes'], 
                (pattern['avg_src_bytes'] + pattern['avg_dst_bytes']) * 0.1
            ))
            payload_size = max(64, min(65536, payload_size))  # Clamp to reasonable range
            
            attack = {
                'attack_type': chaos_attack_type,
                'kdd_attack_type': attack_type,
                'target_ip': target_ip,
                'target_port': target_port,
                'intensity': intensity,
                'stealth_level': stealth_level,
                'payload_size': payload_size,
                'duration': max(0.1, np.random.normal(pattern['avg_duration'], pattern['avg_duration'] * 0.2)),
                'protocol': random.choice(list(pattern['common_protocols'].keys())) if pattern['common_protocols'] else 'TCP',
                'flags': random.choice(list(pattern['common_flags'].keys())) if pattern['common_flags'] else 'SF',
                'category': pattern['category'],
                'timestamp': time.time()
            }
            
            return attack
            
        except Exception as e:
            logging.error(f"Attack generation from pattern failed: {e}")
            return self._generate_default_attack()
    
    def _get_service_port(self, service: str) -> int:
        """Map service to port number"""
        service_ports = {
            'http': 80, 'https': 443, 'ftp': 21, 'ssh': 22, 'telnet': 23,
            'smtp': 25, 'dns': 53, 'pop3': 110, 'imap': 143, 'snmp': 161,
            'ldap': 389, 'smtp': 587, 'imaps': 993, 'pop3s': 995,
            'finger': 79, 'gopher': 70, 'rlogin': 513, 'sunrpc': 111
        }
        return service_ports.get(service.lower(), random.randint(1024, 65535))
    
    def _calculate_intensity(self, pattern: Dict[str, Any]) -> float:
        """Calculate attack intensity based on KDD pattern"""
        # Base intensity on attack characteristics
        intensity = 0.5  # Base intensity
        
        # Increase intensity for high-impact attacks
        if pattern['root_shell_rate'] > 0.1:
            intensity += 0.3
        if pattern['su_attempted_rate'] > 0.1:
            intensity += 0.2
        if pattern['avg_failed_logins'] > 5:
            intensity += 0.2
        
        # Normalize to 0-1 range
        return min(1.0, max(0.1, intensity))
    
    def _calculate_stealth_level(self, pattern: Dict[str, Any]) -> int:
        """Calculate stealth level based on KDD pattern"""
        # Base stealth level
        stealth = 5
        
        # Decrease stealth for attacks with high failed logins (more detectable)
        if pattern['avg_failed_logins'] > 10:
            stealth -= 2
        elif pattern['avg_failed_logins'] > 5:
            stealth -= 1
        
        # Increase stealth for attacks with low duration (harder to detect)
        if pattern['avg_duration'] < 1.0:
            stealth += 2
        elif pattern['avg_duration'] < 5.0:
            stealth += 1
        
        # Normalize to 1-10 range
        return max(1, min(10, stealth))
    
    def _generate_default_attack(self) -> Dict[str, Any]:
        """Generate default attack if pattern analysis fails"""
        return {
            'attack_type': AttackType.MALWARE,
            'kdd_attack_type': 'unknown',
            'target_ip': f"10.0.{random.randint(1, 255)}.{random.randint(1, 255)}",
            'target_port': random.randint(1024, 65535),
            'intensity': random.uniform(0.3, 0.8),
            'stealth_level': random.randint(3, 7),
            'payload_size': random.randint(64, 4096),
            'duration': random.uniform(0.1, 10.0),
            'protocol': 'TCP',
            'flags': 'SF',
            'category': 'unknown',
            'timestamp': time.time()
        }
    
    def simulate_kdd_attacks(self, n_attacks: int = 100, 
                           real_time: bool = False) -> Dict[str, Any]:
        """Simulate KDD-based attacks through CHAOS engine"""
        try:
            logging.info(f"Simulating {n_attacks} KDD-based attacks...")
            
            # Generate KDD-based attacks
            attacks = self.generate_kdd_based_attacks(n_attacks)
            
            # Simulate attacks through CHAOS engine
            simulation_results = {
                'total_attacks': len(attacks),
                'successful_attacks': 0,
                'failed_attacks': 0,
                'attack_results': [],
                'attack_type_performance': {},
                'category_performance': {},
                'total_damage': 0,
                'simulation_time': 0,
                'timestamp': datetime.now().isoformat()
            }
            
            start_time = time.time()
            
            for attack in attacks:
                try:
                    # Launch attack through CHAOS engine
                    attack_id = self.chaos_engine.launch_attack(
                        attack['attack_type'],
                        attack['target_ip'],
                        attack['target_port']
                    )
                    
                    # Simulate attack result based on KDD characteristics
                    success_probability = self._calculate_success_probability(attack)
                    success = random.random() < success_probability
                    
                    if success:
                        simulation_results['successful_attacks'] += 1
                        damage = int(attack['intensity'] * 100 * random.uniform(0.5, 1.5))
                        simulation_results['total_damage'] += damage
                    else:
                        simulation_results['failed_attacks'] += 1
                        damage = 0
                    
                    # Record attack result
                    attack_result = {
                        'attack_id': attack_id,
                        'kdd_attack_type': attack['kdd_attack_type'],
                        'chaos_attack_type': attack['attack_type'].value,
                        'target': f"{attack['target_ip']}:{attack['target_port']}",
                        'success': success,
                        'damage': damage,
                        'intensity': attack['intensity'],
                        'stealth_level': attack['stealth_level'],
                        'category': attack['category'],
                        'timestamp': attack['timestamp']
                    }
                    
                    simulation_results['attack_results'].append(attack_result)
                    
                    # Update performance tracking
                    attack_type = attack['attack_type'].value
                    if attack_type not in simulation_results['attack_type_performance']:
                        simulation_results['attack_type_performance'][attack_type] = {'success': 0, 'total': 0}
                    
                    simulation_results['attack_type_performance'][attack_type]['total'] += 1
                    if success:
                        simulation_results['attack_type_performance'][attack_type]['success'] += 1
                    
                    category = attack['category']
                    if category not in simulation_results['category_performance']:
                        simulation_results['category_performance'][category] = {'success': 0, 'total': 0}
                    
                    simulation_results['category_performance'][category]['total'] += 1
                    if success:
                        simulation_results['category_performance'][category]['success'] += 1
                    
                    # Add delay for real-time simulation
                    if real_time:
                        time.sleep(random.uniform(0.1, 1.0))
                
                except Exception as e:
                    logging.error(f"Attack simulation failed: {e}")
                    simulation_results['failed_attacks'] += 1
            
            simulation_results['simulation_time'] = time.time() - start_time
            
            # Calculate success rates
            for attack_type in simulation_results['attack_type_performance']:
                perf = simulation_results['attack_type_performance'][attack_type]
                perf['success_rate'] = perf['success'] / perf['total'] if perf['total'] > 0 else 0
            
            for category in simulation_results['category_performance']:
                perf = simulation_results['category_performance'][category]
                perf['success_rate'] = perf['success'] / perf['total'] if perf['total'] > 0 else 0
            
            # Store simulation history
            self.simulation_history.append(simulation_results)
            
            logging.info(f"KDD attack simulation completed: {simulation_results['successful_attacks']} successful, {simulation_results['failed_attacks']} failed")
            
            return simulation_results
            
        except Exception as e:
            logging.error(f"KDD attack simulation failed: {e}")
            return {'error': str(e)}
    
    def _calculate_success_probability(self, attack: Dict[str, Any]) -> float:
        """Calculate attack success probability based on KDD characteristics"""
        base_probability = 0.5
        
        # Adjust based on intensity
        base_probability += attack['intensity'] * 0.3
        
        # Adjust based on stealth level
        base_probability += (attack['stealth_level'] - 5) * 0.05
        
        # Adjust based on attack category
        category_modifiers = {
            'dos': 0.8,  # DDoS attacks have high success rate
            'probe': 0.6,  # Probing attacks have medium success rate
            'r2l': 0.4,  # Remote to local attacks have lower success rate
            'u2r': 0.3   # User to root attacks have lowest success rate
        }
        
        category = attack.get('category', 'unknown')
        if category in category_modifiers:
            base_probability *= category_modifiers[category]
        
        # Normalize to 0-1 range
        return max(0.1, min(0.9, base_probability))
    
    def get_attack_intelligence(self, target_ip: str = None) -> Dict[str, Any]:
        """Generate intelligence report based on KDD attack patterns"""
        try:
            if not self.kdd_attack_patterns:
                self.analyze_kdd_attacks()
            
            intelligence = {
                'timestamp': datetime.now().isoformat(),
                'target_ip': target_ip or f"10.0.{random.randint(1, 255)}.{random.randint(1, 255)}",
                'threat_level': 'medium',
                'attack_probabilities': {},
                'recommended_defenses': [],
                'attack_patterns': {},
                'vulnerability_assessment': {}
            }
            
            # Calculate attack probabilities based on KDD patterns
            for attack_type, pattern in self.kdd_attack_patterns.items():
                probability = self._calculate_attack_probability(pattern)
                intelligence['attack_probabilities'][attack_type] = probability
            
            # Generate recommended defenses
            intelligence['recommended_defenses'] = self._generate_defense_recommendations()
            
            # Generate attack patterns
            intelligence['attack_patterns'] = self._generate_attack_patterns()
            
            # Generate vulnerability assessment
            intelligence['vulnerability_assessment'] = self._generate_vulnerability_assessment()
            
            # Determine overall threat level
            max_probability = max(intelligence['attack_probabilities'].values()) if intelligence['attack_probabilities'] else 0
            if max_probability > 0.7:
                intelligence['threat_level'] = 'high'
            elif max_probability > 0.4:
                intelligence['threat_level'] = 'medium'
            else:
                intelligence['threat_level'] = 'low'
            
            logging.info(f"Generated intelligence report for {intelligence['target_ip']}")
            
            return intelligence
            
        except Exception as e:
            logging.error(f"Intelligence generation failed: {e}")
            return {'error': str(e)}
    
    def _calculate_attack_probability(self, pattern: Dict[str, Any]) -> float:
        """Calculate probability of specific attack type"""
        # Base probability on attack frequency and characteristics
        base_prob = min(0.5, pattern['count'] / 1000)  # Normalize by sample size
        
        # Adjust based on attack characteristics
        if pattern['root_shell_rate'] > 0.1:
            base_prob += 0.2
        if pattern['avg_failed_logins'] > 5:
            base_prob += 0.1
        
        return min(1.0, base_prob)
    
    def _generate_defense_recommendations(self) -> List[str]:
        """Generate defense recommendations based on KDD patterns"""
        recommendations = [
            "Implement network segmentation to limit lateral movement",
            "Deploy intrusion detection systems (IDS) for anomaly detection",
            "Enable comprehensive logging and monitoring",
            "Implement strong authentication mechanisms",
            "Regular security updates and patch management",
            "Network traffic analysis and behavioral monitoring",
            "Implement rate limiting and DDoS protection",
            "Deploy honeypots for threat intelligence gathering"
        ]
        
        return recommendations
    
    def _generate_attack_patterns(self) -> Dict[str, Any]:
        """Generate attack patterns based on KDD analysis"""
        patterns = {
            'common_protocols': {},
            'common_services': {},
            'attack_timing': {
                'peak_hours': [9, 10, 11, 14, 15, 16],  # Business hours
                'off_hours': [2, 3, 4, 5]  # Late night/early morning
            },
            'geographical_distribution': {
                'internal_attacks': 0.3,
                'external_attacks': 0.7
            }
        }
        
        # Aggregate patterns from all attack types
        for pattern in self.kdd_attack_patterns.values():
            for protocol, count in pattern['common_protocols'].items():
                if protocol not in patterns['common_protocols']:
                    patterns['common_protocols'][protocol] = 0
                patterns['common_protocols'][protocol] += count
            
            for service, count in pattern['common_services'].items():
                if service not in patterns['common_services']:
                    patterns['common_services'][service] = 0
                patterns['common_services'][service] += count
        
        return patterns
    
    def _generate_vulnerability_assessment(self) -> Dict[str, Any]:
        """Generate vulnerability assessment based on KDD patterns"""
        assessment = {
            'overall_risk': 'medium',
            'vulnerabilities': [
                'Weak authentication mechanisms',
                'Insufficient network monitoring',
                'Outdated security controls',
                'Inadequate access controls',
                'Poor incident response capabilities'
            ],
            'risk_factors': {
                'high_failed_logins': 0.7,
                'root_access_attempts': 0.8,
                'network_scanning': 0.6,
                'suspicious_traffic': 0.5
            }
        }
        
        return assessment
    
    def get_simulation_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent simulation history"""
        return self.simulation_history[-limit:] if self.simulation_history else []
    
    def get_kdd_chaos_status(self) -> Dict[str, Any]:
        """Get KDD-CHAOS integration status"""
        return {
            'attack_patterns_analyzed': len(self.kdd_attack_patterns),
            'attack_statistics': self.attack_statistics,
            'simulation_history_count': len(self.simulation_history),
            'last_analysis': self.attack_statistics.get('analysis_timestamp'),
            'integration_active': True
        }

def main():
    """Example usage of KDD-CHAOS integration"""
    try:
        # Initialize components
        from chaos_engine import ChaosEngine
        
        chaos_engine = ChaosEngine({})
        kdd_loader = KDDDataLoader()
        kdd_chaos = KDDChaosIntegration(chaos_engine, kdd_loader)
        
        # Analyze KDD attacks
        analysis = kdd_chaos.analyze_kdd_attacks(max_samples=5000)
        print("Attack Analysis:", analysis)
        
        # Simulate attacks
        simulation = kdd_chaos.simulate_kdd_attacks(n_attacks=50)
        print("Simulation Results:", simulation)
        
        # Generate intelligence
        intelligence = kdd_chaos.get_attack_intelligence()
        print("Intelligence Report:", intelligence)
        
    except Exception as e:
        logging.error(f"KDD-CHAOS integration example failed: {e}")

if __name__ == "__main__":
    main()
