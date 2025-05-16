# src/models/industry_transformation/electrification.py

import pandas as pd
import numpy as np
# from scipy.optimize import curve_fit # Potentially for fitting S-curves to data points

# --- Helper Functions for Adoption Modeling ---

def logistic_growth(year, l_max, k, year_mid):
    """
    Calculates the value of a logistic growth function (S-curve).

    Args:
        year (int or np.array): The year(s) for which to calculate the adoption rate.
        l_max (float): The maximum adoption rate (e.g., 1.0 for 100%).
        k (float): The growth rate (steepness of the curve).
        year_mid (float): The year at which adoption reaches 50% of l_max.

    Returns:
        float or np.array: The adoption rate(s).
    """
    try:
        return l_max / (1 + np.exp(-k * (year - year_mid)))
    except OverflowError:
        # Handle cases where exp term is too large, typically meaning year is far from year_mid
        if -k * (year - year_mid) > 0:
            return l_max # Approaching max adoption
        else:
            return 0.0   # Approaching zero adoption

# --- Simulation Functions for EV Adoption by Segment ---

def simulate_luxury_premium_ev_adoption(years, initial_params=None):
    """
    Simulates EV adoption for the luxury/premium segment.
    Framework target: 80%+ EV penetration by 2030.

    Args:
        years (np.array): Array of years for the simulation period (e.g., 2025 to 2040).
        initial_params (dict, optional): Parameters for the S-curve (l_max, k, year_mid).
                                         If None, default assumptions will be used.

    Returns:
        pd.DataFrame: DataFrame with years and simulated EV penetration rates.
    """
    # Parameters calibrated to achieve ~80% EV penetration by 2030, with max ~95%.
    # Based on framework target and OEM announcements (e.g., Volvo 100% by 2030).
    # l_max = 0.95 (max penetration)
    # k = 0.56 (growth rate)
    # year_mid = 2027 (year of 50% of l_max adoption)
    # Calculation: 0.80 = 0.95 / (1 + exp(-k * (2030 - 2027))) => k ~ 0.56 for year_mid = 2027
    default_luxury_params = {'l_max': 0.95, 'k': 0.56, 'year_mid': 2027}
    params = initial_params if initial_params else default_luxury_params
    
    penetration = logistic_growth(years, params['l_max'], params['k'], params['year_mid'])
    return pd.DataFrame({'Year': years, 'Luxury_Premium_EV_Penetration': penetration})

def simulate_mass_market_passenger_ev_adoption(years, region='Global', initial_params=None):
    """
    Simulates EV adoption for mass-market passenger vehicles.
    Framework target: Regional variation: 30-90% by 2035.

    Args:
        years (np.array): Array of years for the simulation period.
        region (str): Specific region to model. Options:
                     - 'Europe': 85% by 2035 (EU ban on new ICE vehicles by 2035)
                     - 'China': 80% by 2035 (strong government support)
                     - 'North_America': 70% by 2035 (more conservative adoption)
                     - 'Global': 70% by 2035 (weighted average)
        initial_params (dict, optional): Override parameters for the S-curve (l_max, k, year_mid).

    Returns:
        pd.DataFrame: DataFrame with years and simulated EV penetration rates for the region.
    """
    # Region-specific parameters (l_max, k, year_mid)
    region_params = {
        'Europe': {'l_max': 0.90, 'k': 0.5, 'year_mid': 2032},      # 85% by 2035
        'China': {'l_max': 0.85, 'k': 0.55, 'year_mid': 2031},      # 80% by 2035
        'North_America': {'l_max': 0.80, 'k': 0.45, 'year_mid': 2033}, # 70% by 2035
        'Global': {'l_max': 0.80, 'k': 0.4, 'year_mid': 2034}        # 70% by 2035
    }
    
    # Get parameters for the specified region, default to Global if not found
    default_params = region_params.get(region, region_params['Global'])
    params = initial_params if initial_params else default_params
    
    # Calculate penetration using logistic growth
    penetration = logistic_growth(years, params['l_max'], params['k'], params['year_mid'])
    return pd.DataFrame({'Year': years, f'Mass_Market_EV_Penetration_{region}': penetration})

