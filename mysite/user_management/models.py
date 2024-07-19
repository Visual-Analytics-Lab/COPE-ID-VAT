from django.contrib.auth.models import AbstractUser
from django.db import models

class my_profile_model(AbstractUser):
    title = models.CharField(max_length=32, default="")
    department = models.CharField(max_length=64, default="")
    organization = models.CharField(max_length=64, default="")
    city = models.CharField(max_length=32, default="")

    Alabama, Alaska, Arizona = 'AL', 'AK', 'AZ'
    Arkansas, California, Colorado = 'AR', 'CA', 'CO'
    Connecticut, Delaware, Florida = 'CT', 'DE', 'FL'
    Georgia, Hawaii, Idaho = 'GA', 'HI', 'ID'
    Illinois, Indiana, Iowa = 'IL', 'IN', 'IA'
    Kansas, Kentucky, Louisiana = 'KS', 'KY', 'LA'
    Maine, Maryland, Massachusetts = 'ME', 'MD', 'MA'
    Michigan, Minnesota, Mississippi = 'MI', 'MN', 'MS'
    Missouri, Montana, Nebraska = 'MO', 'MT', 'NE'
    Nevada, New_Hampshire, New_Jersey = 'NV', 'NH', 'NJ'
    New_Mexico, New_York, North_Carolina = 'NM', 'NY', 'NC'
    North_Dakota, Ohio, Oklahoma = 'OR', 'PA', 'RI'
    Oregon, Pennsylvania, Rhode_Island = 'OR', 'PA', 'RI'
    South_Carolina, South_Dakota, Tennessee = 'SC', 'SD', 'TN'
    Texas, Utah, Vermont = 'TX', 'UT', 'VT'
    Virginia, Washington, West_Virginia = 'VA', 'WA', 'WV'
    Wisconsin, Wyoming, Not_Applicable = 'WI', 'WY', 'NA'

    state_choices = [
        (Alabama, 'Alabama'), (Alaska, 'Alaska'), (Arizona, 'Arizon'),
        (Arkansas, 'Arkansas'), (California, 'California'), (Colorado, 'Colorado'),
        (Connecticut, 'Connecticut'), (Delaware, 'Delaware'), (Florida, 'Florida'),
        (Georgia, 'Georgia'), (Hawaii, 'Hawaii'), (Idaho, 'Idaho'),
        (Illinois, 'Illinois'), (Indiana, 'Indiana'), (Iowa, 'Iowa'),
        (Kansas, 'Kansas'), (Kentucky, 'Kentucky'), (Louisiana, 'Louisiana'),
        (Maine, 'Maine'), (Maryland, 'Maryland'), (Massachusetts, 'Massachusetts'),
        (Michigan, 'Michigan'), (Minnesota, 'Minnesota'), (Mississippi, 'Mississippi'),
        (Missouri, 'Missouri'), (Montana, 'Montana'), (Nebraska, 'Nebraska'),
        (Nevada, 'Nevada'), (New_Hampshire, 'New Hampshire'), (New_Jersey, 'New Jersey'),
        (New_Mexico, 'New Mexico'), (New_York, 'New York'), (North_Carolina, 'North Carolina'),
        (North_Dakota, 'North Dakota'), (Ohio, 'Ohio'), (Oklahoma, 'Oklahoma'),
        (Oregon, 'Oregon'), (Pennsylvania, 'Pennsylvania'), (Rhode_Island, 'Rhode Island'),
        (South_Carolina, 'South Carolina'), (South_Dakota, 'South Dakota'), (Tennessee, 'Tennessee'),
        (Texas, 'Texas'), (Utah, 'Utah'), (Vermont, 'Vermont'),
        (Virginia, 'Virginia'), (Washington, 'Washington'), (West_Virginia, 'West Virginia'),
        (Wisconsin, 'Wisconsin'), (Wyoming, 'Wyoming'), (Not_Applicable, 'Not Applicable')
    ]

    state = models.CharField(
        max_length=2,
        choices=state_choices,
        blank=True,
        default='',
    )

    zip_code = models.CharField(max_length=5, default="")
    country = models.CharField(max_length=32, default="")
    favorite_projects = models.ManyToManyField('main.project_model', through='main.project_list_model', related_name='favorited_by')