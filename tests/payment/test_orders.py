
class TestOrders:

    def test_new_user_has_no_orders(self, api_manager, authenticated_user):

        response = api_manager.payment_api.get_orders(authenticated_user)

        data = response.json()
        assert data["total"] == 0
        assert data["items"] == []

