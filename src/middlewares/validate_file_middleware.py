from typing import Annotated
from fastapi import UploadFile, File, HTTPException, status
from src.utils.constants import ALLOWED_IMAGES_TYPE, MAX_FILE_UPLOAD_SIZE


def validate_file(
    file: Annotated[UploadFile, File()] = None,
) -> None:
    """
    Validates the uploaded image file and saves it if it meets the criteria.

    Parameters:
    - file: Annotated[UploadFile, File()]: The uploaded image file.

    Returns:
    - str: File path if the validation is successful.

    Raises:
    - HTTPException: If the file format or size is invalid.
    """
    try:
        # Validate file format
        if file and file.content_type not in ALLOWED_IMAGES_TYPE:
            raise HTTPException(
                detail="Invalid File Format, only supports .png, .jpg, or .jpeg",
                status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            )

        # Validate file size
        if file and file.size > MAX_FILE_UPLOAD_SIZE:
            raise HTTPException(
                detail="Max 2 MB file is allowed",
                status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            )
        return None
    except HTTPException as http_error:
        # Re-raise HTTPException to propagate it
        raise http_error
    except Exception as error:
        # Handle other exceptions
        raise HTTPException(
            detail="Something Went Wrong !",
            status_code=status.HTTP_400_BAD_REQUEST,
        ) from error
