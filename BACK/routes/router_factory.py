"""Fábrica dos routers de catálogos JSON."""

from pathlib import Path
from typing import Any

from fastapi import APIRouter, Body, Response, status

from crud.perfumes import PerfumeRepository

DATA_DIRECTORY = Path(__file__).resolve().parent.parent / "data"


def create_perfume_router(catalog: str, prefix: str) -> APIRouter:
    repository = PerfumeRepository(DATA_DIRECTORY / f"{catalog}.json")
    router = APIRouter(prefix=prefix, tags=[catalog])

    @router.get("")
    def list_perfumes() -> list[dict[str, Any]]:
        return repository.list()

    @router.get("/{perfume_id}")
    def get_perfume(perfume_id: str) -> dict[str, Any]:
        return repository.get(perfume_id)

    @router.post("", status_code=status.HTTP_201_CREATED)
    def create_perfume(
        perfume: dict[str, Any] = Body(...),
    ) -> dict[str, Any]:
        return repository.create(perfume)

    @router.put("/{perfume_id}")
    def replace_perfume(
        perfume_id: str, perfume: dict[str, Any] = Body(...)
    ) -> dict[str, Any]:
        return repository.update(perfume_id, perfume)

    @router.patch("/{perfume_id}")
    def update_perfume(
        perfume_id: str, changes: dict[str, Any] = Body(...)
    ) -> dict[str, Any]:
        return repository.patch(perfume_id, changes)

    @router.delete("/{perfume_id}", status_code=status.HTTP_204_NO_CONTENT)
    def delete_perfume(perfume_id: str) -> Response:
        repository.delete(perfume_id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    return router
