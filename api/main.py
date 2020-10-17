from fastapi import FastAPI

import routers

app = FastAPI()
routers.setup_routers(app)
