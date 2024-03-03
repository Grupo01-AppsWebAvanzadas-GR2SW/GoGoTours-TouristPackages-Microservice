from typing import List

from fastapi import APIRouter, Depends, HTTPException

from src.application.tourist_packages.dtos.tourist_packages_request_dto import TouristPackagesRequestDto
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


@tourist_packages_router.get("/name/{name}", response_model=TouristPackagesResponseDto)
async def get_tourist_package_by_name(
    name: str,
    tourist_packages_service: TouristPackagesServiceAsync = Depends(TouristPackagesServiceAsync)
):
    return await tourist_packages_service.get_tourist_package_by_name(name)


@tourist_packages_router.get("/{id}", response_model=TouristPackagesResponseDto, responses={404: {}})
async def get_tourist_packages_by_id(
        id: str,
        tourist_packages_service: TouristPackagesServiceAsync = Depends(TouristPackagesServiceAsync)
) -> TouristPackagesResponseDto:
    response = await tourist_packages_service.get_tourist_packages_by_id(id)
    if response is None:
        raise HTTPException(status_code=404, detail=f"")

    return response


@tourist_packages_router.put("/", response_model=bool)
async def edit_tourist_package(
        id: str,
        updated_tourist_package: TouristPackagesRequestDto,
        tourist_packages_service: TouristPackagesServiceAsync = Depends(TouristPackagesServiceAsync)
) -> bool:
    return await tourist_packages_service.edit_package(id, updated_tourist_package)


@tourist_packages_router.delete("/", response_model=bool)
async def delete_tourist_package(
        id: str,
        tourist_packages_service: TouristPackagesServiceAsync = Depends(TouristPackagesServiceAsync)
) -> bool:
    return await tourist_packages_service.delete_package(id)
