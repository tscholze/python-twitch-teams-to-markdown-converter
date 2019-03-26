import os
import requests
import datetime

""" 
Twitch API client id (https://dev.twitch.tv/console/apps)
"""
TWITCH_CLIENT_ID = "<KEY>"

"""
Name of the Twitch team
"""
TWITCH_TEAMS_NAME = "<NAME>"

"""
Computed API teams endpoint url
"""
TWITCH_TEAMS_ENDPOINT_URL = "https://api.twitch.tv/kraken/teams/" + TWITCH_TEAMS_NAME

"""
Maximum length of status
"""
MAX_STATUS_LENGTH = 60

"""
This converter helps to transform the, from the Twitch API requested data, into a
template-based markdown overview page.
"""


class TwitchTeamConverter:
    """
    Cached team response property
    """
    team = None

    def get_team(self):
        """
        Gets the team from the api or if already present the cached property of it.
        :param self: Self
        :return: Team response
        """

        if self.team is None:
            headers = {
                'Accept': 'application/vnd.twitchtv.v5+json',
                'Client-ID': TWITCH_CLIENT_ID
            }

            self.team = requests.get(TWITCH_TEAMS_ENDPOINT_URL, headers=headers).json()
            return self.team
        else:
            return self.team

    def create_members_content(self):
        """
        Creates the content string for all team member
        :return: Content string that represents all members
        """

        members_content = '<div style="display: flex; flex-wrap: wrap">'
        for member in self.get_team()["users"]:
            members_content += self.create_member_content(member)
        members_content += '</div>'

        return members_content

    def create_member_content(self, member):
        """
        Creates the content string for a given member
        :return: Content string that represents given member
        """

        with open("templates/member-template.html", "r") as file:
            content = file.read()
            content = content.replace("{logo}", member["logo"])
            content = content.replace("{name}", member["display_name"])
            content = content.replace("{link}", member["url"])
            content = content.replace("{lang}", self.get_formatted_language(member))
            content = content.replace("{status}", self.get_formatted_status(member))
            content = content.replace("\n", "")
            content = content.replace("\t", "")

            return content

    def create_markdown(self):
        """
        Creates the content string for underlying Twitch team.
        :return: Content string that represents the underlying Twitch team.
        """

        with open("templates/markdown-template.md", "r") as file:
            content = file.read()
            content = content.replace("{members_content}", self.create_members_content())
            content = content.replace("{generation_date}", datetime.date.today().ctime())

            with open("output.md", "wb") as output_file:
                output_file.write(content.encode('utf-8'))
                print(f"New markdown file has been generated.\nLocation: {os.path.realpath(output_file.name)}")

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
        if len(status) > MAX_STATUS_LENGTH:
            status = status[:MAX_STATUS_LENGTH - 4]
            status += " ..."

        return status


"""
Entry point. 
Will start the creation of the markdown file.
"""
if __name__ == "__main__":
    converter = TwitchTeamConverter()
    converter.create_markdown()
