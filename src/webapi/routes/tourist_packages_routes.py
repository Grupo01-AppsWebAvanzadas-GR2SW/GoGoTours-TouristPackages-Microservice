from typing import List

from fastapi import APIRouter, Depends, Security, HTTPException
from fastapi_jwt import JwtAuthorizationCredentials

from src.application.tourist_packages.dtos.tourist_packages_response_dto import TouristPackagesResponseDto
from src.application.tourist_packages.services.tourist_packages_service_async import TouristPackagesServiceAsync
from src.webapi.access_security import access_security
from src.webapi.decorators import admin_only_async

tourist_packages_router = APIRouter()


@tourist_packages_router.post("/", response_model=TouristPackagesResponseDto)
@admin_only_async
async def create_tourist_packages(
        tourist_package: TouristPackagesResponseDto,
        tourist_packages_service: TouristPackagesServiceAsync = Depends(TouristPackagesServiceAsync),
        credentials: JwtAuthorizationCredentials = Security(access_security)
) -> TouristPackagesResponseDto:
    tourist_package.admin_id = credentials.subject["user_id"]
    await tourist_packages_service.add_package(tourist_package)
    return tourist_package


@tourist_packages_router.get("/", response_model=List[TouristPackagesResponseDto])
async def get_tourist_packages(
        destination_place: str | None = None,
        tourist_packages_service: TouristPackagesServiceAsync = Depends(TouristPackagesServiceAsync)
):
    tourist_packages = await tourist_packages_service.get_tourist_packages()
    if destination_place is not None:
        filtered_packages = list(
            filter(
                lambda package:
                destination_place.lower().replace(" ", "") in package.destination_place.lower()
                .replace(" ", ""),
                tourist_packages
            )
        )
        return filtered_packages
    return tourist_packages


@tourist_packages_router.get("/{id}", response_model=TouristPackagesResponseDto, responses={404: {}})
async def get_tourist_packages_by_id(
        id: str,
        tourist_packages_service: TouristPackagesServiceAsync = Depends(TouristPackagesServiceAsync)
) -> TouristPackagesResponseDto:
    response = await tourist_packages_service.get_tourist_packages_by_id(id)
    if response is None:
        raise HTTPException(status_code=404, detail=f"")

    return response


@tourist_packages_router.put("/{id}", response_model=bool)
@admin_only_async
async def edit_tourist_package(
        id: str,
        updated_tourist_package: TouristPackagesResponseDto,
        tourist_packages_service: TouristPackagesServiceAsync = Depends(TouristPackagesServiceAsync),
        credentials: JwtAuthorizationCredentials = Security(access_security)
) -> bool:
    updated_tourist_package.id = id
    updated_tourist_package.admin_id = credentials.subject["user_id"]
    return await tourist_packages_service.edit_package(updated_tourist_package)


@tourist_packages_router.delete("/{id}", response_model=bool)
@admin_only_async
async def delete_tourist_package(
        id: str,
        tourist_packages_service: TouristPackagesServiceAsync = Depends(TouristPackagesServiceAsync),
        credentials: JwtAuthorizationCredentials = Security(access_security)
) -> bool:
    return await tourist_packages_service.delete_package(id)
