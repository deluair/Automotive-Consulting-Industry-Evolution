"""
Tests for the New Mobility & Business Model Evolution simulation.
"""

import sys
import os
import unittest
import numpy as np
import pandas as pd
from pathlib import Path

# Add the src directory to the Python path
src_path = str(Path(__file__).parent.parent / 'src')
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from models.industry_transformation.new_mobility import (
    NewMobilitySimulator,
    MobilityServiceType,
    OwnershipModel,
    Region,
    VehicleSegment,
    run_new_mobility_simulation
)

class TestNewMobilitySimulation(unittest.TestCase):
    """Test cases for the New Mobility simulation."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.simulator = NewMobilitySimulator()
        self.years = np.arange(2020, 2041)
        
    def test_service_adoption_shape(self):
        """Test that service adoption returns correct shape."""
        # Only test service types that are actually implemented in the simulator
        test_services = [
            MobilityServiceType.RIDE_HAILING,
            MobilityServiceType.CAR_SHARING,
            MobilityServiceType.ROBOTAXI,
            MobilityServiceType.SUBSCRIPTION
        ]
        
        for service_type in test_services:
            with self.subTest(service_type=service_type):
                adoption = self.simulator.simulate_service_adoption(
                    self.years, service_type, Region.NORTH_AMERICA, VehicleSegment.MIDSIZE
                )
                self.assertEqual(adoption.shape, self.years.shape)
                self.assertTrue(np.all(adoption >= 0))
                self.assertTrue(np.all(adoption <= 1))
    
    def test_ownership_evolution_shares(self):
        """Test that ownership model shares sum to approximately 1."""
        ownership = self.simulator.simulate_ownership_evolution(
            self.years, Region.NORTH_AMERICA, VehicleSegment.MIDSIZE
        )
        total_shares = np.zeros_like(self.years, dtype=float)
        
        for model in OwnershipModel:
            total_shares += ownership[model]
        
        # Check that shares sum to approximately 1 (allowing for floating point errors)
        np.testing.assert_allclose(total_shares, 1.0, rtol=1e-10)
    
    def test_economics_calculation(self):
        """Test that economics calculations are reasonable."""
        # Test with known adoption rates
        adoption = np.linspace(0, 0.5, len(self.years))
        economics = self.simulator.calculate_service_economics(
            self.years, MobilityServiceType.ROBOTAXI, adoption
        )
        
        # Check that all required keys are present
        expected_keys = ['vehicles', 'revenue_millions', 'cost_millions', 'profit_millions', 'margin']
        for key in expected_keys:
            self.assertIn(key, economics)
        
        # Check that vehicles scale with adoption
        self.assertTrue(np.all(economics['vehicles'] == adoption * 1_000_000))
        
        # Check that profit = revenue - cost
        np.testing.assert_allclose(
            economics['profit_millions'],
            economics['revenue_millions'] - economics['cost_millions'],
            rtol=1e-10
        )
        
        # Check margin calculation (with division by zero protection)
        non_zero_revenue = economics['revenue_millions'] > 0
        if np.any(non_zero_revenue):
            np.testing.assert_allclose(
                economics['margin'][non_zero_revenue],
                economics['profit_millions'][non_zero_revenue] / economics['revenue_millions'][non_zero_revenue],
                rtol=1e-10
            )
    
    def test_full_simulation_output(self):
        """Test that the full simulation runs and produces expected outputs."""
        # Get the current working directory
        cwd = Path.cwd()
        print(f"Current working directory: {cwd}")
        
        # The simulation saves files in the src/data/processed_data/new_mobility directory
        output_dir = cwd / 'src' / 'data' / 'processed_data' / 'new_mobility'
        print(f"Expected output directory: {output_dir}")
        
        # Create output directory if it doesn't exist
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Clean up any existing files
        for file in output_dir.glob('*.csv'):
            try:
                file.unlink()
                print(f"Deleted existing file: {file}")
            except OSError as e:
                print(f"Error deleting {file}: {e}")
        
        try:
            print("Running simulation...")
            # Run a minimal simulation with default parameters
            results = run_new_mobility_simulation(2020, 2025)  # Shorter time frame for testing
            
            # Check that results have the expected structure
            self.assertIn('service_adoption', results)
            self.assertIn('ownership', results)
            self.assertIn('economics', results)
            
            # Check if files were created in the expected location
            service_file = output_dir / 'service_adoption.csv'
            ownership_file = output_dir / 'ownership_models.csv'
            economics_file = output_dir / 'economic_metrics.csv'
            
            print(f"Checking for files in: {output_dir}")
            print(f"Contents of {output_dir}:")
            for f in output_dir.glob('*'):
                print(f"  - {f.name}")
            
            # Check each file individually to see which ones exist
            self.assertTrue(service_file.exists(), f"File not found: {service_file}")
            self.assertTrue(ownership_file.exists(), f"File not found: {ownership_file}")
            self.assertTrue(economics_file.exists(), f"File not found: {economics_file}")
            
            # Verify the files have content
            for file in [service_file, ownership_file, economics_file]:
                self.assertGreater(file.stat().st_size, 0, f"File is empty: {file}")
            
        except Exception as e:
            print(f"Error during test: {e}")
            raise
            
        finally:
            # Clean up test files
            for file in output_dir.glob('*.csv'):
                try:
                    file.unlink()
                    print(f"Cleaned up: {file}")
                except OSError as e:
                    print(f"Error cleaning up {file}: {e}")
            
            # Try to remove the directory if it's empty
            try:
                output_dir.rmdir()
                print(f"Removed directory: {output_dir}")
            except OSError as e:
                print(f"Could not remove directory {output_dir}: {e}")

if __name__ == '__main__':
    unittest.main()