def simulate_commercial_vehicle_ev_adoption(years, vehicle_class='Global_Average', initial_params=None):
    """
    Simulates EV adoption for commercial vehicles by class.
    Framework target: Differentiated timelines for Class 1-8.

    Args:
        years (np.array): Array of years for the simulation period.
        vehicle_class (str): Specific commercial vehicle class. Options:
                          - 'Class_1_2': Small delivery vans (fastest adoption)
                          - 'Class_3_5': Medium-duty trucks
                          - 'Class_6_7': Medium-heavy trucks
                          - 'Class_8': Heavy-duty trucks (slowest adoption)
                          - 'Bus': Transit and school buses
                          - 'Global_Average': Weighted average across all classes
        initial_params (dict, optional): Override parameters for the S-curve (l_max, k, year_mid).

    Returns:
        pd.DataFrame: DataFrame with years and simulated EV penetration rates for the class.
    """
    # Class-specific parameters (l_max, k, year_mid)
    # Lighter classes (1-3) adopt faster due to lower battery requirements and urban delivery use cases
    # Heavier classes (6-8) adopt more slowly due to higher battery costs and longer range requirements
    class_params = {
        'Class_1_2': {'l_max': 0.85, 'k': 0.5, 'year_mid': 2030},  # 80%+ by 2035
        'Class_3_5': {'l_max': 0.80, 'k': 0.45, 'year_mid': 2032},  # 70% by 2035
        'Class_6_7': {'l_max': 0.75, 'k': 0.4, 'year_mid': 2034},   # 60% by 2035
        'Class_8': {'l_max': 0.65, 'k': 0.35, 'year_mid': 2036},    # 50% by 2040
        'Bus': {'l_max': 0.90, 'k': 0.6, 'year_mid': 2029},          # 85% by 2035 (strong policy push)
        'Global_Average': {'l_max': 0.75, 'k': 0.4, 'year_mid': 2033}  # ~65% by 2035
    }
    
    # Get parameters for the specified class, default to Global_Average if not found
    default_params = class_params.get(vehicle_class, class_params['Global_Average'])
    params = initial_params if initial_params else default_params
    
    # Calculate penetration using logistic growth
    penetration = logistic_growth(years, params['l_max'], params['k'], params['year_mid'])
    return pd.DataFrame({'Year': years, f'Commercial_EV_Penetration_{vehicle_class}': penetration})

def simulate_two_three_wheeler_ev_adoption(years, region='Emerging_Markets', initial_params=None):
    """
    Simulates EV adoption for two/three-wheelers in emerging markets.
    Framework target: 60-85% by 2030.

    Two/three-wheelers are leading EV adoption in many emerging markets due to:
    - Lower battery costs relative to vehicle price
    - Well-suited for urban mobility
    - Strong policy support in countries like India and Southeast Asia

    Args:
        years (np.array): Array of years for the simulation period.
        region (str): Specific region. Options:
                    - 'India': ~75% by 2030 (strong policy push from FAME II)
                    - 'China': ~85% by 2030 (already high adoption, nearing saturation)
                    - 'Southeast_Asia': ~70% by 2030 (growing adoption)
                    - 'Africa': ~50% by 2030 (slower infrastructure development)
                    - 'Emerging_Markets': ~75% by 2030 (weighted average)
        initial_params (dict, optional): Override parameters for the S-curve (l_max, k, year_mid).

    Returns:
        pd.DataFrame: DataFrame with years and simulated EV penetration rates.
    """
    # Region-specific parameters (l_max, k, year_mid)
    region_params = {
        'India': {'l_max': 0.85, 'k': 1.0, 'year_mid': 2027},         # 75% by 2030
        'China': {'l_max': 0.90, 'k': 1.2, 'year_mid': 2025},         # 85% by 2030 (already high)
        'Southeast_Asia': {'l_max': 0.80, 'k': 0.9, 'year_mid': 2028}, # 70% by 2030
        'Africa': {'l_max': 0.70, 'k': 0.6, 'year_mid': 2032},        # 50% by 2030
        'Emerging_Markets': {'l_max': 0.85, 'k': 0.9, 'year_mid': 2027}  # 75% by 2030
    }
    
    # Get parameters for the specified region, default to 'Emerging_Markets' if not found
    default_params = region_params.get(region, region_params['Emerging_Markets'])
    params = initial_params if initial_params else default_params
    
    # Calculate penetration using logistic growth
    penetration = logistic_growth(years, params['l_max'], params['k'], params['year_mid'])
    return pd.DataFrame({'Year': years, f'Two_Three_Wheeler_EV_Penetration_{region}': penetration})

