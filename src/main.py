import os

from dotenv import load_dotenv
from fastapi import FastAPI

from google.cloud.firestore import AsyncClient

from src.application.tourist_packages.repositories.tourist_packages_repository_async import \
    TouristPackagesRepositoryAsync
from src.application.tourist_packages.services.tourist_packages_service_async import TouristPackagesServiceAsync
from src.infrastructure.firebase.config.config import initialize_firebase, get_firestore_async
from src.infrastructure.firebase.tourist_packages.repositories.firestore_tourist_packages_repository_async import \
    FirestoreTouristPackagesRepositoryAsync
from src.infrastructure.services.tourist_packages.default_tourist_packages_service_async import \
    DefaultTouristPackagesServiceAsync
from src.rabbitmq.connection import RabbitMQConnection
from src.webapi.routes.tourist_packages_routes import tourist_packages_router


load_dotenv("src/.env")
initialize_firebase("/etc/secrets/firebase-credentials.json")
app = FastAPI()
app.dependency_overrides = {
    TouristPackagesServiceAsync: DefaultTouristPackagesServiceAsync,
    TouristPackagesRepositoryAsync: FirestoreTouristPackagesRepositoryAsync,
    AsyncClient: get_firestore_async
}
app.include_router(tourist_packages_router)
