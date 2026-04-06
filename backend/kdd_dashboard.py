"""
KDD Cup 99 Dashboard Integration
Enhanced Streamlit dashboard with KDD data visualization and analysis
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import requests
import time

from kdd_data_loader import KDDDataLoader
from kdd_order_integration import KDDOrderIntegration
from kdd_chaos_integration import KDDChaosIntegration
from kdd_enhanced_training import KDDEnhancedTrainingSystem

# Configure logging
logging.basicConfig(level=logging.INFO)

class KDDDashboard:
    """Enhanced dashboard with KDD Cup 99 integration"""
    
    def __init__(self):
        self.kdd_loader = KDDDataLoader()
        self.api_base_url = "http://localhost:8000"
        
        # Initialize components
        self.order_engine = None
        self.chaos_engine = None
        self.kdd_order_integration = None
        self.kdd_chaos_integration = None
        self.training_system = None
        
        self._initialize_components()
    
    def _initialize_components(self):
        """Initialize dashboard components"""
        try:
            # Initialize training system
            self.training_system = KDDEnhancedTrainingSystem()
            
            # Load KDD data
            self.kdd_data = self.kdd_loader.load_data("kddcup.data_10_percent", max_rows=10000)
            
            logging.info("KDD Dashboard components initialized")
            
        except Exception as e:
            logging.error(f"Dashboard initialization failed: {e}")
    
    def render_main_dashboard(self):
        """Render the main KDD dashboard"""
        st.set_page_config(
            page_title="KDD Cup 99 Cybersecurity Dashboard",
            page_icon="🛡️",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        
        # Header
        st.title("🛡️ KDD Cup 99 Cybersecurity Dashboard")
        st.markdown("**Real-World Dataset Integration for Self-Morphing AI Cybersecurity Engine**")
        
        # Sidebar
        self._render_sidebar()
        
        # Main content tabs
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📊 Dataset Overview", 
            "🔍 Attack Analysis", 
            "🤖 AI Training", 
            "⚔️ Attack Simulation", 
            "📈 Performance Metrics"
        ])
        
        with tab1:
            self._render_dataset_overview()
        
        with tab2:
            self._render_attack_analysis()
        
        with tab3:
            self._render_ai_training()
        
        with tab4:
            self._render_attack_simulation()
        
        with tab5:
            self._render_performance_metrics()
    
    def _render_sidebar(self):
        """Render sidebar controls"""
        st.sidebar.title("🎛️ Controls")
        
        # Dataset selection
        st.sidebar.subheader("Dataset Selection")
        dataset_option = st.sidebar.selectbox(
            "Select Dataset",
            ["10% Sample", "Full Dataset"],
            index=0
        )
        
        # Sample size
        sample_size = st.sidebar.slider(
            "Sample Size",
            min_value=1000,
            max_value=50000,
            value=10000,
            step=1000
        )
        
        # Attack type filter
        st.sidebar.subheader("Attack Filters")
        attack_categories = ['All'] + list(self.kdd_data['attack_category'].unique())
        selected_category = st.sidebar.selectbox("Attack Category", attack_categories)
        
        # Update button
        if st.sidebar.button("🔄 Refresh Data"):
            st.rerun()
        
        # Store selections in session state
        st.session_state.dataset_option = dataset_option
        st.session_state.sample_size = sample_size
        st.session_state.selected_category = selected_category
    
    def _render_dataset_overview(self):
        """Render dataset overview tab"""
        st.header("📊 KDD Cup 99 Dataset Overview")
        
        # Dataset statistics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Records", f"{len(self.kdd_data):,}")
        
        with col2:
            normal_count = len(self.kdd_data[self.kdd_data['attack_category'] == 'normal'])
            st.metric("Normal Traffic", f"{normal_count:,}")
        
        with col3:
            attack_count = len(self.kdd_data[self.kdd_data['attack_category'] != 'normal'])
            st.metric("Attack Records", f"{attack_count:,}")
        
        with col4:
            attack_types = len(self.kdd_data['attack_type'].unique()) - 1  # Exclude 'normal'
            st.metric("Attack Types", attack_types)
        
        # Attack distribution charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Attack Category Distribution")
            category_counts = self.kdd_data['attack_category'].value_counts()
            
            fig = px.pie(
                values=category_counts.values,
                names=category_counts.index,
                title="Attack Categories",
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("Top 10 Attack Types")
            attack_type_counts = self.kdd_data['attack_type'].value_counts().head(10)
            
            fig = px.bar(
                x=attack_type_counts.values,
                y=attack_type_counts.index,
                orientation='h',
                title="Most Common Attack Types",
                color=attack_type_counts.values,
                color_continuous_scale='Reds'
            )
            fig.update_layout(yaxis={'categoryorder': 'total ascending'})
            st.plotly_chart(fig, use_container_width=True)
        
        # Feature analysis
        st.subheader("Feature Analysis")
        
        # Select features to analyze
        numeric_features = self.kdd_data.select_dtypes(include=[np.number]).columns.tolist()
        selected_features = st.multiselect(
            "Select Features to Analyze",
            numeric_features,
            default=numeric_features[:5]
        )
        
        if selected_features:
            # Feature distribution
            fig = make_subplots(
                rows=2, cols=2,
                subplot_titles=selected_features[:4],
                specs=[[{"secondary_y": False}, {"secondary_y": False}],
                       [{"secondary_y": False}, {"secondary_y": False}]]
            )
            
            for i, feature in enumerate(selected_features[:4]):
                row = (i // 2) + 1
                col = (i % 2) + 1
                
                fig.add_trace(
                    go.Histogram(x=self.kdd_data[feature], name=feature),
                    row=row, col=col
                )
            
            fig.update_layout(height=600, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
    
    def _render_attack_analysis(self):
        """Render attack analysis tab"""
        st.header("🔍 Attack Pattern Analysis")
        
        # Filter data based on sidebar selection
        filtered_data = self._filter_data()
        
        # Attack characteristics analysis
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Attack Duration Analysis")
            attack_data = filtered_data[filtered_data['attack_category'] != 'normal']
            
            if not attack_data.empty:
                fig = px.box(
                    attack_data,
                    x='attack_category',
                    y='duration',
                    title="Attack Duration by Category",
                    color='attack_category'
                )
                fig.update_xaxes(tickangle=45)
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("Protocol Distribution")
            protocol_counts = filtered_data['protocol_type'].value_counts()
            
            fig = px.bar(
                x=protocol_counts.index,
                y=protocol_counts.values,
                title="Protocol Type Distribution",
                color=protocol_counts.values,
                color_continuous_scale='Blues'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Service analysis
        st.subheader("Service Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Top Services by Attack Count")
            service_attacks = filtered_data[filtered_data['attack_category'] != 'normal']['service'].value_counts().head(10)
            
            fig = px.bar(
                x=service_attacks.values,
                y=service_attacks.index,
                orientation='h',
                title="Most Targeted Services",
                color=service_attacks.values,
                color_continuous_scale='Oranges'
            )
            fig.update_layout(yaxis={'categoryorder': 'total ascending'})
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("Service vs Attack Category")
            service_category = pd.crosstab(
                filtered_data['service'],
                filtered_data['attack_category']
            ).head(10)
            
            fig = px.imshow(
                service_category,
                title="Service vs Attack Category Heatmap",
                color_continuous_scale='Reds'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Attack patterns over time (simulated)
        st.subheader("Attack Patterns Over Time")
        
        # Generate simulated time series data
        time_data = self._generate_time_series_data(filtered_data)
        
        fig = px.line(
            time_data,
            x='hour',
            y='attack_count',
            color='attack_category',
            title="Simulated Attack Patterns by Hour",
            markers=True
        )
        st.plotly_chart(fig, use_container_width=True)
    
    def _render_ai_training(self):
        """Render AI training tab"""
        st.header("🤖 AI Training with KDD Data")
        
        # Training controls
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🚀 Start KDD Training", type="primary"):
                with st.spinner("Training AI models with KDD data..."):
                    try:
                        results = self.training_system.run_comprehensive_training()
                        st.session_state.training_results = results
                        st.success("Training completed successfully!")
                    except Exception as e:
                        st.error(f"Training failed: {e}")
        
        with col2:
            if st.button("📊 View Training Status"):
                status = self.training_system.get_training_status()
                st.json(status)
        
        with col3:
            if st.button("🔄 Refresh Training Data"):
                st.rerun()
        
        # Display training results
        if 'training_results' in st.session_state:
            results = st.session_state.training_results
            
            st.subheader("Training Results")
            
            # Training metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Training Time", f"{results.get('total_training_time', 0):.2f}s")
            
            with col2:
                components_trained = len(results.get('components_trained', []))
                st.metric("Components Trained", components_trained)
            
            with col3:
                success = results.get('success', False)
                st.metric("Training Status", "✅ Success" if success else "❌ Failed")
            
            with col4:
                errors = len(results.get('errors', []))
                st.metric("Errors", errors)
            
            # Component performance
            st.subheader("Component Performance")
            
            performance_metrics = results.get('performance_metrics', {})
            
            for component, metrics in performance_metrics.items():
                with st.expander(f"📈 {component.replace('_', ' ').title()}"):
                    if isinstance(metrics, dict):
                        st.json(metrics)
                    else:
                        st.write(metrics)
        
        # Training history
        st.subheader("Training History")
        
        if hasattr(self.training_system, 'training_history') and self.training_system.training_history:
            history_df = pd.DataFrame([
                {
                    'Training ID': h['training_id'],
                    'Start Time': h['start_time'],
                    'Duration': h.get('total_training_time', 0),
                    'Components': len(h.get('components_trained', [])),
                    'Success': h.get('success', False)
                }
                for h in self.training_system.training_history
            ])
            
            st.dataframe(history_df, use_container_width=True)
        else:
            st.info("No training history available")
    
    def _render_attack_simulation(self):
        """Render attack simulation tab"""
        st.header("⚔️ KDD-Based Attack Simulation")
        
        # Simulation controls
        col1, col2, col3 = st.columns(3)
        
        with col1:
            n_attacks = st.number_input("Number of Attacks", min_value=10, max_value=1000, value=100)
        
        with col2:
            attack_types = st.multiselect(
                "Attack Types",
                ['All'] + list(self.kdd_data['attack_type'].unique()),
                default=['All']
            )
        
        with col3:
            real_time = st.checkbox("Real-time Simulation", value=False)
        
        # Simulation buttons
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🎯 Generate KDD Attacks", type="primary"):
                with st.spinner("Generating KDD-based attacks..."):
                    try:
                        # Initialize CHAOS integration if not done
                        if not hasattr(self, 'kdd_chaos_integration'):
                            from chaos_engine import ChaosEngine
                            chaos_engine = ChaosEngine({})
                            self.kdd_chaos_integration = KDDChaosIntegration(chaos_engine, self.kdd_loader)
                        
                        attacks = self.kdd_chaos_integration.generate_kdd_based_attacks(n_attacks)
                        st.session_state.generated_attacks = attacks
                        st.success(f"Generated {len(attacks)} KDD-based attacks!")
                    except Exception as e:
                        st.error(f"Attack generation failed: {e}")
        
        with col2:
            if st.button("🚀 Run Simulation"):
                if 'generated_attacks' in st.session_state:
                    with st.spinner("Running attack simulation..."):
                        try:
                            simulation_results = self.kdd_chaos_integration.simulate_kdd_attacks(
                                n_attacks=n_attacks,
                                real_time=real_time
                            )
                            st.session_state.simulation_results = simulation_results
                            st.success("Simulation completed!")
                        except Exception as e:
                            st.error(f"Simulation failed: {e}")
                else:
                    st.warning("Please generate attacks first!")
        
        # Display generated attacks
        if 'generated_attacks' in st.session_state:
            st.subheader("Generated Attacks")
            
            attacks_df = pd.DataFrame(st.session_state.generated_attacks)
            
            # Attack type distribution
            col1, col2 = st.columns(2)
            
            with col1:
                attack_type_counts = attacks_df['kdd_attack_type'].value_counts()
                fig = px.pie(
                    values=attack_type_counts.values,
                    names=attack_type_counts.index,
                    title="Generated Attack Types"
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                intensity_dist = attacks_df['intensity'].hist(bins=20)
                st.pyplot(intensity_dist.figure)
            
            # Attack details table
            st.subheader("Attack Details")
            st.dataframe(attacks_df, use_container_width=True)
        
        # Display simulation results
        if 'simulation_results' in st.session_state:
            results = st.session_state.simulation_results
            
            st.subheader("Simulation Results")
            
            # Results metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Attacks", results.get('total_attacks', 0))
            
            with col2:
                st.metric("Successful Attacks", results.get('successful_attacks', 0))
            
            with col3:
                st.metric("Failed Attacks", results.get('failed_attacks', 0))
            
            with col4:
                success_rate = (results.get('successful_attacks', 0) / results.get('total_attacks', 1)) * 100
                st.metric("Success Rate", f"{success_rate:.1f}%")
            
            # Attack type performance
            st.subheader("Attack Type Performance")
            
            attack_performance = results.get('attack_type_performance', {})
            if attack_performance:
                perf_df = pd.DataFrame([
                    {
                        'Attack Type': attack_type,
                        'Success Rate': perf['success_rate'],
                        'Total Attacks': perf['total'],
                        'Successful': perf['success']
                    }
                    for attack_type, perf in attack_performance.items()
                ])
                
                fig = px.bar(
                    perf_df,
                    x='Attack Type',
                    y='Success Rate',
                    title="Success Rate by Attack Type",
                    color='Success Rate',
                    color_continuous_scale='RdYlGn'
                )
                fig.update_xaxes(tickangle=45)
                st.plotly_chart(fig, use_container_width=True)
    
    def _render_performance_metrics(self):
        """Render performance metrics tab"""
        st.header("📈 Performance Metrics")
        
        # KDD data statistics
        st.subheader("KDD Dataset Statistics")
        
        stats = self.kdd_loader.get_data_statistics()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Total Samples", f"{stats.get('total_samples', 0):,}")
            st.metric("Feature Count", stats.get('feature_count', 0))
            st.metric("Attack Types", len(stats.get('attack_types', {})))
        
        with col2:
            st.metric("Normal Traffic", f"{stats.get('normal_percentage', 0):.1f}%")
            st.metric("Anomaly Traffic", f"{stats.get('anomaly_percentage', 0):.1f}%")
        
        # Attack category breakdown
        st.subheader("Attack Category Breakdown")
        
        attack_categories = stats.get('attack_categories', {})
        if attack_categories:
            fig = px.bar(
                x=list(attack_categories.keys()),
                y=list(attack_categories.values()),
                title="Attack Categories Distribution",
                color=list(attack_categories.values()),
                color_continuous_scale='Viridis'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # System performance (if available)
        st.subheader("System Performance")
        
        try:
            # Try to get system status from API
            response = requests.get(f"{self.api_base_url}/status", timeout=5)
            if response.status_code == 200:
                system_status = response.json()
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("System Running", "✅ Yes" if system_status.get('system_running') else "❌ No")
                
                with col2:
                    st.metric("Simulation Mode", "✅ Yes" if system_status.get('simulation_mode') else "❌ No")
                
                with col3:
                    total_sims = system_status.get('performance_metrics', {}).get('total_simulations', 0)
                    st.metric("Total Simulations", total_sims)
                
                # Performance trends
                st.subheader("Performance Trends")
                
                # This would typically come from historical data
                st.info("Performance trend data would be displayed here based on historical training runs.")
                
            else:
                st.warning("Unable to connect to system API")
        
        except Exception as e:
            st.warning(f"API connection failed: {e}")
    
    def _filter_data(self):
        """Filter data based on sidebar selections"""
        data = self.kdd_data.copy()
        
        # Filter by category
        if st.session_state.get('selected_category') != 'All':
            data = data[data['attack_category'] == st.session_state.selected_category]
        
        # Limit sample size
        sample_size = st.session_state.get('sample_size', 10000)
        if len(data) > sample_size:
            data = data.sample(n=sample_size, random_state=42)
        
        return data
    
    def _generate_time_series_data(self, data):
        """Generate simulated time series data"""
        # Create hourly attack counts
        hours = list(range(24))
        time_data = []
        
        for category in data['attack_category'].unique():
            category_data = data[data['attack_category'] == category]
            
            for hour in hours:
                # Simulate attack count based on category
                base_count = len(category_data) // 24
                if category == 'normal':
                    # Normal traffic peaks during business hours
                    multiplier = 1.5 if 9 <= hour <= 17 else 0.5
                else:
                    # Attacks are more common during off-hours
                    multiplier = 1.2 if hour < 6 or hour > 18 else 0.8
                
                attack_count = max(0, int(base_count * multiplier * np.random.uniform(0.5, 1.5)))
                
                time_data.append({
                    'hour': hour,
                    'attack_count': attack_count,
                    'attack_category': category
                })
        
        return pd.DataFrame(time_data)

def main():
    """Run the KDD Dashboard"""
    dashboard = KDDDashboard()
    dashboard.render_main_dashboard()

if __name__ == "__main__":
    main()
