def fallback_summary(text: str) -> str:
    sentences = text.split(".")
    bullets = []

    for s in sentences:
        s = s.strip()
        if len(s) > 40:
            bullets.append(f"• {s}")
        if len(bullets) >= 6:
            break

    return "📘 Manual Overview\n\n" + "\n".join(bullets)
