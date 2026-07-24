from .user_service import UserService


class ProfileService:

    @classmethod
    def get_profile(
        cls,
        user_id: str,
    ):

        return UserService.get(
            user_id
        )

    @classmethod
    def update_language(
        cls,
        user_id: str,
        language: str,
    ):

        user = UserService.get(
            user_id
        )

        if not user:
            return None

        user.language = language

        return UserService.update(
            user
        )

    @classmethod
    def update_country(
        cls,
        user_id: str,
        country: str,
    ):

        user = UserService.get(
            user_id
        )

        if not user:
            return None

        user.country = country

        return UserService.update(
            user
        )