from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from enum import Enum, auto
from typing import Any, List, Mapping, Optional


def parse_date(date_str: str) -> date:
    return datetime.strptime(date_str, "%Y-%m-%d").date()


def parse_datetime(date_str: str) -> datetime:
    return datetime.fromisoformat(date_str)


@dataclass(frozen=True)
class TokenResponse:
    access_token: str
    token_type: str

    @classmethod
    def from_json(cls, json_data: Mapping[str, Any]) -> TokenResponse:
        return TokenResponse(
            access_token=json_data["access_token"],
            token_type=json_data["token_type"],
        )


@dataclass(frozen=True)
class ErrorResponse:
    detail: List[Detail]

    @classmethod
    def from_json(cls, json_data: Mapping[str, Any]) -> ErrorResponse:
        return ErrorResponse(
            detail=[
                Detail.from_json(json_data=detail)
                for detail in json_data.get("detail", list())
            ]
        )


@dataclass(frozen=True)
class Detail:
    loc: List[str]
    msg: Optional[str]
    type: Optional[str]

    @classmethod
    def from_json(cls, json_data: Mapping[str, Any]) -> Detail:
        return Detail(
            loc=[str(entry) for entry in json_data.get("loc", list())],
            msg=json_data.get("msg"),
            type=json_data.get("type"),
        )


class Status(Enum):
    SUCCESS = auto()
    FAILURE = auto()


@dataclass(frozen=True)
class Response:
    status: Status
    status_code: int
    data: Optional[Mapping[str, Any]]


@dataclass(frozen=True)
class MealPlanResponse:
    group: str
    start_date: date
    end_date: date
    plan_days: List[PlanDay]
    uid: int
    shopping_list: int

    @classmethod
    def from_json(cls, json_data: Mapping[str, Any]) -> MealPlanResponse:
        return MealPlanResponse(
            group=json_data["group"],
            start_date=parse_date(json_data["startDate"]),
            end_date=parse_date(json_data["endDate"]),
            plan_days=[
                PlanDay.from_json(json_data=plan_day)
                for plan_day in json_data.get("planDays", list())
            ],
            uid=json_data["uid"],
            shopping_list=json_data["shoppingList"],
        )


@dataclass(frozen=True)
class PlanDay:
    date: date
    meals: List[Meal]

    @classmethod
    def from_json(cls, json_data: Mapping[str, Any]) -> PlanDay:
        return PlanDay(
            date=parse_date(json_data["date"]),
            meals=[
                Meal.from_json(json_data=meal)
                for meal in json_data.get("meals", list())
            ],
        )


@dataclass(frozen=True)
class Meal:
    slug: Optional[str]
    name: Optional[str]
    description: Optional[str]

    @classmethod
    def from_json(cls, json_data: Mapping[str, Any]) -> Meal:
        return Meal(
            slug=json_data.get("slug"),
            name=json_data.get("name"),
            description=json_data.get("description"),
        )


@dataclass(frozen=True)
class UserResponse:
    username: str
    full_name: str
    email: str
    admin: bool
    group: str
    favorite_recipes: List[str]
    id: int
    tokens: List[Token]

    @classmethod
    def from_json(cls, json_data: Mapping[str, Any]) -> UserResponse:
        return UserResponse(
            username=json_data["username"],
            full_name=json_data["fullName"],
            email=json_data["email"],
            admin=json_data["admin"],
            group=json_data["group"],
            favorite_recipes=[
                str(recipe)
                for recipe in json_data.get("favoriteRecipes", list())
            ],
            id=int(json_data["id"]),
            tokens=[
                Token.from_json(token)
                for token in json_data.get("tokens", list())
            ],
        )


@dataclass(frozen=True)
class Token:
    name: str
    id: int

    @classmethod
    def from_json(cls, json_data: Mapping[str, Any]) -> Token:
        return Token(name=json_data["name"], id=int(json_data["id"]))


@dataclass(frozen=True)
class StatisticsResponse:
    total_recipes: int
    total_users: int
    total_groups: int
    uncategorized_recipes: int
    untagged_recipes: int

    @classmethod
    def from_json(cls, json_data: Mapping[str, Any]) -> StatisticsResponse:
        return StatisticsResponse(
            total_recipes=json_data["totalRecipes"],
            total_users=json_data["totalUsers"],
            total_groups=json_data["totalGroups"],
            uncategorized_recipes=json_data["uncategorizedRecipes"],
            untagged_recipes=json_data["untaggedRecipes"],
        )


