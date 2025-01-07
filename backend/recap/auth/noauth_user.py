from collections.abc import Mapping
from typing import Any
from typing import cast

from recap.auth.schemas import UserRole
from recap.configs.constants import KV_NO_AUTH_USER_PREFERENCES_KEY
from recap.configs.constants import NO_AUTH_USER_EMAIL
from recap.configs.constants import NO_AUTH_USER_ID
from recap.key_value_store.store import KeyValueStore
from recap.key_value_store.store import KvKeyNotFoundError
from recap.server.manage.models import UserInfo
from recap.server.manage.models import UserPreferences


def set_no_auth_user_preferences(
    store: KeyValueStore, preferences: UserPreferences
) -> None:
    store.store(KV_NO_AUTH_USER_PREFERENCES_KEY, preferences.model_dump())


def load_no_auth_user_preferences(store: KeyValueStore) -> UserPreferences:
    try:
        preferences_data = cast(
            Mapping[str, Any], store.load(KV_NO_AUTH_USER_PREFERENCES_KEY)
        )
        return UserPreferences(**preferences_data)
    except KvKeyNotFoundError:
        return UserPreferences(
            chosen_assistants=None, default_model=None, auto_scroll=True
        )


def fetch_no_auth_user(
    store: KeyValueStore, *, anonymous_user_enabled: bool | None = None
) -> UserInfo:
    return UserInfo(
        id=NO_AUTH_USER_ID,
        email=NO_AUTH_USER_EMAIL,
        is_active=True,
        is_superuser=False,
        is_verified=True,
        role=UserRole.BASIC if anonymous_user_enabled else UserRole.ADMIN,
        preferences=load_no_auth_user_preferences(store),
        is_anonymous_user=anonymous_user_enabled,
    )
