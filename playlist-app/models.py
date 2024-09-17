from flask import Flask, render_template, redirect, flash
from models import db, connect_db, Playlist, Song, PlaylistSong
from forms import PlaylistForm, SongForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///your_database_name'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'

connect_db(app)

@app.route('/playlists/new', methods=['GET', 'POST'])
def create_playlist():
    """Create a new playlist."""
    
    form = PlaylistForm()
    
    if form.validate_on_submit():
        name = form.name.data
        description = form.description.data
        
        new_playlist = Playlist(name=name, description=description)
        db.session.add(new_playlist)
        db.session.commit()
        
        flash("Playlist created successfully!", "success")
        return redirect('/')
    
    return render_template('new_playlist.html', form=form)

@app.route('/songs/new', methods=['GET', 'POST'])
def create_song():
    """Create a new song."""
    
    form = SongForm()
    
    if form.validate_on_submit():
        title = form.title.data
        artist = form.artist.data
        
        new_song = Song(title=title, artist=artist)
        db.session.add(new_song)
        db.session.commit()
        
        flash("Song added successfully!", "success")
        return redirect('/')
    
    return render_template('new_song.html', form=form)

# Additional view function for the homepage or playlists
@app.route('/')
def home():
    """Display playlists or homepage."""
    playlists = Playlist.query.all()
    return render_template('index.html', playlists=playlists)

@app.route("/playlists/<int:playlist_id>/add-song", methods=["GET", "POST"])
def add_song_to_playlist(playlist_id):
"""Add a playlist and redirect to list."""

  playlist = Playlist.query.get_or_404(playlist_id)
  form = NewSongForPlaylistForm()

  # Restrict form to songs not already on this playlist

  curr_on_playlist = [s.id for s in playlist.songs]
  form.song.choices = (db.session.query(Song.id, Song.title)
                      .filter(Song.id.notin_(curr_on_playlist))
                      .all())

  if form.validate_on_submit():

      # This is one way you could do this ...
      playlist_song = PlaylistSong(song_id=form.song.data,
                                  playlist_id=playlist_id)
      db.session.add(playlist_song)

      # Here's another way you could that is slightly more ORM-ish:
      #
      # song = Song.query.get(form.song.data)
      # playlist.songs.append(song)

      # Either way, you have to commit:
      db.session.commit()

      return redirect(f"/playlists/{playlist_id}")

  return render_template("add_song_to_playlist.html",
                         playlist=playlist,
                         form=form)