"""CRUD persistente para os catálogos de perfumes armazenados em JSON."""

from __future__ import annotations

import json
import os
import tempfile
from copy import deepcopy
from pathlib import Path
from threading import RLock
from typing import Any

from fastapi import HTTPException, status


class PerfumeRepository:
    """Acessa um arquivo JSON e oferece as operações básicas de CRUD."""

    def __init__(self, file_path: Path) -> None:
        self.file_path = file_path
        self._lock = RLock()

    def list(self) -> list[dict[str, Any]]:
        with self._lock:
            return deepcopy(self._read())

    def get(self, perfume_id: str) -> dict[str, Any]:
        with self._lock:
            perfume = self._find(self._read(), perfume_id)
            return deepcopy(perfume)

    def create(self, perfume: dict[str, Any]) -> dict[str, Any]:
        perfume = self._validate_payload(perfume)
        with self._lock:
            perfumes = self._read()
            if any(item.get("id") == perfume["id"] for item in perfumes):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Já existe um perfume com este id.",
                )
            perfumes.append(perfume)
            self._write(perfumes)
            return deepcopy(perfume)

    def update(self, perfume_id: str, perfume: dict[str, Any]) -> dict[str, Any]:
        perfume = self._validate_payload(perfume)
        if perfume["id"] != perfume_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="O id do corpo deve ser igual ao id da URL.",
            )

        with self._lock:
            perfumes = self._read()
            current = self._find(perfumes, perfume_id)
            perfumes[perfumes.index(current)] = perfume
            self._write(perfumes)
            return deepcopy(perfume)

    def patch(self, perfume_id: str, changes: dict[str, Any]) -> dict[str, Any]:
        if not isinstance(changes, dict) or not changes:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Informe ao menos um campo para atualizar.",
            )
        if "id" in changes and changes["id"] != perfume_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="O id de um perfume não pode ser alterado.",
            )

        with self._lock:
            perfumes = self._read()
            current = self._find(perfumes, perfume_id)
            updated = self._validate_payload({**current, **changes})
            perfumes[perfumes.index(current)] = updated
            self._write(perfumes)
            return deepcopy(updated)

    def delete(self, perfume_id: str) -> None:
        with self._lock:
            perfumes = self._read()
            perfume = self._find(perfumes, perfume_id)
            perfumes.remove(perfume)
            self._write(perfumes)

    def _read(self) -> list[dict[str, Any]]:
        try:
            with self.file_path.open(encoding="utf-8") as file:
                content = json.load(file)
        except (OSError, json.JSONDecodeError) as error:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Não foi possível carregar {self.file_path.name}.",
            ) from error

        if not isinstance(content, list) or not all(
            isinstance(item, dict) for item in content
        ):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"O arquivo {self.file_path.name} possui formato inválido.",
            )
        return content

    def _write(self, perfumes: list[dict[str, Any]]) -> None:
        """Substitui o catálogo atomicamente para evitar JSON parcial."""
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        temporary_path: str | None = None
        try:
            with tempfile.NamedTemporaryFile(
                "w",
                encoding="utf-8",
                dir=self.file_path.parent,
                delete=False,
            ) as temporary:
                temporary_path = temporary.name
                json.dump(perfumes, temporary, ensure_ascii=False, indent=2)
                temporary.write("\n")
            os.replace(temporary_path, self.file_path)
        except OSError as error:
            if temporary_path:
                Path(temporary_path).unlink(missing_ok=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Não foi possível salvar {self.file_path.name}.",
            ) from error

    @staticmethod
    def _find(
        perfumes: list[dict[str, Any]], perfume_id: str
    ) -> dict[str, Any]:
        perfume = next(
            (item for item in perfumes if item.get("id") == perfume_id), None
        )
        if perfume is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Perfume não encontrado.",
            )
        return perfume

    @staticmethod
    def _validate_payload(perfume: dict[str, Any]) -> dict[str, Any]:
        if not isinstance(perfume, dict):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="O perfume deve ser um objeto JSON.",
            )
        perfume_id = perfume.get("id")
        if not isinstance(perfume_id, str) or not perfume_id.strip():
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="O campo id é obrigatório e deve ser um texto.",
            )
        return deepcopy(perfume)
