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
    """
    Alzar el avatar a Cloudinary

    Parameters
    ----------
    file: UploadFile
        avatar del deck, by default File(...)

    Returns
    -------
    result['secure_url']
        devuelve la url para copiar directo y armarlo
        para su posterior subida a la base de datos con su deck
    """
    try:
        result = upload(file.file)
        
        return result['secure_url']
    except Exception as e:
        return {'error': str(e)}