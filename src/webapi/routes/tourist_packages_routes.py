from typing import List

from fastapi import APIRouter, Depends

from src.application.tourist_packages.dtos.tourist_packages_response_dto import TouristPackagesResponseDto
from src.application.tourist_packages.services.tourist_packages_service_async import TouristPackagesServiceAsync

tourist_packages_router = APIRouter()


@tourist_packages_router.post("/", response_model=TouristPackagesResponseDto)
async def create_tourist_packages(
        tourist_package: TouristPackagesResponseDto,
        tourist_packages_service: TouristPackagesServiceAsync = Depends(TouristPackagesServiceAsync)
) -> TouristPackagesResponseDto:
    await tourist_packages_service.add_package(tourist_package)
    return tourist_package

@tourist_packages_router.get("/", response_model=List[TouristPackagesResponseDto])
async def get_tourist_packages(
    tourist_packages_service: TouristPackagesServiceAsync = Depends(TouristPackagesServiceAsync)
):
    return await tourist_packages_service.get_tourist_packages()