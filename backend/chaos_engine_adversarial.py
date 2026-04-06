"""
Enhanced CHAOS Engine - Adversarial Machine Learning
Implements FGSM and PGD attacks as per paper claims
"""

import numpy as np
import tensorflow as tf
from tensorflow import keras
from typing import Dict, List, Tuple, Optional, Any
import logging
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from chaos_engine import ChaosEngine
except ImportError:
    ChaosEngine = object
    logging.warning("Base ChaosEngine not available")

logging.basicConfig(level=logging.INFO)

class AdversarialAttackGenerator:
    """Generate adversarial examples using FGSM and PGD"""
    
    def __init__(self, model=None, epsilon: float = 0.1):
        self.model = model
        self.epsilon = epsilon  # Perturbation size
    
    def fgsm_attack(self, X: np.ndarray, y: np.ndarray) -> np.ndarray:
        """
        Fast Gradient Sign Method (FGSM) attack
        Paper claim: "gradient-based attacks like Fast Gradient Sign Method (FGSM)"
        """
        if self.model is None:
            raise ValueError("Model not set for adversarial attack")
        
        # Convert to TensorFlow tensor
        X_tensor = tf.Variable(X, dtype=tf.float32)
        
        with tf.GradientTape() as tape:
            tape.watch(X_tensor)
            predictions = self.model(X_tensor)
            loss = keras.losses.sparse_categorical_crossentropy(y, predictions)
        
        # Compute gradient
        gradient = tape.gradient(loss, X_tensor)
        
        # Generate adversarial examples
        adversarial_X = X_tensor + self.epsilon * tf.sign(gradient)
        
        # Clip to valid range
        adversarial_X = tf.clip_by_value(adversarial_X, 0.0, 1.0)
        
        return adversarial_X.numpy()
    
    def pgd_attack(self, X: np.ndarray, y: np.ndarray, 
                   iterations: int = 10, alpha: float = 0.01) -> np.ndarray:
        """
        Projected Gradient Descent (PGD) attack
        Paper claim: "Projected Gradient Descent (PGD)"
        """
        if self.model is None:
            raise ValueError("Model not set for adversarial attack")
        
        # Start with original data
        adversarial_X = X.copy().astype(np.float32)
        
        for i in range(iterations):
            # Convert to tensor
            X_tensor = tf.Variable(adversarial_X, dtype=tf.float32)
            
            with tf.GradientTape() as tape:
                tape.watch(X_tensor)
                predictions = self.model(X_tensor)
                loss = keras.losses.sparse_categorical_crossentropy(y, predictions)
            
            # Compute gradient
            gradient = tape.gradient(loss, X_tensor)
            
            # Update adversarial examples
            adversarial_X = adversarial_X + alpha * np.sign(gradient.numpy())
            
            # Project back to epsilon ball
            perturbation = adversarial_X - X
            perturbation = np.clip(perturbation, -self.epsilon, self.epsilon)
            adversarial_X = X + perturbation
            
            # Clip to valid range
            adversarial_X = np.clip(adversarial_X, 0.0, 1.0)
        
        return adversarial_X
    
    def generate_adversarial_traffic(self, normal_traffic: np.ndarray, 
                                    attack_type: str = 'fgsm') -> np.ndarray:
        """
        Generate adversarial network traffic patterns
        Paper claim: "adversarial examples toward the machine-learning parts of ORDER module"
        """
        # Create dummy labels (assuming normal traffic = class 0)
        y = np.zeros(len(normal_traffic), dtype=np.int32)
        
        if attack_type.lower() == 'fgsm':
            adversarial_traffic = self.fgsm_attack(normal_traffic, y)
        elif attack_type.lower() == 'pgd':
            adversarial_traffic = self.pgd_attack(normal_traffic, y)
        else:
            raise ValueError(f"Unknown attack type: {attack_type}")
        
        return adversarial_traffic


