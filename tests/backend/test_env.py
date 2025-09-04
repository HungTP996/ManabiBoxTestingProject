def test_base_url(app_settings):
    # Kiểm tra xem URL cơ sở dữ liệu có tồn tại không
    assert app_settings.BASE_URL is not None
    print(f"BASE_URL: {app_settings.BASE_URL}")

def test_api_call(app_settings):
    # Sử dụng API key trong bài kiểm thử
    assert app_settings.ENVIRONMENT is not None
    print(f"ENVIRONMENT: {app_settings.ENVIRONMENT}")
