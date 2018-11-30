import falcon

class StorageError(falcon.HTTPError):

    @staticmethod
    def handle(ex, req, resp, params):
        description = ('There was an error with storage')

        raise falcon.HTTPError(falcon.HTTP_500,
                               'Database Error',
                               description)
