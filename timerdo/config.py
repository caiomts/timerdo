import os
import platform
from pathlib import Path


def get_user_dir(dir_data: bool = True) -> Path:
    """Get user directories."""
    home = Path.home()
    env_test = os.environ.get('TIMERDOTEST', '')
    match platform.system(), env_test:
        case 'Windows', '':
            if os.getenv('APPDATA'):
                return Path(os.getenv('APPDATA'))
            else:
                return Path(os.getenv('LOCALAPPDATA'))
        case 'Darwin', '':
            return Path(home, 'Library')
        case _, '':
            if dir_data is True:
                return Path(home, '.local/share')
            else:
                return Path(home, '.config')
        case _, _:
            return Path(os.environ['TIMERDOTEST']) / 'TimerdoTest'


data_dir = get_user_dir() / 'Timerdo'
config_dir = get_user_dir(dir_data=False)

data_dir.mkdir(parents=True, exist_ok=True)
config_dir.mkdir(parents=True, exist_ok=True)  # On hold. Might be useful.
