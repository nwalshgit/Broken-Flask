# app/home/forms.py

from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from ..models import Location, Area

class LocationForm(FlaskForm):
    """Form for admins to create Locations(Buildings,Stores,home) that store food"""
    location= StringField('Location', validators=[DataRequired()])
    submit = SubmitField('Submit')
    def validate_location(self, field):
        if Location.query.filter_by(location=field.data).first():
            raise ValidationError('Location is already in use.')

class AreaForm(FlaskForm):
    """Form for admins to create Areas(places within home or store, like cabinet or aisles)"""
    area= StringField('Area', validators=[DataRequired()])
    location= QuerySelectField(query_factory=lambda: Location.query.all(), get_label="location")
    listorder= IntegerField('List Order', validators=[DataRequired()])
    submit = SubmitField('Submit')
    #def validate_area(self, field):
    #    if Area.query.filter_by(area=field.data).first():
    #        raise ValidationError('Area is already in use.')

