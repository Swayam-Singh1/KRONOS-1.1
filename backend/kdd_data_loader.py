"""
KDD Cup 99 Dataset Integration for Self-Morphing AI Cybersecurity Engine
Professional cybersecurity platform with real-world dataset integration
"""

import pandas as pd
import numpy as np
import gzip
import os
import logging
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
from enum import Enum
import pickle
import json
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - KDD_LOADER - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('kdd_data_loader.log'),
        logging.StreamHandler()
    ]
)

class AttackCategory(Enum):
    """KDD Cup 99 attack categories"""
    NORMAL = "normal"
    DOS = "dos"  # Denial of Service
    PROBE = "probe"  # Surveillance and probing
    R2L = "r2l"  # Remote to Local
    U2R = "u2r"  # User to Root

class KDDDataLoader:
    """KDD Cup 99 dataset loader and preprocessor"""
    
    def __init__(self, dataset_path: str = "datset/KDD cup 99"):
        self.dataset_path = dataset_path
        self.feature_names = self._get_feature_names()
        self.attack_categories = self._get_attack_categories()
        self.label_encoders = {}
        self.scaler = StandardScaler()
        
        # Data storage
        self.raw_data = None
        self.processed_data = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        
        logging.info("KDD Cup 99 Data Loader initialized")
    
    def _get_feature_names(self) -> List[str]:
        """Get feature names from kddcup.names file"""
        feature_names = [
            'duration', 'protocol_type', 'service', 'flag', 'src_bytes',
            'dst_bytes', 'land', 'wrong_fragment', 'urgent', 'hot',
            'num_failed_logins', 'logged_in', 'num_compromised', 'root_shell',
            'su_attempted', 'num_root', 'num_file_creations', 'num_shells',
            'num_access_files', 'num_outbound_cmds', 'is_host_login',
            'is_guest_login', 'count', 'srv_count', 'serror_rate',
            'srv_serror_rate', 'rerror_rate', 'srv_rerror_rate',
            'same_srv_rate', 'diff_srv_rate', 'srv_diff_host_rate',
            'dst_host_count', 'dst_host_srv_count', 'dst_host_same_srv_rate',
            'dst_host_diff_srv_rate', 'dst_host_same_src_port_rate',
            'dst_host_srv_diff_host_rate', 'dst_host_serror_rate',
            'dst_host_srv_serror_rate', 'dst_host_rerror_rate',
            'dst_host_srv_rerror_rate'
        ]
        return feature_names
    
    def _get_attack_categories(self) -> Dict[str, str]:
        """Get attack type to category mapping"""
        return {
            'back': 'dos', 'buffer_overflow': 'u2r', 'ftp_write': 'r2l',
            'guess_passwd': 'r2l', 'imap': 'r2l', 'ipsweep': 'probe',
            'land': 'dos', 'loadmodule': 'u2r', 'multihop': 'r2l',
            'neptune': 'dos', 'nmap': 'probe', 'perl': 'u2r',
            'phf': 'r2l', 'pod': 'dos', 'portsweep': 'probe',
            'rootkit': 'u2r', 'satan': 'probe', 'smurf': 'dos',
            'spy': 'r2l', 'teardrop': 'dos', 'warezclient': 'r2l',
            'warezmaster': 'r2l', 'normal': 'normal'
        }
    
    def load_data(self, file_name: str = "kddcup.data_10_percent", 
                  max_rows: Optional[int] = None) -> pd.DataFrame:
        """Load KDD Cup 99 dataset"""
        try:
            file_path = os.path.join(self.dataset_path, file_name)
            
            # Handle compressed files
            if file_name.endswith('.gz'):
                with gzip.open(file_path, 'rt') as f:
                    data = pd.read_csv(f, header=None, nrows=max_rows)
            else:
                data = pd.read_csv(file_path, header=None, nrows=max_rows)
            
            # Add column names
            data.columns = self.feature_names + ['attack_type']
            
            # Add attack category
            data['attack_category'] = data['attack_type'].map(self.attack_categories)
            
            self.raw_data = data
            logging.info(f"Loaded {len(data)} records from {file_name}")
            logging.info(f"Attack distribution:\n{data['attack_category'].value_counts()}")
            
            return data
            
        except Exception as e:
            logging.error(f"Failed to load data: {e}")
            raise
    
    def preprocess_data(self, data: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray]:
        """Preprocess the KDD Cup 99 data for machine learning"""
        try:
            logging.info("Starting data preprocessing...")
            
            # Separate features and target
            X = data.drop(['attack_type', 'attack_category'], axis=1)
            y = data['attack_category']
            
            # Handle categorical variables
            categorical_features = ['protocol_type', 'service', 'flag', 'land', 
                                 'logged_in', 'is_host_login', 'is_guest_login']
            
            for feature in categorical_features:
                if feature in X.columns:
                    le = LabelEncoder()
                    X[feature] = le.fit_transform(X[feature].astype(str))
                    self.label_encoders[feature] = le
            
            # Encode target variable
            le_target = LabelEncoder()
            y_encoded = le_target.fit_transform(y)
            self.label_encoders['target'] = le_target
            
            # Scale features
            X_scaled = self.scaler.fit_transform(X)
            
            self.processed_data = X_scaled
            logging.info(f"Data preprocessed: {X_scaled.shape[0]} samples, {X_scaled.shape[1]} features")
            
            return X_scaled, y_encoded
            
        except Exception as e:
            logging.error(f"Data preprocessing failed: {e}")
            raise
    
    def split_data(self, X: np.ndarray, y: np.ndarray, 
                   test_size: float = 0.2, random_state: int = 42) -> Tuple:
        """Split data into train and test sets"""
        try:
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=test_size, random_state=random_state, stratify=y
            )
            
            self.X_train = X_train
            self.X_test = X_test
            self.y_train = y_train
            self.y_test = y_test
            
            logging.info(f"Data split: Train {X_train.shape[0]} samples, Test {X_test.shape[0]} samples")
            
            return X_train, X_test, y_train, y_test
            
        except Exception as e:
            logging.error(f"Data splitting failed: {e}")
            raise
    
    def get_attack_samples(self, attack_type: str, n_samples: int = 1000) -> pd.DataFrame:
        """Get specific attack type samples"""
        if self.raw_data is None:
            raise ValueError("No data loaded. Call load_data() first.")
        
        attack_data = self.raw_data[self.raw_data['attack_type'] == attack_type]
        
        if len(attack_data) < n_samples:
            logging.warning(f"Only {len(attack_data)} samples available for {attack_type}")
            return attack_data
        else:
            return attack_data.sample(n=n_samples, random_state=42)
    
    def get_category_samples(self, category: str, n_samples: int = 1000) -> pd.DataFrame:
        """Get specific attack category samples"""
        if self.raw_data is None:
            raise ValueError("No data loaded. Call load_data() first.")
        
        category_data = self.raw_data[self.raw_data['attack_category'] == category]
        
        if len(category_data) < n_samples:
            logging.warning(f"Only {len(category_data)} samples available for {category}")
            return category_data
        else:
            return category_data.sample(n=n_samples, random_state=42)
    
    def generate_network_flows(self, n_samples: int = 1000) -> List[Dict[str, Any]]:
        """Convert KDD data to network flow format for ORDER engine"""
        if self.raw_data is None:
            raise ValueError("No data loaded. Call load_data() first.")
        
        flows = []
        sample_data = self.raw_data.sample(n=min(n_samples, len(self.raw_data)), random_state=42)
        
        for _, row in sample_data.iterrows():
            flow = {
                'src_ip': f"192.168.{np.random.randint(1, 255)}.{np.random.randint(1, 255)}",
                'dst_ip': f"10.0.{np.random.randint(1, 255)}.{np.random.randint(1, 255)}",
                'src_port': np.random.randint(1024, 65535),
                'dst_port': self._get_service_port(row['service']),
                'protocol': row['protocol_type'].upper(),
                'packet_count': int(row['count']),
                'byte_count': int(row['src_bytes'] + row['dst_bytes']),
                'duration': float(row['duration']),
                'timestamp': np.random.uniform(0, 86400),  # Random time in day
                'flags': self._get_flags_from_flag(row['flag']),
                'attack_type': row['attack_type'],
                'attack_category': row['attack_category'],
                'is_anomaly': row['attack_category'] != 'normal'
            }
            flows.append(flow)
        
        logging.info(f"Generated {len(flows)} network flows from KDD data")
        return flows
    
    def _get_service_port(self, service: str) -> int:
        """Map service to port number"""
        service_ports = {
            'http': 80, 'https': 443, 'ftp': 21, 'ssh': 22, 'telnet': 23,
            'smtp': 25, 'dns': 53, 'pop3': 110, 'imap': 143, 'snmp': 161,
            'ldap': 389, 'https': 443, 'smtp': 587, 'imaps': 993, 'pop3s': 995
        }
        return service_ports.get(service.lower(), np.random.randint(1024, 65535))
    
    def _get_flags_from_flag(self, flag: str) -> str:
        """Convert KDD flag to network flags"""
        flag_mapping = {
            'SF': 'SYN,FIN', 'S0': 'SYN', 'S1': 'SYN,ACK', 'S2': 'SYN,ACK',
            'S3': 'ACK', 'RSTO': 'RST', 'RSTR': 'RST', 'RSTOS0': 'RST,SYN',
            'RSTRH': 'RST', 'SH': 'SYN,FIN', 'SHR': 'SYN,FIN,ACK'
        }
        return flag_mapping.get(flag, '')
    
    def save_processed_data(self, file_path: str):
        """Save processed data and encoders"""
        try:
            data_dict = {
                'X_train': self.X_train,
                'X_test': self.X_test,
                'y_train': self.y_train,
                'y_test': self.y_test,
                'label_encoders': self.label_encoders,
                'scaler': self.scaler,
                'feature_names': self.feature_names
            }
            
            with open(file_path, 'wb') as f:
                pickle.dump(data_dict, f)
            
            logging.info(f"Processed data saved to {file_path}")
            
        except Exception as e:
            logging.error(f"Failed to save processed data: {e}")
            raise
    
    def load_processed_data(self, file_path: str):
        """Load previously processed data"""
        try:
            with open(file_path, 'rb') as f:
                data_dict = pickle.load(f)
            
            self.X_train = data_dict['X_train']
            self.X_test = data_dict['X_test']
            self.y_train = data_dict['y_train']
            self.y_test = data_dict['y_test']
            self.label_encoders = data_dict['label_encoders']
            self.scaler = data_dict['scaler']
            self.feature_names = data_dict['feature_names']
            
            logging.info(f"Processed data loaded from {file_path}")
            
        except Exception as e:
            logging.error(f"Failed to load processed data: {e}")
            raise
    
    def get_data_statistics(self) -> Dict[str, Any]:
        """Get comprehensive data statistics"""
        if self.raw_data is None:
            return {"error": "No data loaded"}
        
        stats = {
            'total_samples': len(self.raw_data),
            'feature_count': len(self.feature_names),
            'attack_types': self.raw_data['attack_type'].value_counts().to_dict(),
            'attack_categories': self.raw_data['attack_category'].value_counts().to_dict(),
            'normal_percentage': (self.raw_data['attack_category'] == 'normal').mean() * 100,
            'anomaly_percentage': (self.raw_data['attack_category'] != 'normal').mean() * 100
        }
        
        return stats
    
    def visualize_attack_distribution(self, save_path: str = None):
        """Create visualization of attack distribution"""
        if self.raw_data is None:
            logging.error("No data loaded for visualization")
            return
        
        try:
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
            
            # Attack type distribution
            attack_counts = self.raw_data['attack_type'].value_counts()
            attack_counts.plot(kind='bar', ax=ax1)
            ax1.set_title('Attack Type Distribution')
            ax1.set_xlabel('Attack Type')
            ax1.set_ylabel('Count')
            ax1.tick_params(axis='x', rotation=45)
            
            # Attack category distribution
            category_counts = self.raw_data['attack_category'].value_counts()
            category_counts.plot(kind='pie', ax=ax2, autopct='%1.1f%%')
            ax2.set_title('Attack Category Distribution')
            
            plt.tight_layout()
            
            if save_path:
                plt.savefig(save_path, dpi=300, bbox_inches='tight')
                logging.info(f"Visualization saved to {save_path}")
            else:
                plt.show()
                
        except Exception as e:
            logging.error(f"Visualization failed: {e}")

def main():
    """Example usage of KDD Data Loader"""
    try:
        # Initialize loader
        loader = KDDDataLoader()
        
        # Load data
        data = loader.load_data("kddcup.data_10_percent", max_rows=10000)
        
        # Preprocess data
        X, y = loader.preprocess_data(data)
        
        # Split data
        X_train, X_test, y_train, y_test = loader.split_data(X, y)
        
        # Get statistics
        stats = loader.get_data_statistics()
        print("Data Statistics:")
        print(json.dumps(stats, indent=2))
        
        # Generate network flows
        flows = loader.generate_network_flows(100)
        print(f"\nGenerated {len(flows)} network flows")
        
        # Save processed data
        loader.save_processed_data("models/kdd_processed_data.pkl")
        
        logging.info("KDD data processing completed successfully")
        
    except Exception as e:
        logging.error(f"KDD data processing failed: {e}")

if __name__ == "__main__":
    main()
