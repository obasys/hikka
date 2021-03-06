from hikka.decorators import auth_required, permission_required
from hikka.services.permissions import PermissionService
from werkzeug.datastructures import FileStorage
from hikka.services.users import UserService
from hikka.services.teams import TeamService
from hikka.tools.upload import UploadHelper
from flask_restful import Resource
from flask_restful import reqparse
from hikka.errors import abort
from flask import Response
from flask import request

class NewTeam(Resource):
    @auth_required
    @permission_required("global", "admin")
    def post(self):
        result = {"error": None, "data": {}}

        parser = reqparse.RequestParser()
        parser.add_argument("members", type=list, default=[], location="json")
        parser.add_argument("admins", type=list, default=[], location="json")
        parser.add_argument("avatar", type=FileStorage, location="files")
        parser.add_argument("description", type=str, required=True)
        parser.add_argument("name", type=str, required=True)
        parser.add_argument("slug", type=str, required=True)
        args = parser.parse_args()

        team = TeamService.get_by_slug(args["slug"])
        if team is not None:
            return abort("team", "slug-exists")

        avatar = None
        if args["avatar"] is not None:
            helper = UploadHelper(request.account, args["avatar"], "avatar")
            data = helper.upload_image()

            if type(data) is Response:
                return data

            avatar = data

        team = TeamService.create(args["name"], args["slug"], args["description"])

        if avatar is not None:
            TeamService.update_avatar(team, avatar)

        for username in args["members"]:
            account = UserService.get_by_username(username)

            if account is None:
                return abort("account", "not-found")

            TeamService.add_member(team, account)
            if account.username in args["admins"]:
                PermissionService.add(account, "global", "publishing")

        result["data"] = team.dict(True)
        return result

class AddMember(Resource):
    @auth_required
    @permission_required("global", "admin")
    def post(self):
        result = {"error": None, "data": {}}

        parser = reqparse.RequestParser()
        parser.add_argument("username", type=str, required=True)
        parser.add_argument("admin", type=bool, default=False)
        parser.add_argument("slug", type=str, required=True)
        args = parser.parse_args()

        team = TeamService.get_by_slug(args["slug"])
        if team is None:
            return abort("team", "not-found")

        account = UserService.get_by_username(args["username"])
        if account is None:
            return abort("account", "not-found")

        TeamService.add_member(team, account)
        if args["admin"]:
            PermissionService.add(account, "global", "publishing")

        result["data"] = team.dict(True)
        return result

class RemoveMember(Resource):
    @auth_required
    @permission_required("global", "admin")
    def post(self):
        result = {"error": None, "data": {}}

        parser = reqparse.RequestParser()
        parser.add_argument("username", type=str, required=True)
        parser.add_argument("admin", type=bool, default=False)
        parser.add_argument("slug", type=str, required=True)
        args = parser.parse_args()

        team = TeamService.get_by_slug(args["slug"])
        if team is None:
            return abort("team", "not-found")

        account = UserService.get_by_username(args["username"])
        if account is None:
            return abort("account", "not-found")

        TeamService.remove_member(team, account)
        PermissionService.remove(account, "global", "publishing")

        result["data"] = team.dict(True)
        return result

class GetTeam(Resource):
    def get(self, slug):
        result = {"error": None, "data": {}}

        team = TeamService.get_by_slug(slug)
        if team is None:
            return abort("team", "not-found")

        result["data"] = team.dict(True)
        return result

class ListTeams(Resource):
    def get(self):
        result = {"error": None, "data": []}

        teams = TeamService.list()
        for team in teams:
            result["data"].append(team.dict())

        return result
