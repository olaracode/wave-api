from Users.routes import user
from music.songs.routes import song
from music.projects.routes import project
from music.collaborators.routes import collaborator

api_routes_v1 = [user, song, project, collaborator]
