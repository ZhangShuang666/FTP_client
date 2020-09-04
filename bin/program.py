from src import service
import sys
from config import settings


sys.path.append(settings.BASE_DIR)


if __name__ == '__main__':
    service.main()


