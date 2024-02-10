class ApiError(Exception):
    code = 422
    description = "Default message"

class TokenInvalid(ApiError):
    code = 401
    description = "El token es inválido o ha expirado"

class TokenMissing(ApiError):
    code = 403
    description = "No hay token en la solicitud"

class FieldsMissing(ApiError):
    code = 400
    description = "Algunos campos están vacíos en la solicitud"

class InvalidFormat(ApiError):
    code = 400
    description = "Formato invalido para algunos campos"

class InvalidValues(ApiError):
    code = 412
    description = "Algunos valores no están dentro del rango esperado"
    
class OfferNotFound(ApiError):
    code = 404
    description = "La oferta con ese id no existe"

class OfferCreationSuccess(ApiError):
    code = 201
    description = "Oferta creada exitosamente"

    def __init__(self, offer_details):
        super().__init__(self.description)
        self.offer_details = offer_details