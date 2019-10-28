import argparse
import asyncio
from concurrent import futures
from lib.utils import get_current_sha1
from websockets import WebSocketException
from bot import QuantumBot

__version__ = get_current_sha1()


def process_arg():
    parser = argparse.ArgumentParser(
        description=__doc__,
        epilog=f"Quantum {__version__}"
    )
    parser.add_argument(
        "--version", "-v",
        action="version", version=f"Quantum {__version__}"
    )
    parser.add_argument(
        "--config", "-c",
        help="path to configuation file",
        default="default.toml"
    )
    parser.add_argument(
        "--logging", "-l",
        choices=["i", "c", "ws", "d", "w", "e"],
        help="set logging to Info, Chat, WebSocket, Debug, Warn, Error; respectively",
        default="i"
    )
    return parser.parse_args()


async def start(executor, bot):
    asyncio.get_event_loop().run_in_executor(executor, bot.process_message_queue)
    asyncio.get_event_loop().run_in_executor(executor, bot.process_input)
    settings = bot.settings
    while settings["bot"]["auto_restart"]:
        try:
            await bot.run()
        except WebSocketException:
            bot.log.error(f"websocket crashed, Restarting in {settings['bot']['restart_time']}")
            if settings["bot"]["restart_attempts"] != 0:
                settings["bot"]["restart_attempts"] -= 1
            await asyncio.sleep(settings['bot']['restart_time'])


executor = futures.ThreadPoolExecutor(max_workers=3, )
args = process_arg()
bot = QuantumBot(args)
asyncio.get_event_loop().run_until_complete(start(executor, bot))
print("completed??? ")
