from flask import Blueprint, render_template

index_blueprint = Blueprint('index', __name__)

# Route for the main index page
@index_blueprint.route('/')
def index():
    """Render the main game interface."""
    return render_template('index.html')

# Route for the moon base page
@index_blueprint.route('/moon_base')
def moon_base():
    """Render the Moon Base interface."""
    return render_template('moon_base.html')

# Route for the galactic map page
@index_blueprint.route('/galactic_map')
def galactic_map():
    """Render the Galactic Map interface."""
    return render_template('galactic_map.html')

# Route for the alliance management page
@index_blueprint.route('/alliance_management')
def alliance_management():
    """Render the Alliance Management interface."""
    return render_template('alliance_management.html')

# Route for the galactic marketplace
@index_blueprint.route('/marketplace')
def marketplace():
    """Render the Galactic Marketplace interface."""
    return render_template('marketplace.html')
