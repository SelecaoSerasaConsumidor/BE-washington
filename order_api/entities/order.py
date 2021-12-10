from flask_marshmallow import Marshmallow

ma = Marshmallow()


class OrderEntity(ma.Schema):

    class Meta:
        fields = (
            "id",
            "user_id",
            "item_description",
            "item_quantity",
            "item_price",
            "total_value",
            "created_at",
            "updated_at"
        )
