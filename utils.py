def get_user_input(prompt: str) -> str:
    """Get user input with error handling"""
    try:
        return input(prompt).strip()
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        return ""
    except Exception as e:
        print(f"Input error: {e}")
        return ""