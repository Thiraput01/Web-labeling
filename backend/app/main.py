from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from .database.init_db import engine
from .models.user import User
from .models.data_for_label import DataForLabel
from .models.labeled_data import LabeledData
from .models.map_img import MapImage

from .api import data_for_label, labeled_data, map_img, user

User.metadata.create_all(bind=engine)
DataForLabel.metadata.create_all(bind=engine)
MapImage.metadata.create_all(bind=engine)
LabeledData.metadata.create_all(bind=engine)

app = FastAPI()

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app.include_router(data_for_label.router)
app.include_router(labeled_data.router)
app.include_router(map_img.router)
app.include_router(user.router)


@app.get("/hello")
def hello():
    return "hello world"


# if __name__ == '__main__':
#     pass

