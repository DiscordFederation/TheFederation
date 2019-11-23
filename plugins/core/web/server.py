from discord.ext import commands
from erin.core.loggers import access_logger, get_hypercorn_logger
from hypercorn import Config
from hypercorn.asyncio import serve

from fds.web import app


class WebServer(commands.Cog, name="Web Server"):
    def __init__(self, bot):
        self.bot = bot

        config = Config()
        config.bind = ["localhost:5000"]
        config.access_log_format = (
            "%(h)s %(l)s %(l)s %(t)s " '"%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'
        )
        config.accesslog = access_logger
        config.logconfig_dict = get_hypercorn_logger(
            log_level=self.bot.config["bot"]["log_level"]
        )
        self.bot.loop.create_task(serve(app, config))
