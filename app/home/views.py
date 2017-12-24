# app/home/views.py

from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from . import home
from .forms import LocationForm, AreaForm
from .. import db
from ..models import Location, Area

# home page
@home.route('/')
def homepage():
    """Render the homepage template on the / route"""
    return render_template('home/index.html', title="Welcome")

# user dashboard
@home.route('/dashboard')
@login_required
def dashboard():
    """Render the dashboard template on the /dashboard route"""
    return render_template('home/dashboard.html', title="Dashboard")

# admin dashboard
@home.route('/admin.dashboard')
@login_required
def admin_dashboard():
    #prevent non-admins from accessing the page
    if not current_user.is_admin:
        abort(403)
    return render_template('home/admin_dashboard.html',title="Dashboard")

# Location Views

#Read Locations
@home.route('/locations', methods=['GET'])
#@login_required
def list_locations():
    """List all locations"""
    locations = Location.query.all()
    return render_template('home/locations/locations.html',
                           locations=locations, title="Locations")

#creates a blank form if GET (no form data) or POST (fowith form failing validation)
#submits the form to Create a Location if POST (with valid data)
@home.route('/location', methods=['GET', 'POST'])
#@login_required
def add_location():
    """Add a location to the database"""
    add_location = True
    form = LocationForm()
    if form.validate_on_submit():
        print(form)
        location = Location(location=form.location.data)
        try:
            #add location to database
            db.session.add(location)
            db.session.commit()
            flash('You have successfully added a new location.')
        except:
            #in case location name exists
            flash('Error: Most likely cause is the location name already exists.')
        #redirects to the locations page
        return redirect(url_for('home.list_locations'))
    # load location template
    return render_template('home/locations/location.html', action="Add",
                           add_location=add_location, form=form, title="Add Location")

# PUT is an HTTP concept not HTML.  However, <form action=”http://www.example.org/users/123” method=”put” if-none-match=”*”> may work...
#@home.route('/location/<int:id>', methods=['PUT'])
#creates an edit form if GET (reads data from db) or POST (with form failing validation)
#submits the form to Edit a Location if POST (with valid data)
@home.route('/location/<int:id>/edit', methods=['GET', 'POST'])  #TODO THIS SHOULD BE POST AT A MINIMUM
@login_required
def edit_location(id):
    """ Edit a location """
    add_location = False
    location = Location.query.get_or_404(id)
    form = LocationForm(obj=location)
    if form.validate_on_submit():
        location.location = form.location.data
        db.session.commit()
        flash('You have successfully edited the location.')
        #redirect to the locations page
        return redirect(url_for('home.list_locations'))
    form.location.data = location.location
    return render_template('home/locations/location.html', action="Edit",
                           add_location=add_location, form=form,
                           location=location, title="Edit Location")

@home.route('/location/<int:id>/delete', methods=['GET'])  #THIS SHOULD BE POST AT A MINIMUM
@home.route('/location/<int:id>', methods=['DELETE'])
@login_required
def delete_location(id):
    """ Delete a Location from the database """
    location = Location.query.get_or_404(id)
    db.session.delete(location)
    db.session.commit()
    flash('You have successfully deleted the location.');
    #redirect tot the locations page
    return redirect(url_for('home.list_locations'))
    return render_template(title="Delete Location");

# Area Views

#Read Areas
@home.route('/location/<int:location_id>/areas', methods=['GET'])
#@login_required
def list_areas(location_id):
    """List all locations"""
    areas = Area.query.all()
    location_name=Location.query.filter_by(id=location_id).first().location
    return render_template('home/locations/areas.html',
            areas=areas, title="Areas", location_name=location_name, location_id=location_id)

#creates a blank form if GET (no form data) or POST (fowith form failing validation)
#submits the form to Create a Location if POST (with valid data)
@home.route('/location/<int:location_id>/area', methods=['GET', 'POST'])
#@login_required
def add_area(location_id):
    """Add an area to the database"""
    add_area = True
    form = AreaForm()
    if form.validate_on_submit():
        print(form)
        area = Area(area=form.area.data, location=form.location.data, listorder=form.listorder.data)
        try:
            #add area to database
            db.session.add(area)
            db.session.commit()
            flash('You have successfully added a new area.')
        except:
            #in case location name exists
            flash('Error: Most likely cause is the area name already exists. ')
        #redirects to the locations page
        return redirect(url_for('home.list_areas', location_id=location_id))
    # load area template
    return render_template('home/locations/area.html', action="Add",
                           add_area=add_area, form=form, title="Add Area")

# PUT is an HTTP concept not HTML.  However, <form action=”http://www.example.org/users/123” method=”put” if-none-match=”*”> may work...
#@home.route('/area/<int:id>', methods=['PUT'])
#creates an edit form if GET (reads data from db) or POST (with form failing validation)
#submits the form to Edit an Area if POST (with valid data)
@home.route('/area/<int:id>/edit', methods=['GET', 'POST'])  #TODO THIS SHOULD BE POST AT A MINIMUM
@login_required
def edit_area(id):
    """ Edit an area """
    add_area = False
    area = Area.query.get_or_404(id)
    form = AreaForm(obj=area)
    if form.validate_on_submit():
        area.area = form.area.data
        area.location = form.location.data
        area.listorder = form.listorder.data
        db.session.add(area)
        db.session.commit()
        flash('You have successfully edited the area.')
        #redirect to the areas page
        return redirect(url_for('home.list_areas', location_id=area.location.location_id))
    form.area.data = area.area
    return render_template('home/locations/area.html', action="Edit",
                           add_area=add_area, form=form,
                           area=area, title="Edit Area")

@home.route('/area/<int:id>/delete', methods=['GET'])  #THIS SHOULD BE POST AT A MINIMUM
@home.route('/area/<int:id>', methods=['DELETE'])
@login_required
def delete_area(id):
    """ Delete an area from the database """
    area = Area.query.get_or_404(id)
    db.session.delete(area)
    db.session.commit()
    flash('You have successfully deleted the area.');
    #redirect tot the areas page
    return redirect(url_for('home.list_areas'))
    return render_template(title="Delete Area");
    