# --- Main Electrification Simulation Orchestrator (Example) ---

def run_electrification_simulation(start_year=2025, end_year=2040, save_to_csv=True):
    """
    Runs the full electrification adoption simulation across all segments and regions.
    
    Args:
        start_year (int): First year of the simulation.
        end_year (int): Last year of the simulation.
        save_to_csv (bool): Whether to save results to a CSV file.
        
    Returns:
        dict: Dictionary containing DataFrames for each segment and combined results.
    """
    years = np.arange(start_year, end_year + 1)
    
    # 1. Luxury/ Premium Segment
    luxury_adoption = simulate_luxury_premium_ev_adoption(years)
    
    # 2. Mass Market Passenger Vehicles by Region
    mass_market_regions = ['Global', 'Europe', 'China', 'North_America']
    mass_market_dfs = []
    for region in mass_market_regions:
        df = simulate_mass_market_passenger_ev_adoption(years, region=region)
        mass_market_dfs.append(df)
    mass_market_all = pd.concat(mass_market_dfs, axis=1)
    mass_market_all = mass_market_all.loc[:,~mass_market_all.columns.duplicated()]  # Remove duplicate 'Year' columns
    
    # 3. Commercial Vehicles by Class
    commercial_classes = ['Class_1_2', 'Class_3_5', 'Class_6_7', 'Class_8', 'Bus', 'Global_Average']
    commercial_dfs = []
    for vehicle_class in commercial_classes:
        df = simulate_commercial_vehicle_ev_adoption(years, vehicle_class=vehicle_class)
        commercial_dfs.append(df)
    commercial_all = pd.concat(commercial_dfs, axis=1)
    commercial_all = commercial_all.loc[:,~commercial_all.columns.duplicated()]
    
    # 4. Two/Three-Wheelers by Region
    two_wheeler_regions = ['India', 'China', 'Southeast_Asia', 'Africa', 'Emerging_Markets']
    two_wheeler_dfs = []
    for region in two_wheeler_regions:
        df = simulate_two_three_wheeler_ev_adoption(years, region=region)
        two_wheeler_dfs.append(df)
    two_wheeler_all = pd.concat(two_wheeler_dfs, axis=1)
    two_wheeler_all = two_wheeler_all.loc[:,~two_wheeler_all.columns.duplicated()]
    
    # Combine all results into a single DataFrame
    df_final = luxury_adoption
    for df in [mass_market_all, commercial_all, two_wheeler_all]:
        df_final = pd.merge(df_final, df, on='Year', how='outer')
    
    # Save to CSV if requested
    if save_to_csv:
        import os
        os.makedirs('../../data/processed_data', exist_ok=True)
        csv_path = f'../../data/processed_data/ev_adoption_simulation_{start_year}_{end_year}.csv'
        df_final.to_csv(csv_path, index=False)
        print(f"Simulation results saved to {os.path.abspath(csv_path)}")
    
    # Return all results in a dictionary
    return {
        'luxury': luxury_adoption,
        'mass_market': mass_market_all,
        'commercial': commercial_all,
        'two_wheelers': two_wheeler_all,
        'combined': df_final
    }

