from unittest.mock import Mock

from app.billing.services.plan_service import PlanService


def test_all_delegates_to_repository():
    service = PlanService.__new__(PlanService)

    repository = Mock()
    repository.all.return_value = ["plan1", "plan2"]

    service.repository = repository

    result = service.all()

    assert result == ["plan1", "plan2"]
    repository.all.assert_called_once_with()


def test_get_delegates_to_repository():
    service = PlanService.__new__(PlanService)

    repository = Mock()
    repository.get_by_code.return_value = "plan"

    service.repository = repository

    result = service.get("pro")

    assert result == "plan"
    repository.get_by_code.assert_called_once_with("pro")