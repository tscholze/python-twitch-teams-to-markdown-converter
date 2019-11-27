# Twitch Teams to Markdown converter
> A simple Python script that helps to transform Twitch API team data into a markdown table-based overview.

## Status

|Type|Status|
|----|------|
|Build (Travis)| - |

## Requirements

- Python 3.6.3
- `pip install requests`
- Twitch API client id ([Developer Dashboard](https://dev.twitch.tv/console/apps))

## Configuration

Set the environment variables `TWITCH_CLIENT_ID` and `TWITCH_TEAMS_NAME` set before running.

You can set them at runtime like so:

```
TWITCH_CLIENT_ID="foo" TWITCH_TEAMS_NAME="bar" python converter.py
```

To change the templates, have a look at the folder `templates/`.

## Run

```
> python twitch-teams-to-markdown-converter/converter.py
New markdown file has been generated.
Location: twitch-teams-to-markdown-converter/output.md
```

<a href="example.png"><img src="example.png" width="500" /></a>

See [example](example.md).

## GitHub Action

You can use this script as well as a GitHub Action. With such, you need set the environment variables as described earlier.

Here's an example usage:

```yaml
steps:
  - uses: tscholze/python-twitch-teams-to-markdown-converter@1.0.0
    env:
      TWITCH_CLIENT_ID: ${{ secrets.TWITCH_CLIENT_ID }}
      TWITCH_TEAMS_NAME: ${{ secrets.TWITCH_TEAMS_NAME }}
```

It will generate the output.md file into your `$GITHUB_WORKSPACE` directory which is where your code is checked out to in a normal workflow run.

## Contributing

Feel free to improve the quality of the code. It would be great to learn more from experienced Python developers.

## Authors

Just me, [Tobi]([https://tscholze.github.io).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE.md) file for details.
Dependencies or assets maybe licensed differently.
