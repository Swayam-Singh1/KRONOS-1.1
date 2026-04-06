"""
Enhanced BALANCE Controller - Active Parameter Optimization
Implements active genetic algorithm optimization and policy gradient methods as per paper
"""

import numpy as np
import random
import logging
from typing import Dict, List, Tuple, Optional, Any
from deap import base, creator, tools, algorithms
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from balance_controller import BalanceController
except ImportError:
    BalanceController = object
    logging.warning("Base BalanceController not available")

logging.basicConfig(level=logging.INFO)

class ActiveBalanceController(BalanceController):
    """
    Enhanced BALANCE Controller with active optimization
    Paper claims:
    - Genetic algorithms for parameter optimization
    - Policy gradient methods
    - Actor-critic architecture
    - Meta-learning
    """
    
    def __init__(self, config: Dict[str, Any] = None, order_engine=None):
        if config is None:
            config = {}
        
        # Required base config
        config.setdefault('experience_buffer_size', 1000)
        config.setdefault('population_size', 50)
        config.setdefault('initial_epsilon', 0.3)
        config.setdefault('learning_rate', 0.001)
        config.setdefault('discount_factor', 0.95)
        config.setdefault('mutation_rate', 0.1)
        config.setdefault('crossover_rate', 0.8)
        
        # Enhanced config
        config.setdefault('enable_active_ga', True)
        config.setdefault('enable_policy_gradient', True)
        config.setdefault('enable_actor_critic', True)
        config.setdefault('enable_meta_learning', True)
        config.setdefault('ga_population_size', 50)
        config.setdefault('ga_generations', 20)
        config.setdefault('optimization_frequency', 100)  # Optimize every N interactions
        
        # Initialize base BALANCE controller
        super().__init__(config)
        
        # Reference to ORDER engine for active optimization
        self.order_engine = order_engine
        
        # Active optimization tracking
        self.optimization_counter = 0
        self.parameter_history = []
        self.performance_history = []
        
        # Actor-Critic components
        self.actor_model = None
        self.critic_model = None
        
        # Meta-learning components
        self.meta_learner = None
        self.adaptation_experiences = []
        
        # Initialize enhanced components
        self._initialize_actor_critic()
        self._initialize_meta_learner()
        
        logging.info("Active BALANCE Controller initialized with optimization capabilities")
    
    def _initialize_actor_critic(self):
        """Initialize Actor-Critic architecture"""
        if not self.config.get('enable_actor_critic', True):
            return
        
        state_dim = 10  # System state dimensions
        action_dim = 5  # Number of actions (parameter adjustments)
        
        # Actor (policy network)
        actor_input = layers.Input(shape=(state_dim,))
        x = layers.Dense(64, activation='relu')(actor_input)
        x = layers.Dense(32, activation='relu')(x)
        actor_output = layers.Dense(action_dim, activation='softmax')(x)
        self.actor_model = keras.Model(actor_input, actor_output)
        self.actor_model.compile(optimizer=keras.optimizers.Adam(learning_rate=0.001))
        
        # Critic (value network)
        critic_input = layers.Input(shape=(state_dim,))
        x = layers.Dense(64, activation='relu')(critic_input)
        x = layers.Dense(32, activation='relu')(x)
        critic_output = layers.Dense(1)(x)
        self.critic_model = keras.Model(critic_input, critic_output)
        self.critic_model.compile(optimizer=keras.optimizers.Adam(learning_rate=0.001))
        
        logging.info("Actor-Critic architecture initialized")
    
    def _initialize_meta_learner(self):
        """Initialize meta-learning framework"""
        if not self.config.get('enable_meta_learning', True):
            return
        
        # Meta-learner for fast adaptation
        # This would learn to quickly adapt to new scenarios
        self.meta_learner = {
            'adaptation_policy': None,
            'experience_library': [],
            'transfer_weights': {}
        }
        
        logging.info("Meta-learning framework initialized")
    
    def optimize_order_parameters_genetic(self) -> Dict[str, Any]:
        """
        Actively optimize ORDER module parameters using genetic algorithm
        Paper claim: "genetic algorithm part of the system retains a number of populations"
        """
        if not self.config.get('enable_active_ga', True) or self.order_engine is None:
            return {'status': 'disabled'}
        
        logging.info("Starting genetic algorithm optimization of ORDER parameters")
        
        # Define parameter space for ORDER module
        # Paper mentions: contamination (0.05-0.15), n_estimators (trees)
        param_bounds = {
            'contamination': (0.05, 0.15),
            'n_estimators': (100, 300),
            'max_depth': (10, 30),
            'threshold': (0.5, 0.9)
        }
        
        # Create DEAP genetic algorithm setup
        creator.create("FitnessMax", base.Fitness, weights=(1.0,))
        creator.create("Individual", list, fitness=creator.FitnessMax)
        
        toolbox = base.Toolbox()
        
        # Define genes (parameters)
        def create_individual():
            return creator.Individual([
                random.uniform(*param_bounds['contamination']),
                random.randint(*param_bounds['n_estimators']),
                random.randint(*param_bounds['max_depth']),
                random.uniform(*param_bounds['threshold'])
            ])
        
        toolbox.register("individual", create_individual)
        toolbox.register("population", tools.initRepeat, list, toolbox.individual)
        
        # Define fitness function
        def evaluate(individual):
            contamination, n_estimators, max_depth, threshold = individual
            
            # Update ORDER engine parameters
            if hasattr(self.order_engine, 'config'):
                self.order_engine.config['contamination'] = contamination
                self.order_engine.config['n_estimators'] = int(n_estimators)
                # Note: Would need to retrain model with new parameters
            
            # Evaluate performance (simplified - would use actual test data)
            # Fitness = detection_rate - false_positive_rate
            fitness = self._evaluate_order_performance()
            
            return (fitness,)
        
        toolbox.register("evaluate", evaluate)
        toolbox.register("mate", tools.cxBlend, alpha=0.5)
        toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=0.1, indpb=0.2)
        toolbox.register("select", tools.selTournament, tournsize=3)
        
        # Create population
        population = toolbox.population(n=self.config.get('ga_population_size', 50))
        
        # Run genetic algorithm
        generations = self.config.get('ga_generations', 20)
        for gen in range(generations):
            # Evaluate population
            fitnesses = list(map(toolbox.evaluate, population))
            for ind, fit in zip(population, fitnesses):
                ind.fitness.values = fit
            
            # Select and clone next generation
            offspring = algorithms.varAnd(population, toolbox, cxpb=0.5, mutpb=0.2)
            fits = toolbox.map(toolbox.evaluate, offspring)
            
            for fit, ind in zip(fits, offspring):
                ind.fitness.values = fit
            
            # Select best individuals
            population = toolbox.select(offspring, len(population))
            
            # Track best individual
            best_ind = tools.selBest(population, 1)[0]
            logging.info(f"Generation {gen}: Best fitness = {best_ind.fitness.values[0]:.4f}")
        
        # Apply best parameters to ORDER engine
        best_params = tools.selBest(population, 1)[0]
        self._apply_optimized_parameters(best_params)
        
        result = {
            'status': 'success',
            'best_parameters': {
                'contamination': best_params[0],
                'n_estimators': int(best_params[1]),
                'max_depth': int(best_params[2]),
                'threshold': best_params[3]
            },
            'best_fitness': best_params.fitness.values[0],
            'generations': generations
        }
        
        self.parameter_history.append(result)
        logging.info(f"GA optimization completed: {result['best_parameters']}")
        
        return result
    
    def _evaluate_order_performance(self) -> float:
        """Evaluate ORDER module performance for fitness calculation"""
        # Simplified fitness function
        # In practice, would use actual test data and metrics
        if hasattr(self.order_engine, 'performance_metrics'):
            metrics = self.order_engine.performance_metrics
            detection_rate = metrics.get('true_positives', 0) / max(
                metrics.get('total_flows_processed', 1), 1
            )
            false_positive_rate = metrics.get('false_positives', 0) / max(
                metrics.get('total_flows_processed', 1), 1
            )
            fitness = detection_rate - false_positive_rate
            return max(0.0, fitness)
        return 0.5  # Default fitness
    
    def _apply_optimized_parameters(self, params):
        """Apply optimized parameters to ORDER engine"""
        if self.order_engine is None:
            return
        
        contamination, n_estimators, max_depth, threshold = params
        
        # Update ORDER config
        if hasattr(self.order_engine, 'config'):
            self.order_engine.config['contamination'] = contamination
            self.order_engine.config['n_estimators'] = int(n_estimators)
            # Would trigger model retraining with new parameters
        
        logging.info(f"Applied optimized parameters to ORDER engine")
    
    def optimize_with_policy_gradient(self, state: np.ndarray) -> Dict[str, Any]:
        """
        Optimize using policy gradient methods
        Paper claim: "policy gradient methods to learn optimal real time decision making"
        """
        if not self.config.get('enable_policy_gradient', True) or self.actor_model is None:
            return {'status': 'disabled'}
        
        # Get action from actor
        state_tensor = np.expand_dims(state, axis=0)
        action_probs = self.actor_model.predict(state_tensor, verbose=0)[0]
        action = np.random.choice(len(action_probs), p=action_probs)
        
        # Execute action (adjust ORDER parameters)
        parameter_adjustment = self._action_to_parameter_adjustment(action)
        
        # Get reward
        reward = self._calculate_reward_from_performance()
        
        # Update actor-critic (simplified - would use full PPO/A2C implementation)
        self._update_actor_critic(state, action, reward)
        
        return {
            'action': action,
            'parameter_adjustment': parameter_adjustment,
            'reward': reward
        }
    
    def _action_to_parameter_adjustment(self, action: int) -> Dict[str, float]:
        """Convert action to parameter adjustment"""
        adjustments = {
            0: {'contamination': +0.01},
            1: {'contamination': -0.01},
            2: {'n_estimators': +10},
            3: {'n_estimators': -10},
            4: {'threshold': +0.05}
        }
        return adjustments.get(action, {})
    
    def _calculate_reward_from_performance(self) -> float:
        """Calculate reward based on ORDER performance"""
        if self.order_engine is None:
            return 0.0
        
        if hasattr(self.order_engine, 'performance_metrics'):
            metrics = self.order_engine.performance_metrics
            detection_rate = metrics.get('true_positives', 0) / max(
                metrics.get('total_flows_processed', 1), 1
            )
            false_positive_rate = metrics.get('false_positives', 0) / max(
                metrics.get('total_flows_processed', 1), 1
            )
            reward = detection_rate - 0.5 * false_positive_rate
            return reward
        return 0.0
    
    def _update_actor_critic(self, state: np.ndarray, action: int, reward: float):
        """Update actor-critic models (simplified implementation)"""
        # Simplified update - full implementation would use PPO/A2C
        state_tensor = np.expand_dims(state, axis=0)
        
        # Critic value
        value = self.critic_model.predict(state_tensor, verbose=0)[0][0]
        
        # Advantage
        advantage = reward - value
        
        # Update critic
        target_value = np.array([[reward]])
        self.critic_model.fit(state_tensor, target_value, epochs=1, verbose=0)
        
        # Update actor (simplified)
        action_onehot = np.zeros((1, 5))
        action_onehot[0, action] = 1
        self.actor_model.fit(state_tensor, action_onehot, epochs=1, verbose=0)
    
    def meta_learn_adaptation(self, source_scenario: Dict, target_scenario: Dict) -> Dict[str, Any]:
        """
        Meta-learning for fast adaptation
        Paper claim: "meta learning part enables fast adaptation to new environments"
        """
        if not self.config.get('enable_meta_learning', True):
            return {'status': 'disabled'}
        
        # Store adaptation experience
        experience = {
            'source': source_scenario,
            'target': target_scenario,
            'adaptation_strategy': self._learn_adaptation_strategy(source_scenario, target_scenario),
            'timestamp': time.time()
        }
        
        self.adaptation_experiences.append(experience)
        self.meta_learner['experience_library'].append(experience)
        
        logging.info("Meta-learning adaptation strategy learned")
        return experience
    
    def _learn_adaptation_strategy(self, source: Dict, target: Dict) -> Dict[str, Any]:
        """Learn adaptation strategy from source to target scenario"""
        # Simplified - would use MAML or similar meta-learning algorithm
        strategy = {
            'parameter_transfer': {},
            'feature_mapping': {},
            'confidence': 0.7
        }
        return strategy
    
    def auto_optimize(self):
        """
        Automatic optimization trigger
        Runs GA optimization periodically based on performance
        """
        self.optimization_counter += 1
        
        if self.optimization_counter >= self.config.get('optimization_frequency', 100):
            # Check if optimization is needed
            if self._should_optimize():
                logging.info("Triggering automatic optimization")
                result = self.optimize_order_parameters_genetic()
                self.optimization_counter = 0
                return result
        
        return {'status': 'not_needed'}
    
    def _should_optimize(self) -> bool:
        """Determine if optimization is needed"""
        if self.order_engine is None:
            return False
        
        if hasattr(self.order_engine, 'performance_metrics'):
            metrics = self.order_engine.performance_metrics
            accuracy = metrics.get('model_accuracy', 0.0)
            
            # Optimize if accuracy drops below threshold
            return accuracy < self.config.get('optimization_threshold', 0.7)
        
        return False

import time
