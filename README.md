# Crowdsourced Response Platform

A comprehensive platform for managing and coordinating emergency responses, events, and volunteer activities. The platform connects reporters, professional responders, and volunteers while facilitating resource donations and real-time communication.

## Features

### Core Functionality
- **Incident Reporting**: Users can report incidents that require professional attention
- **Event Management**: Create and manage community events
- **Resource Donation**: Support causes through various donation types:
  - Tools and Equipment
  - Monetary Contributions
  - Volunteer Labor
  - Professional Personnel

### User Roles
- **Reporters**: Any registered user can report incidents or create events
- **Professional Responders**: Verified professionals (e.g., doctors, engineers) who respond to incidents
- **Volunteers**: Community members who can offer assistance for events or incidents
- **Administrators**: Platform moderators with enhanced access
- **Super Administrators**: System-level administrators

### Communication Features
- Live chat functionality between users
- Forum discussions for incidents
- Messaging system for coordination

### Technical Features
- REST API built with Django REST Framework
- Real-time communication capabilities
- Location-based services (PostGIS) in development version
- Authentication and authorization system
- File storage and media handling

## Installation

### Prerequisites
- Python 3.8+
- pip
- Virtual environment (recommended)

### Basic Setup
1. Clone the repository:
```bash
git clone https://github.com/CodeLord2020/crowdsourced.git crowdsourced
cd crowdsourced
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Run migrations:
```bash
python manage.py migrate
```

6. Create superuser:
```bash
python manage.py createsuperuser
```

7. Run the development server:
```bash
python manage.py runserver
```

### Production Setup

For production deployment, additional steps are required:

1. Set `DEBUG=False` in settings
2. Configure your production database
3. Set up static files serving
4. Configure HTTPS
5. Set up proper email backend

A working example can be found at: crowdsourcelab.onrender.com

### PostGIS Setup (Optional)

For location-based features:

1. Install PostGIS:
```bash
# Ubuntu
sudo apt-get install postgis postgresql-12-postgis-3
```

2. Create spatial database:
```sql
CREATE EXTENSION postgis;
```

3. Update database settings in your .env file

## Project Structure

Main applications:
- `accounts`: User management and authentication
- `incident`: Incident reporting and management
- `Blogs`: Blogs about an Incident or Event
- `Forums`: Forum about an Incident or Event
- `event`: Event coordination
- `messaging`: Communication system
- `responders`: Professional responder management
- `volunteer`: Volunteer coordination
- `dashboard`: Administrative interface
- `cloud_resource`: Media Resources
- `cddp_resource`: Resource and donation management
- `cddp`: App Core

## API Documentation

The API is built using Django REST Framework. Swagger documentation can be accessed at localhost:8000 after running the server.

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request


## Contact

[rasheedbabatunde76@gmail.com]