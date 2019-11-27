FROM python:3-alpine

WORKDIR /opt/workspace

COPY converter.py /opt/workspace/converter.py
COPY templates /opt/workspace/templates/

RUN pip install requests

ENV TWITCH_CLIENT_ID=""
ENV TWITCH_TEAMS_NAME=""

CMD cd /opt/workspace && python converter.py && cp output.md $GITHUB_WORKSPACE/output.md