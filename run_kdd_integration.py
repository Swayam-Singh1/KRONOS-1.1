#!/usr/bin/env python3
"""
KDD Cup 99 Integration Launcher
Complete integration of KDD Cup 99 dataset with Self-Morphing AI Cybersecurity Engine
"""

import sys
import os
import time
import logging
import subprocess
import threading
import webbrowser
from pathlib import Path
from datetime import datetime

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from kdd_data_loader import KDDDataLoader
from kdd_enhanced_training import KDDEnhancedTrainingSystem
from kdd_dashboard import KDDDashboard

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - KDD_LAUNCHER - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('kdd_integration.log'),
        logging.StreamHandler()
    ]
)

class KDDIntegrationLauncher:
    """Launcher for KDD Cup 99 integration"""
    
    def __init__(self):
        self.processes = {}
        self.running = False
        
        # Check if KDD dataset exists
        self.kdd_path = "datset/KDD cup 99"
        if not os.path.exists(self.kdd_path):
            logging.error(f"KDD dataset not found at {self.kdd_path}")
            logging.error("Please ensure the KDD Cup 99 dataset is in the 'datset' folder")
            sys.exit(1)
        
        logging.info("KDD Integration Launcher initialized")
    
    def check_requirements(self):
        """Check if all requirements are met"""
        try:
            logging.info("Checking requirements...")
            
            # Check Python version
            if sys.version_info < (3, 8):
                logging.error("Python 3.8+ is required")
                return False
            
            # Check required packages
            required_packages = [
                'fastapi', 'uvicorn', 'streamlit', 'pandas', 'numpy',
                'scikit-learn', 'plotly', 'requests'
            ]
            
            missing_packages = []
            for package in required_packages:
                try:
                    __import__(package)
                except ImportError:
                    missing_packages.append(package)
            
            if missing_packages:
                logging.error(f"Missing packages: {', '.join(missing_packages)}")
                logging.error("Please install requirements: pip install -r backend/requirements.txt")
                return False
            
            # Check KDD dataset files
            required_files = [
                "kddcup.data_10_percent",
                "kddcup.names",
                "training_attack_types"
            ]
            
            missing_files = []
            for file in required_files:
                if not os.path.exists(os.path.join(self.kdd_path, file)):
                    missing_files.append(file)
            
            if missing_files:
                logging.error(f"Missing KDD files: {', '.join(missing_files)}")
                return False
            
            logging.info("All requirements met")
            return True
            
        except Exception as e:
            logging.error(f"Requirements check failed: {e}")
            return False
    
    def start_api_server(self):
        """Start the API server with KDD endpoints"""
        try:
            logging.info("Starting API server with KDD integration...")
            
            cmd = [
                sys.executable, "-m", "uvicorn",
                "backend.api_server:app",
                "--host", "0.0.0.0",
                "--port", "8000",
                "--reload"
            ]
            
            self.processes['api_server'] = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=os.path.dirname(__file__)
            )
            
            # Wait for server to start
            time.sleep(5)
            
            logging.info("API server started on http://localhost:8000")
            return True
            
        except Exception as e:
            logging.error(f"Failed to start API server: {e}")
            return False
    
    def start_kdd_dashboard(self):
        """Start the KDD-enhanced dashboard"""
        try:
            logging.info("Starting KDD dashboard...")
            
            cmd = [
                sys.executable, "-m", "streamlit",
                "run", "backend/kdd_dashboard.py",
                "--server.port", "8501",
                "--server.address", "0.0.0.0"
            ]
            
            self.processes['kdd_dashboard'] = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=os.path.dirname(__file__)
            )
            
            # Wait for dashboard to start
            time.sleep(3)
            
            logging.info("KDD dashboard started on http://localhost:8501")
            return True
            
        except Exception as e:
            logging.error(f"Failed to start KDD dashboard: {e}")
            return False
    
    def run_kdd_training(self):
        """Run KDD-enhanced training"""
        try:
            logging.info("Starting KDD-enhanced training...")
            
            # Initialize training system
            training_system = KDDEnhancedTrainingSystem({
                'kdd_dataset_size': 10000,
                'use_full_dataset': False,
                'train_order_engine': True,
                'train_chaos_engine': True,
                'train_balance_controller': True
            })
            
            # Run training
            results = training_system.run_comprehensive_training()
            
            if results.get('success', False):
                logging.info("KDD training completed successfully")
                return True
            else:
                logging.error(f"KDD training failed: {results.get('error', 'Unknown error')}")
                return False
                
        except Exception as e:
            logging.error(f"KDD training failed: {e}")
            return False
    
    def test_kdd_integration(self):
        """Test KDD integration"""
        try:
            logging.info("Testing KDD integration...")
            
            # Test data loader
            kdd_loader = KDDDataLoader()
            data = kdd_loader.load_data("kddcup.data_10_percent", max_rows=1000)
            stats = kdd_loader.get_data_statistics()
            
            logging.info(f"KDD data loaded: {len(data)} records")
            logging.info(f"Attack types: {len(stats.get('attack_types', {}))}")
            
            # Test network flow generation
            flows = kdd_loader.generate_network_flows(100)
            logging.info(f"Generated {len(flows)} network flows")
            
            logging.info("KDD integration test passed")
            return True
            
        except Exception as e:
            logging.error(f"KDD integration test failed: {e}")
            return False
    
    def open_browser(self):
        """Open browser to dashboard and API docs"""
        try:
            time.sleep(2)  # Wait for services to start
            
            # Open KDD dashboard
            webbrowser.open("http://localhost:8501")
            
            # Open API documentation
            webbrowser.open("http://localhost:8000/docs")
            
            logging.info("Browser opened to dashboard and API docs")
            
        except Exception as e:
            logging.warning(f"Failed to open browser: {e}")
    
    def show_menu(self):
        """Show interactive menu"""
        while True:
            print("\n" + "="*60)
            print("🛡️ KDD Cup 99 Cybersecurity Engine Integration")
            print("="*60)
            print("1. 🔍 Test KDD Integration")
            print("2. 🤖 Run KDD Training")
            print("3. 🚀 Start Full System (API + Dashboard)")
            print("4. 📊 Start KDD Dashboard Only")
            print("5. 🔧 Start API Server Only")
            print("6. 📈 View Training Results")
            print("7. 🧹 Clean Up Generated Files")
            print("8. ❌ Exit")
            print("="*60)
            
            choice = input("Select an option (1-8): ").strip()
            
            if choice == '1':
                self.test_kdd_integration()
            
            elif choice == '2':
                self.run_kdd_training()
            
            elif choice == '3':
                self.start_full_system()
            
            elif choice == '4':
                self.start_kdd_dashboard()
                input("Press Enter to stop dashboard...")
                self.stop_process('kdd_dashboard')
            
            elif choice == '5':
                self.start_api_server()
                input("Press Enter to stop API server...")
                self.stop_process('api_server')
            
            elif choice == '6':
                self.view_training_results()
            
            elif choice == '7':
                self.cleanup_files()
            
            elif choice == '8':
                self.shutdown()
                break
            
            else:
                print("Invalid choice. Please try again.")
    
    def start_full_system(self):
        """Start the complete system with KDD integration"""
        try:
            logging.info("Starting full KDD-integrated system...")
            
            # Check requirements
            if not self.check_requirements():
                return False
            
            # Test integration
            if not self.test_kdd_integration():
                return False
            
            # Start API server
            if not self.start_api_server():
                return False
            
            # Start KDD dashboard
            if not self.start_kdd_dashboard():
                return False
            
            # Open browser
            self.open_browser()
            
            self.running = True
            logging.info("Full system started successfully")
            
            print("\n✅ KDD-integrated system is running!")
            print("📊 Dashboard: http://localhost:8501")
            print("🔧 API Docs: http://localhost:8000/docs")
            print("🛡️ KDD Endpoints: http://localhost:8000/kdd/")
            print("\nPress Ctrl+C to stop all services...")
            
            try:
                while self.running:
                    time.sleep(1)
            except KeyboardInterrupt:
                logging.info("Received interrupt signal")
                self.shutdown()
            
            return True
            
        except Exception as e:
            logging.error(f"Failed to start full system: {e}")
            return False
    
    def stop_process(self, process_name):
        """Stop a specific process"""
        if process_name in self.processes:
            try:
                self.processes[process_name].terminate()
                self.processes[process_name].wait(timeout=5)
                del self.processes[process_name]
                logging.info(f"Stopped {process_name}")
            except Exception as e:
                logging.error(f"Failed to stop {process_name}: {e}")
    
    def view_training_results(self):
        """View training results"""
        try:
            results_dir = "training_results/kdd_enhanced"
            if not os.path.exists(results_dir):
                print("No training results found")
                return
            
            results_files = [f for f in os.listdir(results_dir) if f.endswith('.json')]
            
            if not results_files:
                print("No training results found")
                return
            
            print(f"\nFound {len(results_files)} training result files:")
            for i, file in enumerate(results_files, 1):
                print(f"{i}. {file}")
            
            choice = input("Select a file to view (number): ").strip()
            
            try:
                file_index = int(choice) - 1
                if 0 <= file_index < len(results_files):
                    file_path = os.path.join(results_dir, results_files[file_index])
                    
                    with open(file_path, 'r') as f:
                        import json
                        results = json.load(f)
                    
                    print(f"\nTraining Results: {results_files[file_index]}")
                    print("="*50)
                    print(f"Training ID: {results.get('training_id', 'N/A')}")
                    print(f"Start Time: {results.get('start_time', 'N/A')}")
                    print(f"Duration: {results.get('total_training_time', 0):.2f} seconds")
                    print(f"Success: {results.get('success', False)}")
                    print(f"Components Trained: {len(results.get('components_trained', []))}")
                    
                    if results.get('errors'):
                        print(f"Errors: {len(results['errors'])}")
                        for error in results['errors']:
                            print(f"  - {error}")
                
            except (ValueError, IndexError):
                print("Invalid selection")
                
        except Exception as e:
            logging.error(f"Failed to view training results: {e}")
    
    def cleanup_files(self):
        """Clean up generated files"""
        try:
            logging.info("Cleaning up generated files...")
            
            # Clean up log files
            log_files = [
                'kdd_integration.log',
                'kdd_data_loader.log',
                'kdd_order_integration.log',
                'kdd_chaos_integration.log',
                'kdd_enhanced_training.log',
                'kdd_dashboard.log'
            ]
            
            for log_file in log_files:
                if os.path.exists(log_file):
                    os.remove(log_file)
                    print(f"Removed {log_file}")
            
            # Clean up model files
            model_dirs = [
                'models/kdd_models',
                'models/kdd_enhanced',
                'training_results/kdd_enhanced'
            ]
            
            for model_dir in model_dirs:
                if os.path.exists(model_dir):
                    import shutil
                    shutil.rmtree(model_dir)
                    print(f"Removed {model_dir}")
            
            print("Cleanup completed")
            
        except Exception as e:
            logging.error(f"Cleanup failed: {e}")
    
    def shutdown(self):
        """Shutdown all processes"""
        try:
            logging.info("Shutting down KDD integration...")
            
            self.running = False
            
            # Stop all processes
            for process_name in list(self.processes.keys()):
                self.stop_process(process_name)
            
            logging.info("KDD integration shutdown complete")
            
        except Exception as e:
            logging.error(f"Shutdown failed: {e}")

def main():
    """Main entry point"""
    try:
        launcher = KDDIntegrationLauncher()
        
        # Check if running in interactive mode
        if len(sys.argv) > 1:
            if sys.argv[1] == '--test':
                launcher.test_kdd_integration()
            elif sys.argv[1] == '--train':
                launcher.run_kdd_training()
            elif sys.argv[1] == '--start':
                launcher.start_full_system()
            elif sys.argv[1] == '--dashboard':
                launcher.start_kdd_dashboard()
                input("Press Enter to stop...")
                launcher.stop_process('kdd_dashboard')
            elif sys.argv[1] == '--api':
                launcher.start_api_server()
                input("Press Enter to stop...")
                launcher.stop_process('api_server')
            else:
                print("Usage: python run_kdd_integration.py [--test|--train|--start|--dashboard|--api]")
        else:
            # Interactive mode
            launcher.show_menu()
    
    except KeyboardInterrupt:
        logging.info("Received interrupt signal")
    except Exception as e:
        logging.error(f"KDD integration launcher failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
