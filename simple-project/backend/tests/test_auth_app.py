class TestClass:
    def test_one(self):
        x = "Hello, hi"
        assert "h" in x

    def test_two(self):
        x = "what"
        assert hasattr(x, "who")