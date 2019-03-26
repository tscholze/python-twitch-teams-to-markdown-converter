import os
import requests
import datetime


# Twitch API client id (https://dev.twitch.tv/console/apps)
TWITCH_CLIENT_ID = "7y5ny7hnvkhceu0t2ytccuyv4f8wtn"

# Name of the Twitch team
TWITCH_TEAMS_NAME = "livecoders"

# Computed API teams endpoint url
TWITCH_TEAMS_ENDPOINT_URL = "https://api.twitch.tv/kraken/teams/" + TWITCH_TEAMS_NAME

# Maximum length of status
MAX_STATUS_LENGTH = 120

# Image url that will be used if member's logo url is not valid.
FALLBACK_LOGO_IMAGE_URL = "https://static-cdn.jtvnw.net/jtv_user_pictures/team-livecoders-team_logo_image-2dfbdddbcf5a44e69bbc1a45a179b152-600x600.png"


class TwitchTeamConverter:
    """
    This converter helps to transform the, from the Twitch API requested data, into a
    template-based markdown overview page.
    """

    # Cached team response property
    _team = None

    def get_team(self):
        """
        Gets the team from the api or if already present the cached property of it.
        :param self: Self
        :return: Team response
        """

        if self._team is None:
            headers = {
                'Accept': 'application/vnd.twitchtv.v5+json',
                'Client-ID': TWITCH_CLIENT_ID
            }

            self._team = requests.get(TWITCH_TEAMS_ENDPOINT_URL, headers=headers).json()
            return self._team
        else:
            return self._team

    def create_members_content(self):
        """
        Creates the content string for all team member
        :return: Content string that represents all members
        """

        members_content = '| |Name|Status|Language|Family Friendly| \n |-|:-|:-|:-:|:-:| \n'
        for member in self.get_team()["users"]:
            members_content += self.create_member_content(member)

        return members_content

    def create_member_content(self, member):
        """
        Creates the content string for a given member
        :return: Content string that represents given member
        """

        with open("templates/member-template.md", "r") as file:
            content = file.read()
            content = content.replace("{logo}", self.get_formatted_logo(member))
            content = content.replace("{name}", member["display_name"])
            content = content.replace("{link}", member["url"])
            content = content.replace("{lang}", self.get_formatted_language(member))
            content = content.replace("{status}", self.get_formatted_status(member))
            content = content.replace("{family_friendy}", self.get_formatted_family_friendly(member))

            return content

    def create_markdown(self):
        """
        Creates the content string for underlying Twitch team.
        :return: Content string that represents the underlying Twitch team.
        """

        with open("templates/markdown-template.md", "r") as file:
            content = file.read()
            content = content.replace("{members_content}", self.create_members_content())
            content = content.replace("{generation_date}", f"{datetime.datetime.now():%Y-%m-%d %H:%M}")

            with open("output.md", "wb") as output_file:
                output_file.write(content.encode('utf-8'))
                print(f"New markdown file has been generated.\nLocation: {os.path.realpath(output_file.name)}")

    @staticmethod
    def get_formatted_logo(member):
        """
        Gets the formatted logo url.
        Caution: Urls that ends with `jpeg` does not work in
        GitHub mardown files. That's why a placeholder will be
        returned.
        :param member: Underlying member
        :return: Formatted logo image url
        """

        logo = member["logo"]
        if logo.endswith(".jpeg"):
            logo = FALLBACK_LOGO_IMAGE_URL

        return logo

    @staticmethod
    def get_formatted_language(member):
        """
        Gets the formatted language text of the given member
        :param member: Underlying member
        :return: Formatted language text
        """

        language = member["language"]
        language = language.split("-")[0]

        return language

    @staticmethod
    def get_formatted_status(member):
        """
        Gets the formatted status text of the given member
        :param member: Underlying member
        :return: Formatted status text
        """

        status = member["status"]
        status = status.replace("|", "-")
        status = status.replace("\n", "")

        if len(status) > MAX_STATUS_LENGTH:
            status = status[:MAX_STATUS_LENGTH - 4]
            status += " ..."

        return status

    @staticmethod
    def get_formatted_family_friendly(member):
        """
        Gets the formatted family friendly indicator
        :param member: Underlying member
        :return: Formatted family friendly indicator
        """

        if member["mature"] is False:
            return "✅"
        else:
            return "🚫"


if __name__ == "__main__":
    """
    Entry point. 
    Will start the creation of the markdown file.
    """
    converter = TwitchTeamConverter()
    converter.create_markdown()
