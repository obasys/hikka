from hikka.modules import releases
from hikka.modules import genres
from hikka.modules import types
from hikka.modules import teams
from hikka.modules import auth
from hikka import api

# Auth routes
api.add_resource(auth.Join, "/api/join")
api.add_resource(auth.Login, "/api/login")
api.add_resource(auth.Activate, "/api/activate/<string:token>")

# Team routes
api.add_resource(teams.NewTeam, "/api/teams/new")

# Genre routes
api.add_resource(genres.NewGenre, "/api/genres/new")
api.add_resource(genres.UpdateGenre, "/api/genres/update")

# Type routes
api.add_resource(types.NewReleaseType, "/api/types/new")
api.add_resource(types.UpdateReleaseType, "/api/types/update")

# Release routes
api.add_resource(releases.NewRelease, "/api/releases/new")