class EnhancedChaosEngine(ChaosEngine):
    """
    Enhanced CHAOS Engine with adversarial ML capabilities
    Implements FGSM, PGD, and GAN-based attack generation as per paper
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        if config is None:
            config = {}
        
        # Required base config
        config.setdefault('max_concurrent_attacks', 5)
        config.setdefault('attack_interval', 1.0)
        config.setdefault('stealth_threshold', 0.7)
        config.setdefault('adaptation_threshold', 0.3)
        
        # Enhanced config
        config.setdefault('enable_fgsm', True)
        config.setdefault('enable_pgd', True)
        config.setdefault('enable_gan', True)
        config.setdefault('adversarial_epsilon', 0.1)
        config.setdefault('pgd_iterations', 10)
        
        # Initialize base CHAOS engine
        super().__init__(config)
        
        # Adversarial attack generator
        self.adversarial_generator = None
        self.target_model = None  # ORDER module's model to attack
        
        # GAN components (for future implementation)
        self.gan_generator = None
        self.gan_discriminator = None
        
        logging.info("Enhanced CHAOS Engine initialized with adversarial ML capabilities")
    
    def set_target_model(self, model):
        """Set the target model (ORDER module) to attack"""
        self.target_model = model
        if self.adversarial_generator is None:
            self.adversarial_generator = AdversarialAttackGenerator(
                model=model,
                epsilon=self.config.get('adversarial_epsilon', 0.1)
            )
        else:
            self.adversarial_generator.model = model
    
    def generate_fgsm_attack(self, normal_traffic: np.ndarray) -> Dict[str, Any]:
        """
        Generate FGSM adversarial attack
        Paper claim: "gradient-based attacks like Fast Gradient Sign Method (FGSM)"
        """
        if self.adversarial_generator is None or self.target_model is None:
            return {'error': 'Target model not set'}
        
        try:
            adversarial_traffic = self.adversarial_generator.generate_adversarial_traffic(
                normal_traffic, attack_type='fgsm'
            )
            
            attack_result = {
                'attack_type': 'FGSM',
                'original_traffic': normal_traffic,
                'adversarial_traffic': adversarial_traffic,
                'perturbation': adversarial_traffic - normal_traffic,
                'epsilon': self.config.get('adversarial_epsilon', 0.1),
                'success': True
            }
            
            logging.info(f"FGSM attack generated: {len(adversarial_traffic)} samples")
            return attack_result
            
        except Exception as e:
            logging.error(f"FGSM attack generation failed: {e}")
            return {'error': str(e), 'success': False}
    
    def generate_pgd_attack(self, normal_traffic: np.ndarray) -> Dict[str, Any]:
        """
        Generate PGD adversarial attack
        Paper claim: "Projected Gradient Descent (PGD)"
        """
        if self.adversarial_generator is None or self.target_model is None:
            return {'error': 'Target model not set'}
        
        try:
            adversarial_traffic = self.adversarial_generator.generate_adversarial_traffic(
                normal_traffic, attack_type='pgd'
            )
            
            attack_result = {
                'attack_type': 'PGD',
                'original_traffic': normal_traffic,
                'adversarial_traffic': adversarial_traffic,
                'perturbation': adversarial_traffic - normal_traffic,
                'epsilon': self.config.get('adversarial_epsilon', 0.1),
                'iterations': self.config.get('pgd_iterations', 10),
                'success': True
            }
            
            logging.info(f"PGD attack generated: {len(adversarial_traffic)} samples")
            return attack_result
            
        except Exception as e:
            logging.error(f"PGD attack generation failed: {e}")
            return {'error': str(e), 'success': False}
    
    def generate_adversarial_training_data(self, normal_samples: np.ndarray,
                                          num_adversarial: int = 1000) -> Dict[str, Any]:
        """
        Generate adversarial examples for training ORDER module
        Paper claim: "Adversarial training is enriched with advanced methods"
        """
        results = {
            'fgsm_samples': [],
            'pgd_samples': [],
            'total_generated': 0
        }
        
        # Generate FGSM samples
        if self.config.get('enable_fgsm', True):
            try:
                fgsm_result = self.generate_fgsm_attack(normal_samples[:num_adversarial])
                if fgsm_result.get('success'):
                    results['fgsm_samples'] = fgsm_result['adversarial_traffic']
                    results['total_generated'] += len(results['fgsm_samples'])
            except Exception as e:
                logging.warning(f"FGSM generation failed: {e}")
        
        # Generate PGD samples
        if self.config.get('enable_pgd', True):
            try:
                pgd_result = self.generate_pgd_attack(normal_samples[:num_adversarial])
                if pgd_result.get('success'):
                    results['pgd_samples'] = pgd_result['adversarial_traffic']
                    results['total_generated'] += len(results['pgd_samples'])
            except Exception as e:
                logging.warning(f"PGD generation failed: {e}")
        
        logging.info(f"Generated {results['total_generated']} adversarial samples")
        return results
    
    def _build_gan(self, input_dim: int = 41, latent_dim: int = 100):
        """
        Build GAN for attack generation (future work)
        Paper claim: "machine learning based generator leverages GANs"
        """
        # Generator
        generator_input = keras.Input(shape=(latent_dim,))
        x = layers.Dense(128, activation='relu')(generator_input)
        x = layers.Dense(256, activation='relu')(x)
        x = layers.Dense(input_dim, activation='tanh')(x)
        self.gan_generator = keras.Model(generator_input, x)
        
        # Discriminator
        discriminator_input = keras.Input(shape=(input_dim,))
        x = layers.Dense(256, activation='relu')(discriminator_input)
        x = layers.Dense(128, activation='relu')(x)
        x = layers.Dense(1, activation='sigmoid')(x)
        self.gan_discriminator = keras.Model(discriminator_input, x)
        
        # Combined GAN
        gan_output = self.gan_discriminator(self.gan_generator(generator_input))
        self.gan = keras.Model(generator_input, gan_output)
        
        logging.info("GAN architecture built (requires training)")
