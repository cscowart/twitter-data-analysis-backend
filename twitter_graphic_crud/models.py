from django.db import models

# Create your models here.
class Graphic(models.Model):
    ## Parameters for display of the graphic
    # user submitted title for their graphic
    title = models.CharField(max_length = 100, blank=True)
    # graphic author
    author = models.CharField(max_length = 50, blank=True)
    # date created
    date_created = models.DateField()
    ## Parameters for replicating graphics
    # JS code for recreating the graphic
    graph_code_js = models.TextField()
    # STRETCH GOALS
    # vote count
    # vote_count = models.PositiveSmallIntegerField(default=0)
    # query to replicate the data (in case raw data is desired)
    # replicate_data_query = models.TextField()
    # query to update the data (in case raw data is desired)
    # update_data_query = models.TextField()
    # data that has been manipulated post query (data used in the graphics) format:JSON string passed to the front end



