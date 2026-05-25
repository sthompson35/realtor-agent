# Realtor Agent Web Interface

A modern, responsive web dashboard for managing your AI-powered real estate acquisition platform.

## Features

- **Dashboard**: Real-time overview of deals, bot status, and key metrics
- **Deal Management**: Comprehensive deal tracking with filtering and bulk actions
- **Bot Management**: Monitor and control all AI acquisition bots
- **Analytics**: Performance metrics and data visualization
- **Reports**: Generate and download detailed reports
- **Settings**: Configure API keys, bot settings, and system preferences

## Quick Start

### Prerequisites

- Python 3.8+
- Flask (`pip install flask`)

### Running the Web Server

1. Navigate to the project directory:
   ```bash
   cd c:\realtor_agent
   ```

2. Install dependencies:
   ```bash
   pip install flask
   ```

3. Start the web server:
   ```bash
   python web_server.py
   ```

4. Open your browser and go to:
   - **Dashboard**: http://localhost:5000/
   - **Deals**: http://localhost:5000/deals
   - **Bots**: http://localhost:5000/bots
   - **Analytics**: http://localhost:5000/analytics
   - **Reports**: http://localhost:5000/reports
   - **Settings**: http://localhost:5000/settings

## Project Structure

```
web/
├── templates/          # HTML templates
│   ├── base.html      # Main layout template
│   ├── dashboard.html # Dashboard page
│   ├── deals.html     # Deal management page
│   ├── bots.html      # Bot management page
│   ├── analytics.html # Analytics page
│   ├── reports.html   # Reports page
│   └── settings.html  # Settings page
├── static/            # Static assets
│   ├── css/
│   │   └── style.css # Custom styles
│   ├── js/
│   │   └── main.js   # Main JavaScript
│   └── img/           # Images
└── server.py         # Flask web server
```

## Technologies Used

- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Framework**: Bootstrap 5.3 (Responsive design)
- **Charts**: Chart.js (Data visualization)
- **Icons**: Font Awesome 6.4
- **Backend**: Flask (Python web framework)

## API Endpoints

The web server provides REST API endpoints for data:

- `GET /api/deals` - Get all deals
- `GET /api/deals/{id}` - Get specific deal
- `GET /api/bots` - Get bot statuses
- `POST /api/bots/{name}/toggle` - Toggle bot on/off
- `GET /api/stats` - Get dashboard statistics
- `GET /api/analytics/{time_range}` - Get analytics data

## Customization

### Styling

Edit `web/static/css/style.css` to customize the appearance. The design uses CSS custom properties for easy theming.

### Templates

Modify the Jinja2 templates in `web/templates/` to change the layout and content.

### JavaScript

Update `web/static/js/main.js` to modify interactive behavior and API calls.

## Browser Support

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is part of the Realtor Agent system. See the main project license for details.

## Support

For support or questions, please refer to the main Realtor Agent documentation or create an issue in the project repository.