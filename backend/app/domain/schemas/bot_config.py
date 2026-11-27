from pydantic import BaseModel


class BotConfigRead(BaseModel):
    id: str
    welcome_message: str
    fallback_message: str
    menu_title: str
    menu_button_label: str
    handoff_keywords: list[str]
    menu_keywords: list[str]
    menu_sections: list[dict]
    option_replies: dict

    model_config = {"from_attributes": True}


class BotConfigUpdate(BaseModel):
    welcome_message: str
    fallback_message: str
    menu_title: str
    menu_button_label: str
    handoff_keywords: list[str]
    menu_keywords: list[str]
    menu_sections: list[dict]
    option_replies: dict
