"""
Tests for the Chinese Manufacturer Expansion simulation module.
"""

import unittest
from pathlib import Path
import numpy as np
import pandas as pd
from src.models.industry_reconfiguration.chinese_manufacturer_expansion import (
    ChineseExpansionSimulator,
    Region,
    MarketSegment,
    ChineseManufacturer,
    ExpansionStrategy,
    run_chinese_expansion_simulation
)

class TestChineseManufacturerExpansion(unittest.TestCase):
    """Test cases for the Chinese Manufacturer Expansion simulation."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.simulator = ChineseExpansionSimulator()
        self.test_regions = [Region.CHINA, Region.EUROPE, Region.NORTH_AMERICA]
        self.test_segments = [MarketSegment.EV, MarketSegment.MASS_MARKET]
        self.test_manufacturers = list(ChineseManufacturer)[:3]  # Test with first 3 manufacturers
    
    def test_initialization(self):
        """Test that the simulator initializes correctly."""
        self.assertIsNotNone(self.simulator.manufacturers)
        self.assertIsNotNone(self.simulator.market_conditions)
        self.assertGreater(len(self.simulator.manufacturers), 0)
        self.assertEqual(len(self.simulator.market_conditions), len(Region))
    
    def test_calculate_market_attractiveness(self):
        """Test market attractiveness calculation."""
        # Test with different regions and segments
        for region in self.test_regions:
            for segment in self.test_segments:
                attractiveness = self.simulator.calculate_market_attractiveness(region, segment)
                self.assertIsInstance(attractiveness, float)
                self.assertGreaterEqual(attractiveness, 0)
                
                # EV segments should generally be more attractive
                if segment == MarketSegment.EV:
                    ev_attractiveness = self.simulator.calculate_market_attractiveness(
                        region, MarketSegment.EV
                    )
                    mass_attractiveness = self.simulator.calculate_market_attractiveness(
                        region, MarketSegment.MASS_MARKET
                    )
                    self.assertGreaterEqual(ev_attractiveness, mass_attractiveness)
    
    def test_determine_strategy(self):
        """Test strategy determination logic."""
        # Test for new market entry
        strategy = self.simulator._determine_strategy(
            ChineseManufacturer.BYD, 
            Region.SOUTH_ASIA,  # New market for BYD
            MarketSegment.EV,
            2025
        )
        self.assertIn(strategy, [
            ExpansionStrategy.EXPORT, 
            ExpansionStrategy.JOINT_VENTURE, 
            ExpansionStrategy.BRAND_ACQUISITION
        ])
        
        # Test for existing market
        strategy = self.simulator._determine_strategy(
            ChineseManufacturer.GEELY, 
            Region.EUROPE,  # Geely has presence via Volvo
            MarketSegment.PREMIUM,
            2025
        )
        self.assertIn(strategy, [
            ExpansionStrategy.EXPORT,
            ExpansionStrategy.LOCAL_PRODUCTION
        ])
    
    def test_calculate_market_share(self):
        """Test market share calculation."""
        # Test with different strategies
        strategies = [
            ExpansionStrategy.EXPORT,
            ExpansionStrategy.LOCAL_PRODUCTION,
            ExpansionStrategy.JOINT_VENTURE
        ]
        
        for strategy in strategies:
            share = self.simulator._calculate_market_share(
                ChineseManufacturer.BYD,
                Region.EUROPE,
                MarketSegment.EV,
                2025,
                strategy,
                1000000  # Market size
            )
            self.assertIsInstance(share, float)
            self.assertGreaterEqual(share, 0)
            self.assertLessEqual(share, 1.0)  # Should not exceed 100%
    
    def test_simulate_expansion_structure(self):
        """Test the structure of simulation results."""
        results = self.simulator.simulate_expansion(
            2025, 2027,  # Shorter time frame for testing
            regions=self.test_regions,
            segments=self.test_segments
        )
        
        # Check top-level keys
        self.assertIn('market_share', results)
        self.assertIn('revenue', results)
        self.assertIn('strategy', results)
        
        # Check manufacturer level
        for mfg in self.test_manufacturers:
            self.assertIn(mfg, results['market_share'])
            self.assertIn(mfg, results['revenue'])
            self.assertIn(mfg, results['strategy'])
            
            # Check region level
            for region in self.test_regions:
                self.assertIn(region, results['market_share'][mfg])
                self.assertIn(region, results['revenue'][mfg])
                self.assertIn(region, results['strategy'][mfg])
                
                # Check segment level
                for segment in self.test_segments:
                    self.assertIn(segment, results['market_share'][mfg][region])
                    self.assertIn(segment, results['revenue'][mfg][region])
                    self.assertIn(segment, results['strategy'][mfg][region])
                    
                    # Check time series data
                    market_shares = results['market_share'][mfg][region][segment]
                    revenues = results['revenue'][mfg][region][segment]
                    strategies = results['strategy'][mfg][region][segment]
                    
                    self.assertEqual(len(market_shares), 3)  # 2025-2027
                    self.assertEqual(len(revenues), 3)
                    self.assertEqual(len(strategies), 3)
                    
                    # Market shares should be between 0 and 1
                    for share in market_shares:
                        self.assertGreaterEqual(share, 0)
                        self.assertLessEqual(share, 1.0)
    
    def test_run_simulation_function(self):
        """Test the run_chinese_expansion_simulation function."""
        # Get the project root directory
        project_root = Path(__file__).parent.parent
        output_dir = project_root / 'data' / 'processed_data' / 'chinese_expansion'
        
        # Clean up any existing files
        if output_dir.exists():
            for file in output_dir.glob('*'):
                file.unlink()
            output_dir.rmdir()
        
        # Run the simulation
        results = run_chinese_expansion_simulation(
            2025, 2026,  # Just 2 years for testing
            regions=[Region.CHINA, Region.EUROPE],
            segments=[MarketSegment.EV]
        )
        
        # Check basic structure
        self.assertIn('market_share', results)
        self.assertIn('revenue', results)
        self.assertIn('strategy', results)
        
        # Check that files were created
        output_file = output_dir / 'market_share_evolution.csv'
        summary_file = output_dir / 'market_share_summary.csv'
        
        self.assertTrue(output_file.exists(), f"Output file not found: {output_file}")
        self.assertTrue(summary_file.exists(), f"Summary file not found: {summary_file}")
        
        # Check file content
        df = pd.read_csv(output_file)
        self.assertGreater(len(df), 0, "Output file is empty")
        
        summary_df = pd.read_csv(summary_file)
        self.assertGreater(len(summary_df), 0, "Summary file is empty")

if __name__ == '__main__':
    unittest.main()
