# Lunch Tag

A Django web application that facilitates lunch pairings among users using intelligent matching algorithms. Users can set preferences for who they'd like to have lunch with (crushes) and who they'd prefer to avoid (strikes), and the system creates optimal pairings using weighted graph algorithms.

## Features

- **Smart Pairing Algorithm**: Uses NetworkX to create optimal lunch pairings based on user preferences
- **User Preferences**: Set crushes (preferred partners) and strikes (people to avoid)
- **Flexible Grouping**: Supports both 2-person and 3-person lunch groups
- **Profile Management**: Upload avatars, set pronouns, and manage contact information
- **Social Authentication**: Login with Google, ORCID, or Twitter
- **Admin Tools**: Comprehensive pairing management for administrators
- **Repeat Prevention**: Algorithm reduces likelihood of repeat pairings

## Prerequisites

- Python 3.10.5
- PostgreSQL
- Git

## Local Development Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd lunchTag
```

### 2. Create and Activate Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Variables

Create a `.env` file in the project root with the following variables:

```bash
# Required for Django
LUNCH_TAG_SECRET_KEY=your-secret-key-here

# Required for local PostgreSQL
POSTGRES_PW=your-postgres-password

# Optional: Cloudinary (for image uploads)
API_KEY=your-cloudinary-api-key
API_SECRET=your-cloudinary-api-secret
```

**Note**: For local development, you can use a simple secret key. For production, use a secure, randomly generated key.

### 5. Database Setup

#### Install PostgreSQL
- **Ubuntu/Debian**: `sudo apt-get install postgresql postgresql-contrib`
- **macOS**: `brew install postgresql`
- **Windows**: Download from [postgresql.org](https://www.postgresql.org/download/windows/)

#### Create Database
```bash
# Connect to PostgreSQL
sudo -u postgres psql

# Create database and user
CREATE DATABASE lunch_tag_local;
CREATE USER postgres WITH PASSWORD p63d953baf7e23b5157ddffed11b;
GRANT ALL PRIVILEGES ON DATABASE lunch_tag_local TO postgres;
\q
```

### 6. Django Setup

```bash
# Run migrations
python manage.py migrate

# Create superuser (optional, for admin access)
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic
```

### 7. Run Development Server

```bash
# Set Django settings to local
export DJANGO_SETTINGS_MODULE=config.settings.local

# Run server
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`

## Usage

### For Regular Users

1. **Register**: Create an account with your email and name
2. **Set Preferences**: 
   - Add a crush (preferred lunch partner)
   - Add strikes (people you'd prefer not to be paired with)
3. **View Pairings**: Check your homepage to see your current lunch partner(s)
4. **Manage Profile**: Upload a photo, set pronouns, and add contact information

### For Administrators

1. **Access Admin Panel**: Go to `/admin/` and login with superuser credentials
2. **Manage Pairings**: Use the "Edit Pairings" page to:
   - Create new pairings using the algorithm
   - Review pairings before pushing to users
   - Push pairings to make them visible to all users

### Management Commands

```bash
# Create and push pairings
python manage.py pair

# Count active users
python manage.py countActive

# Deactivate all users (end of semester)
python manage.py deactivate

# Reset all preferences and pairings
python manage.py wipe

# Merge two user accounts
python manage.py merge old_username new_username
```

## Project Structure

```
lunchTag/
├── config/                 # Django project configuration
│   ├── settings/          # Environment-specific settings
│   └── urls.py           # Main URL routing
├── core/                  # Main application
│   ├── models.py         # Database models (Profile, Edge, Pairing)
│   ├── views.py          # View logic
│   ├── utils.py          # Pairing algorithms
│   └── management/       # Custom Django commands
├── lunchTag/             # Static files and templates
│   ├── static/          # CSS, JS, images
│   └── templates/       # HTML templates
└── requirements.txt      # Python dependencies
```

## Key Files

- **`core/models.py`**: Database models for users, relationships, and pairings
- **`core/utils.py`**: Core pairing algorithm using NetworkX
- **`core/views.py`**: Web interface logic
- **`config/settings/`**: Environment-specific Django settings
- **`lunchTag/templates/`**: HTML templates for the web interface

## Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Ensure PostgreSQL is running
   - Check database credentials in `.env` file
   - Verify database exists

2. **Static Files Not Loading**
   - Run `python manage.py collectstatic`
   - Check `STATIC_ROOT` and `STATIC_URL` settings

3. **Image Upload Issues**
   - Cloudinary credentials required for image uploads
   - For local development, you can disable image uploads

4. **Pairing Algorithm Errors**
   - Check that users have valid preferences
   - Ensure no users are paired with their strikes
   - Use admin interface to review pairings before pushing

### Development Tips

- Use Django's debug toolbar for development
- Check Django logs for detailed error messages
- Use the admin interface to manage users and test functionality
- Test pairing algorithms with small user sets first

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

[Add your license information here]

## Support

For technical support or questions about the pairing algorithm, contact the development team or refer to the `PROJECT_CONTEXT.md` file for detailed technical documentation.
