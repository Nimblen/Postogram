from rest_framework import viewsets
from src.apps.post.models import Hashtag
from src.apps.post.serializers import HashtagSerializer





class HashtagModelViewSet(viewsets.ModelViewSet):
    queryset = Hashtag.objects.all()
    serializer_class = HashtagSerializer
    start_name = "Hashtag"

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)


    def list(self, request, *args, **kwargs):
        '''
        # Hashtag list
        ## Deacription
        This endpoint returns all hashtags.
        '''
        return super().list(request, *args, **kwargs)
    

    def create(self, request, *args, **kwargs):
        '''
        # Hashtag create
        ## Deacription
        This endpoint creates a new hashtag.
        '''
        return super().create(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        '''
        # Hashtag retrieve
        ## Deacription
        This endpoint returns a single hashtag.
        '''
        return super().retrieve(request, *args, **kwargs)
    

    def update(self, request, *args, **kwargs):
        '''
        # Hashtag update
        ## Deacription
        This endpoint updates a single hashtag.
        '''
        return super().update(request, *args, **kwargs)
    

    def destroy(self, request, *args, **kwargs):
        '''
        # Hashtag destroy
        ## Deacription
        This endpoint destroys a single hashtag.
        '''
        return super().destroy(request, *args, **kwargs)
    





