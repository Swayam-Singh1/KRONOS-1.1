"""
KDD Cup 99 Integration for ORDER Engine
Enhanced training and anomaly detection using real-world dataset
"""

import numpy as np
import pandas as pd
import logging
import pickle
import json
from typing import Dict, List, Tuple, Optional, Any
from sklearn.ensemble import IsolationForest, RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
from sklearn.model_selection import cross_val_score
import joblib
import os
from datetime import datetime

from kdd_data_loader import KDDDataLoader, AttackCategory
from order_engine import OrderEngine, NetworkFlow

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - KDD_ORDER - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('kdd_order_integration.log'),
        logging.StreamHandler()
    ]
)

class KDDOrderIntegration:
    """Integration of KDD Cup 99 data with ORDER engine"""
    
    def __init__(self, order_engine: OrderEngine, kdd_loader: KDDDataLoader):
        self.order_engine = order_engine
        self.kdd_loader = kdd_loader
        self.kdd_models = {}
        self.kdd_scaler = StandardScaler()
        self.training_history = []
        
        logging.info("KDD-ORDER integration initialized")
    
    def train_with_kdd_data(self, use_full_dataset: bool = False, 
                           max_samples: int = 50000) -> Dict[str, Any]:
        """Train ORDER engine using KDD Cup 99 data"""
        try:
            logging.info("Starting KDD-based ORDER engine training...")
            
            # Load KDD data
            if use_full_dataset:
                data = self.kdd_loader.load_data("kddcup.data", max_rows=max_samples)
            else:
                data = self.kdd_loader.load_data("kddcup.data_10_percent", max_rows=max_samples)
            
            # Preprocess data
            X, y = self.kdd_loader.preprocess_data(data)
            
            # Split data
            X_train, X_test, y_train, y_test = self.kdd_loader.split_data(X, y)
            
            # Train Isolation Forest for anomaly detection
            isolation_forest = self._train_isolation_forest(X_train, y_train)
            
            # Train Random Forest for attack classification
            random_forest = self._train_random_forest(X_train, y_train)
            
            # Evaluate models
            evaluation_results = self._evaluate_models(
                isolation_forest, random_forest, X_test, y_test
            )
            
            # Store models
            self.kdd_models = {
                'isolation_forest': isolation_forest,
                'random_forest': random_forest,
                'scaler': self.kdd_loader.scaler,
                'label_encoders': self.kdd_loader.label_encoders,
                'feature_names': self.kdd_loader.feature_names,
                'training_timestamp': datetime.now().isoformat(),
                'evaluation_results': evaluation_results
            }
            
            # Save models
            self._save_kdd_models()
            
            # Update ORDER engine with KDD-trained models
            self._update_order_engine()
            
            logging.info("KDD-based ORDER engine training completed successfully")
            
            return {
                'status': 'success',
                'models_trained': list(self.kdd_models.keys()),
                'evaluation_results': evaluation_results,
                'training_samples': len(X_train),
                'test_samples': len(X_test)
            }
            
        except Exception as e:
            logging.error(f"KDD-based training failed: {e}")
            return {'status': 'error', 'error': str(e)}
    
    def _train_isolation_forest(self, X_train: np.ndarray, y_train: np.ndarray) -> IsolationForest:
        """Train Isolation Forest for anomaly detection"""
        try:
            logging.info("Training Isolation Forest...")
            
            # Create binary labels (normal vs anomaly)
            y_binary = (y_train != 0).astype(int)  # 0 is 'normal' in encoded labels
            
            # Train Isolation Forest
            isolation_forest = IsolationForest(
                contamination=0.1,  # 10% contamination
                random_state=42,
                n_estimators=100,
                max_samples='auto',
                max_features=1.0
            )
            
            isolation_forest.fit(X_train)
            
            logging.info("Isolation Forest training completed")
            return isolation_forest
            
        except Exception as e:
            logging.error(f"Isolation Forest training failed: {e}")
            raise
    
    def _train_random_forest(self, X_train: np.ndarray, y_train: np.ndarray) -> RandomForestClassifier:
        """Train Random Forest for attack classification"""
        try:
            logging.info("Training Random Forest...")
            
            random_forest = RandomForestClassifier(
                n_estimators=100,
                random_state=42,
                max_depth=20,
                min_samples_split=5,
                min_samples_leaf=2,
                n_jobs=-1
            )
            
            random_forest.fit(X_train, y_train)
            
            logging.info("Random Forest training completed")
            return random_forest
            
        except Exception as e:
            logging.error(f"Random Forest training failed: {e}")
            raise
    
    def _evaluate_models(self, isolation_forest: IsolationForest, 
                        random_forest: RandomForestClassifier,
                        X_test: np.ndarray, y_test: np.ndarray) -> Dict[str, Any]:
        """Evaluate trained models"""
        try:
            logging.info("Evaluating models...")
            
            # Evaluate Isolation Forest
            y_binary = (y_test != 0).astype(int)
            isolation_predictions = isolation_forest.predict(X_test)
            isolation_scores = isolation_forest.decision_function(X_test)
            
            # Convert isolation forest predictions to binary (1 = normal, -1 = anomaly)
            isolation_binary = (isolation_predictions == 1).astype(int)
            
            # Evaluate Random Forest
            rf_predictions = random_forest.predict(X_test)
            rf_probabilities = random_forest.predict_proba(X_test)
            
            # Calculate metrics
            isolation_auc = roc_auc_score(y_binary, isolation_scores)
            rf_accuracy = random_forest.score(X_test, y_test)
            
            # Cross-validation scores
            cv_scores = cross_val_score(random_forest, X_test, y_test, cv=5)
            
            evaluation_results = {
                'isolation_forest': {
                    'auc_score': isolation_auc,
                    'accuracy': (isolation_binary == y_binary).mean(),
                    'confusion_matrix': confusion_matrix(y_binary, isolation_binary).tolist()
                },
                'random_forest': {
                    'accuracy': rf_accuracy,
                    'cv_mean': cv_scores.mean(),
                    'cv_std': cv_scores.std(),
                    'classification_report': classification_report(y_test, rf_predictions, output_dict=True)
                }
            }
            
            logging.info(f"Isolation Forest AUC: {isolation_auc:.4f}")
            logging.info(f"Random Forest Accuracy: {rf_accuracy:.4f}")
            
            return evaluation_results
            
        except Exception as e:
            logging.error(f"Model evaluation failed: {e}")
            raise
    
    def _save_kdd_models(self):
        """Save KDD-trained models"""
        try:
            models_dir = "models/kdd_models"
            os.makedirs(models_dir, exist_ok=True)
            
            # Save individual models
            joblib.dump(self.kdd_models['isolation_forest'], 
                       f"{models_dir}/kdd_isolation_forest.pkl")
            joblib.dump(self.kdd_models['random_forest'], 
                       f"{models_dir}/kdd_random_forest.pkl")
            joblib.dump(self.kdd_models['scaler'], 
                       f"{models_dir}/kdd_scaler.pkl")
            
            # Save metadata
            metadata = {
                'label_encoders': self.kdd_models['label_encoders'],
                'feature_names': self.kdd_models['feature_names'],
                'training_timestamp': self.kdd_models['training_timestamp'],
                'evaluation_results': self.kdd_models['evaluation_results']
            }
            
            with open(f"{models_dir}/kdd_metadata.json", 'w') as f:
                json.dump(metadata, f, indent=2, default=str)
            
            logging.info(f"KDD models saved to {models_dir}")
            
        except Exception as e:
            logging.error(f"Failed to save KDD models: {e}")
            raise
    
    def _update_order_engine(self):
        """Update ORDER engine with KDD-trained models"""
        try:
            logging.info("Updating ORDER engine with KDD models...")
            
            # Update ORDER engine's models
            self.order_engine.isolation_forest = self.kdd_models['isolation_forest']
            self.order_engine.random_forest = self.kdd_models['random_forest']
            self.order_engine.scaler = self.kdd_models['scaler']
            
            # Update feature names
            self.order_engine.feature_names = self.kdd_models['feature_names']
            
            # Update performance metrics
            self.order_engine.performance_metrics.update({
                'kdd_trained': True,
                'kdd_training_timestamp': self.kdd_models['training_timestamp'],
                'kdd_isolation_auc': self.kdd_models['evaluation_results']['isolation_forest']['auc_score'],
                'kdd_rf_accuracy': self.kdd_models['evaluation_results']['random_forest']['accuracy']
            })
            
            logging.info("ORDER engine updated with KDD models")
            
        except Exception as e:
            logging.error(f"Failed to update ORDER engine: {e}")
            raise
    
    def load_kdd_models(self, models_dir: str = "models/kdd_models"):
        """Load previously trained KDD models"""
        try:
            logging.info(f"Loading KDD models from {models_dir}")
            
            # Load individual models
            isolation_forest = joblib.load(f"{models_dir}/kdd_isolation_forest.pkl")
            random_forest = joblib.load(f"{models_dir}/kdd_random_forest.pkl")
            scaler = joblib.load(f"{models_dir}/kdd_scaler.pkl")
            
            # Load metadata
            with open(f"{models_dir}/kdd_metadata.json", 'r') as f:
                metadata = json.load(f)
            
            # Store models
            self.kdd_models = {
                'isolation_forest': isolation_forest,
                'random_forest': random_forest,
                'scaler': scaler,
                'label_encoders': metadata['label_encoders'],
                'feature_names': metadata['feature_names'],
                'training_timestamp': metadata['training_timestamp'],
                'evaluation_results': metadata['evaluation_results']
            }
            
            # Update ORDER engine
            self._update_order_engine()
            
            logging.info("KDD models loaded successfully")
            
        except Exception as e:
            logging.error(f"Failed to load KDD models: {e}")
            raise
    
    def generate_kdd_network_flows(self, n_samples: int = 1000) -> List[NetworkFlow]:
        """Generate network flows from KDD data for ORDER engine testing"""
        try:
            flows_data = self.kdd_loader.generate_network_flows(n_samples)
            network_flows = []
            
            for flow_data in flows_data:
                flow = NetworkFlow(
                    src_ip=flow_data['src_ip'],
                    dst_ip=flow_data['dst_ip'],
                    src_port=flow_data['src_port'],
                    dst_port=flow_data['dst_port'],
                    protocol=flow_data['protocol'],
                    packet_count=flow_data['packet_count'],
                    byte_count=flow_data['byte_count'],
                    duration=flow_data['duration'],
                    timestamp=flow_data['timestamp'],
                    flags=flow_data['flags']
                )
                
                # Add KDD-specific attributes
                flow.attack_type = flow_data['attack_type']
                flow.attack_category = flow_data['attack_category']
                flow.is_anomaly = flow_data['is_anomaly']
                
                network_flows.append(flow)
            
            logging.info(f"Generated {len(network_flows)} KDD-based network flows")
            return network_flows
            
        except Exception as e:
            logging.error(f"Failed to generate KDD network flows: {e}")
            raise
    
    def test_order_engine_with_kdd(self, n_samples: int = 1000) -> Dict[str, Any]:
        """Test ORDER engine with KDD-generated flows"""
        try:
            logging.info("Testing ORDER engine with KDD data...")
            
            # Generate KDD flows
            flows = self.generate_kdd_network_flows(n_samples)
            
            # Process flows through ORDER engine
            results = {
                'total_flows': len(flows),
                'anomalies_detected': 0,
                'true_positives': 0,
                'false_positives': 0,
                'true_negatives': 0,
                'false_negatives': 0,
                'attack_classifications': {},
                'processing_time': 0
            }
            
            start_time = datetime.now()
            
            for flow in flows:
                # Process flow through ORDER engine
                detection_result = self.order_engine.process_flow(flow)
                
                if detection_result['is_anomaly']:
                    results['anomalies_detected'] += 1
                    
                    if flow.is_anomaly:
                        results['true_positives'] += 1
                    else:
                        results['false_positives'] += 1
                else:
                    if not flow.is_anomaly:
                        results['true_negatives'] += 1
                    else:
                        results['false_negatives'] += 1
                
                # Track attack classifications
                if hasattr(flow, 'attack_type'):
                    attack_type = flow.attack_type
                    if attack_type not in results['attack_classifications']:
                        results['attack_classifications'][attack_type] = 0
                    results['attack_classifications'][attack_type] += 1
            
            results['processing_time'] = (datetime.now() - start_time).total_seconds()
            
            # Calculate metrics
            total_anomalies = results['true_positives'] + results['false_negatives']
            total_normal = results['true_negatives'] + results['false_positives']
            
            if total_anomalies > 0:
                results['precision'] = results['true_positives'] / (results['true_positives'] + results['false_positives'])
                results['recall'] = results['true_positives'] / total_anomalies
                results['f1_score'] = 2 * (results['precision'] * results['recall']) / (results['precision'] + results['recall'])
            else:
                results['precision'] = 0
                results['recall'] = 0
                results['f1_score'] = 0
            
            logging.info(f"ORDER engine KDD test completed: {results['anomalies_detected']} anomalies detected")
            logging.info(f"Precision: {results['precision']:.4f}, Recall: {results['recall']:.4f}, F1: {results['f1_score']:.4f}")
            
            return results
            
        except Exception as e:
            logging.error(f"ORDER engine KDD test failed: {e}")
            return {'error': str(e)}
    
    def get_kdd_training_status(self) -> Dict[str, Any]:
        """Get KDD training status and metrics"""
        if not self.kdd_models:
            return {'status': 'not_trained', 'message': 'No KDD models trained'}
        
        return {
            'status': 'trained',
            'training_timestamp': self.kdd_models.get('training_timestamp'),
            'models_available': list(self.kdd_models.keys()),
            'evaluation_results': self.kdd_models.get('evaluation_results', {}),
            'feature_count': len(self.kdd_models.get('feature_names', [])),
            'order_engine_updated': hasattr(self.order_engine, 'kdd_trained') and self.order_engine.performance_metrics.get('kdd_trained', False)
        }

def main():
    """Example usage of KDD-ORDER integration"""
    try:
        # Initialize components
        from order_engine import OrderEngine
        
        order_engine = OrderEngine({})
        kdd_loader = KDDDataLoader()
        kdd_integration = KDDOrderIntegration(order_engine, kdd_loader)
        
        # Train with KDD data
        training_results = kdd_integration.train_with_kdd_data(max_samples=10000)
        print("Training Results:", json.dumps(training_results, indent=2))
        
        # Test ORDER engine
        test_results = kdd_integration.test_order_engine_with_kdd(1000)
        print("Test Results:", json.dumps(test_results, indent=2))
        
        # Get status
        status = kdd_integration.get_kdd_training_status()
        print("Status:", json.dumps(status, indent=2))
        
    except Exception as e:
        logging.error(f"KDD-ORDER integration example failed: {e}")

if __name__ == "__main__":
    main()
