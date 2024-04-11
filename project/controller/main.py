from flask import Blueprint, render_template, url_for, redirect, request
from flask_wtf import FlaskForm
from jinja2 import UndefinedError
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired
from project.object.locations import db as towns_db, Location
from project.utils.cookies import get_current_user
from project.utils.database import db
from project.utils.weather import (get_current_weather_by_ip, get_current_weather, get_weather_forecast,
                                   get_weather_history)

main = Blueprint('main', __name__)


class WeatherForm(FlaskForm):
    city = StringField("City Name", validators=[InputRequired()],
                       render_kw={"class": "form-control", "placeholder": "City Name"})
    get_weather = SubmitField("Get Weather", render_kw={"class": "btn btn-primary"})
    add_to_favorites = SubmitField("Add to Favorites", render_kw={"class": "btn btn-success"})


@main.route('/', methods=['POST'])
def post():
    user = get_current_user()
    if not user:
        return redirect(url_for('user.signIn'))

    weather_form = WeatherForm(request.form)
    if weather_form.validate():
        city_name = weather_form.city.data
        add_to_favorites = weather_form.add_to_favorites.data

        if city_name:
            if add_to_favorites:
                new_town = Location(city_name, user)
                try:
                    towns_db.session.add(new_town)
                    towns_db.session.commit()
                except Exception as e:
                    towns_db.session.rollback()
                    error = "Cannot add new town."
                    return render_template('error.html', error=error)

    return redirect(url_for('main.get'))


@main.route('/', methods=['GET'])
def get():
    form = WeatherForm()
    current_weather_from_ip = get_current_weather_by_ip()
    current_weather_fail = get_current_weather("Liberec")
    user = get_current_user()
    favorites = get_favorites()
    try:
        if user:
            return render_template('index.html', user=user, current_weather_from_ip=current_weather_from_ip, form=form,
                                   favorite_locations=favorites)
        else:
            return render_template('index.html', user=user, current_weather_from_ip=current_weather_from_ip, form=form)
    except Exception as e:
        return render_template('index.html', user=user, current_weather_from_ip=current_weather_fail, form=form,
                               favorite_locations=favorites)

@main.route('/weather', methods=['GET', 'POST'])
def weather():
    weather_form = WeatherForm(request.form)
    location = request.args.get('location')
    if location:
        current_weather_data = get_current_weather(location)
        favorites = get_favorites()
        user = get_current_user()
        forecast_weather_data = get_weather_forecast(location)
        history_weather_data = get_weather_history(location)

        if user and location in favorites:
            return render_template('index.html', current_weather=current_weather_data, forecast=forecast_weather_data,
                                   form=weather_form, user=user, favorite_locations=favorites,
                                   history=history_weather_data)
        else:
            return render_template('index.html', current_weather=current_weather_data, forecast=forecast_weather_data,
                                   form=weather_form, user=user, favorite_locations=favorites)

    try:
        if weather_form.validate_on_submit():
            city_name = weather_form.city.data
            current_weather_data = get_current_weather(city_name)
            user = get_current_user()

            if user and user.getSubscribed():
                favorites = get_favorites()
                forecast_weather_data = get_weather_forecast(city_name)
                history_weather_data = get_weather_history(city_name)

                if city_name in favorites:
                    return render_template('index.html', current_weather=current_weather_data,
                                           forecast=forecast_weather_data, form=weather_form, user=user,
                                           favorite_locations=favorites, history=history_weather_data)
                else:
                    return render_template('index.html', current_weather=current_weather_data,
                                           forecast=forecast_weather_data, form=weather_form, user=user,
                                           favorite_locations=favorites)
            else:
                return render_template('index.html', current_weather=current_weather_data, form=weather_form, user=user)
    except UndefinedError:
        return redirect(url_for('main.get'))


@main.route('/addToFavourite')
def add_to_favourite():
    location = request.args.get('location')
    form = WeatherForm()
    user = get_current_user()
    if not user:
        return redirect(url_for('user.signIn'))

    try:
        location_new = Location(location, user)
        db.session.add(location_new)
        db.session.commit()
        return redirect(url_for('main.weather', location=location))
    except Exception as e:
        db.session.rollback()
        error_message = "Unable to add to favourite."
        return render_template('index.html', error=error_message, form=form, user=user)


def get_favorites():
    user = get_current_user()
    if user:
        favorite_locations = Location.query.filter_by(user_id=user.id).all()
        favorite_location_names = [location.location for location in favorite_locations]
        return favorite_location_names
    else:
        return []