@dataclass(frozen=True)
class RecipeResponse:
    id: int
    name: str
    slug: str
    image: Optional[str]
    description: Optional[str]
    recipe_category: List[str]
    tags: List[str]
    rating: Optional[int]
    date_added: date
    date_updated: datetime
    recipe_yield: Optional[str]
    recipe_ingredient: List[RecipeIngredient]
    recipe_instructions: List[Any]
    nutrition: Nutrition
    tools: List[str]
    total_time: Optional[str]
    prep_time: Optional[str]
    perform_time: Optional[str]
    settings: List[Setting]
    assets: List[Asset]
    notes: List[Note]
    org_url: Optional[str]
    extras: Optional[Mapping[str, Any]]
    comments: List[Comment]

    @classmethod
    def from_json(cls, json_data: Mapping[str, Any]) -> RecipeResponse:
        return RecipeResponse(
            id=json_data["id"],
            name=json_data["name"],
            slug=json_data["slug"],
            image=json_data.get("image"),
            description=json_data.get("description"),
            recipe_category=[
                category for category in json_data.get("recipeCategory", [])
            ],
            tags=[tag for tag in json_data.get("tags", [])],
            rating=json_data.get("rating"),
            date_added=parse_date(json_data["dateAdded"]),
            date_updated=parse_datetime(json_data["dateUpdated"]),
            recipe_yield=json_data.get("recipeYield"),
            recipe_ingredient=[
                RecipeIngredient.from_json(data)
                for data in json_data.get("recipeIngredient", [])
            ],
            recipe_instructions=[
                RecipeStep.from_json(data)
                for data in json_data.get("recipeInstructions", [])
            ],
            nutrition=Nutrition.from_json(json_data["nutrition"])
            if json_data.get("nutrition")
            else None,
            tools=[tool for tool in json_data.get("tools", [])],
            total_time=json_data.get("totalTime"),
            prep_time=json_data.get("prepTime"),
            perform_time=json_data.get("performTime"),
            settings=Setting.from_json(json_data["settings"]),
            assets=[
                Asset.from_json(data) for data in json_data.get("assets", [])
            ],
            notes=[Note.from_json(data) for data in json_data.get("notes", [])],
            org_url=json_data.get("orgURL"),
            extras=json_data.get("extras", []),
            comments=[
                Comment.from_json(data) for data in json_data.get("comments")
            ],
        )


@dataclass(frozen=True)
class Comment:
    text: str
    id: int
    uuid: str
    recipe_slug: str
    date_added: datetime
    user: str

    @classmethod
    def from_json(cls, json_data: Mapping[str, Any]) -> Comment:
        return Comment(
            text=json_data["text"],
            id=json_data["id"],
            uuid=json_data["uuid"],
            recipe_slug=json_data["recipeSlug"],
            date_added=parse_datetime(json_data["dateAdded"]),
            user=UserResponse.from_json(json_data["user"]),
        )


@dataclass(frozen=True)
class Note:
    title: Optional[str]
    text: Optional[str]

    @classmethod
    def from_json(cls, json_data: Mapping[str, Any]) -> Note:
        Note(
            title=json_data.get("title"),
            text=json_data.get("text"),
        )


@dataclass(frozen=True)
class Asset:
    name: Optional[str]
    icon: Optional[str]
    file_name: Optional[str]

    @classmethod
    def from_json(cls, json_data: Mapping[str, Any]) -> Asset:
        return Asset(
            name=json_data.get("name"),
            icon=json_data.get("icon"),
            file_name=json_data.get("fileName"),
        )


@dataclass(frozen=True)
class Setting:
    public: bool
    show_nutrition: bool
    show_assets: bool
    landscape_view: bool
    disable_comments: bool
    disable_amount: bool

    @classmethod
    def from_json(cls, json_data: Mapping[str, Any]) -> Setting:
        print(json_data)
        return Setting(
            public=json_data.get("public"),
            show_nutrition=json_data.get("showNutrition"),
            show_assets=json_data.get("showAssets"),
            landscape_view=json_data.get("landscapeView"),
            disable_comments=json_data.get("disableComments"),
            disable_amount=json_data.get("disableAmount"),
        )


@dataclass(frozen=True)
class Nutrition:
    calories: Optional[str]
    fat_content: Optional[str]
    protein_content: Optional[str]
    carbohydrate_content: Optional[str]
    fiber_content: Optional[str]
    sodium_content: Optional[str]
    sugar_content: Optional[str]

    @classmethod
    def from_json(cls, json_data: Mapping[str, Any]) -> Nutrition:
        return Nutrition(
            calories=json_data.get("calories"),
            fat_content=json_data.get("fatContent"),
            protein_content=json_data.get("proteinContent"),
            carbohydrate_content=json_data.get("carbohydrateContent"),
            fiber_content=json_data.get("fiberContent"),
            sodium_content=json_data.get("sodiumContent"),
            sugar_content=json_data.get("sugarContent"),
        )


@dataclass(frozen=True)
class RecipeIngredient:
    title: Optional[str]
    note: Optional[str]
    unit: Optional[RecipeIngredientUnit]
    food: Optional[RecipeIngredientFood]
    disable_amount: Optional[bool]
    quantity: Optional[int]

    @classmethod
    def from_json(cls, json_data: Mapping[str, Any]) -> RecipeIngredient:
        return RecipeIngredient(
            title=json_data.get("title"),
            note=json_data.get("note"),
            unit=RecipeIngredientUnit.from_json(json_data.get("unit"))
            if json_data.get("unit")
            else None,
            food=RecipeIngredientFood.from_json(json_data.get("food"))
            if json_data.get("food")
            else None,
            disable_amount=json_data.get("disableAmount"),
            quantity=json_data.get("quantity"),
        )


@dataclass(frozen=True)
class RecipeIngredientUnit:
    name: Optional[str]
    description: Optional[str]

    @classmethod
    def from_json(cls, json_data: Mapping[str, Any]) -> RecipeIngredientUnit:
        return RecipeIngredientUnit(
            name=json_data.get("name"),
            description=json_data.get("description"),
        )


@dataclass(frozen=True)
class RecipeIngredientFood:
    name: Optional[str]
    description: Optional[str]

    @classmethod
    def from_json(cls, json_data: Mapping[str, Any]) -> RecipeIngredientFood:
        return RecipeIngredientFood(
            name=json_data.get("name"),
            description=json_data.get("description"),
        )


@dataclass(frozen=True)
class RecipeStep:
    title: Optional[str]
    text: Optional[str]

    @classmethod
    def from_json(cls, json_data: Mapping[str, Any]) -> RecipeStep:
        return RecipeStep(
            title=json_data.get("title"),
            text=json_data.get("text"),
        )
