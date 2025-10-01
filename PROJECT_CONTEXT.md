# Lunch Tag Project Context

## Project Overview

**Lunch Tag** is a Django-based web application designed to facilitate lunch pairings among users (likely students or colleagues). The system uses a sophisticated algorithm to create optimal pairings based on user preferences, including "crushes" (preferred lunch partners) and "strikes" (people they don't want to be paired with).

## Core Purpose

The application serves as a social matching system that:
- Connects users for lunch meetings
- Respects user preferences (crushes and strikes)
- Uses weighted graph algorithms to optimize pairings
- Prevents repeat pairings through edge weight reduction
- Supports both 2-person and 3-person groups when needed

## Technical Architecture

### Framework & Dependencies
- **Django 3.2.14** - Main web framework
- **PostgreSQL** - Database (local and production)
- **Cloudinary** - Image storage and management
- **NetworkX** - Graph algorithms for pairing optimization
- **Django Allauth** - Authentication with social providers (Google, ORCID, Twitter)
- **Bootstrap** - Frontend styling
- **Gunicorn** - WSGI server for production

### Project Structure

```
lunchTag/
├── config/                 # Django project configuration
│   ├── settings/          # Environment-specific settings
│   │   ├── base.py       # Common settings
│   │   ├── local.py      # Local development
│   │   └── production.py # Production deployment
│   ├── urls.py           # Main URL routing
│   └── wsgi.py           # WSGI configuration
├── core/                  # Main application
│   ├── models.py         # Database models
│   ├── views.py          # View logic
│   ├── forms.py          # Form definitions
│   ├── urls.py           # App URL routing
│   ├── utils.py          # Pairing algorithms
│   ├── authentication.py # Custom auth backend
│   └── management/       # Django management commands
│       └── commands/     # Custom commands
├── lunchTag/             # Static files and templates
│   ├── static/          # CSS, JS, images
│   └── templates/       # HTML templates
└── manage.py            # Django management script
```

## Data Models

### Profile Model
Extends Django's User model with:
- **Image**: Cloudinary-stored avatar
- **Active**: Boolean for participation status
- **Pronouns**: User's preferred pronouns
- **Phone**: Contact information
- **Strikes**: Many-to-many relationship with users to avoid
- **Crush**: Foreign key to preferred lunch partner
- **Tag Pairing**: Current lunch partner(s)
- **Has Tag Pairing**: Boolean flag for pairing status

### Edge Model
Represents relationships between users:
- **User1/User2**: The two users in the relationship
- **Active**: Whether the edge is currently valid
- **Weight**: Numerical weight for pairing algorithm (higher = more likely to pair)

### Pairing Model
Stores actual lunch pairings:
- **User1/User2**: Primary pair members
- **User3**: Optional third member for 3-person groups

## Core Algorithms

### Pairing Generation (`make_pairings()`)
1. Creates a weighted graph using NetworkX
2. Uses `max_weight_matching()` for optimal pairings
3. Handles 3-person groups for unmatched users
4. Validates against strikes and preferences
5. Returns status codes for different outcomes

### Edge Weight Management
- **Initial weight**: 100.0 for all new relationships
- **Crush bonus**: Weight × 2 for crush relationships
- **Post-pairing reduction**: Weight ÷ 10 after being paired
- **Strike handling**: Edges deactivated when users strike each other

## User Workflow

### Registration & Profile Setup
1. Users register with email, name, and password
2. Profile automatically created with default settings
3. Edges created between new user and all existing users
4. Users can upload avatar, set pronouns, and contact info

### Preference Management
- **Crushes**: Select up to 1 preferred lunch partner
- **Strikes**: Add multiple people to avoid (private to user)
- **Active Status**: Opt in/out of lunch tag participation

### Pairing Process (Admin)
1. **Create Pairings**: Generate optimal pairings using algorithm
2. **Review**: Check pairings for errors or issues
3. **Push**: Deploy pairings to all users
4. **Weight Adjustment**: Reduce weights of newly paired users

## Management Commands

### `pair.py`
- Creates and pushes pairings in one command
- Used for automated pairing generation

### `merge.py`
- Merges two user accounts
- Transfers all relationships and preferences
- Useful for duplicate account cleanup

### `deactivate.py`
- Deactivates all users (end of semester)
- Clears all pairings and preferences
- Resets system for new term

### `countActive.py`
- Reports number of active vs total users
- Useful for pairing feasibility assessment

### `wipe.py`
- Resets all user preferences and pairings
- Maintains user accounts but clears data
- Used between lunch tag rounds

## Authentication & Security

### Custom Authentication
- Email-based login (username field stores email)
- Custom backend for email authentication
- Social authentication via Django Allauth

### User Permissions
- **Regular Users**: Manage own profile and preferences
- **Pairer Group**: Access to pairing management interface
- **Superusers**: Full admin access

## Deployment

### Production Setup
- **Heroku**: Primary deployment platform
- **PostgreSQL**: Database via Heroku Postgres
- **Cloudinary**: Image storage and CDN
- **Environment Variables**: Secret keys and API credentials
- **WhiteNoise**: Static file serving

### Environment Configuration
- **Local**: SQLite/PostgreSQL for development
- **Production**: Heroku with environment variables
- **Settings**: Modular configuration per environment

## Key Features

### User Interface
- **Homepage**: Shows current lunch partner(s)
- **Account Page**: Manage preferences and profile
- **Admin Interface**: Pairing management for authorized users
- **Responsive Design**: Bootstrap-based mobile-friendly UI

### Social Features
- **Profile Pictures**: Cloudinary-hosted avatars
- **Contact Information**: Phone numbers for coordination
- **Pronouns**: Inclusive identity support
- **Private Preferences**: Strikes are user-only visible

### Algorithm Intelligence
- **Weight Optimization**: Maximizes satisfaction through weighted matching
- **Strike Prevention**: Never pairs users who have struck each other
- **Repeat Avoidance**: Reduces likelihood of repeat pairings
- **Flexible Grouping**: Supports both pairs and trios

## Business Logic

### Pairing Constraints
1. Users cannot be paired with their strikes
2. Users cannot be paired with themselves
3. Superusers are excluded from pairings
4. Inactive users are excluded from pairings
5. Crush relationships increase pairing probability

### Edge Cases Handled
- **Odd Numbers**: Creates 3-person groups when needed
- **No Valid Pairings**: Error handling and admin notification
- **Strike Conflicts**: Validation and error reporting
- **Weight Overflow**: Automatic weight reduction after pairings

## Integration Points

### External Services
- **Cloudinary**: Image upload, storage, and transformation
- **Social Auth**: Google, ORCID, Twitter login options
- **Email**: User registration and notifications
- **Heroku**: Deployment and database hosting

### Data Flow
1. **User Registration** → Profile Creation → Edge Population
2. **Preference Updates** → Edge Weight Modification
3. **Pairing Generation** → Algorithm Execution → Validation
4. **Pairing Deployment** → User Notification → Weight Adjustment

This system represents a sophisticated social matching application with robust algorithms, user-friendly interfaces, and comprehensive admin tools for managing lunch pairings in an educational or workplace setting.
