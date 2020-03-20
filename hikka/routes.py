from hikka.modules import descriptors
from hikka.modules import episodes
from hikka.modules import system
from hikka.modules import anime
from hikka.modules import teams
from hikka.modules import votes
from hikka.modules import jikan
from hikka.modules import auth
from hikka import errors
import flask

def init(api, app):
    # Auth routes
    api.add_resource(auth.Join, "/auth/join")
    api.add_resource(auth.Login, "/auth/login")
    api.add_resource(auth.Activate, "/auth/activate")

    # Team routes
    api.add_resource(teams.NewTeam, "/teams/new")
    api.add_resource(teams.GetTeam, "/teams/get/<string:slug>")
    api.add_resource(teams.AddMember, "/teams/member/add")
    api.add_resource(teams.RemoveMember, "/teams/member/remove")

    # Descriptor routes
    api.add_resource(descriptors.NewDescriptor, "/descriptors/new")
    api.add_resource(descriptors.UpdateDescriptor, "/descriptors/update")

    # Anime routes
    api.add_resource(anime.NewAnime, "/anime/new")
    api.add_resource(anime.GetAnime, "/anime/get/<string:slug>")
    api.add_resource(anime.AnimesList, "/anime/list")
    api.add_resource(anime.Search, "/anime/search")

    # Episode routes
    api.add_resource(episodes.AddEpisode, "/episodes/add")
    api.add_resource(episodes.UpdateEpisode, "/episodes/update")
    api.add_resource(episodes.DeleteEpisode, "/episodes/delete")

    # System routes
    api.add_resource(system.ManagePermissions, "/system/permissions/manage")
    api.add_resource(system.UserPermissions, "/system/permissions/user")

    # Jikan routes
    api.add_resource(jikan.JikanSearch, "/jikan/search")

    # Voting routes
    api.add_resource(votes.MakeVote, "/vote")

    @app.route("/")
    def root():
        return flask.render_template("index.html")

    @app.errorhandler(404)
    def error404(error):
        return errors.abort("general", "not-found", 404)

    @app.errorhandler(405)
    def error405(error):
        return errors.abort("general", "method-not-allowed", 405)

    @app.errorhandler(429)
    def error429(error):
        return errors.abort("general", "too-many-requests", 429)
