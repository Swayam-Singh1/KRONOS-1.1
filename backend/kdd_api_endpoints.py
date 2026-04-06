"""
KDD Cup 99 API Endpoints
Additional API endpoints for KDD dataset integration
"""

from fastapi import APIRouter, HTTPException, Query, BackgroundTasks
from pydantic import BaseModel
from typing import Dict, List, Any, Optional
import logging
import json
import time
from datetime import datetime

from kdd_data_loader import KDDDataLoader
from kdd_order_integration import KDDOrderIntegration
from kdd_chaos_integration import KDDChaosIntegration
from kdd_enhanced_training import KDDEnhancedTrainingSystem
from order_engine import OrderEngine
from chaos_engine import ChaosEngine

# Configure logging
logging.basicConfig(level=logging.INFO)

# Create router for KDD endpoints
kdd_router = APIRouter(prefix="/kdd", tags=["KDD Cup 99"])

# Global instances
kdd_loader = None
kdd_order_integration = None
kdd_chaos_integration = None
training_system = None

# Pydantic models
class KDDTrainingRequest(BaseModel):
    dataset_size: int = 10000
    use_full_dataset: bool = False
    train_order_engine: bool = True
    train_chaos_engine: bool = True
    train_balance_controller: bool = True

class KDDAttackSimulationRequest(BaseModel):
    n_attacks: int = 100
    attack_types: Optional[List[str]] = None
    real_time: bool = False

class KDDIntelligenceRequest(BaseModel):
    target_ip: Optional[str] = None
    include_patterns: bool = True
    include_recommendations: bool = True

# Initialize KDD components
def initialize_kdd_components():
    """Initialize KDD components"""
    global kdd_loader, kdd_order_integration, kdd_chaos_integration, training_system
    
    try:
        if kdd_loader is None:
            kdd_loader = KDDDataLoader()
        
        if training_system is None:
            training_system = KDDEnhancedTrainingSystem()
        
        logging.info("KDD components initialized")
        
    except Exception as e:
        logging.error(f"Failed to initialize KDD components: {e}")

