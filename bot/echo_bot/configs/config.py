from dataclasses import dataclass
from environs import Env

@dataclass
class TgBot:
    token: str


@dataclass
class Configs:
    tg_bot: TgBot


def load_configs(path: str | None = None) -> Configs:
    env = Env()
    env.read_env(path)
    return Configs(tg_bot=TgBot(token=env('BOT_TOKEN')))

