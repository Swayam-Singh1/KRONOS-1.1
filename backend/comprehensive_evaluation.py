"""
Comprehensive Evaluation Script for KRONOS Research Paper
Generates all required metrics, baselines, visualizations, and reports
"""

import numpy as np
import pandas as pd
import time
import json
import os
import platform
import psutil
import sys
from datetime import datetime
from typing import Dict, List, Tuple, Any
import warnings
warnings.filterwarnings('ignore')

# Fix Windows encoding issues
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# ML Libraries
from sklearn.ensemble import IsolationForest, RandomForestClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report, roc_auc_score,
    roc_curve, precision_recall_curve
)

# Visualization
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns

# Import KDD loader
import sys
sys.path.append('backend')
from kdd_data_loader import KDDDataLoader

class ComprehensiveEvaluator:
    """Comprehensive evaluation system for KRONOS research paper"""
    
    def __init__(self, dataset_path: str = None, max_samples: int = 50000):
        # Fix path - if running from backend directory, go up one level
        if dataset_path is None:
            if os.path.exists("../datset/KDD cup 99"):
                dataset_path = "../datset/KDD cup 99"
            elif os.path.exists("datset/KDD cup 99"):
                dataset_path = "datset/KDD cup 99"
            else:
                dataset_path = "datset/KDD cup 99"
        self.dataset_path = dataset_path
        self.max_samples = max_samples
        self.kdd_loader = KDDDataLoader(dataset_path)
        
        # Results storage
        self.results = {
            'hardware_info': {},
            'dataset_info': {},
            'baseline_results': {},
            'runtime_metrics': {},
            'confusion_matrices': {},
            'per_class_metrics': {},
            'visualizations': {}
        }
        
        # Models
        self.models = {}
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.y_train_binary = None
        self.y_test_binary = None
        self.label_names = None
        
    def collect_hardware_info(self):
        """Collect hardware and environment information"""
        print("[*] Collecting hardware information...")
        
        self.results['hardware_info'] = {
            'cpu_model': platform.processor(),
            'cpu_count': psutil.cpu_count(logical=True),
            'cpu_count_physical': psutil.cpu_count(logical=False),
            'ram_gb': round(psutil.virtual_memory().total / (1024**3), 2),
            'ram_available_gb': round(psutil.virtual_memory().available / (1024**3), 2),
            'os': platform.system(),
            'os_version': platform.version(),
            'python_version': platform.python_version(),
            'gpu_available': False,  # Set to True if GPU available
            'timestamp': datetime.now().isoformat()
        }
        
        print(f"[+] CPU: {self.results['hardware_info']['cpu_model']}")
        print(f"[+] RAM: {self.results['hardware_info']['ram_gb']} GB")
        print(f"[+] OS: {self.results['hardware_info']['os']}")
        
    def load_and_preprocess_data(self):
        """Load and preprocess KDD dataset"""
        print("\n[*] Loading and preprocessing KDD Cup 99 dataset...")
        
        # Load data - try different possible paths
        data_file = None
        possible_files = [
            "kddcup.data_10_percent/kddcup.data_10_percent",
            "kddcup.data_10_percent",
            "kddcup.data_10_percent.gz"
        ]
        
        for file_name in possible_files:
            file_path = os.path.join(self.dataset_path, file_name)
            if os.path.exists(file_path):
                data_file = file_name
                print(f"[+] Found dataset file: {file_path}")
                break
        
        if data_file is None:
            # Try to find any kddcup file
            import glob
            search_pattern = os.path.join(self.dataset_path, "**/kddcup.data*")
            found_files = glob.glob(search_pattern, recursive=True)
            if found_files:
                # Use the first found file that's not compressed
                for f in found_files:
                    if not f.endswith('.gz') and os.path.isfile(f):
                        # Get relative path
                        rel_path = os.path.relpath(f, self.dataset_path)
                        data_file = rel_path.replace('\\', '/')
                        print(f"[+] Using dataset file: {f}")
                        break
        
        if data_file is None:
            raise FileNotFoundError(f"Could not find KDD dataset file in {self.dataset_path}")
        
        data = self.kdd_loader.load_data(data_file, max_rows=self.max_samples)
        
        # Fix attack_type values - remove trailing periods
        if 'attack_type' in data.columns:
            data['attack_type'] = data['attack_type'].str.rstrip('.')
            # Recreate attack_category with cleaned values
            data['attack_category'] = data['attack_type'].map(self.kdd_loader.attack_categories)
            # Fill NaN with 'unknown' or use attack_type directly
            data['attack_category'] = data['attack_category'].fillna(data['attack_type'])
            # Update loader's raw_data
            self.kdd_loader.raw_data = data
        
        # Debug: Check attack categories
        if 'attack_category' in data.columns:
            print(f"[+] Attack category distribution:")
            print(data['attack_category'].value_counts())
        else:
            print("[!] Warning: attack_category column not found")
        
        # Preprocess
        X, y = self.kdd_loader.preprocess_data(data)
        
        # Debug: Check unique labels
        unique_labels = np.unique(y)
        print(f"[+] Unique labels after encoding: {unique_labels}")
        print(f"[+] Number of unique classes: {len(unique_labels)}")
        
        if len(unique_labels) < 2:
            print("[!] Warning: Only one class found. Checking raw data...")
            if 'attack_category' in data.columns:
                print(f"[+] Raw attack_category values: {data['attack_category'].unique()}")
            if 'attack_type' in data.columns:
                print(f"[+] Raw attack_type values: {data['attack_type'].unique()[:10]}")  # First 10
        
        # Split data
        self.X_train, self.X_test, self.y_train, self.y_test = self.kdd_loader.split_data(
            X, y, test_size=0.2, random_state=42
        )
        
        # Create binary labels for anomaly detection (0 = normal, 1 = attack)
        self.y_train_binary = (self.y_train != 0).astype(int)
        self.y_test_binary = (self.y_test != 0).astype(int)
        
        # Get label names
        le_target = self.kdd_loader.label_encoders['target']
        self.label_names = le_target.classes_
        
        # Dataset info
        self.results['dataset_info'] = {
            'total_samples': len(data),
            'train_samples': len(self.X_train),
            'test_samples': len(self.X_test),
            'features': X.shape[1],
            'classes': len(np.unique(y)),
            'class_distribution': {
                name: int(count) for name, count in zip(
                    self.label_names, 
                    np.bincount(self.y_test)
                )
            },
            'attack_percentage': (self.y_test_binary == 1).mean() * 100,
            'normal_percentage': (self.y_test_binary == 0).mean() * 100
        }
        
        print(f"[+] Loaded {len(data)} samples")
        print(f"[+] Train: {len(self.X_train)}, Test: {len(self.X_test)}")
        print(f"[+] Features: {X.shape[1]}, Classes: {len(np.unique(y))}")
        
    def train_baseline_models(self):
        """Train all baseline models"""
        print("\n[*] Training baseline models...")
        
        # 1. Isolation Forest (Anomaly Detection)
        print("  Training Isolation Forest...")
        start_time = time.time()
        iso_forest = IsolationForest(
            contamination=0.1,
            random_state=42,
            n_estimators=100,
            max_samples='auto',
            max_features=1.0
        )
        iso_forest.fit(self.X_train)
        iso_train_time = time.time() - start_time
        
        # Evaluate Isolation Forest
        iso_predictions = iso_forest.predict(self.X_test)
        iso_scores = iso_forest.decision_function(self.X_test)
        iso_binary = (iso_predictions == 1).astype(int)  # Convert: 1=normal, -1=anomaly -> 0=normal, 1=anomaly
        iso_binary = 1 - iso_binary  # Flip: IsolationForest returns 1 for normal, we want 1 for anomaly
        
        iso_accuracy = accuracy_score(self.y_test_binary, iso_binary)
        iso_precision = precision_score(self.y_test_binary, iso_binary, zero_division=0)
        iso_recall = recall_score(self.y_test_binary, iso_binary, zero_division=0)
        iso_f1 = f1_score(self.y_test_binary, iso_binary, zero_division=0)
        iso_auc = roc_auc_score(self.y_test_binary, iso_scores)
        iso_cm = confusion_matrix(self.y_test_binary, iso_binary)
        
        # Inference time
        start_time = time.time()
        _ = iso_forest.predict(self.X_test[:1000])
        iso_inference_time = max((time.time() - start_time) / 1000, 0.0001)  # per sample, min 0.0001s
        
        self.models['IsolationForest'] = iso_forest
        self.results['baseline_results']['IsolationForest'] = {
            'accuracy': round(iso_accuracy * 100, 2),
            'precision': round(iso_precision, 4),
            'recall': round(iso_recall, 4),
            'f1_score': round(iso_f1, 4),
            'roc_auc': round(iso_auc, 4),
            'training_time_seconds': round(iso_train_time, 2),
            'inference_time_ms': round(iso_inference_time * 1000, 3),
            'throughput_samples_per_sec': round(1.0 / iso_inference_time, 0) if iso_inference_time > 0 else 0
        }
        self.results['confusion_matrices']['IsolationForest'] = iso_cm.tolist()
        
        print(f"    [+] Accuracy: {iso_accuracy*100:.2f}%, F1: {iso_f1:.4f}, AUC: {iso_auc:.4f}")
        
        # 2. Random Forest (Classification)
        print("  Training Random Forest...")
        start_time = time.time()
        rf = RandomForestClassifier(
            n_estimators=100,
            random_state=42,
            max_depth=20,
            min_samples_split=5,
            min_samples_leaf=2,
            n_jobs=-1
        )
        rf.fit(self.X_train, self.y_train)
        rf_train_time = time.time() - start_time
        
        # Evaluate Random Forest
        rf_predictions = rf.predict(self.X_test)
        rf_proba = rf.predict_proba(self.X_test)
        
        rf_accuracy = accuracy_score(self.y_test, rf_predictions)
        rf_precision = precision_score(self.y_test, rf_predictions, average='weighted', zero_division=0)
        rf_recall = recall_score(self.y_test, rf_predictions, average='weighted', zero_division=0)
        rf_f1 = f1_score(self.y_test, rf_predictions, average='weighted', zero_division=0)
        rf_cm = confusion_matrix(self.y_test, rf_predictions)
        
        # Cross-validation
        cv_scores = cross_val_score(rf, self.X_test, self.y_test, cv=5, scoring='accuracy')
        
        # Per-class metrics
        rf_report = classification_report(self.y_test, rf_predictions, 
                                         target_names=self.label_names, 
                                         output_dict=True, zero_division=0)
        
        # Inference time
        start_time = time.time()
        _ = rf.predict(self.X_test[:1000])
        rf_inference_time = max((time.time() - start_time) / 1000, 0.0001)
        
        self.models['RandomForest'] = rf
        self.results['baseline_results']['RandomForest'] = {
            'accuracy': round(rf_accuracy * 100, 2),
            'precision': round(rf_precision, 4),
            'recall': round(rf_recall, 4),
            'f1_score': round(rf_f1, 4),
            'cv_mean': round(cv_scores.mean(), 4),
            'cv_std': round(cv_scores.std(), 4),
            'training_time_seconds': round(rf_train_time, 2),
            'inference_time_ms': round(rf_inference_time * 1000, 3),
            'throughput_samples_per_sec': round(1.0 / rf_inference_time, 0) if rf_inference_time > 0 else 0
        }
        self.results['confusion_matrices']['RandomForest'] = rf_cm.tolist()
        self.results['per_class_metrics']['RandomForest'] = rf_report
        
        print(f"    [+] Accuracy: {rf_accuracy*100:.2f}%, F1: {rf_f1:.4f}, CV: {cv_scores.mean():.4f}+/-{cv_scores.std():.4f}")
        
        # 3. SVM (RBF Kernel)
        print("  Training SVM (RBF)...")
        start_time = time.time()
        svm = SVC(
            kernel='rbf',
            C=1.0,
            gamma='scale',
            random_state=42,
            probability=True
        )
        svm.fit(self.X_train, self.y_train)
        svm_train_time = time.time() - start_time
        
        # Evaluate SVM
        svm_predictions = svm.predict(self.X_test)
        svm_proba = svm.predict_proba(self.X_test)
        
        svm_accuracy = accuracy_score(self.y_test, svm_predictions)
        svm_precision = precision_score(self.y_test, svm_predictions, average='weighted', zero_division=0)
        svm_recall = recall_score(self.y_test, svm_predictions, average='weighted', zero_division=0)
        svm_f1 = f1_score(self.y_test, svm_predictions, average='weighted', zero_division=0)
        svm_cm = confusion_matrix(self.y_test, svm_predictions)
        
        # Cross-validation
        cv_scores_svm = cross_val_score(svm, self.X_test, self.y_test, cv=5, scoring='accuracy')
        
        # Per-class metrics
        svm_report = classification_report(self.y_test, svm_predictions,
                                         target_names=self.label_names,
                                         output_dict=True, zero_division=0)
        
        # Inference time
        start_time = time.time()
        _ = svm.predict(self.X_test[:1000])
        svm_inference_time = max((time.time() - start_time) / 1000, 0.0001)
        
        self.models['SVM'] = svm
        self.results['baseline_results']['SVM'] = {
            'accuracy': round(svm_accuracy * 100, 2),
            'precision': round(svm_precision, 4),
            'recall': round(svm_recall, 4),
            'f1_score': round(svm_f1, 4),
            'cv_mean': round(cv_scores_svm.mean(), 4),
            'cv_std': round(cv_scores_svm.std(), 4),
            'training_time_seconds': round(svm_train_time, 2),
            'inference_time_ms': round(svm_inference_time * 1000, 3),
            'throughput_samples_per_sec': round(1.0 / svm_inference_time, 0) if svm_inference_time > 0 else 0
        }
        self.results['confusion_matrices']['SVM'] = svm_cm.tolist()
        self.results['per_class_metrics']['SVM'] = svm_report
        
        print(f"    [+] Accuracy: {svm_accuracy*100:.2f}%, F1: {svm_f1:.4f}, CV: {cv_scores_svm.mean():.4f}+/-{cv_scores_svm.std():.4f}")
        
        # 4. Logistic Regression
        print("  Training Logistic Regression...")
        start_time = time.time()
        lr = LogisticRegression(
            max_iter=1000,
            random_state=42,
            n_jobs=-1,
            multi_class='multinomial'
        )
        lr.fit(self.X_train, self.y_train)
        lr_train_time = time.time() - start_time
        
        # Evaluate Logistic Regression
        lr_predictions = lr.predict(self.X_test)
        lr_proba = lr.predict_proba(self.X_test)
        
        lr_accuracy = accuracy_score(self.y_test, lr_predictions)
        lr_precision = precision_score(self.y_test, lr_predictions, average='weighted', zero_division=0)
        lr_recall = recall_score(self.y_test, lr_predictions, average='weighted', zero_division=0)
        lr_f1 = f1_score(self.y_test, lr_predictions, average='weighted', zero_division=0)
        lr_cm = confusion_matrix(self.y_test, lr_predictions)
        
        # Cross-validation
        cv_scores_lr = cross_val_score(lr, self.X_test, self.y_test, cv=5, scoring='accuracy')
        
        # Per-class metrics
        lr_report = classification_report(self.y_test, lr_predictions,
                                         target_names=self.label_names,
                                         output_dict=True, zero_division=0)
        
        # Inference time
        start_time = time.time()
        _ = lr.predict(self.X_test[:1000])
        lr_inference_time = max((time.time() - start_time) / 1000, 0.0001)
        
        self.models['LogisticRegression'] = lr
        self.results['baseline_results']['LogisticRegression'] = {
            'accuracy': round(lr_accuracy * 100, 2),
            'precision': round(lr_precision, 4),
            'recall': round(lr_recall, 4),
            'f1_score': round(lr_f1, 4),
            'cv_mean': round(cv_scores_lr.mean(), 4),
            'cv_std': round(cv_scores_lr.std(), 4),
            'training_time_seconds': round(lr_train_time, 2),
            'inference_time_ms': round(lr_inference_time * 1000, 3),
            'throughput_samples_per_sec': round(1.0 / lr_inference_time, 0) if lr_inference_time > 0 else 0
        }
        self.results['confusion_matrices']['LogisticRegression'] = lr_cm.tolist()
        self.results['per_class_metrics']['LogisticRegression'] = lr_report
        
        print(f"    [+] Accuracy: {lr_accuracy*100:.2f}%, F1: {lr_f1:.4f}, CV: {cv_scores_lr.mean():.4f}+/-{cv_scores_lr.std():.4f}")
        
        # 5. Naive Bayes (Optional)
        print("  Training Naive Bayes...")
        start_time = time.time()
        nb = GaussianNB()
        nb.fit(self.X_train, self.y_train)
        nb_train_time = time.time() - start_time
        
        # Evaluate Naive Bayes
        nb_predictions = nb.predict(self.X_test)
        
        nb_accuracy = accuracy_score(self.y_test, nb_predictions)
        nb_precision = precision_score(self.y_test, nb_predictions, average='weighted', zero_division=0)
        nb_recall = recall_score(self.y_test, nb_predictions, average='weighted', zero_division=0)
        nb_f1 = f1_score(self.y_test, nb_predictions, average='weighted', zero_division=0)
        nb_cm = confusion_matrix(self.y_test, nb_predictions)
        
        # Cross-validation
        cv_scores_nb = cross_val_score(nb, self.X_test, self.y_test, cv=5, scoring='accuracy')
        
        # Per-class metrics
        nb_report = classification_report(self.y_test, nb_predictions,
                                         target_names=self.label_names,
                                         output_dict=True, zero_division=0)
        
        # Inference time
        start_time = time.time()
        _ = nb.predict(self.X_test[:1000])
        nb_inference_time = max((time.time() - start_time) / 1000, 0.0001)
        
        self.models['NaiveBayes'] = nb
        self.results['baseline_results']['NaiveBayes'] = {
            'accuracy': round(nb_accuracy * 100, 2),
            'precision': round(nb_precision, 4),
            'recall': round(nb_recall, 4),
            'f1_score': round(nb_f1, 4),
            'cv_mean': round(cv_scores_nb.mean(), 4),
            'cv_std': round(cv_scores_nb.std(), 4),
            'training_time_seconds': round(nb_train_time, 2),
            'inference_time_ms': round(nb_inference_time * 1000, 3),
            'throughput_samples_per_sec': round(1.0 / nb_inference_time, 0) if nb_inference_time > 0 else 0
        }
        self.results['confusion_matrices']['NaiveBayes'] = nb_cm.tolist()
        self.results['per_class_metrics']['NaiveBayes'] = nb_report
        
        print(f"    [+] Accuracy: {nb_accuracy*100:.2f}%, F1: {nb_f1:.4f}, CV: {cv_scores_nb.mean():.4f}+/-{cv_scores_nb.std():.4f}")
        
    def generate_visualizations(self):
        """Generate all required visualizations"""
        print("\n[*] Generating visualizations...")
        
        os.makedirs('results/figures', exist_ok=True)
        
        # 1. Confusion Matrix Heatmaps
        print("  Creating confusion matrices...")
        fig, axes = plt.subplots(2, 3, figsize=(18, 12))
        axes = axes.flatten()
        
        models_to_plot = ['RandomForest', 'SVM', 'LogisticRegression', 'NaiveBayes', 'IsolationForest']
        
        for idx, model_name in enumerate(models_to_plot):
            if model_name in self.results['confusion_matrices']:
                cm = np.array(self.results['confusion_matrices'][model_name])
                
                if model_name == 'IsolationForest':
                    # Binary confusion matrix
                    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=axes[idx],
                              xticklabels=['Normal', 'Attack'],
                              yticklabels=['Normal', 'Attack'])
                else:
                    # Multi-class confusion matrix
                    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=axes[idx],
                              xticklabels=self.label_names,
                              yticklabels=self.label_names)
                
                axes[idx].set_title(f'{model_name} Confusion Matrix', fontsize=12, fontweight='bold')
                axes[idx].set_ylabel('True Label')
                axes[idx].set_xlabel('Predicted Label')
        
        # Remove empty subplot
        axes[5].axis('off')
        
        plt.tight_layout()
        plt.savefig('results/figures/confusion_matrices.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("    [+] Confusion matrices saved")
        
        # 2. Baseline Comparison Bar Chart
        print("  Creating baseline comparison chart...")
        models = ['RandomForest', 'SVM', 'LogisticRegression', 'NaiveBayes']
        metrics = ['accuracy', 'precision', 'recall', 'f1_score']
        
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        axes = axes.flatten()
        
        for idx, metric in enumerate(metrics):
            values = []
            labels = []
            for model in models:
                if model in self.results['baseline_results']:
                    if metric == 'accuracy':
                        values.append(self.results['baseline_results'][model][metric] / 100)
                    else:
                        values.append(self.results['baseline_results'][model][metric])
                    labels.append(model)
            
            bars = axes[idx].bar(labels, values, color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728'])
            axes[idx].set_title(f'{metric.replace("_", " ").title()}', fontsize=12, fontweight='bold')
            axes[idx].set_ylabel('Score')
            axes[idx].set_ylim([0, 1])
            axes[idx].grid(axis='y', alpha=0.3)
            
            # Add value labels on bars
            for bar in bars:
                height = bar.get_height()
                axes[idx].text(bar.get_x() + bar.get_width()/2., height,
                             f'{height:.3f}',
                             ha='center', va='bottom', fontsize=9)
        
        plt.tight_layout()
        plt.savefig('results/figures/baseline_comparison.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("    [+] Baseline comparison chart saved")
        
        # 3. ROC Curve (for binary classification models)
        print("  Creating ROC curves...")
        fig, ax = plt.subplots(figsize=(10, 8))
        
        # Isolation Forest ROC
        iso_scores = self.models['IsolationForest'].decision_function(self.X_test)
        iso_fpr, iso_tpr, _ = roc_curve(self.y_test_binary, iso_scores)
        iso_auc = roc_auc_score(self.y_test_binary, iso_scores)
        ax.plot(iso_fpr, iso_tpr, label=f'Isolation Forest (AUC = {iso_auc:.4f})', linewidth=2)
        
        # Random Forest ROC (binary)
        rf_binary_proba = self.models['RandomForest'].predict_proba(self.X_test)[:, 1:]  # Attack class probabilities
        rf_binary_proba = rf_binary_proba.sum(axis=1)  # Sum all attack classes
        rf_fpr, rf_tpr, _ = roc_curve(self.y_test_binary, rf_binary_proba)
        rf_auc = roc_auc_score(self.y_test_binary, rf_binary_proba)
        ax.plot(rf_fpr, rf_tpr, label=f'Random Forest (AUC = {rf_auc:.4f})', linewidth=2)
        
        ax.plot([0, 1], [0, 1], 'k--', label='Random Classifier', linewidth=1)
        ax.set_xlabel('False Positive Rate', fontsize=12)
        ax.set_ylabel('True Positive Rate', fontsize=12)
        ax.set_title('ROC Curves - Anomaly Detection', fontsize=14, fontweight='bold')
        ax.legend(loc='lower right', fontsize=11)
        ax.grid(alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('results/figures/roc_curves.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("    [+] ROC curves saved")
        
        # 4. Runtime Comparison
        print("  Creating runtime comparison...")
        models_runtime = ['RandomForest', 'SVM', 'LogisticRegression', 'NaiveBayes']
        train_times = [self.results['baseline_results'][m]['training_time_seconds'] for m in models_runtime]
        infer_times = [self.results['baseline_results'][m]['inference_time_ms'] for m in models_runtime]
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        
        # Training time
        bars1 = ax1.bar(models_runtime, train_times, color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728'])
        ax1.set_title('Training Time Comparison', fontsize=12, fontweight='bold')
        ax1.set_ylabel('Time (seconds)')
        ax1.grid(axis='y', alpha=0.3)
        for bar in bars1:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.2f}s',
                    ha='center', va='bottom', fontsize=9)
        
        # Inference time
        bars2 = ax2.bar(models_runtime, infer_times, color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728'])
        ax2.set_title('Inference Time Comparison', fontsize=12, fontweight='bold')
        ax2.set_ylabel('Time (milliseconds per sample)')
        ax2.grid(axis='y', alpha=0.3)
        for bar in bars2:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.3f}ms',
                    ha='center', va='bottom', fontsize=9)
        
        plt.tight_layout()
        plt.savefig('results/figures/runtime_comparison.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("    [+] Runtime comparison saved")
        
    def generate_comparison_table(self):
        """Generate LaTeX/CSV comparison table"""
        print("\n[*] Generating comparison tables...")
        
        # Create comparison DataFrame
        models = ['RandomForest', 'SVM', 'LogisticRegression', 'NaiveBayes', 'IsolationForest']
        data = []
        
        for model in models:
            if model in self.results['baseline_results']:
                result = self.results['baseline_results'][model]
                data.append({
                    'Model': model,
                    'Accuracy (%)': result['accuracy'],
                    'Precision': result['precision'],
                    'Recall': result['recall'],
                    'F1-Score': result['f1_score'],
                    'Training Time (s)': result['training_time_seconds'],
                    'Inference Time (ms)': result['inference_time_ms'],
                    'Throughput (samples/s)': int(result['throughput_samples_per_sec'])
                })
        
        df = pd.DataFrame(data)
        
        # Save as CSV
        os.makedirs('results', exist_ok=True)
        df.to_csv('results/baseline_comparison_table.csv', index=False)
        print("    [+] Comparison table saved (CSV)")
        
        # Generate LaTeX table
        latex_table = df.to_latex(index=False, float_format="%.4f")
        with open('results/baseline_comparison_table.tex', 'w') as f:
            f.write(latex_table)
        print("    [+] Comparison table saved (LaTeX)")
        
        return df
    
    def analyze_failures(self):
        """Analyze model failures and limitations"""
        print("\n[*] Analyzing model failures...")
        
        failures = {}
        
        # Analyze per-class performance
        for model_name in ['RandomForest', 'SVM', 'LogisticRegression']:
            if model_name in self.results['per_class_metrics']:
                report = self.results['per_class_metrics'][model_name]
                
                worst_class = None
                worst_recall = 1.0
                
                for class_name in self.label_names:
                    if class_name in report and isinstance(report[class_name], dict):
                        recall = report[class_name].get('recall', 0)
                        if recall < worst_recall:
                            worst_recall = recall
                            worst_class = class_name
                
                failures[model_name] = {
                    'worst_performing_class': worst_class,
                    'worst_recall': round(worst_recall, 4),
                    'false_positive_rate': self._calculate_fpr(model_name),
                    'false_negative_rate': self._calculate_fnr(model_name)
                }
        
        self.results['failure_analysis'] = failures
        
        print(f"    [+] Worst performing class identified for each model")
        return failures
    
    def _calculate_fpr(self, model_name):
        """Calculate false positive rate"""
        cm = np.array(self.results['confusion_matrices'][model_name])
        if cm.shape == (2, 2):  # Binary
            tn, fp, fn, tp = cm.ravel()
            return round(fp / (fp + tn), 4) if (fp + tn) > 0 else 0
        else:  # Multi-class - average FPR
            fprs = []
            for i in range(len(cm)):
                fp = cm[i, :].sum() - cm[i, i]
                tn = cm.sum() - (cm[i, :].sum() + cm[:, i].sum() - cm[i, i])
                fpr = fp / (fp + tn) if (fp + tn) > 0 else 0
                fprs.append(fpr)
            return round(np.mean(fprs), 4)
    
    def _calculate_fnr(self, model_name):
        """Calculate false negative rate"""
        cm = np.array(self.results['confusion_matrices'][model_name])
        if cm.shape == (2, 2):  # Binary
            tn, fp, fn, tp = cm.ravel()
            return round(fn / (fn + tp), 4) if (fn + tp) > 0 else 0
        else:  # Multi-class - average FNR
            fnrs = []
            for i in range(len(cm)):
                fn = cm[:, i].sum() - cm[i, i]
                tp = cm[i, i]
                fnr = fn / (fn + tp) if (fn + tp) > 0 else 0
                fnrs.append(fnr)
            return round(np.mean(fnrs), 4)
    
    def save_results(self):
        """Save all results to JSON"""
        print("\n[*] Saving results...")
        
        os.makedirs('results', exist_ok=True)
        
        # Save full results
        with open('results/comprehensive_results.json', 'w') as f:
            json.dump(self.results, f, indent=2, default=str)
        
        # Save summary report
        summary = {
            'experiment_date': datetime.now().isoformat(),
            'hardware': self.results['hardware_info'],
            'dataset': self.results['dataset_info'],
            'baseline_results': self.results['baseline_results'],
            'failure_analysis': self.results.get('failure_analysis', {})
        }
        
        with open('results/summary_report.json', 'w') as f:
            json.dump(summary, f, indent=2, default=str)
        
        print("    [+] Results saved to results/")
        
    def print_summary(self):
        """Print summary of results"""
        print("\n" + "="*80)
        print("COMPREHENSIVE EVALUATION SUMMARY")
        print("="*80)
        
        print("\n[*] Hardware Information:")
        hw = self.results['hardware_info']
        print(f"  CPU: {hw['cpu_model']}")
        print(f"  RAM: {hw['ram_gb']} GB")
        print(f"  OS: {hw['os']} {hw['os_version']}")
        print(f"  Python: {hw['python_version']}")
        
        print("\n[*] Dataset Information:")
        ds = self.results['dataset_info']
        print(f"  Total Samples: {ds['total_samples']}")
        print(f"  Train/Test: {ds['train_samples']}/{ds['test_samples']}")
        print(f"  Features: {ds['features']}, Classes: {ds['classes']}")
        
        print("\n[*] Baseline Model Results:")
        print(f"{'Model':<20} {'Accuracy':<12} {'Precision':<12} {'Recall':<12} {'F1-Score':<12}")
        print("-" * 80)
        
        for model_name, results in self.results['baseline_results'].items():
            print(f"{model_name:<20} {results['accuracy']:>6.2f}%     {results['precision']:>8.4f}     "
                  f"{results['recall']:>8.4f}     {results['f1_score']:>8.4f}")
        
        print("\n[*] Runtime Performance:")
        print(f"{'Model':<20} {'Train (s)':<12} {'Infer (ms)':<12} {'Throughput':<12}")
        print("-" * 80)
        
        for model_name, results in self.results['baseline_results'].items():
            print(f"{model_name:<20} {results['training_time_seconds']:>8.2f}     "
                  f"{results['inference_time_ms']:>8.3f}     {int(results['throughput_samples_per_sec']):>8}")
        
        if 'failure_analysis' in self.results:
            print("\n[*] Failure Analysis:")
            for model_name, analysis in self.results['failure_analysis'].items():
                print(f"  {model_name}:")
                print(f"    Worst Class: {analysis['worst_performing_class']} (Recall: {analysis['worst_recall']})")
                print(f"    FPR: {analysis['false_positive_rate']}, FNR: {analysis['false_negative_rate']}")
        
        print("\n" + "="*80)
        print("[+] Evaluation complete! Check results/ directory for detailed outputs.")
        print("="*80)

def main():
    """Main evaluation function"""
    print("="*80)
    print("KRONOS COMPREHENSIVE EVALUATION SYSTEM")
    print("="*80)
    
    evaluator = ComprehensiveEvaluator(max_samples=50000)
    
    # Run evaluation pipeline
    evaluator.collect_hardware_info()
    evaluator.load_and_preprocess_data()
    evaluator.train_baseline_models()
    evaluator.generate_visualizations()
    evaluator.generate_comparison_table()
    evaluator.analyze_failures()
    evaluator.save_results()
    evaluator.print_summary()

if __name__ == "__main__":
    main()

