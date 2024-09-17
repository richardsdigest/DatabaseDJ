from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import InputRequired, Length

class PlaylistForm(FlaskForm):
    """Form for adding a new playlist."""
    
    name = StringField("Playlist Name", validators=[InputRequired(), Length(max=100)])
    description = StringField("Description", validators=[Length(max=200)])


class SongForm(FlaskForm):
    """Form for adding a new song."""
    
    title = StringField("Song Title", validators=[InputRequired(), Length(max=100)])
    artist = StringField("Artist", validators=[InputRequired(), Length(max=100)])
