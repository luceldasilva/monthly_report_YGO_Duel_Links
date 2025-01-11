import cloudinary
from cloudinary.uploader import upload
from config.cfg import CLOUD_NAME, API_KEY, API_SECRET
from fastapi import APIRouter, HTTPException, status, File, UploadFile


cloudinary.config(
    cloud_name=CLOUD_NAME,
    api_key=API_KEY,
    api_secret=API_SECRET
)


circular_images = APIRouter(
    prefix="/circular_images",
    tags=["circular_images"],
    responses={status.HTTP_418_IM_A_TEAPOT: {"message": "Soy una tetera :'v"}}
)


@circular_images.post("/", status_code=status.HTTP_201_CREATED) 
async def upload_image_archetype(file: UploadFile = File(...)):
    try:
        result = upload(file.file)
        
        return {'url': result['secure_url']}
    except Exception as e:
        return {'error': str(e)}