# KDD Dataset Endpoints
@kdd_router.get("/dataset/status")
async def get_dataset_status():
    """Get KDD dataset status and statistics"""
    try:
        initialize_kdd_components()
        
        if kdd_loader is None:
            raise HTTPException(status_code=500, detail="KDD loader not initialized")
        
        # Load sample data to get statistics
        data = kdd_loader.load_data("kddcup.data_10_percent", max_rows=1000)
        stats = kdd_loader.get_data_statistics()
        
        return {
            "status": "available",
            "dataset_path": kdd_loader.dataset_path,
            "statistics": stats,
            "last_loaded": datetime.now().isoformat()
        }
        
    except Exception as e:
        logging.error(f"Dataset status check failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@kdd_router.get("/dataset/load")
async def load_dataset(
    file_name: str = Query("kddcup.data_10_percent", description="Dataset file name"),
    max_rows: Optional[int] = Query(None, description="Maximum number of rows to load")
):
    """Load KDD dataset"""
    try:
        initialize_kdd_components()
        
        data = kdd_loader.load_data(file_name, max_rows)
        stats = kdd_loader.get_data_statistics()
        
        return {
            "status": "loaded",
            "file_name": file_name,
            "rows_loaded": len(data),
            "statistics": stats,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logging.error(f"Dataset loading failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@kdd_router.get("/dataset/attack-types")
async def get_attack_types():
    """Get available attack types from KDD dataset"""
    try:
        initialize_kdd_components()
        
        if kdd_loader.raw_data is None:
            kdd_loader.load_data("kddcup.data_10_percent", max_rows=1000)
        
        attack_types = kdd_loader.raw_data['attack_type'].value_counts().to_dict()
        attack_categories = kdd_loader.raw_data['attack_category'].value_counts().to_dict()
        
        return {
            "attack_types": attack_types,
            "attack_categories": attack_categories,
            "total_attack_types": len(attack_types) - 1,  # Exclude 'normal'
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logging.error(f"Attack types retrieval failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@kdd_router.get("/dataset/samples")
async def get_dataset_samples(
    attack_type: Optional[str] = Query(None, description="Filter by attack type"),
    category: Optional[str] = Query(None, description="Filter by attack category"),
    limit: int = Query(100, description="Maximum number of samples")
):
    """Get dataset samples with optional filtering"""
    try:
        initialize_kdd_components()
        
        if kdd_loader.raw_data is None:
            kdd_loader.load_data("kddcup.data_10_percent", max_rows=1000)
        
        data = kdd_loader.raw_data.copy()
        
        # Apply filters
        if attack_type:
            data = data[data['attack_type'] == attack_type]
        
        if category:
            data = data[data['attack_category'] == category]
        
        # Limit results
        if len(data) > limit:
            data = data.sample(n=limit, random_state=42)
        
        # Convert to JSON-serializable format
        samples = data.to_dict('records')
        
        return {
            "samples": samples,
            "total_samples": len(samples),
            "filters_applied": {
                "attack_type": attack_type,
                "category": category
            },
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logging.error(f"Dataset samples retrieval failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# KDD Training Endpoints
@kdd_router.post("/training/start")
async def start_kdd_training(request: KDDTrainingRequest, background_tasks: BackgroundTasks):
    """Start KDD-based training"""
    try:
        initialize_kdd_components()
        
        if training_system is None:
            raise HTTPException(status_code=500, detail="Training system not initialized")
        
        # Update training system config
        training_system.config.update({
            'kdd_dataset_size': request.dataset_size,
            'use_full_dataset': request.use_full_dataset,
            'train_order_engine': request.train_order_engine,
            'train_chaos_engine': request.train_chaos_engine,
            'train_balance_controller': request.train_balance_controller
        })
        
        # Start training in background
        training_id = f"kdd_training_{int(time.time())}"
        
        def run_training():
            try:
                results = training_system.run_comprehensive_training()
                logging.info(f"KDD training {training_id} completed")
            except Exception as e:
                logging.error(f"KDD training {training_id} failed: {e}")
        
        background_tasks.add_task(run_training)
        
        return {
            "status": "started",
            "training_id": training_id,
            "config": request.dict(),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logging.error(f"KDD training start failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@kdd_router.get("/training/status")
async def get_training_status():
    """Get KDD training status"""
    try:
        initialize_kdd_components()
        
        if training_system is None:
            raise HTTPException(status_code=500, detail="Training system not initialized")
        
        status = training_system.get_training_status()
        
        return {
            "status": "available",
            "training_status": status,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logging.error(f"Training status check failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@kdd_router.get("/training/results/{training_id}")
async def get_training_results(training_id: str):
    """Get specific training results"""
    try:
        initialize_kdd_components()
        
        if training_system is None:
            raise HTTPException(status_code=500, detail="Training system not initialized")
        
        results = training_system.load_training_results(training_id)
        
        if 'error' in results:
            raise HTTPException(status_code=404, detail=results['error'])
        
        return {
            "status": "found",
            "training_id": training_id,
            "results": results,
            "timestamp": datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Training results retrieval failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# KDD Attack Simulation Endpoints
@kdd_router.post("/attacks/generate")
async def generate_kdd_attacks(request: KDDAttackSimulationRequest):
    """Generate KDD-based attacks"""
    try:
        initialize_kdd_components()
        
        if kdd_chaos_integration is None:
            # Initialize CHAOS integration
            from chaos_engine import ChaosEngine
            chaos_engine = ChaosEngine({})
            kdd_chaos_integration = KDDChaosIntegration(chaos_engine, kdd_loader)
        
        attacks = kdd_chaos_integration.generate_kdd_based_attacks(
            n_attacks=request.n_attacks,
            attack_types=request.attack_types
        )
        
        return {
            "status": "generated",
            "attacks": attacks,
            "total_attacks": len(attacks),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logging.error(f"KDD attack generation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@kdd_router.post("/attacks/simulate")
async def simulate_kdd_attacks(request: KDDAttackSimulationRequest):
    """Simulate KDD-based attacks"""
    try:
        initialize_kdd_components()
        
        if kdd_chaos_integration is None:
            # Initialize CHAOS integration
            from chaos_engine import ChaosEngine
            chaos_engine = ChaosEngine({})
            kdd_chaos_integration = KDDChaosIntegration(chaos_engine, kdd_loader)
        
        results = kdd_chaos_integration.simulate_kdd_attacks(
            n_attacks=request.n_attacks,
            real_time=request.real_time
        )
        
        return {
            "status": "completed",
            "simulation_results": results,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logging.error(f"KDD attack simulation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@kdd_router.get("/attacks/intelligence")
async def get_attack_intelligence(request: KDDIntelligenceRequest):
    """Get attack intelligence based on KDD patterns"""
    try:
        initialize_kdd_components()
        
        if kdd_chaos_integration is None:
            # Initialize CHAOS integration
            from chaos_engine import ChaosEngine
            chaos_engine = ChaosEngine({})
            kdd_chaos_integration = KDDChaosIntegration(chaos_engine, kdd_loader)
        
        intelligence = kdd_chaos_integration.get_attack_intelligence(
            target_ip=request.target_ip
        )
        
        return {
            "status": "generated",
            "intelligence": intelligence,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logging.error(f"Attack intelligence generation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# KDD ORDER Engine Endpoints
@kdd_router.post("/order/train")
async def train_order_with_kdd(
    dataset_size: int = Query(10000, description="Dataset size for training"),
    use_full_dataset: bool = Query(False, description="Use full dataset")
):
    """Train ORDER engine with KDD data"""
    try:
        initialize_kdd_components()
        
        if kdd_order_integration is None:
            # Initialize ORDER integration
            from order_engine import OrderEngine
            order_engine = OrderEngine({})
            kdd_order_integration = KDDOrderIntegration(order_engine, kdd_loader)
        
        results = kdd_order_integration.train_with_kdd_data(
            use_full_dataset=use_full_dataset,
            max_samples=dataset_size
        )
        
        return {
            "status": "completed",
            "training_results": results,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logging.error(f"ORDER engine KDD training failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@kdd_router.get("/order/status")
async def get_order_kdd_status():
    """Get ORDER engine KDD training status"""
    try:
        initialize_kdd_components()
        
        if kdd_order_integration is None:
            return {"status": "not_initialized"}
        
        status = kdd_order_integration.get_kdd_training_status()
        
        return {
            "status": "available",
            "order_status": status,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logging.error(f"ORDER engine status check failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@kdd_router.post("/order/test")
async def test_order_with_kdd(
    n_samples: int = Query(1000, description="Number of test samples")
):
    """Test ORDER engine with KDD data"""
    try:
        initialize_kdd_components()
        
        if kdd_order_integration is None:
            raise HTTPException(status_code=400, detail="ORDER engine not trained with KDD data")
        
        results = kdd_order_integration.test_order_engine_with_kdd(n_samples)
        
        return {
            "status": "completed",
            "test_results": results,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logging.error(f"ORDER engine KDD test failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# KDD Analytics Endpoints
@kdd_router.get("/analytics/attack-patterns")
async def get_attack_patterns():
    """Get attack pattern analysis"""
    try:
        initialize_kdd_components()
        
        if kdd_chaos_integration is None:
            # Initialize CHAOS integration
            from chaos_engine import ChaosEngine
            chaos_engine = ChaosEngine({})
            kdd_chaos_integration = KDDChaosIntegration(chaos_engine, kdd_loader)
        
        analysis = kdd_chaos_integration.analyze_kdd_attacks(max_samples=10000)
        
        return {
            "status": "completed",
            "analysis": analysis,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logging.error(f"Attack pattern analysis failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@kdd_router.get("/analytics/network-flows")
async def get_network_flows(
    n_samples: int = Query(1000, description="Number of network flows to generate")
):
    """Generate network flows from KDD data"""
    try:
        initialize_kdd_components()
        
        if kdd_order_integration is None:
            # Initialize ORDER integration
            from order_engine import OrderEngine
            order_engine = OrderEngine({})
            kdd_order_integration = KDDOrderIntegration(order_engine, kdd_loader)
        
        flows = kdd_order_integration.generate_kdd_network_flows(n_samples)
        
        return {
            "status": "generated",
            "flows": flows,
            "total_flows": len(flows),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logging.error(f"Network flow generation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@kdd_router.get("/analytics/statistics")
async def get_kdd_statistics():
    """Get comprehensive KDD statistics"""
    try:
        initialize_kdd_components()
        
        if kdd_loader is None:
            raise HTTPException(status_code=500, detail="KDD loader not initialized")
        
        # Load data if not already loaded
        if kdd_loader.raw_data is None:
            kdd_loader.load_data("kddcup.data_10_percent", max_rows=10000)
        
        stats = kdd_loader.get_data_statistics()
        
        # Get attack patterns if available
        attack_patterns = {}
        if kdd_chaos_integration is not None:
            try:
                analysis = kdd_chaos_integration.analyze_kdd_attacks(max_samples=5000)
                attack_patterns = analysis.get('attack_patterns', {})
            except Exception as e:
                logging.warning(f"Attack pattern analysis failed: {e}")
        
        return {
            "status": "available",
            "dataset_statistics": stats,
            "attack_patterns": attack_patterns,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logging.error(f"KDD statistics retrieval failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Health check endpoint
@kdd_router.get("/health")
async def kdd_health_check():
    """KDD integration health check"""
    try:
        initialize_kdd_components()
        
        health_status = {
            "status": "healthy",
            "components": {
                "kdd_loader": kdd_loader is not None,
                "training_system": training_system is not None,
                "order_integration": kdd_order_integration is not None,
                "chaos_integration": kdd_chaos_integration is not None
            },
            "timestamp": datetime.now().isoformat()
        }
        
        return health_status
        
    except Exception as e:
        logging.error(f"KDD health check failed: {e}")
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }
