from datetime import date, datetime
from decimal import Decimal
from uuid import UUID, uuid4

import pytest


def _new_email() -> str:
    return f"qa_{uuid4().hex}@example.com"


def _assert_uuid(value: str):
    assert isinstance(value, str)
    UUID(value)


def _assert_iso_datetime(value: str):
    assert isinstance(value, str)
    datetime.fromisoformat(value.replace("Z", "+00:00"))


def _assert_iso_date(value: str):
    assert isinstance(value, str)
    date.fromisoformat(value)


def _assert_amount(value):
    assert isinstance(value, (int, float, str))
    Decimal(str(value))


def _assert_user_schema(data: dict):
    assert set(data.keys()) >= {"id", "email", "is_active", "created_at"}
    _assert_uuid(data["id"])
    assert isinstance(data["email"], str)
    assert isinstance(data["is_active"], bool)
    _assert_iso_datetime(data["created_at"])


def _assert_token_schema(data: dict):
    assert set(data.keys()) >= {"access_token", "token_type", "expires_in"}
    assert isinstance(data["access_token"], str)
    assert data["token_type"] == "bearer"
    assert isinstance(data["expires_in"], int)


def _assert_category_schema(data: dict):
    assert set(data.keys()) >= {"id", "name", "type", "created_at", "updated_at"}
    _assert_uuid(data["id"])
    assert isinstance(data["name"], str)
    assert data["type"] in {"income", "expense", "both"}
    _assert_iso_datetime(data["created_at"])
    _assert_iso_datetime(data["updated_at"])


def _assert_transaction_schema(data: dict):
    assert set(data.keys()) >= {
        "id",
        "category_id",
        "type",
        "amount",
        "description",
        "date",
        "created_at",
        "updated_at",
    }
    _assert_uuid(data["id"])
    if data["category_id"] is not None:
        _assert_uuid(data["category_id"])
    assert data["type"] in {"income", "expense"}
    _assert_amount(data["amount"])
    if data["description"] is not None:
        assert isinstance(data["description"], str)
    _assert_iso_date(data["date"])
    _assert_iso_datetime(data["created_at"])
    _assert_iso_datetime(data["updated_at"])


def _assert_dashboard_schema(data: dict):
    assert set(data.keys()) >= {
        "start_date",
        "end_date",
        "total_income",
        "total_expense",
        "balance",
    }
    if data["start_date"] is not None:
        _assert_iso_date(data["start_date"])
    if data["end_date"] is not None:
        _assert_iso_date(data["end_date"])
    _assert_amount(data["total_income"])
    _assert_amount(data["total_expense"])
    _assert_amount(data["balance"])


def _register_and_login(client, api_prefix: str):
    email = _new_email()
    password = "secret123"

    register = client.post(
        f"{api_prefix}/auth/register",
        json={"email": email, "password": password},
    )
    assert register.status_code == 201
    _assert_user_schema(register.json())

    login = client.post(
        f"{api_prefix}/auth/login",
        json={"email": email, "password": password},
    )
    assert login.status_code == 200
    data = login.json()
    _assert_token_schema(data)

    headers = {"Authorization": f"Bearer {data['access_token']}"}
    return headers, email


def test_auth_register_returns_user_schema(client, api_prefix):
    payload = {"email": _new_email(), "password": "secret123"}
    response = client.post(f"{api_prefix}/auth/register", json=payload)
    assert response.status_code == 201
    data = response.json()
    _assert_user_schema(data)
    assert data["email"] == payload["email"]
    assert data["is_active"] is True


def test_auth_login_returns_token_schema(client, api_prefix):
    email = _new_email()
    password = "secret123"

    register = client.post(
        f"{api_prefix}/auth/register",
        json={"email": email, "password": password},
    )
    assert register.status_code == 201
    _assert_user_schema(register.json())

    response = client.post(
        f"{api_prefix}/auth/login",
        json={"email": email, "password": password},
    )
    assert response.status_code == 200
    _assert_token_schema(response.json())


def test_auth_me_returns_user_schema(client, api_prefix):
    headers, email = _register_and_login(client, api_prefix)

    response = client.get(f"{api_prefix}/auth/me", headers=headers)
    assert response.status_code == 200
    data = response.json()
    _assert_user_schema(data)
    assert data["email"] == email


def test_users_me_if_present(client, api_prefix):
    headers, email = _register_and_login(client, api_prefix)

    response = client.get(f"{api_prefix}/users/me", headers=headers)
    if response.status_code == 404:
        pytest.skip("/api/v1/users/me not found; only /api/v1/auth/me is defined")
    assert response.status_code == 200
    data = response.json()
    _assert_user_schema(data)
    assert data["email"] == email


