from flask_marshmallow import Marshmallow

ma = Marshmallow()


class UserEntity(ma.Schema):

    class Meta:
        fields = ("id", "name", "cpf", "email", "phone_number", "created_at", "updated_at")
