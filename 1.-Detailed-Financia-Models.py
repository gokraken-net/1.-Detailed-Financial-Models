
import pandas as pd
import numpy as np

def calculate_token_emissions(total_supply=1_000_000_000, months=48):
    """Calculate monthly token emissions and financial metrics"""
    
    # Token allocation and prices
    allocations = {
        'seed': {'percentage': 0.05, 'price': 0.04, 'lockup': 6, 'vesting': 18},
        'strategic': {'percentage': 0.10, 'price': 0.06, 'lockup': 3, 'vesting': 15},
        'public': {'percentage': 0.14, 'price': 0.07, 'lockup': 0, 'vesting': 12},
        'ido': {'percentage': 0.06, 'price': 0.08, 'lockup': 0, 'vesting': 3},
        'network_rewards': {'percentage': 0.20, 'vesting': 48},
        'developer_incentives': {'percentage': 0.10, 'vesting': 36},
        'team_advisors': {'percentage': 0.20, 'lockup': 12, 'vesting': 36},
        'operations': {'percentage': 0.10, 'vesting': 48},
        'reserve': {'percentage': 0.05, 'lockup': 24}
    }
    
    # Initialize monthly emission dataframe
    df = pd.DataFrame(index=range(months))
    
    # Calculate emissions for each allocation
    for category, params in allocations.items():
        tokens = total_supply * params['percentage']
        lockup = params.get('lockup', 0)
        vesting = params.get('vesting', 0)
        
        if category == 'ido':
            # Special case for IDO with 50% upfront
            initial_release = tokens * 0.5
            remaining = tokens * 0.5
            monthly = remaining / vesting
            emissions = [0] * lockup + [initial_release] + [monthly] * (vesting - 1)
        else:
            monthly = tokens / vesting if vesting > 0 else 0
            emissions = [0] * lockup + [monthly] * (vesting if vesting > 0 else 1)
        
        df[f'{category}_emissions'] = emissions[:months] + [0] * (months - len(emissions))
    
    # Calculate cumulative metrics
    df['monthly_emissions'] = df.sum(axis=1)
    df['cumulative_supply'] = df['monthly_emissions'].cumsum()
    
    return df

def project_network_metrics(months=48, initial_users=6000, initial_models=270000):
    """Project network growth and usage metrics"""
    
    # Growth assumptions
    monthly_user_growth = 0.40  # 40% monthly growth
    monthly_model_growth = 0.35  # 35% monthly model growth
    compute_cost_savings = 0.90  # 90% cost savings vs traditional
    
    # Initialize projections dataframe
    df = pd.DataFrame(index=range(months))
    
    # Calculate user and model growth
    df['active_users'] = [initial_users * (1 + monthly_user_growth) ** i for i in range(months)]
    df['models_processed'] = [initial_models * (1 + monthly_model_growth) ** i for i in range(months)]
    
    # Calculate compute metrics
    avg_compute_cost_per_model = 5  # USD
    df['traditional_compute_costs'] = df['models_processed'] * avg_compute_cost_per_model
    df['kraken_compute_costs'] = df['traditional_compute_costs'] * (1 - compute_cost_savings)
    df['cost_savings'] = df['traditional_compute_costs'] - df['kraken_compute_costs']
    
    # Calculate network revenue
    take_rate = 0.20  # 20% platform fee
    df['network_revenue'] = df['kraken_compute_costs'] * take_rate
    
    return df

def calculate_token_metrics(total_supply=1_000_000_000, initial_price=0.08):
    """Calculate key token metrics"""
    
    emissions_df = calculate_token_emissions(total_supply)
    network_df = project_network_metrics()
    
    # Combine metrics
    df = pd.concat([emissions_df, network_df], axis=1)
    
    # Calculate token metrics
    df['token_price'] = initial_price  # Simplified - would need market dynamics model
    df['market_cap'] = df['cumulative_supply'] * df['token_price']
    df['fully_diluted_valuation'] = total_supply * df['token_price']
    
    return df

# Generate projections
projections = calculate_token_metrics()

# Print key metrics for first 12 months
print("\nMonthly Projections (First Year):")
print(projections.head(12)[['active_users', 'models_processed', 'network_revenue', 'market_cap']])

# Calculate key statistics
initial_circulating = projections['cumulative_supply'][0]
initial_market_cap = initial_circulating * 0.08  # Initial token price
total_raise = (50_000_000 * 0.04) + (100_000_000 * 0.06) + (140_000_000 * 0.07) + (60_000_000 * 0.08)

print("\nKey Token Metrics:")
print(f"Initial Circulating Supply: {initial_circulating:,.0f} $INK")
print(f"Initial Market Cap: ${initial_market_cap:,.2f}")
print(f"Total Raise: ${total_raise:,.2f}")
Made with
Artifacts are user-generated and may contain unverified or potentially unsafe content.
Report
Remix Artifact

