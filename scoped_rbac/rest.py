from rest_framework.views import APIView


class AccessControlledAPIView(APIView):
    """
    This `APIView` interface is required for non-object based views in combination with
    the `IsAuthorized` permission class.
    """

    def context_id_for(request):
        """
        Subclasses **MUST** override this method.
        """
        raise "Not implemented"

    def resource_type_iri_for(request):
        """
        Subclasses **MUST** override this method.
        """
        raise "Not implemented"