def test_categories_crud(client, api_prefix):
    headers, _ = _register_and_login(client, api_prefix)

    create_payload = {"name": "Alimentacao", "type": "expense"}
    create_resp = client.post(
        f"{api_prefix}/categories",
        json=create_payload,
        headers=headers,
    )
    assert create_resp.status_code == 201
    created = create_resp.json()
    _assert_category_schema(created)

    category_id = created["id"]

    list_resp = client.get(f"{api_prefix}/categories", headers=headers)
    assert list_resp.status_code == 200
    items = list_resp.json()
    assert isinstance(items, list)
    assert any(item["id"] == category_id for item in items)
    for item in items:
        _assert_category_schema(item)

    update_payload = {"name": "Alimentacao Atualizada", "type": "income"}
    update_resp = client.put(
        f"{api_prefix}/categories/{category_id}",
        json=update_payload,
        headers=headers,
    )
    assert update_resp.status_code == 200
    updated = update_resp.json()
    _assert_category_schema(updated)
    assert updated["name"] == update_payload["name"]
    assert updated["type"] == update_payload["type"]

    delete_resp = client.delete(f"{api_prefix}/categories/{category_id}", headers=headers)
    assert delete_resp.status_code == 204
    assert delete_resp.text == ""


def test_transactions_crud(client, api_prefix):
    headers, _ = _register_and_login(client, api_prefix)

    category_resp = client.post(
        f"{api_prefix}/categories",
        json={"name": "Salario", "type": "income"},
        headers=headers,
    )
    assert category_resp.status_code == 201
    category = category_resp.json()
    _assert_category_schema(category)
    category_id = category["id"]

    today = date.today().isoformat()
    create_payload = {
        "category_id": category_id,
        "type": "income",
        "amount": "1200.50",
        "description": "Pagamento",
        "date": today,
    }
    create_resp = client.post(
        f"{api_prefix}/transactions",
        json=create_payload,
        headers=headers,
    )
    assert create_resp.status_code == 201
    created = create_resp.json()
    _assert_transaction_schema(created)
    transaction_id = created["id"]
    assert created["category_id"] == category_id

    list_resp = client.get(f"{api_prefix}/transactions", headers=headers)
    assert list_resp.status_code == 200
    items = list_resp.json()
    assert isinstance(items, list)
    assert any(item["id"] == transaction_id for item in items)
    for item in items:
        _assert_transaction_schema(item)

    update_payload = {
        "category_id": category_id,
        "type": "income",
        "amount": "1500.00",
        "description": "Pagamento Atualizado",
        "date": today,
    }
    update_resp = client.put(
        f"{api_prefix}/transactions/{transaction_id}",
        json=update_payload,
        headers=headers,
    )
    assert update_resp.status_code == 200
    updated = update_resp.json()
    _assert_transaction_schema(updated)
    assert Decimal(str(updated["amount"])) == Decimal(update_payload["amount"])
    assert updated["description"] == update_payload["description"]

    delete_resp = client.delete(f"{api_prefix}/transactions/{transaction_id}", headers=headers)
    assert delete_resp.status_code == 204
    assert delete_resp.text == ""


def test_dashboard_summary(client, api_prefix):
    headers, _ = _register_and_login(client, api_prefix)
    today = date.today().isoformat()

    income_payload = {
        "category_id": None,
        "type": "income",
        "amount": "100.00",
        "description": "Receita",
        "date": today,
    }
    expense_payload = {
        "category_id": None,
        "type": "expense",
        "amount": "40.00",
        "description": "Despesa",
        "date": today,
    }

    income_resp = client.post(
        f"{api_prefix}/transactions",
        json=income_payload,
        headers=headers,
    )
    assert income_resp.status_code == 201
    _assert_transaction_schema(income_resp.json())

    expense_resp = client.post(
        f"{api_prefix}/transactions",
        json=expense_payload,
        headers=headers,
    )
    assert expense_resp.status_code == 201
    _assert_transaction_schema(expense_resp.json())

    summary_resp = client.get(f"{api_prefix}/dashboard/summary", headers=headers)
    assert summary_resp.status_code == 200
    summary = summary_resp.json()
    _assert_dashboard_schema(summary)
    assert summary["start_date"] is None
    assert summary["end_date"] is None
    assert Decimal(str(summary["total_income"])) == Decimal("100.00")
    assert Decimal(str(summary["total_expense"])) == Decimal("40.00")
    assert Decimal(str(summary["balance"])) == Decimal("60.00")
