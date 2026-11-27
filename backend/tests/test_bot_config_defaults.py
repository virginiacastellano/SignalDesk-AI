from app.domain.models.bot_config import default_menu_sections, default_option_replies


def test_default_menu_has_portfolio_options():
    rows = [row for section in default_menu_sections() for row in section["rows"]]
    option_ids = {row["id"] for row in rows}

    assert {"pricing", "demo", "human", "integrations", "faq"}.issubset(option_ids)


def test_default_human_reply_requests_handoff():
    replies = default_option_replies()

    assert replies["human"]["handoff_required"] is True
    assert replies["pricing"]["handoff_required"] is False
