from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

import pytest

from app.database.models.guest_resume import GuestResume
from app.guest.services.guest_resume_service import GuestResumeService


def test_get_resume(db):
    service = GuestResumeService(db)

    resume = GuestResume(
        guest_id="guest-1",
        original_filename="resume.docx",
        stored_filename="stored-resume.docx",
        file_path="uploads/stored-resume.docx",
        file_size=100,
        status="uploaded",
    )

    db.add(resume)
    db.commit()
    db.refresh(resume)

    result = service.get_resume(resume.id)

    assert result is not None
    assert result.id == resume.id


def test_get_resume_returns_none_for_unknown_id(db):
    service = GuestResumeService(db)

    result = service.get_resume(
        "does-not-exist"
    )

    assert result is None


def test_get_guest_resumes(db):
    service = GuestResumeService(db)

    first = GuestResume(
        guest_id="guest-1",
        original_filename="resume1.docx",
        stored_filename="stored1.docx",
        file_path="uploads/stored1.docx",
        file_size=100,
        status="uploaded",
    )

    second = GuestResume(
        guest_id="guest-1",
        original_filename="resume2.docx",
        stored_filename="stored2.docx",
        file_path="uploads/stored2.docx",
        file_size=200,
        status="uploaded",
    )

    db.add_all([first, second])
    db.commit()

    results = service.get_guest_resumes(
        "guest-1"
    )

    assert len(results) == 2
    assert all(
        resume.guest_id == "guest-1"
        for resume in results
    )


def test_count_guest_resumes(db):
    service = GuestResumeService(db)

    db.add_all(
        [
            GuestResume(
                guest_id="guest-1",
                original_filename="one.docx",
                stored_filename="one-stored.docx",
                file_path="uploads/one-stored.docx",
                file_size=100,
                status="uploaded",
            ),
            GuestResume(
                guest_id="guest-1",
                original_filename="two.docx",
                stored_filename="two-stored.docx",
                file_path="uploads/two-stored.docx",
                file_size=200,
                status="uploaded",
            ),
        ]
    )

    db.commit()

    assert (
        service.count_guest_resumes("guest-1")
        == 2
    )


@pytest.mark.asyncio
async def test_upload_resume(db):
    service = GuestResumeService(db)

    stored = SimpleNamespace(
        original_filename="resume.docx",
        stored_filename="stored-resume.docx",
        file_path="uploads/stored-resume.docx",
        file_size=1234,
    )

    service.storage.save_upload = AsyncMock(
        return_value=stored
    )

    file = MagicMock()

    result = await service.upload_resume(
        guest_id="guest-1",
        file=file,
    )

    assert result is not None
    assert result.guest_id == "guest-1"
    assert result.original_filename == "resume.docx"
    assert result.stored_filename == "stored-resume.docx"
    assert result.file_size == 1234
    assert result.status == "uploaded"

    service.storage.save_upload.assert_awaited_once_with(
        file
    )


@pytest.mark.asyncio
async def test_upload_resume_rolls_back_on_failure(db):
    service = GuestResumeService(db)

    service.storage.save_upload = AsyncMock(
        side_effect=RuntimeError(
            "Storage failure"
        )
    )

    file = MagicMock()

    with pytest.raises(RuntimeError):
        await service.upload_resume(
            guest_id="guest-1",
            file=file,
        )


def test_delete_resume(db):
    service = GuestResumeService(db)

    resume = GuestResume(
        guest_id="guest-1",
        original_filename="resume.docx",
        stored_filename="delete-me.docx",
        file_path="uploads/delete-me.docx",
        file_size=100,
        status="uploaded",
    )

    db.add(resume)
    db.commit()
    db.refresh(resume)

    service.storage.delete = MagicMock(
        return_value=True
    )

    result = service.delete_resume(
        resume
    )

    assert result is True

    service.storage.delete.assert_called_once_with(
        "uploads/delete-me.docx"
    )

    assert (
        service.get_resume(resume.id)
        is None
    )