if __name__ == '__main__':
    # Example usage with visualization
    print("Running Electrification Simulation (2025-2040)...")
    
    # Run the simulation
    results = run_electrification_simulation(2025, 2040, save_to_csv=True)
    
    # Display summary of results
    combined_df = results['combined']
    print("\n=== Simulation Summary ===")
    print(f"Simulation Period: {combined_df['Year'].min()} - {combined_df['Year'].max()}")
    
    # Show key metrics for 2030 and 2035
    years_of_interest = [2030, 2035, 2040]
    print("\nKey Metrics:")
    for year in years_of_interest:
        if year in combined_df['Year'].values:
            row = combined_df[combined_df['Year'] == year].iloc[0]
            print(f"\n--- {year} ---")
            print(f"Luxury Premium EV Penetration: {row.get('Luxury_Premium_EV_Penetration', 0)*100:.1f}%")
            print(f"Mass Market EV Penetration (Global): {row.get('Mass_Market_EV_Penetration_Global', 0)*100:.1f}%")
            print(f"Commercial EV Penetration (Class 8): {row.get('Commercial_EV_Penetration_Class_8', 0)*100:.1f}%")
            print(f"2/3-Wheeler EV Penetration (India): {row.get('Two_Three_Wheeler_EV_Penetration_India', 0)*100:.1f}%")
    
    # Plotting the results
    try:
        import matplotlib.pyplot as plt
        import seaborn as sns
        
        # Set the style
        sns.set_theme(style="whitegrid")
        plt.figure(figsize=(14, 8))
        
        # Plot luxury and mass market adoption
        plt.subplot(2, 2, 1)
        plt.plot(combined_df['Year'], combined_df['Luxury_Premium_EV_Penetration']*100, label='Luxury/ Premium', marker='o')
        plt.plot(combined_df['Year'], combined_df['Mass_Market_EV_Penetration_Global']*100, label='Mass Market (Global)', marker='s')
        plt.title('Passenger Vehicle EV Adoption')
        plt.ylabel('EV Penetration (%)')
        plt.legend()
        plt.grid(True)
        
        # Plot mass market by region
        plt.subplot(2, 2, 2)
        for col in combined_df.columns:
            if 'Mass_Market_EV_Penetration_' in col and 'Global' not in col:
                region = col.replace('Mass_Market_EV_Penetration_', '')
                plt.plot(combined_df['Year'], combined_df[col]*100, label=region, marker='^')
        plt.title('Mass Market EV Adoption by Region')
        plt.ylabel('EV Penetration (%)')
        plt.legend()
        
        # Plot commercial vehicles by class
        plt.subplot(2, 2, 3)
        for col in combined_df.columns:
            if 'Commercial_EV_Penetration_Class_' in col:
                vehicle_class = col.replace('Commercial_EV_Penetration_', '')
                plt.plot(combined_df['Year'], combined_df[col]*100, label=vehicle_class, marker='*')
        plt.title('Commercial Vehicle EV Adoption by Class')
        plt.xlabel('Year')
        plt.ylabel('EV Penetration (%)')
        plt.legend()
        
        # Plot two/three wheelers by region
        plt.subplot(2, 2, 4)
        for col in combined_df.columns:
            if 'Two_Three_Wheeler_EV_Penetration_' in col and 'Emerging_Markets' not in col:
                region = col.replace('Two_Three_Wheeler_EV_Penetration_', '')
                plt.plot(combined_df['Year'], combined_df[col]*100, label=region, marker='x')
        plt.title('2/3-Wheeler EV Adoption by Region')
        plt.xlabel('Year')
        plt.ylabel('EV Penetration (%)')
        plt.legend()
        
        plt.tight_layout()
        
        # Save the figure
        import os
        os.makedirs('../../reports/figures', exist_ok=True)
        plt.savefig('../../reports/figures/ev_adoption_forecasts.png', dpi=300, bbox_inches='tight')
        print("\nVisualization saved to 'reports/figures/ev_adoption_forecasts.png'")
        
        plt.show()
        
    except ImportError:
        print("\nNote: Install matplotlib and seaborn for visualization:")
        print("pip install matplotlib seaborn")
    
    print("\nSimulation completed successfully!")
