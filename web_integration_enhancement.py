
# Web Integration for Real Estate Investment Toolkit
# Add this to your web_server.py to integrate toolkit data

def load_toolkit_data():
    """Load integrated toolkit data for web interface"""
    try:
        with open('web_integration_data.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {
            'states': [],
            'formulas': [],
            'tips': [],
            'market_data': {},
            'contact_count': 0
        }

# Enhanced route for toolkit dashboard
@app.route('/toolkit-dashboard')
def toolkit_dashboard():
    toolkit_data = load_toolkit_data()
    return render_template('toolkit_dashboard.html',
                         states=toolkit_data['states'],
                         formulas=toolkit_data['formulas'],
                         tips=toolkit_data['tips'],
                         market_data=toolkit_data['market_data'],
                         contact_count=toolkit_data['contact_count'])

# Enhanced deal finding with toolkit integration
@app.route('/enhanced-deals')
def enhanced_deals():
    # Load toolkit data
    toolkit_data = load_toolkit_data()

    # Get AI-powered deals
    scraper = RealEstateLeadScraper()
    deals = scraper.auto_find_deals()

    # Enhance deals with toolkit data
    enhanced_deals = []
    for deal in deals:
        # Add state-specific insights
        deal_state = deal.get('state', '')
        state_info = next((s for s in toolkit_data['states'] if s['name'] == deal_state), None)

        if state_info:
            deal['market_status'] = state_info['status']
            deal['investment_focus'] = state_info['focus']

        # Add formula calculations
        if 'price' in deal and 'noi' in deal:
            cap_rate = (deal['noi'] / deal['price']) * 100 if deal['price'] > 0 else 0
            deal['cap_rate'] = round(cap_rate, 2)

        enhanced_deals.append(deal)

    return render_template('enhanced_deals.html', deals=enhanced_deals)
